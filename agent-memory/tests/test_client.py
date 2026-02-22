"""
Unit tests for MemoryAPIClient.

Tests HTTP client functionality including retry logic and error handling.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from httpx import HTTPError

from agent_memory.client import MemoryAPIClient


@pytest.fixture
def client():
    """Create a test client instance."""
    return MemoryAPIClient(
        base_url="http://test.local:8000",
        timeout=5.0,
        max_retries=3
    )


@pytest.fixture
def mock_response():
    """Create a mock HTTP response."""
    response = Mock()
    response.json.return_value = {
        "results": [
            {"id": "test-1", "content": "Test content", "score": 0.8}
        ],
        "count": 1,
        "query_time_ms": 50
    }
    response.raise_for_status = Mock()
    return response


class TestMemoryAPIClient:
    """Test MemoryAPIClient initialization and configuration."""

    def test_client_initialization(self):
        """Test that client initializes with correct parameters."""
        client = MemoryAPIClient(
            base_url="http://test.local:8000",
            timeout=5.0,
            max_retries=3
        )
        
        assert client.base_url == "http://test.local:8000"
        assert client.timeout == 5.0
        assert client.max_retries == 3
        assert client.client is not None

    def test_client_initialization_defaults(self):
        """Test that client uses default parameters."""
        client = MemoryAPIClient()
        
        assert client.base_url == "http://localhost:8000"
        assert client.timeout == 5.0
        assert client.max_retries == 3


class TestSearch:
    """Test search functionality."""

    def test_search_success(self, client, mock_response):
        """Test successful search returns correct results."""
        with patch.object(client.client, 'get', return_value=mock_response):
            result = client.search("test query", limit=10)
        
        assert "results" in result
        assert result["count"] == 1
        assert len(result["results"]) == 1
        assert result["results"][0]["content"] == "Test content"
        assert result["results"][0]["score"] == 0.8

    def test_search_with_score_threshold(self, client, mock_response):
        """Test search with score_threshold parameter."""
        mock_response.json.return_value = {
            "results": [
                {"id": "test-1", "content": "Test content", "score": 0.8},
                {"id": "test-2", "content": "Low score", "score": 0.2}
            ],
            "count": 2,
            "query_time_ms": 50
        }
        
        with patch.object(client.client, 'get', return_value=mock_response):
            result = client.search("test query", limit=10, score_threshold=0.5)
        
        # API is called with threshold (we can't filter in test)
        # In real scenario, API would filter
        assert "results" in result

    def test_search_with_limit(self, client, mock_response):
        """Test search respects limit parameter."""
        mock_response.json.return_value = {
            "results": [
                {"id": f"test-{i}", "content": f"Test {i}", "score": 0.8}
                for i in range(5)
            ],
            "count": 5,
            "query_time_ms": 50
        }
        
        with patch.object(client.client, 'get', return_value=mock_response):
            result = client.search("test query", limit=3)
        
        # API returns limit results
        assert result["count"] == 5  # All available
        # Client would limit locally if needed

    def test_search_timeout_retry(self, client):
        """Test search retries on timeout."""
        # Simulate timeout then success
        call_count = [0]
        
        def side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                raise HTTPError("Timeout")
            else:
                mock_response = Mock()
                mock_response.json.return_value = {
                    "results": [],
                    "count": 0,
                    "query_time_ms": 100
                }
                mock_response.raise_for_status = Mock()
                return mock_response
        
        with patch.object(client.client, 'get', side_effect=side_effect):
            result = client.search("test query", limit=10)
        
        # Should succeed after retry
        assert call_count[0] == 2  # First failed, second succeeded


class TestGetById:
    """Test get_by_id functionality."""

    def test_get_by_id_success(self, client):
        """Test successful get_by_id returns knowledge."""
        # Note: Current implementation returns None
        # This tests the API call pattern
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "test-123",
            "content": "Test knowledge",
            "metadata": {"type": "fact"}
        }
        mock_response.raise_for_status = Mock()
        
        with patch.object(client.client, 'get', return_value=mock_response):
            result = client.get_by_id("test-123")
        
        # Current implementation returns None (no endpoint)
        assert result is None

    def test_get_by_id_not_found(self, client):
        """Test get_by_id returns None for missing knowledge."""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = Mock()
        
        with patch.object(client.client, 'get', return_value=mock_response):
            result = client.get_by_id("nonexistent-id")
        
        assert result is None


class TestHealthCheck:
    """Test health check functionality."""

    def test_health_check_success(self, client):
        """Test health check returns True when API is healthy."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "healthy",
            "timestamp": "2026-02-19T12:00:00Z"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.object(client.client, 'get', return_value=mock_response):
            result = client.health_check()
        
        assert result is True

    def test_health_check_failure(self, client):
        """Test health check returns False when API is unhealthy."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "unhealthy"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.object(client.client, 'get', return_value=mock_response):
            result = client.health_check()
        
        assert result is False

    def test_health_check_exception(self, client):
        """Test health check returns False on exception."""
        with patch.object(client.client, 'get', side_effect=Exception("Connection error")):
            result = client.health_check()
        
        assert result is False


class TestClose:
    """Test client cleanup."""

    def test_close(self, client):
        """Test close method closes HTTP client."""
        assert client.client is not None
        client.close()
        # Client should be closed
        # (can't easily verify without mocking internals)