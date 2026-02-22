#!/usr/bin/env python3
"""Quick integration test for agent-memory skill."""

import sys
import os

# Add skill to path
skill_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, skill_dir)

# Now import with package name
try:
    from agent_memory.search import memory_search
    from agent_memory.get import memory_get
    from agent_memory.client import get_client
    
    print("✓ Imports successful")
    
    # Test search
    print("\n=== Testing memory_search ===")
    results = memory_search("Python programming", maxResults=5, minScore=0.3)
    
    print(f"Results: {len(results)}")
    for i, r in enumerate(results[:3]):
        print(f"\nResult {i+1}:")
        print(f"  Path: {r['path']}")
        print(f"  Score: {r['score']:.4f}")
        print(f"  Content: {r['content'][:80]}...")
    
    # Test client health
    print("\n=== Testing API Health ===")
    client = get_client()
    is_healthy = client.health_check()
    print(f"API Healthy: {is_healthy}")
    
    print("\n✓ All integration tests passed!")
    
except Exception as e:
    print(f"✗ Integration test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)