"""Setup configuration for agent-memory skill."""

from setuptools import setup

# Package structure: all .py files are modules in current directory
# No package subdirectory (agent_memory/* files are at agent-memory/*)
setup(
    name="agent-memory",
    version="0.1.0",
    description="Agent Memory System Integration for OpenClaw",
    packages=["agent_memory"],  # Explicitly define package name
    package_dir=".",  # Current directory is the package root
    install_requires=[
        "httpx>=0.25.0",
        "tenacity>=8.2.0",
    ],
    python_requires=">=3.9",
)