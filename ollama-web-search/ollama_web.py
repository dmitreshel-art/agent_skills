#!/usr/bin/env python3
"""Ollama Web Search CLI - Search and fetch web content using Ollama API."""

import argparse
import json
import os
import sys
from typing import Optional

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)


def get_api_key() -> str:
    """Get Ollama API key from environment or config file."""
    # Try environment variable first
    api_key = os.getenv("OLLAMA_API_KEY")
    if api_key:
        return api_key
    
    # Try config file
    config_paths = [
        os.path.expanduser("~/.openclaw/.env"),
        os.path.expanduser("~/.ollama/.env"),
        ".env",
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("OLLAMA_API_KEY="):
                        return line.split("=", 1)[1]
    
    raise ValueError(
        "OLLAMA_API_KEY not found. Set it in environment or ~/.openclaw/.env\n"
        "Get your API key at: https://ollama.com/settings/keys"
    )


def web_search(query: str, max_results: int = 5) -> list[dict]:
    """Search the web using Ollama API.
    
    Args:
        query: Search query string
        max_results: Maximum results to return (1-10)
    
    Returns:
        List of search results with title, url, content
    """
    api_key = get_api_key()
    
    response = requests.post(
        "https://ollama.com/api/web_search",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"query": query, "max_results": min(max_results, 10)},
        timeout=30,
    )
    
    if response.status_code == 401:
        raise ValueError("Invalid API key. Check your OLLAMA_API_KEY")
    
    response.raise_for_status()
    return response.json().get("results", [])


def web_fetch(url: str) -> dict:
    """Fetch a webpage using Ollama API.
    
    Args:
        url: URL to fetch
    
    Returns:
        Dict with title, content, links
    """
    api_key = get_api_key()
    
    # Add protocol if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    response = requests.post(
        "https://ollama.com/api/web_fetch",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"url": url},
        timeout=60,
    )
    
    if response.status_code == 401:
        raise ValueError("Invalid API key. Check your OLLAMA_API_KEY")
    
    response.raise_for_status()
    return response.json()


def format_search_results(results: list[dict], format_type: str = "text") -> str:
    """Format search results for output."""
    if not results:
        return "No results found."
    
    if format_type == "json":
        return json.dumps(results, indent=2, ensure_ascii=False)
    
    lines = []
    for i, r in enumerate(results, 1):
        if format_type == "text":
            lines.append(f"{i}. {r.get('title', 'No title')}")
            lines.append(f"   URL: {r.get('url', '')}")
            content = r.get('content', '')[:200]
            if len(r.get('content', '')) > 200:
                content += "..."
            lines.append(f"   {content}")
            lines.append("")
        elif format_type == "markdown":
            lines.append(f"## {i}. {r.get('title', 'No title')}")
            lines.append(f"**URL:** {r.get('url', '')}")
            lines.append("")
            lines.append(r.get('content', '')[:500])
            lines.append("")
            lines.append("---")
            lines.append("")
        elif format_type == "simple":
            lines.append(f"{r.get('title', 'No title')}")
            lines.append(r.get('url', ''))
            lines.append("")
    
    return "\n".join(lines)


def format_fetch_result(result: dict, format_type: str = "text") -> str:
    """Format fetch result for output."""
    if format_type == "json":
        return json.dumps(result, indent=2, ensure_ascii=False)
    
    lines = []
    
    if format_type == "markdown":
        lines.append(f"# {result.get('title', 'No title')}")
        lines.append("")
        lines.append(result.get('content', ''))
        if result.get('links'):
            lines.append("")
            lines.append("## Links")
            for link in result['links'][:20]:
                lines.append(f"- {link}")
    else:
        lines.append(f"Title: {result.get('title', 'No title')}")
        lines.append("-" * 50)
        lines.append(result.get('content', ''))
        if result.get('links'):
            lines.append("")
            lines.append(f"Links ({len(result['links'])}):")
            for link in result['links'][:10]:
                lines.append(f"  - {link}")
    
    return "\n".join(lines)


def cmd_search(args):
    """Handle search command."""
    try:
        results = web_search(args.query, args.max)
        print(format_search_results(results, args.format))
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Request error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_fetch(args):
    """Handle fetch command."""
    try:
        result = web_fetch(args.url)
        print(format_fetch_result(result, args.format))
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Request error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="ollama-web",
        description="Web search and fetch using Ollama API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ollama-web search "Python asyncio tutorial"
  ollama-web search "AI news" --max 10 --format json
  ollama-web fetch https://docs.ollama.com
  ollama-web fetch example.com --format markdown
        """,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search the web")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument(
        "--max", "-m", type=int, default=5,
        help="Maximum results (default: 5, max: 10)"
    )
    search_parser.add_argument(
        "--format", "-f", 
        choices=["text", "json", "markdown", "simple"],
        default="text",
        help="Output format (default: text)"
    )
    search_parser.set_defaults(func=cmd_search)
    
    # Fetch command
    fetch_parser = subparsers.add_parser("fetch", help="Fetch a webpage")
    fetch_parser.add_argument("url", help="URL to fetch")
    fetch_parser.add_argument(
        "--format", "-f",
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format (default: text)"
    )
    fetch_parser.set_defaults(func=cmd_fetch)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()