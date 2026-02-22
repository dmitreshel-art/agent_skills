"""
Semantic memory search using Agent Memory System API.

Provides memory_search function for OpenClaw integration.
Falls back to MEMORY.md if API is unavailable.
"""

import logging
import re
import time
from typing import List, Dict, Any
from pathlib import Path

from .client import get_client, StructuredLogger
from .fallback import search_memory_md
from .metrics import record_metric

logger = logging.getLogger(__name__)
s_logger = StructuredLogger("memory_search")


def memory_search(
    query: str,
    maxResults: int = 10,
    minScore: float = 0.3
) -> List[Dict[str, Any]]:
    """
    Search knowledge using semantic vector search.
    
    This is the main integration point for OpenClaw's memory_search tool.
    Performs semantic search via API, falls back to MEMORY.md on failure.
    
    Args:
        query: Search query (can be in any language)
        maxResults: Maximum number of results to return
        minScore: Minimum similarity score (0-1)
        
    Returns:
        List of results in OpenClaw format:
        [
            {
                "path": "memory:<id>",
                "score": <similarity_score>,
                "content": "<text_content>",
                "citation": "memory/file.md#<line_number>"
            },
            ...
        ]
        
    Note:
        - Results are ranked by similarity score (higher is better)
        - Fallback to MEMORY.md if API is unavailable
        - Paths use format "memory:<id>" for knowledge units
    """
    logger.info(f"memory_search: query='{query}', maxResults={maxResults}, minScore={minScore}")

    start_time = time.time()

    try:
        # Get API client
        client = get_client()

        # Check API health
        if not client.health_check():
            logger.warning("API unhealthy, falling back to MEMORY.md")
            s_logger.log(
                level="INFO",
                query=query,
                maxResults=maxResults,
                minScore=minScore,
                fallback_used=True,
                success=True
            )
            return search_memory_md(query, maxResults)

        # Perform semantic search
        start_time = time.time()
        api_result = client.search(
            query=query,
            limit=maxResults,
            score_threshold=minScore
        )
        query_time = (time.time() - start_time) * 1000
        
        # Format results for OpenClaw
        results = []
        api_results = api_result.get("results", [])
        
        for api_result in api_results:
            knowledge_id = api_result.get("id")
            content = api_result.get("content", "")
            score = api_result.get("score", 0.0)
            
            # OpenClaw format
            result = {
                "path": f"memory:{knowledge_id}",
                "score": score,
                "content": content,
                "citation": f"memory:{knowledge_id}"
            }
            
            results.append(result)
        
        # Log metrics
        result_count = len(results)
        # query_time is already calculated above
        max_score = results[0]["score"] if results else 0.0

        logger.info(
            f"memory_search completed: {result_count} results, "
            f"query_time={query_time}ms, API_used=True"
        )

        s_logger.log(
            level="INFO",
            query=query,
            maxResults=maxResults,
            minScore=minScore,
            latency_ms=query_time,
            success=True,
            results_count=result_count,
            max_score=max_score,
            fallback_used=False
        )

        # Record metrics
        record_metric(latency_ms=int(query_time), success=True)

        return results

    except Exception as e:
        logger.error(f"memory_search failed: {e}, falling back to MEMORY.md")

        # Log error
        s_logger.log(
            level="ERROR",
            query=query,
            maxResults=maxResults,
            minScore=minScore,
            error=str(e),
            fallback_used=True,
            success=False
        )

        # Record metrics (failed)
        record_metric(latency_ms=0, success=False)

        # Fallback to MEMORY.md
        try:
            fallback_results = search_memory_md(query, maxResults)

            s_logger.log(
                level="INFO",
                query=query,
                maxResults=maxResults,
                minScore=minScore,
                fallback_used=True,
                success=True,
                results_count=len(fallback_results)
            )

            return fallback_results
        except Exception as fallback_error:
            logger.error(f"Fallback also failed: {fallback_error}")

            s_logger.log(
                level="ERROR",
                query=query,
                error=str(fallback_error),
                fallback_used=True,
                success=False
            )

            return []