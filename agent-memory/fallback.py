"""
Legacy fallback functions for MEMORY.md.

Provides simple keyword-based search when API is unavailable.
"""

import logging
import re
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


def search_memory_md(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search MEMORY.md using simple keyword matching.
    
    This is a fallback when the Agent Memory System API is unavailable.
    Performs basic keyword extraction and matching.
    
    Args:
        query: Search query
        limit: Maximum number of results
        
    Returns:
        List of results in OpenClaw format
    """
    logger.debug(f"Searching MEMORY.md: query='{query}'")
    
    try:
        # Path to MEMORY.md
        memory_path = Path.home() / ".openclaw/workspace/MEMORY.md"
        
        if not memory_path.exists():
            logger.warning(f"MEMORY.md not found: {memory_path}")
            return []
        
        # Read MEMORY.md
        with open(memory_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract keywords from query
        keywords = extract_keywords(query)
        
        if not keywords:
            logger.debug("No keywords extracted from query")
            return []
        
        # Find matches in MEMORY.md
        matches = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check if line contains any keyword
            if any(keyword.lower() in line.lower() for keyword in keywords):
                match_score = calculate_match_score(line, keywords)
                
                # Extract context (previous and next lines)
                context = extract_context(lines, i - 1, window=2)
                
                matches.append({
                    "path": str(memory_path),
                    "score": match_score,
                    "content": context,
                    "citation": f"{memory_path}#L{i}"
                })
        
        # Sort by score and limit
        matches.sort(key=lambda x: x["score"], reverse=True)
        results = matches[:limit]
        
        logger.debug(f"MEMORY.md search: {len(results)} matches")
        return results
        
    except Exception as e:
        logger.error(f"MEMORY.md search failed: {e}")
        return []


def extract_keywords(text: str) -> List[str]:
    """
    Extract keywords from text.
    
    Args:
        text: Input text
        
    Returns:
        List of keywords
    """
    # Remove special characters and split
    cleaned = re.sub(r'[^\w\s]', ' ', text.lower())
    words = cleaned.split()
    
    # Filter out common stop words
    stop_words = {
        'the', 'is', 'at', 'which', 'on', 'and', 'a', 'an',
        'как', 'это', 'что', 'и', 'на', 'в', 'с', 'к',
        'the', 'is', 'a', 'an', 'and', 'or', 'but', 'in'
    }
    
    keywords = [w for w in words if len(w) > 2 and w not in stop_words]
    
    return list(set(keywords))  # Remove duplicates


def calculate_match_score(line: str, keywords: List[str]) -> float:
    """
    Calculate match score for a line.
    
    Args:
        line: Text line to score
        keywords: List of keywords
        
    Returns:
        Score between 0 and 1
    """
    if not keywords:
        return 0.0
    
    matches = sum(1 for kw in keywords if kw.lower() in line.lower())
    score = min(matches / len(keywords), 1.0)
    
    return score


def extract_context(lines: List[str], index: int, window: int = 2) -> str:
    """
    Extract context around a line.
    
    Args:
        lines: List of all lines
        index: Index of the matched line
        window: Number of lines before/after to include
        
    Returns:
        Context string
    """
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    
    context_lines = lines[start:end]
    return '\n'.join(context_lines)


def get_memory_md(path: str, from_line: int, lines: int) -> str:
    """
    Get specific lines from MEMORY.md.
    
    Args:
        path: Path to MEMORY.md
        from_line: Starting line number (1-indexed)
        lines: Number of lines to retrieve
        
    Returns:
        Content of specified lines
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If parameters are invalid
    """
    logger.debug(f"Getting MEMORY.md: path={path}, from={from_line}, lines={lines}")
    
    memory_path = Path(path)
    
    if not memory_path.exists():
        raise FileNotFoundError(f"MEMORY.md not found: {memory_path}")
    
    if from_line < 1:
        raise ValueError(f"from_line must be >= 1, got {from_line}")
    
    if lines < 1:
        raise ValueError(f"lines must be >= 1, got {lines}")
    
    with open(memory_path, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()
    
    # Convert to 0-indexed
    start_index = from_line - 1
    end_index = start_index + lines
    
    if start_index >= len(all_lines):
        return ""  # Beyond end of file
    
    if end_index > len(all_lines):
        end_index = len(all_lines)
    
    selected_lines = all_lines[start_index:end_index]
    
    return ''.join(selected_lines)