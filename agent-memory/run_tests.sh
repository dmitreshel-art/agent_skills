#!/bin/bash
# Run tests with proper Python path setup

cd "$(dirname "$0")"

# Add skill to Python path
export PYTHONPATH="/root/.openclaw/workspace/skills/agent-memory:$PYTHONPATH"

# Run integration test
python3 test_integration.py

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "✓ Integration tests passed"
else
    echo "✗ Integration tests failed"
fi

exit $exit_code