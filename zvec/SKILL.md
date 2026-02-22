---
name: zvec
description: Use this skill for ZVEC open-source in-process vector database. Covers installation, basics, dense/sparse vectors, querying, collections, and performance optimization for semantic search applications.
tags: ["zvec", "vector-database", "semantic-search", "inference", "alibaba"]
related: ["trading-graph", "development-graph"]
---

# ZVEC Graph Skill

This skill provides access to the **zvec-graph** — a structured knowledge graph for ZVEC, an open-source in-process vector database from Alibaba for fast semantic search.

## When to use

Use this skill when user asks about:
- Vector databases and semantic search
- ZVEC installation and setup
- Dense vs sparse vector representations
- Vector similarity search and querying
- Collection management and data operations
- Performance optimization for vector DBs
- Python/Go integration with ZVEC

## Graph structure

The zvec graph files are now located at:
```
skills/zvec/
├── INDEX.md                    # Entry point
├── zvec-basics.md            # ZVEC fundamentals
├── installation.md             # Installation and setup
├── dense-vectors.md           # Dense vector representations
├── sparse-vectors.md          # Sparse vector representations
├── query.md                  # Vector search and querying
├── collections.md             # Collection management
├── data-operations.md        # Data operations
└── performance.md            # Performance and optimization
```

## How to use

### 1. Start with INDEX

```bash
"Read skills/zvec/INDEX.md"
```

The INDEX.md provides:
- Quick start guide with 5 steps
- Navigation to all 12 skills
- YAML frontmatter for quick scanning

### 2. Scan frontmatter

Before reading a skill file, check its frontmatter:
```yaml
---
description: "Brief description"
tags: ["tag1", "tag2"]
related: ["skill-1", "skill-2"]
---
```

This allows progressive disclosure:
- Skip skills not relevant to query
- Follow [[wiki-links]] to related concepts
- Provide targeted knowledge, not entire files

### 3. Follow wiki-links

When navigating to graph:
- Start with [[zvec-basics]] for fundamentals
- Follow [[installation]] for setup questions
- Use [[query]] for search operations
- Use [[performance]] for optimization

## Available skills

### Quick start (5 steps)
1. [[installation]] — Install ZVEC
2. [[zvec-basics]] — Learn fundamentals
3. [[dense-vectors]] — Study dense vectors
4. [[sparse-vectors]] — Study sparse vectors
5. [[query]] — Start searching

### Core concepts
- [[zvec-basics]] — What ZVEC is and how it works
- [[installation]] — Installation and configuration

### Vector types
- [[dense-vectors]] — Dense vector representations
- [[sparse-vectors]] — Sparse vector representations

### Operations
- [[query]] — Vector search and similarity queries
- [[collections]] — Collection creation and management
- [[data-operations]] — Data operations and batch processing

### Advanced
- [[performance]] — Performance optimization and tuning
- [[filtering]] — Vector filtering and pre-filtering
- [[indexing]] — Indexing strategies and parameters
- [[integration-openclaw]] — Integration with OpenClaw and agents

## Agent behavior

When answering ZVEC questions:

1. **Read INDEX.md** first for overview
2. **Scan frontmatter** of relevant skills
3. **Follow [[wiki-links]]** based on query relevance
4. **Provide progressive knowledge** — index → descriptions → targeted sections
5. **Maintain context** — keep track of related concepts

## Best practices

- **Start with basics**: [[zvec-basics]] → [[installation]] → specific operations
- **Use wiki-links** for navigation — don't read everything linearly
- **Cross-reference concepts**: dense vectors connect to query and performance
- **Progressive disclosure**: Show quick start first, details only when needed

## Reference

- **Graph location:** `skills/zvec/INDEX.md`
- **Main docs:** `skills/README.md`
- **Agent guide:** `skills/AGENT-GUIDE.md`
- **Creation guide:** `skills/skill-graph-creation/SKILL.md`
- **External:** https://github.com/alibaba/ZVEC

## Summary

The zvec graph provides structured knowledge for working with ZVEC vector database. Access via `skills/zvec/INDEX.md` and navigate using wiki-links.

This skill is a **wrapper** that provides access to zvec knowledge graph files.
