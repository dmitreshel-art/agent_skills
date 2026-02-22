"""Setup configuration for agent-memory skill."""

from setuptools import setup, find_packages

setup(
    name="agent-memory",
    version="0.1.0",
    description="Agent Memory System Integration for OpenClaw",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "httpx>=0.25.0",
        "tenacity>=8.2.0",
    ],
    python_requires=">=3.9",
)
