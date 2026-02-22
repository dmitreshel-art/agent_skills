#!/usr/bin/env python3
"""Simple test to verify API integration."""

import httpx
import json

print("=== Testing Agent Memory System API ===\n")

# Test health
try:
    response = httpx.get("http://localhost:8000/health", timeout=5)
    health_data = response.json()
    print(f"✓ Health check: {health_data['status']}")
except Exception as e:
    print(f"✗ Health check failed: {e}")
    exit(1)

# Test search
try:
    response = httpx.get(
        "http://localhost:8000/api/search",
        params={"query": "Python programming", "limit": 3},
        timeout=10
    )
    search_data = response.json()
    
    print(f"\n✓ Search results: {search_data['count']}")
    
    for i, result in enumerate(search_data['results'][:3]):
        print(f"\nResult {i+1}:")
        print(f"  ID: {result['id']}")
        print(f"  Score: {result['score']:.4f}")
        print(f"  Content: {result['content'][:80]}...")
        
except Exception as e:
    print(f"\n✗ Search failed: {e}")
    exit(1)

print("\n✓ All tests passed!")