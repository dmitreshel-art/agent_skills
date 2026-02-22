"""
Memory retrieval for OpenClaw.

Provides memory_get function for retrieving knowledge by ID.
Falls back to MEMORY.md if API is unavailable.
"""

import logging
import time
from typing import Optional, Dict, Any
from pathlib import Path

from .client import get_client, StructuredLogger
from .fallback import get_memory_md
from .metrics import record_metric

logger = logging.getLogger(__name__)
g_logger = StructuredLogger("memory_get")


def memory_get(path: str, from_line: int = None, lines: int = None) -> str:
    """
    Get knowledge unit by path (ID).
    
    This is the main integration point for OpenClaw's memory_get tool.
    Parses path format "memory:<id>" and retrieves the knowledge.
    
    Args:
        path: Path in format "memory:<knowledge_id>" or "MEMORY.md#L<line>"
        from_line: Line number to start from (for MEMORY.md fallback, ignored for API)
        lines: Number of lines to return (for MEMORY.md fallback, ignored for API)
        
    Returns:
        Content of the knowledge unit as string
        
    Raises:
        ValueError: If path format is invalid
        FileNotFoundError: If knowledge is not found
        
    Note:
        - Path format for API: "memory:<knowledge_id>"
        - Path format for fallback: "MEMORY.md#L<line>"
        - from_line and lines are only used for MEMORY.md fallback
    """
    logger.debug(f"memory_get: path='{path}', from_line={from_line}, lines={lines}")

    start_time = time.time()

    # Parse path format
    knowledge_id = parse_path(path)

    if knowledge_id is None:
        # It's a MEMORY.md path format
        content = get_memory_md(path, from_line or 1, lines or 10)
        g_logger.log(
            level="INFO",
            path=path,
            from_line=from_line,
            lines=lines,
            fallback_used=True,
            success=True,
            latency_ms=int((time.time() - start_time) * 1000)
        )

        # Record metrics
        record_metric(latency_ms=int((time.time() - start_time) * 1000), success=True)

        return content

    try:
        # Get API client
        client = get_client()

        # Check API health
        if not client.health_check():
            logger.warning("API unhealthy, falling back to MEMORY.md")
            g_logger.log(
                level="INFO",
                path=path,
                knowledge_id=knowledge_id,
                fallback_used=True,
                success=True,
                reason="API unhealthy"
            )
            raise FileNotFoundError("API unavailable, use MEMORY.md format")

        # Get knowledge by ID
        # Note: Current API doesn't have get_by_id endpoint
        # In future, this will use: client.get_by_id(knowledge_id)
        # For now, trigger fallback

        logger.warning("get_by_id not implemented in API")
        raise FileNotFoundError("Use MEMORY.md format for now")

    except FileNotFoundError as e:
        # This is expected for now (no get_by_id endpoint)
        # Re-raise for caller to handle
        g_logger.log(
            level="INFO",
            path=path,
            knowledge_id=knowledge_id,
            fallback_used=True,
            success=True,
            reason="get_by_id not implemented"
        )
        raise

    except Exception as e:
        logger.error(f"memory_get failed: {e}")
        g_logger.log(
            level="ERROR",
            path=path,
            knowledge_id=knowledge_id,
            error=str(e),
            fallback_used=True,
            success=False
        )
        raise


def parse_path(path: str) -> Optional[str]:
    """
    Parse path and extract knowledge ID.
    
    Supports formats:
    - "memory:<id>" → returns "<id>"
    - "MEMORY.md" → returns None (fallback)
    - "/full/path/MEMORY.md" → returns None (fallback)
    - "memory:123" → returns "123"
    
    Args:
        path: Path string to parse
        
    Returns:
        Knowledge ID as string, or None if fallback format
        
    Raises:
        ValueError: If path format is invalid
    """
    if not path:
        raise ValueError("Path cannot be empty")
    
    # Check if it's an API format
    if path.startswith("memory:"):
        # Format: "memory:<id>"
        parts = path.split(":", 1)
        
        if len(parts) != 2:
            raise ValueError(f"Invalid memory path format: {path}")
        
        knowledge_id = parts[1].strip()
        
        if not knowledge_id:
            raise ValueError(f"Knowledge ID cannot be empty: {path}")
        
        return knowledge_id
    
    # Check if it's a MEMORY.md fallback format
    if "MEMORY.md" in path or path.endswith(".md"):
        # It's a fallback format
        return None
    
    # Unknown format
    raise ValueError(f"Unknown path format: {path}")