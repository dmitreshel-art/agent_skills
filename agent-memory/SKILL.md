# Agent Memory System Skill

## Overview

The Agent Memory System skill provides semantic memory search using vector database technology. Replaces flat MEMORY.md files with fast, scalable, multilingual knowledge retrieval.

## When to Use This Skill

Use this skill when:
- Шелдон needs to search across long-term memories
- Semantic search by meaning, not just keywords
- Multilingual support (English, Russian, 50+ languages)
- Fast retrieval (<500ms typical)
- Scalable storage (millions of knowledge units)

## Core Concepts

### Vector Database
- **Technology:** Qdrant (vector similarity search)
- **Embeddings:** sentence-transformers (paraphrase-multilingual-mpnet-base-v2)
- **Dimensions:** 768
- **Distance Metric:** Cosine similarity

### Semantic Search
- **How it works:** Converts query to embedding vector, finds similar knowledge
- **Score:** 0.0-1.0 (higher = more similar)
- **Threshold:** minScore parameter filters low-relevance results

### Fallback
- **When:** API unavailable or fails
- **Behavior:** Falls back to MEMORY.md keyword search
- **Purpose:** Graceful degradation

## Functions

### `memory_search(query, maxResults, minScore, search_type, filters, pagination, ranking)`

Search knowledge using advanced search with multiple retrieval modes.

**Parameters:**
- `query` (str): Search query text (any language)
- `maxResults` (int, default=10): Maximum number of results
- `minScore` (float, default=0.3): Minimum similarity score (0-1)
- `search_type` (str, default="hybrid"): Search type - "vector", "fulltext", or "hybrid"
- `filters` (dict, optional): Search filters
  - `type` (list): Filter by knowledge type ["skill", "document", "log", "config"]
  - `importance` (list): Filter by importance level ["high", "medium", "low"]
  - `date_range` (dict): Date range filter {"start": "2026-01-01", "end": "2026-12-31"}
  - `tags` (list): Filter by tags (AND logic - must match ALL tags)
- `pagination` (dict, optional): Pagination parameters
  - `offset` (int, default=0): Number of results to skip
  - `limit` (int, default=10, max=100): Number of results to return
- `ranking` (dict, optional): Ranking parameters
  - `enabled` (bool, default=True): Enable/disable ranking
  - `weights` (dict): Custom ranking weights
    - `semantic` (float, default=0.5): Weight for semantic score (0-1)
    - `importance` (float, default=0.3): Weight for importance score (0-1)
    - `freshness` (float, default=0.15): Weight for freshness score (0-1)
    - `popularity` (float, default=0.05): Weight for popularity score (0-1)

**Returns:**
```python
[
    {
        "path": "memory:<knowledge_id>",
        "score": <similarity_score>,
        "content": "<text_content>",
        "citation": "memory:<knowledge_id>",
        "search_type": "<search_type>",  # Added: search type used
        "filters_applied": {...},  # Added: filters applied
        "page": 1  # Added: current page
    },
    ...
]
```

**Usage:**
```python
from agent_memory import memory_search

# Basic vector search (backward compatible)
results = memory_search(
    "как работает Python",
    maxResults=5,
    minScore=0.5
)

# Full-text search (NEW)
results = memory_search(
    "Python tutorial",
    search_type="fulltext"
)

# Hybrid search (NEW - default)
results = memory_search(
    "Python tutorial",
    search_type="hybrid"
)

# Hybrid search with filters (NEW)
results = memory_search(
    "Python",
    search_type="hybrid", 
    filters={
        "type": ["skill"],
        "importance": ["high"],
        "tags": ["python"]
    }
)

# Hybrid search with pagination (NEW)
results = memory_search(
    "Python",
    search_type="hybrid",
    pagination={"offset": 0, "limit": 5}
)

# Hybrid search with custom ranking (NEW)
results = memory_search(
    "Python",
    search_type="hybrid",
    ranking={
        "enabled": True,
        "weights": {
            "semantic": 0.7,
            "importance": 0.3,
            "freshness": 0.0,
            "popularity": 0.0
        }
    }
)

# Full advanced search (NEW)
results = memory_search(
    "Python",
    search_type="hybrid",
    filters={"type": ["skill"], "importance": ["high"]},
    pagination={"offset": 0, "limit": 5},
    ranking={"enabled": True, "weights": {"semantic": 0.6, "importance": 0.4}}
)
```

