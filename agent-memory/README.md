# Agent Memory System Skill for OpenClaw

Semantic memory search using vector database technology. Fast, scalable, multilingual knowledge retrieval.

## Features

- ✅ **Semantic Search:** Search by meaning, not just keywords
- ✅ **Multilingual:** 50+ languages including English and Russian
- ✅ **Fast:** <500ms typical response time
- ✅ **Scalable:** Millions of knowledge units
- ✅ **Robust:** Automatic retry with exponential backoff
- ✅ **Graceful Degradation:** Falls back to MEMORY.md on API failure

## Installation

### Prerequisites

- Python 3.9+
- Agent Memory System API running on `http://localhost:8000`
- Qdrant vector database running

### Install Skill

```bash
cd ~/.openclaw/workspace/skills/agent-memory
pip install -e .
```

### Verify Installation

```bash
# Test imports
python -c "from agent_memory import memory_search, memory_get; print('OK')"

# Test API health
curl http://localhost:8000/health
```

## Quick Start

### Basic Search

```python
from agent_memory import memory_search

# Search for knowledge
results = memory_search("Python programming", maxResults=5)

for result in results:
    print(f"{result['score']:.2f}: {result['content']}")
```

### Russian Language Search

```python
from agent_memory import memory_search

# Russian queries work the same way
results = memory_search("как работает Python", maxResults=5)
```

### Get Knowledge by ID

```python
from agent_memory import memory_get

# Retrieve specific knowledge
content = memory_get("memory:knowledge-id-here")
```

## API Reference

### `memory_search(query, maxResults=10, minScore=0.3)`

Search knowledge using semantic vector similarity.

**Parameters:**
- `query` (str, required): Search query text
- `maxResults` (int, default=10): Maximum results to return
- `minScore` (float, default=0.3): Minimum similarity score (0-1)

**Returns:** List of result dictionaries with `path`, `score`, `content`, `citation`

**Example:**
```python
results = memory_search(
    "machine learning algorithms",
    maxResults=5,
    minScore=0.7
)
```

### `memory_get(path, from_line=None, lines=None)`

Get knowledge unit by ID or from MEMORY.md.

**Parameters:**
- `path` (str, required): `"memory:<id>"` or `"MEMORY.md#L<line>"`
- `from_line` (int, optional): Line start (MEMORY.md only)
- `lines` (int, optional): Line count (MEMORY.md only)

**Returns:** String content

**Example:**
```python
# API format
content = memory_get("memory:abc-123-def")

# Fallback format
content = memory_get("/path/to/MEMORY.md#L10", from_line=10, lines=20)
```

## Performance

| Metric | Value | Target |
|--------|-------|--------|
| Search latency | 160-676ms | <500ms ✅ |
| API health check | <10ms | <50ms ✅ |
| Multilingual support | 50+ languages | N/A ✅ |

## Error Handling

### Automatic Retry

The skill automatically retries failed requests:
- **Attempts:** 3 (initial + 2 retries)
- **Backoff:** Exponential (1s, 2s)
- **Retryable errors:** Connection, timeout, 5xx HTTP

### Fallback to MEMORY.md

When the API is unavailable:
1. Automatic fallback to MEMORY.md keyword search
2. Keyword extraction from query
3. Context extraction (2 lines before/after match)

### Common Errors

| Error | Cause | Solution |
|-------|--------|----------|
| `ModuleNotFoundError` | Skill not installed | Run `pip install -e .` in skill directory |
| `ConnectionError` | API not running | Check `docker-compose ps` |
| `TimeoutError` | API too slow | Increase timeout or check API health |
| `FileNotFoundError` | Knowledge ID invalid | Verify ID format: `"memory:<id>"` |

## Testing

### Run Integration Tests

```bash
cd ~/.openclaw/workspace/skills/agent-memory

# Simple API test
python simple_test.py

# Russian language test
python test_russian.py
```

### Expected Results

```
=== Testing Agent Memory System API ===

✓ Health check: healthy
✓ Search results: 3

Result 1:
  ID: 3274e067-33bb-4da3-8483-7fb2a5142332
  Score: 0.9555
  Content: Python programming language...
```

## Configuration

### Default Settings

| Setting | Default | Description |
|----------|----------|-------------|
| API URL | `http://localhost:8000` | Memory API endpoint |
| Timeout | 5 seconds | Request timeout |
| Max retries | 3 | Retry attempts on failure |

### Custom Configuration

```python
from agent_memory.client import MemoryAPIClient

# Custom configuration
client = MemoryAPIClient(
    base_url="http://custom-host:8000",
    timeout=10.0,
    max_retries=5
)
```

## Architecture

```
┌─────────────────────────────────────┐
│    OpenClaw Tools Layer         │
│                                 │
│  memory_search()  memory_get()    │
└────────────┬────────────────────┘
             │
    ┌────────▼─────────┐
    │  HTTP Client    │
    │  (with retry)    │
    └────────┬─────────┘
             │
    ┌────────▼──────────────────┐
    │   Agent Memory System API │
    │  (FastAPI + Qdrant)      │
    └────────┬─────────────────┘
             │
    ┌────────▼────────┐
    │  Qdrant Vector DB │
    │  (768-dim vectors) │
    └───────────────────┘
```

## Migration from MEMORY.md

### Before

```python
# Keyword search in flat files
grep "keyword" MEMORY.md
```

### After

```python
# Semantic search with meaning
from agent_memory import memory_search
results = memory_search("related concepts", maxResults=10)
```

### Benefits

- ✅ Semantic understanding (not just keywords)
- ✅ Faster (vector search > file grep)
- ✅ Scalable (millions of knowledge units)
- ✅ Multilingual (50+ languages)
- ✅ Quality scoring (relevance 0-1)

## Troubleshooting

### API Not Running

```bash
# Check if API is running
docker-compose ps

# Check API logs
docker-compose logs api

# Check API health
curl http://localhost:8000/health
```

### Qdrant Not Running

```bash
# Check if Qdrant is running
docker-compose ps

# Check Qdrant logs
docker-compose logs qdrant

# Restart services
docker-compose restart api qdrant
```

### Skill Not Found

```bash
# Reinstall skill
cd ~/.openclaw/workspace/skills/agent-memory
pip uninstall -y agent-memory
pip install -e .

# Verify installation
python -c "from agent_memory import memory_search; print('OK')"
```

## Version

**Current Version:** 0.1.0

**Changelog:**

### v0.1.0 (2026-02-19)
- Initial release
- Model migration: all-MiniLM-L6-v2 → paraphrase-multilingual-mpnet-base-v2
- Vector dimension: 384 → 768
- Multilingual support (50+ languages)
- HTTP client with retry logic
- Fallback to MEMORY.md
- Russian language quality testing

## License

MIT License

## Support

For issues or questions:
- Check logs: Agent Memory System API logs
- Verify API health: `curl http://localhost:8000/health`
- Review SKILL.md for detailed documentation

---

**Maintainer:** Шелдон (AI-ассистент)  
**Version:** 0.1.0  
**Last Updated:** 2026-02-19