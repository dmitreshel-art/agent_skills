# Migration Guide: MEMORY.md → Agent Memory System

Guide for migrating from flat MEMORY.md files to semantic vector database.

## Why Migrate?

### Problems with MEMORY.md

| Problem | Impact |
|----------|--------|
| **Linear Search** | O(n) complexity, slow with large files |
| **Keyword Only** | No semantic understanding |
| **No Relevance Scoring** | Can't rank results by quality |
| **Scalability** | File size grows indefinitely |
| **Single Language** | Limited to English-only content |

### Benefits of Agent Memory System

| Benefit | Impact |
|----------|--------|
| **Semantic Search** | Understand meaning, not just keywords |
| **Fast Retrieval** | <500ms typical (vs grep) |
| **Relevance Scoring** | Score 0-1 for result quality |
| **Scalable** | Millions of knowledge units |
| **Multilingual** | 50+ languages including Russian |
| **Vector Similarity** | Find related concepts automatically |

## Prerequisites

### Required

- ✅ Agent Memory System API running on `http://localhost:8000`
- ✅ Qdrant vector database running
- ✅ Existing knowledge in MEMORY.md (optional)

### Verify Setup

```bash
# Check API health
curl http://localhost:8000/health

# Expected: {"status":"healthy","timestamp":"...","service":"agent-memory-api"}

# Check API metadata
curl http://localhost:8000/api/meta

# Expected: {"knowledge_count":175,"collection":"knowledge_units","vector_dimension":768}
```

## Migration Strategy

### Option 1: Manual (Recommended)

Best for:
- Small knowledge bases (< 1000 knowledge units)
- High-quality, curated knowledge
- Manual control over what to migrate

**Steps:**

1. **Review existing knowledge**
   ```bash
   # Read MEMORY.md
   cat ~/.openclaw/workspace/MEMORY.md
   
   # Identify key sections/topics
   ```

2. **Create knowledge units via API**
   ```bash
   # Save knowledge one by one
   curl -X POST http://localhost:8000/api/knowledge \
     -H "Content-Type: application/json" \
     -d '{
       "content": "Python is a programming language",
       "type": "fact",
       "importance": 8
     }'
   ```

3. **Verify migration**
   ```bash
   # Search for migrated knowledge
   curl "http://localhost:8000/api/search?query=Python&limit=5"
   ```

### Option 2: Automated (Future)

Best for:
- Large knowledge bases (> 1000 knowledge units)
- Regular updates/changes
- Batch operations

**Future Feature:**
- Migration script to parse MEMORY.md
- Automatic knowledge unit extraction
- Batch upload via API

**Status:** Not implemented in v0.1.0

## Knowledge Type Mapping

When migrating, map MEMORY.md sections to knowledge types:

| MEMORY.md Section | Knowledge Type | Use For |
|-------------------|---------------|----------|
| Facts and data | `fact` | Objective information |
| Concepts and theories | `concept` | Abstract ideas |
| Procedures and guides | `procedural` | How-to instructions |
| Social notes | `social` | Interactions, preferences |

### Importance Scoring

When creating knowledge units, assign importance (0-10):

| Range | Use Case |
|-------|----------|
| 0-2 | Temporary notes, quick reminders |
| 3-6 | General information, useful knowledge |
| 7-10 | Critical information, must-know content |

## Migration Example

### Before: MEMORY.md

```markdown
# Knowledge

## Python

Python is a high-level programming language created by Guido van Rossum.
It is used for web development, data science, automation.

## Best Practices

- Use type hints
- Write docstrings
- Follow PEP 8
```

### After: Knowledge Units

```bash
# Fact: Python overview
curl -X POST http://localhost:8000/api/knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Python is a high-level programming language created by Guido van Rossum. It is used for web development, data science, automation.",
    "type": "fact",
    "importance": 9
  }'

# Procedural: Best practices
curl -X POST http://localhost:8000/api/knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Python best practices: Use type hints, write docstrings, follow PEP 8",
    "type": "procedural",
    "importance": 7
  }'
```

