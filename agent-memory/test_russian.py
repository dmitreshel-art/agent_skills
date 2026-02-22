#!/usr/bin/env python3
"""Test Russian language search."""

import httpx
import json

print("=== Testing Russian Language Search ===\n")

queries = [
    "как работает Python",
    "лучшие практики кодирования",
    "безопасность API"
]

for query in queries:
    try:
        print(f"Query: {query}")
        
        response = httpx.get(
            "http://localhost:8000/api/search",
            params={"query": query, "limit": 3},
            timeout=10
        )
        data = response.json()
        
        print(f"  Results: {data['count']}")
        
        if data['results']:
            top_score = data['results'][0]['score']
            print(f"  Top score: {top_score:.4f}")
            print(f"  Top result: {data['results'][0]['content'][:60]}...")
        
        print()
        
    except Exception as e:
        print(f"  ✗ Error: {e}\n")

print("✓ Russian language tests completed!")