### `memory_get(path, from_line, lines)`

Get knowledge unit by ID or from MEMORY.md.

**Parameters:**
- `path` (str): Path in format `"memory:<id>"` or `"MEMORY.md#L<line>"`
- `from_line` (int, optional): Starting line (for MEMORY.md only)
- `lines` (int, optional): Number of lines (for MEMORY.md only)

**Returns:**
```python
"Knowledge content as string"
```

**Usage:**
```python
from agent_memory import memory_get

# Get by knowledge ID (API format)
content = memory_get("memory:abc-123")

# Get from MEMORY.md (fallback format)
content = memory_get("/root/.openclaw/workspace/MEMORY.md#L10", from_line=10, lines=20)
```

## Error Handling

### API Unavailable
When the Agent Memory System API is unavailable:
1. Automatic retry (3 attempts with exponential backoff)
2. Fallback to MEMORY.md keyword search
3. Logged with `logger.warning`

### Invalid Path Format
- `ValueError` raised for invalid `"memory:<>"` format
- `"memory:"` requires ID after colon
- `"MEMORY.md"` or `".md"` paths trigger fallback

### Knowledge Not Found
- `FileNotFoundError` raised for missing knowledge
- Triggers fallback behavior if API unavailable

## Performance

| Operation | Target | Actual |
|-----------|--------|--------|
| Search time | <500ms | 160-676ms |
| Memory retrieval | <100ms | ~50ms |
| API health check | <50ms | <10ms |

## Dependencies