### Search Comparison

```python
# Before: MEMORY.md (keyword search)
# grep -i "python programming" MEMORY.md
# Results: Simple keyword matches, no relevance

# After: Agent Memory System (semantic search)
from agent_memory import memory_search

results = memory_search("python programming", maxResults=5)
# Results: Ranked by semantic similarity, with scores
```

## Verification

### Test Migrated Knowledge

```bash
# 1. Search for migrated topic
curl "http://localhost:8000/api/search?query=Python&limit=5"

# 2. Verify results are relevant
# Check score > 0.5 for top results

# 3. Test multilingual
curl "http://localhost:8000/api/search?query=как работает Python&limit=3"
```

### Check Knowledge Count

```bash
# Get metadata
curl http://localhost:8000/api/meta

# Expected: knowledge_count > 0
```

## Rollback Plan

### If Migration Fails

**Rollback Strategy:**

1. Keep MEMORY.md as backup
   - Don't delete after migration
   - Keep as fallback reference

2. Verify fallback works
   ```python
   from agent_memory import memory_search
   
   # API unavailable → falls back to MEMORY.md
   results = memory_search("test query", maxResults=5)
   ```

3. Document issues
   - What didn't work
   - Error messages
   - Steps tried

### Revert to MEMORY.md

If you need to revert completely:

1. Stop using `memory_search` / `memory_get`
2. Continue using MEMORY.md directly
3. Remove Agent Memory System dependency

## Best Practices

### When Migrating

1. **Start Small**
   - Migrate critical knowledge first
   - Test before continuing

2. **Use Appropriate Types**
   - Facts → `fact`
   - Guides → `procedural`
   - Concepts → `concept`

3. **Set Importance Correctly**
   - Critical: 8-10
   - Important: 5-7
   - General: 3-4
   - Temporary: 0-2

4. **Verify After Migration**
   - Search and verify results
   - Check relevance scores
   - Test in multiple languages

### What NOT to Migrate

❌ Don't migrate:
- Very temporary notes
- Test data
- Outdated information
- Personal messages (unless useful)

✅ DO migrate:
- Long-term knowledge
- Frequently referenced information
- Critical procedures
- Important concepts

## Common Issues

### Issue: Knowledge Not Found

**Symptom:** Search returns empty results

**Solutions:**
1. Check if knowledge was migrated
2. Try different query terms
3. Lower `minScore` parameter

### Issue: Low Relevance Scores

**Symptom:** All scores < 0.5, poor results

**Solutions:**
1. Check knowledge content quality
2. Verify migration mapping (type, importance)
3. Try different query formulations

### Issue: API Unavailable

**Symptom:** `memory_search` falls back to MEMORY.md

**Solutions:**
1. Check API health: `curl http://localhost:8000/health`
2. Verify services running: `docker-compose ps`
3. Check logs: `docker-compose logs api`

## Support

### Documentation

- SKILL.md: Detailed API reference
- README.md: Installation and usage guide
- Agent Memory System docs: `/root/.openclaw/workspace/projects/agent-memory-system/README.md`

### Troubleshooting

```bash
# Check API status
curl http://localhost:8000/health

# Check API logs
docker-compose logs api --tail=50

# Check Qdrant status
docker-compose logs qdrant --tail=50

# Verify services
docker-compose ps
```

## Timeline

### Small Migration (< 100 units)
- **Time:** 30-60 minutes
- **Effort:** Manual entry via API
- **Verification:** 10-15 minutes

### Medium Migration (100-1000 units)
- **Time:** 2-4 hours
- **Effort:** Script-assisted or batch API
- **Verification:** 30-45 minutes

### Large Migration (> 1000 units)
- **Time:** 1-2 days
- **Effort:** Automated migration script
- **Verification:** 2-3 hours

---

**Version:** 0.1.0  
**Last Updated:** 2026-02-19  
**Status:** Ready for use