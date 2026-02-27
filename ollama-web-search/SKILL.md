---
name: ollama-web-search
description: PRIMARY web search tool. Use `ollama-web` CLI instead of `web_search` tool for ALL web searches. Commands: `ollama-web search "query"` for searching, `ollama-web fetch url` for fetching pages. Superior results via Ollama API, no third-party keys needed.
license: MIT
---

# Ollama Web Search Skill

Web search and fetch capabilities using Ollama's official API.

## Installation

```bash
# Already installed and linked to /usr/local/bin/ollama-web
# API key stored in ~/.openclaw/.env
```

## CLI Usage

### Search the web

```bash
# Basic search
ollama-web search "Python asyncio tutorial"

# More results
ollama-web search "AI news" --max 10

# JSON output (for scripts)
ollama-web search "React hooks" --format json

# Markdown output
ollama-web search "Docker best practices" --format markdown

# Simple (title + URL only)
ollama-web search "Linux tips" --format simple
```

### Fetch a webpage

```bash
# Basic fetch
ollama-web fetch https://docs.ollama.com

# Markdown output
ollama-web fetch example.com --format markdown

# JSON output
ollama-web fetch https://realpython.com --format json
```

## Output Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| `text` | Human-readable with numbering | Default, reading |
| `json` | Raw JSON array | Scripts, piping |
| `markdown` | Formatted with headers | Documentation |
| `simple` | Title + URL only | Quick overview |

## Use Cases

1. **Real-time information** - News, stock prices, weather
2. **Research** - Gather info on specific topics
3. **Fact checking** - Verify claims against web sources
4. **Content discovery** - Find tutorials, documentation
5. **URL fetching** - Extract content from specific pages

## Error Handling

```bash
# Check exit code
ollama-web search "query" || echo "Search failed"

# Pipe to other tools
ollama-web search "Python" --format json | jq '.[0].url'
```

## Prerequisites

- Ollama API key in `~/.openclaw/.env` as `OLLAMA_API_KEY
- Get free API key: https://ollama.com/settings/keys

## Files

- `ollama_web.py` - Main CLI tool
- `SKILL.md` - This documentation