- **Python:** 3.9+
- **HTTP Client:** httpx>=0.25.0
- **Retry Logic:** tenacity>=8.2.0
- **API:** Agent Memory System (http://localhost:8000)

## Configuration

### Environment Variables

No environment variables required. Uses defaults:
- API URL: `http://localhost:8000`
- Timeout: 5 seconds
- Max retries: 3

### Client Configuration

```python
from agent_memory.client import get_client

client = get_client()
# Uses default configuration
```

## Examples

### Basic Search

```python
from agent_memory import memory_search

# Search for knowledge
results = memory_search("Python programming", maxResults=5)

for result in results:
    print(f"Score: {result['score']:.2f}")
    print(f"Content: {result['content']}")
    print(f"Path: {result['path']}\n")
```

### Multilingual Search

```python
from agent_memory import memory_search

# Russian query
results = memory_search("как работает Python", maxResults=3)

# English query  
results = memory_search("how does Python work", maxResults=3)

# Both use the same multilingual model
```

### Advanced Search Types (NEW)

```python
from agent_memory import memory_search

# Vector search only (semantic similarity)
results = memory_search(
    query="Python tutorial",
    search_type="vector"
)

# Full-text search only (keyword matching, BM25)
results = memory_search(
    query="Python tutorial",
    search_type="fulltext"
)

# Hybrid search (default) - combines vector + full-text
results = memory_search(
    query="Python tutorial",
    search_type="hybrid"  # Best of both worlds
)
```

### Advanced Filtering (NEW)

```python
from agent_memory import memory_search

# Filter by knowledge type
results = memory_search(
    query="Python",
    search_type="hybrid",
    filters={
        "type": ["skill"],  # Only skills
        "importance": ["high"]  # Only high importance
    }
)

# Filter by tags
results = memory_search(
    query="Python",
    search_type="hybrid",
    filters={
        "tags": ["python", "linux"]  # Must have BOTH tags
    }
)

# Filter by date range
results = memory_search(
    query="Python",
    search_type="hybrid",
    filters={
        "date_range": {
            "start": "2026-01-01",
            "end": "2026-12-31"
        }
    }
)

# Combined filters
results = memory_search(
    query="Python",
    search_type="hybrid",
    filters={
        "type": ["skill"],
        "importance": ["high", "medium"],
        "tags": ["python"]
    }
)
```

### Pagination (NEW)

```python
from agent_memory import memory_search

# First page (default)
results = memory_search(
    query="Python",
    search_type="hybrid",
    pagination={
        "offset": 0,  # Skip 0 results
        "limit": 10  # Return 10 results
    }
)

# Second page
results = memory_search(
    query="Python",
    search_type="hybrid",
    pagination={
        "offset": 10,  # Skip first 10 results
        "limit": 10  # Return next 10 results
    }
)

# Large page
results = memory_search(
    query="Python",
    search_type="hybrid",
    pagination={
        "offset": 0,
        "limit": 50  # Up to 100 results
    }
)
```

### Custom Ranking (NEW)

```python
from agent_memory import memory_search

# Disable ranking (use semantic score only)
results = memory_search(
    query="Python",
    search_type="hybrid",
    ranking={"enabled": False}
)

# Custom weights - prioritize importance
results = memory_search(
    query="Python",
    search_type="hybrid",
    ranking={
        "enabled": True,
        "weights": {
            "semantic": 0.4,
            "importance": 0.5,  # High importance priority
            "freshness": 0.1,
            "popularity": 0.0
        }
    }
)

# Custom weights - prioritize freshness
results = memory_search(
    query="Python",
    search_type="hybrid",
    ranking={
        "enabled": True,
        "weights": {
            "semantic": 0.4,
            "importance": 0.1,
            "freshness": 0.5,  # Recent results first
            "popularity": 0.0
        }
    }
)

# Custom weights - prioritize popularity
results = memory_search(
    query="Python",
    search_type="hybrid",
    ranking={
        "enabled": True,
        "weights": {
            "semantic": 0.5,
            "importance": 0.2,
            "freshness": 0.0,
            "popularity": 0.3  # Popular results first
        }
    }
)
```

### Full Advanced Search (NEW)

```python
from agent_memory import memory_search

# Complete advanced search with all features
results = memory_search(
    query="Python",
    search_type="hybrid",  # Best search type
    filters={
        "type": ["skill"],  # Only skills
        "importance": ["high"],  # Only high importance
        "tags": ["python"]  # Must have Python tag
    },
    pagination={
        "offset": 0,  # First page
        "limit": 10  # 10 results per page
    },
    ranking={
        "enabled": True,  # Enable ranking
        "weights": {
            "semantic": 0.6,  # Prioritize relevance
            "importance": 0.3,
            "freshness": 0.1,
            "popularity": 0.0
        }
    }
)

for result in results:
    print(f"Score: {result['score']:.2f}")
    print(f"Search Type: {result.get('search_type', 'N/A')}")
    print(f"Page: {result.get('page', 1)}")
    print(f"Content: {result['content']}\n")
```

### Get Knowledge by ID

```python
from agent_memory import memory_get

# Retrieve specific knowledge
content = memory_get("memory:abc-123-def")

print(content)
```

## Fallback Behavior

When API is unavailable, the skill falls back to MEMORY.md:

**Fallback Search:**
- Keyword-based matching
- Extracts keywords from query
- Finds lines containing keywords
- Returns context (2 lines before/after match)

**Fallback Get:**
- Reads MEMORY.md file directly
- Extracts specified line range
- Returns raw content

## Troubleshooting

### API Not Responding

**Symptom:** `memory_search` takes long time or returns empty

**Solutions:**
1. Check API health: `curl http://localhost:8000/health`
2. Check if API container is running: `docker-compose ps`
3. Check API logs: `docker-compose logs api`

### Module Import Error

**Symptom:** `ModuleNotFoundError: No module named 'agent_memory'`

**Solutions:**
```bash
# Install as editable package
cd ~/.openclaw/workspace/skills/agent-memory
pip install -e .
```

### Low Search Scores

**Symptom:** All scores < 0.5, poor relevance

**Solutions:**
1. Try different query terms
2. Lower `minScore` parameter (e.g., 0.2 instead of 0.3)
3. Check if knowledge exists on topic

### High Latency

**Symptom:** Search > 1 second

**Solutions:**
1. Check if API is overloaded
2. Verify Qdrant is running: `docker-compose logs qdrant`
3. Consider caching frequent queries

## Version History

### v0.1.0 (2026-02-19)
- Initial release
- Model migration: all-MiniLM-L6-v2 → paraphrase-multilingual-mpnet-base-v2
- Vector dimension: 384 → 768
- Multilingual support (50+ languages)
- Russian language quality testing
- HTTP client with retry logic
- Fallback to MEMORY.md

## License

MIT License - See project root for details

## Maintainer

Шелдон (AI-ассистент)
Version: 0.1.0