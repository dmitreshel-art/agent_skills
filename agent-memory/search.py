"""
Semantic memory search using Agent Memory System API.

Provides memory_search function for OpenClaw integration.
Supports advanced search types, filtering, pagination, and ranking.
Falls back to MEMORY.md if API is unavailable.
"""

import logging
import re
import time
from typing import List, Dict, Any, Optional
from pathlib import Path

from .client import get_client, StructuredLogger
from .fallback import search_memory_md

logger = logging.getLogger(__name__)
s_logger = StructuredLogger("memory_search")


def memory_search(
    query: str,
    maxResults: int = 10,
    minScore: float = 0.3,
    search_type: str = "hybrid",
    filters: Optional[Dict] = None,
    pagination: Optional[Dict] = None,
    ranking: Optional[Dict] = None
) -> List[Dict[str, Any]]:
    """
    Search knowledge using advanced search with multiple retrieval modes.
    
    This is the main integration point for OpenClaw's memory_search tool.
    Supports vector, full-text, and hybrid search with advanced features:
    - Search types: vector, fulltext, hybrid
    - Filters: type, importance, date_range, tags
    - Pagination: offset, limit
    - Ranking: enabled, weights (semantic, importance, freshness, popularity)
    
    Args:
        query: Search query (can be in any language)
        maxResults: Maximum number of results to return
        minScore: Minimum similarity score (0-1)
        search_type: Search type - "vector", "fulltext", or "hybrid" (default: "hybrid")
        filters: Search filters
            {
                "type": ["skill", "document"],  # Optional: filter by type
                "importance": ["high", "medium"],  # Optional: filter by importance
                "date_range": {"start": "2026-01-01", "end": "2026-12-31"},  # Optional: date range
                "tags": ["python", "linux"]  # Optional: filter by tags (AND logic)
            }
        pagination: Pagination parameters
            {
                "offset": 0,  # Number of results to skip (default: 0)
                "limit": 10  # Number of results to return (default: 10, max: 100)
            }
        ranking: Ranking parameters
            {
                "enabled": True,  # Enable/disable ranking (default: True)
                "weights": {  # Optional: custom weights
                    "semantic": 0.5,      # Weight for semantic score (0-1)
                    "importance": 0.3,     # Weight for importance score (0-1)
                    "freshness": 0.15,      # Weight for freshness score (0-1)
                    "popularity": 0.05      # Weight for popularity score (0-1)
                }
            }
        
    Returns:
        List of results in OpenClaw format:
        [
            {
                "path": "memory:<id>",
                "score": <similarity_score>,
                "content": "<text_content>",
                "citation": "memory/file.md#<line_number>",
                "search_type": "<search_type>",  # Added: search type used
                "filters_applied": {...},  # Added: filters applied
                "page": 1  # Added: current page
            },
            ...
        ]
        
    Note:
        - Results are ranked by relevance score (higher is better)
        - Ranking considers semantic similarity, importance, freshness, and popularity
        - Pagination metadata included (page, has_next, has_previous)
        - Fallback to MEMORY.md if API is unavailable
        - Paths use format "memory:<id>" for knowledge units
        
    Examples:
        # Basic vector search
        memory_search("Python tutorial")
        
        # Full-text search
        memory_search("Python tutorial", search_type="fulltext")
        
        # Hybrid search with filters
        memory_search("Python", search_type="hybrid", 
                     filters={"type": ["skill"], "importance": ["high"]})
        
        # Hybrid search with pagination
        memory_search("Python", search_type="hybrid",
                     pagination={"offset": 0, "limit": 5})
        
        # Hybrid search with custom ranking
        memory_search("Python", search_type="hybrid",
                     ranking={"enabled": True, "weights": {"semantic": 0.7, "importance": 0.3}})
    """
    logger.info(
        f"memory_search: query='{query}', maxResults={maxResults}, "
        f"minScore={minScore}, search_type={search_type}"
    )

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
                search_type=search_type,
                fallback_used=True,
                success=True
            )
            return search_memory_md(query, maxResults)

        # Prepare search request
        search_request = {
            "query": query,
            "search_type": search_type,
            "limit": maxResults,
            "offset": pagination.get("offset", 0) if pagination else 0
        }

        # Add filters if provided
        if filters:
            search_request["filters"] = filters

        # Add ranking if provided
        if ranking:
            search_request["ranking"] = ranking

        # Log search parameters
        logger.info(f"Search request: {search_request}")

        # Perform advanced search (using advanced API endpoint)
        try:
            # Try advanced search first
            api_result = client.advanced_search(**search_request)
        except AttributeError:
            # Fallback to basic search if advanced_search not implemented
            logger.warning("Advanced search not available, using basic search")
            api_result = client.search(
                query=query,
                limit=maxResults,
                score_threshold=minScore
            )

        # Format results for OpenClaw
        results = []
        
        # Handle advanced search response
        if "results" in api_result and "metadata" in api_result:
            api_results = api_result.get("results", [])
            metadata = api_result.get("metadata", {})
            
            for api_result_item in api_results:
                knowledge_id = api_result_item.get("id")
                content = api_result_item.get("content", "")
                title = api_result_item.get("title", "")
                score = api_result_item.get("relevance_score", api_result_item.get("score", 0.0))
                
                # Use title + content for display
                display_content = f"{title}: {content}" if title else content
                
                # OpenClaw format
                result = {
                    "path": f"memory:{knowledge_id}",
                    "score": score,
                    "content": display_content,
                    "citation": f"memory:{knowledge_id}",
                    "search_type": search_type,  # Added
                    "filters_applied": filters or {},  # Added
                }
                
                results.append(result)
            
            # Log metrics
            result_count = len(results)
            query_time = metadata.get("search_time_ms", 0)
            max_score = results[0]["score"] if results else 0.0
            cached = metadata.get("cached", False)
            page = metadata.get("page", 1)
            total = metadata.get("total", 0)

            logger.info(
                f"memory_search completed: {result_count} results, "
                f"query_time={query_time}ms, page={page}/{total}, "
                f"cached={cached}, API_used=True"
            )

            s_logger.log(
                level="INFO",
                query=query,
                maxResults=maxResults,
                minScore=minScore,
                search_type=search_type,
                filters=str(filters) if filters else None,
                pagination=str(pagination) if pagination else None,
                ranking=str(ranking) if ranking else None,
                latency_ms=query_time,
                success=True,
                results_count=result_count,
                max_score=max_score,
                cached=cached,
                page=page,
                total_results=total,
                fallback_used=False
            )

        else:
            # Handle basic search response (backward compatibility)
            api_results = api_result.get("results", [])
            
            for api_result_item in api_results:
                knowledge_id = api_result_item.get("id")
                content = api_result_item.get("content", "")
                score = api_result_item.get("score", 0.0)
                
                # OpenClaw format
                result = {
                    "path": f"memory:{knowledge_id}",
                    "score": score,
                    "content": content,
                    "citation": f"memory:{knowledge_id}",
                    "search_type": search_type,  # Added
                    "filters_applied": filters or {},  # Added
                }
                
                results.append(result)
            
            # Log metrics
            result_count = len(results)
            query_time = api_result.get("query_time_ms", 0)
            max_score = results[0]["score"] if results else 0.0

            logger.info(
                f"memory_search completed: {result_count} results, "
                f"query_time={query_time}ms, API_used=True (basic)"
            )

            s_logger.log(
                level="INFO",
                query=query,
                maxResults=maxResults,
                minScore=minScore,
                search_type=search_type,
                latency_ms=query_time,
                success=True,
                results_count=result_count,
                max_score=max_score,
                fallback_used=False
            )

        return results

    except Exception as e:
        logger.error(f"memory_search failed: {e}, falling back to MEMORY.md")

        # Log error
        s_logger.log(
            level="ERROR",
            query=query,
            maxResults=maxResults,
            minScore=minScore,
            search_type=search_type,
            filters=str(filters) if filters else None,
            error=str(e),
            fallback_used=True,
            success=False
        )

        # Fallback to MEMORY.md
        try:
            fallback_results = search_memory_md(query, maxResults)

            s_logger.log(
                level="INFO",
                query=query,
                maxResults=maxResults,
                minScore=minScore,
                search_type=search_type,
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