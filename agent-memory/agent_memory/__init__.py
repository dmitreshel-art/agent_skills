"""
Agent Memory System Integration for OpenClaw.

Provides semantic memory search using vector database (Qdrant).
Replaces MEMORY.md with fast, scalable, multilingual knowledge retrieval.
"""

__version__ = "0.1.0"
__author__ = "Шелдон (AI-ассистент)"

# Используем фактическое имя пакета (с подчёркиванием)
try:
    from agent_memory.search import memory_search
    from agent_memory.get import memory_get
except ImportError:
    # Fallback на пробел (редактируемые установки)
    from agent_memory.search import memory_search
    from agent_memory.get import memory_get

__all__ = ["memory_search", "memory_get"]