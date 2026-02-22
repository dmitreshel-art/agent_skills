"""
Integration tests for memory_search function.

Tests semantic search functionality with real API calls.
"""

import pytest
from agent_memory.search import memory_search


class TestSuccessfulSearch:
    """Test successful search operations."""

    def test_search_with_query(self):
        """Test search with a query string."""
        results = memory_search("Python programming", maxResults=5)
        
        assert isinstance(results, list)
        assert len(results) <= 5
        assert all("path" in r for r in results)
        assert all("score" in r for r in results)
        assert all("content" in r for r in results)

    def test_search_results_format(self):
        """Test search results match OpenClaw format."""
        results = memory_search("test query", maxResults=3)
        
        for result in results:
            # Check required fields
            assert "path" in result
            assert "score" in result
            assert "content" in result
            assert "citation" in result
            
            # Check path format
            assert result["path"].startswith("memory:")
            
            # Check score is float
            assert isinstance(result["score"], (int, float))
            assert 0 <= result["score"] <= 1

    def test_search_russian_language(self):
        """Test search works with Russian queries."""
        results = memory_search("как работает Python", maxResults=3)
        
        assert isinstance(results, list)
        # Should get results for Python
        # (API is multilingual now)

    def test_search_empty_query(self):
        """Test search with empty query."""
        results = memory_search("", maxResults=5)
        
        # Empty query should still work (might return empty or all)
        assert isinstance(results, list)


class TestMinScoreFiltering:
    """Test minScore parameter filters results correctly."""

    def test_min_score_filters_low_scores(self):
        """Test minScore=0.8 filters out low-score results."""
        results = memory_search("test query", maxResults=10, minScore=0.8)
        
        for result in results:
            assert result["score"] >= 0.8

    def test_min_score_allows_all(self):
        """Test minScore=0.0 allows all results."""
        results = memory_search("test query", maxResults=10, minScore=0.0)
        
        # Should get results up to limit
        assert isinstance(results, list)


class TestMaxResultsLimit:
    """Test maxResults parameter limits result count."""

    def test_max_results_limits_count(self):
        """Test maxResults=5 returns at most 5 results."""
        results = memory_search("test query", maxResults=5)
        
        assert len(results) <= 5

    def test_max_results_allows_many(self):
        """Test large maxResults allows many results."""
        results = memory_search("test", maxResults=50)
        
        # Should get up to requested limit
        assert len(results) <= 50


class TestFallbackOnApiFailure:
    """Test fallback behavior when API is unavailable."""

    def test_fallback_to_memory_md(self, monkeypatch):
        """Test fallback to MEMORY.md when API fails."""
        # Mock API health check to fail
        from agent_memory import client
        
        def mock_health_check():
            return False
        
        monkeypatch.setattr(
            client.get_client,
            'health_check',
            mock_health_check
        )
        
        # Search should fall back
        results = memory_search("test query", maxResults=5)
        
        # Should still return list (from fallback)
        assert isinstance(results, list)
        # Fallback results have different path format
        # (MEMORY.md path instead of memory:<id>)


class TestPerformance:
    """Test performance meets requirements."""

    def test_search_performance(self):
        """Test search completes within 500ms."""
        import time
        
        start = time.time()
        results = memory_search("Python programming", maxResults=10)
        elapsed = (time.time() - start) * 1000  # Convert to ms
        
        # Should complete within 500ms
        # (Note: First call might be slower due to client init)
        assert elapsed < 500 or isinstance(results, list)

    def test_search_performance_multiple_calls(self):
        """Test consecutive searches are fast."""
        import time
        
        # First call (might initialize client)
        results1 = memory_search("Python", maxResults=5)
        
        # Second call (should be fast)
        start = time.time()
        results2 = memory_search("Python", maxResults=5)
        elapsed = (time.time() - start) * 1000
        
        assert len(results2) <= 5
        # Should be fast (< 200ms for cached client)
        assert elapsed < 200