"""
HTTP Client for Agent Memory System API.

Communicates with the Agent Memory System backend
to perform semantic search and knowledge retrieval.
"""

import httpx
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

# Setup structured logging
LOG_PATH = Path.home() / ".openclaw/workspace/logs/agent-memory.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


class StructuredLogger:
    """Structured logger for agent-memory system."""

    def __init__(self, component: str):
        """
        Initialize structured logger.

        Args:
            component: Component name (e.g., "memory_search", "memory_get")
        """
        self.component = component
        self.log_path = LOG_PATH

    def log(self, level: str, **kwargs):
        """
        Log a structured entry.

        Args:
            level: Log level (INFO, WARNING, ERROR, DEBUG)
            **kwargs: Additional log fields
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            "component": self.component,
            **kwargs
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


class MemoryAPIClient:
    """
    HTTP client for Agent Memory System API.
    
    Handles communication with the memory API, including:
    - Semantic search
    - Knowledge retrieval by ID
    - Health checks
    - Retry logic with exponential backoff
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        timeout: float = 5.0,
        max_retries: int = 3
    ):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL of the memory API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Initialize HTTP client
        self.client = httpx.Client(
            timeout=timeout,
            headers={"Content-Type": "application/json"}
        )
        
        logger.info(
            f"Initialized MemoryAPIClient: url={self.base_url}, "
            f"timeout={timeout}s, max_retries={max_retries}"
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def search(
        self,
        query: str,
        limit: int = 10,
        score_threshold: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Search knowledge by semantic similarity.
        
        Args:
            query: Search query text
            limit: Maximum number of results
            score_threshold: Minimum similarity score (optional)
            
        Returns:
            Dict with 'results', 'count', 'query_time_ms'
            
        Raises:
            httpx.HTTPError: If request fails after retries
        """
        logger.debug(f"Searching: query='{query}', limit={limit}")
        
        try:
            params = {"query": query, "limit": limit}
            if score_threshold is not None:
                params["score_threshold"] = score_threshold
            
            response = self.client.get(
                f"{self.base_url}/api/search",
                params=params
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(
                f"Search completed: query='{query}', "
                f"results={result.get('count', 0)}, "
                f"time={result.get('query_time_ms', 0)}ms"
            )
            
            return result
            
        except httpx.HTTPError as e:
            logger.error(f"Search failed: {e}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def advanced_search(
        self,
        query: str,
        search_type: str = "hybrid",
        limit: int = 10,
        offset: int = 0,
        filters: Optional[Dict] = None,
        ranking: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Advanced search with multiple retrieval modes.
        
        Args:
            query: Search query text
            search_type: Search type - "vector", "fulltext", or "hybrid"
            limit: Maximum number of results
            offset: Number of results to skip
            filters: Search filters (type, importance, date_range, tags)
            ranking: Ranking parameters (enabled, weights)
            
        Returns:
            Dict with 'results', 'metadata'
            {
                "results": [...],
                "metadata": {
                    "total": 150,
                    "offset": 0,
                    "limit": 10,
                    "page": 1,
                    "total_pages": 15,
                    "has_next": true,
                    "has_previous": false,
                    "search_time_ms": 145.5,
                    "cached": false
                }
            }
            
        Raises:
            httpx.HTTPError: If request fails after retries
        """
        logger.debug(f"Advanced search: query='{query}', type={search_type}, limit={limit}")
        
        try:
            # Build request body
            request_body = {
                "query": query,
                "search_type": search_type,
                "pagination": {
                    "offset": offset,
                    "limit": limit
                }
            }
            
            # Add filters if provided
            if filters:
                request_body["filters"] = filters
            
            # Add ranking if provided
            if ranking:
                request_body["ranking"] = ranking
            
            # Make request
            response = self.client.post(
                f"{self.base_url}/api/search/advanced/search",
                json=request_body
            )
            response.raise_for_status()
            
            result = response.json()
            
            logger.info(
                f"Advanced search completed: query='{query}', "
                f"results={len(result.get('results', []))}, "
                f"time={result.get('metadata', {}).get('search_time_ms', 0)}ms"
            )
            
            return result
            
        except httpx.HTTPError as e:
            logger.error(f"Advanced search failed: {e}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def get_by_id(self, knowledge_id: str) -> Optional[Dict[str, Any]]:
        """
        Get knowledge unit by ID.
        
        Note: This uses search with ID as query if
        dedicated endpoint is not available.
        
        Args:
            knowledge_id: Knowledge unit ID
            
        Returns:
            Dict with knowledge data or None if not found
            
        Raises:
            httpx.HTTPError: If request fails after retries
        """
        logger.debug(f"Getting knowledge by ID: {knowledge_id}")
        
        try:
            # Note: Use search endpoint if /api/knowledge/{id} not available
            # This is a workaround - in future, use proper endpoint
            response = self.client.get(
                f"{self.base_url}/api/meta"
            )
            response.raise_for_status()
            
            # For now, we don't have a direct get_by_id endpoint
            # Return None to trigger fallback
            logger.warning(
                f"get_by_id not implemented in API, triggering fallback"
            )
            return None
            
        except httpx.HTTPError as e:
            logger.error(f"Get by ID failed: {e}")
            raise

    def health_check(self) -> bool:
        """
        Check if API is healthy.
        
        Returns:
            True if API is healthy, False otherwise
        """
        try:
            response = self.client.get(f"{self.base_url}/health")
            response.raise_for_status()
            
            data = response.json()
            status = data.get("status") == "healthy"
            
            logger.debug(f"Health check: {status}")
            return status
            
        except Exception as e:
            logger.warning(f"Health check failed: {e}")
            return False

    def close(self):
        """Close HTTP client."""
        if self.client:
            self.client.close()
            logger.info("MemoryAPIClient closed")


# Global client instance (lazy initialization)
_client: Optional[MemoryAPIClient] = None


def get_client() -> MemoryAPIClient:
    """
    Get or create global client instance.
    
    Returns:
        MemoryAPIClient instance
    """
    global _client
    
    if _client is None:
        _client = MemoryAPIClient()
    
    return _client