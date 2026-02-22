---
description: "Интеграция ZVEC с OpenClaw системой"
version: "1.0.0"
tags: ["zvec", "integration", "openclaw", "agent"]
related: ["installation", "collections", "query", "skill-graph-creation"]
---

# Интеграция с OpenClaw

## Overview

Интеграция ZVEC с OpenClaw делает векторную базу данных частью вашей системы знаний. Агент OpenClaw может использовать ZVEC для семантического поиска документов из графов навыков (skill-graphs).

## Ключевые концепты

### 1. ZVEC как Knowledge Graph (Graph Knowledge)

**Что это:** Использование ZVEC для хранения и поиска связей между документами в ваших графах навыков.

**Пример:**
```python
import zvec

# Создайте коллекцию для skill-graphs
schema = zvec.CollectionSchema(
    name="skill_graphs",
    vectors=zvec.VectorSchema("skill_embedding", zvec.DataType.VECTOR_FP32, 768)
)

collection = zvec.create_and_open(path="./skill_graphs_data", schema=schema)

# Индексируйте навыки
for skill_file in skill_files:
    # Создайте embedding из содержания навыка
    skill_content = read_skill(skill_file)
    skill_embedding = zvec.encode(skill_content)
    
    collection.insert(
        zvec.Doc(
            id=skill_file,
            vectors={
                "skill_embedding": skill_embedding,
                "tags": ["zvec", "development", "trading"]
            }
        )
    )
```

### 2. RAG (Retrieval-Augmented Generation)

**Что это:** Использование ZVEC для получения релевантных документов и подачи их в LLM.

**Пример:**
```python
import zvec

# 1. Создайте векторный запрос
query_text = "Как управлять рисками в трейдинге?"
query_vector = zvec.encode(query_text)

# 2. Поиск по сходству
results = zvec_collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=5)
)

# 3. Создайте контекст
context = "\n\n".join([
    f"Document: {r.id}\n"
    f"Score: {r.score}\n"
    for r in results
])

# 4. Питайте в LLM
response = llm.generate(
    prompt=f"На основе этих документов:\n{context}\n\nОтветь на вопрос: {query_text}",
    max_tokens=1000
)
```

### 3. Hybrid Search (Гибридный поиск)

**Что это:** Комбинация векторного поиска с фильтрацией по графу знаний.

**Пример:**
```python
import zvec

# 1. Векторный поиск
query_vector = zvec.encode("risk management")
results = zvec_collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=20)
)

# 2. Фильтрация по графу знаний
filtered_results = []
for result in results:
    # Проверяйте теги документа
    doc_tags = result.values.get('tags', [])
    
    # Фильтруйте по графу
    if 'trading' in doc_tags and 'risk' in doc_tags:
        filtered_results.append(result)

# 3. Верните топ-10
top_10 = filtered_results[:10]
```

## OpenClaw Integration

### 1. Навигация по графу с ZVEC

**Концепция:** Используйте ZVEC для поиска релевантных навыков.

**Пример:**
```python
import zvec

# 1. Создайте коллекцию навыков
schema = zvec.CollectionSchema(
    name="skills",
    vectors=zvec.VectorSchema("skill_embedding", zvec.DataType.VECTOR_FP32, 768)
)

collection = zvec.create_and_open(path="./skills_data", schema=schema)

# 2. Индексируйте все навыки из всех графов
for graph_name in ['trading-graph', 'development-graph', 'zvec']:
    for skill_file in list(f"skill-graphs/{graph_name}/*.md"):
        with open(skill_file, 'r') as f:
            content = f.read()
            # Получите описание из YAML
            description = extract_yaml_description(content)
            
            # Создайте embedding
            embedding = zvec.encode(description)
            
            collection.insert(
                zvec.Doc(
                    id=skill_file,
                    vectors={
                        "skill_embedding": embedding,
                        "graph_name": graph_name
                    }
                )
            )

# 3. Поиск по навыкам
query_text = "Как писать чистый код?"
query_vector = zvec.encode(query_text)

results = collection.query(
    zvec.VectorQuery("skill_embedding", vector=query_vector, topk=10)
)

# 4. Верните релевантные навыки
for result in results:
    print(f"{result.id} - Score: {result.score}")
    print(f"Graph: {result.values.get('graph_name', '')}")
```

### 2. Semantic Search Across Graphs

**Концепция:** Поиск документов из разных графов по смыслу.

**Пример:**
```python
import zvec

# Создайте коллекцию для всех документов
all_docs_collection = zvec.create_and_open(
    path="./all_docs_data",
    schema=zvec.CollectionSchema(
        name="all_docs",
        vectors=zvec.VectorSchema("doc_embedding", zvec.DataType.VECTOR_FP32, 768)
    )
)

# Индексируйте документы из разных графов
for file in find_all_skill_files():
    content = read_file(file)
    embedding = zvec.encode(content)
    
    all_docs_collection.insert(
        zvec.Doc(
            id=file,
            vectors={"doc_embedding": embedding}
        )
    )

# Кросс-графовый поиск
query_text = "кросс-графовые практики"
query_vector = zvec.encode(query_text)

results = all_docs_collection.query(
    zvec.VectorQuery("doc_embedding", vector=query_vector, topk=10)
)

# Результаты могут быть из разных графов
for result in results:
    print(f"{result.id} (из {extract_graph_name(result.id)})")
```

### 3. Graph Traversal (Траверсия графа)

**Концепция:** Используйте ZVEC для поиска путей через граф.

**Пример:**
```python
import zvec

# 1. Создайте коллекцию связей
schema = zvec.CollectionSchema(
    name="graph_links",
    vectors=zvec.VectorSchema("link_embedding", zvec.DataType.VECTOR_FP32, 384)
)

links_collection = zvec.create_and_open(path="./links_data", schema=schema)

# 2. Индексируйте связи
for graph_name in ['trading-graph', 'development-graph']:
    skills = list_skills_in_graph(graph_name)
    
    for i, skill_a in enumerate(skills):
        for j, skill_b in enumerate(skills):
            if i == j:
                continue
            
            # Проверяйте связь (wiki-links в файлах)
            if skills_are_connected(skill_a, skill_b):
                link_text = f"{skill_a} related to {skill_b}"
                embedding = zvec.encode(link_text)
                
                links_collection.insert(
                    zvec.Doc(
                        id=f"{skill_a}_{skill_b}",
                        vectors={"link_embedding": embedding},
                        values={
                            "source": skill_a,
                            "target": skill_b,
                            "graph_name": graph_name
                        }
                    )
                )
```

## Best Practices

### 1. Batch Indexing

```python
import zvec

# Индексируйте пачками вместо по одному
batch_size = 100

for i in range(0, len(documents), batch_size):
    batch = documents[i:i + batch_size]
    collection.insert(batch)

    print(f"Индексировано {i + batch_size} из {len(documents)}")
```

### 2. Incremental Updates

```python
import zvec

# Добавляйте новые навыки без переиндексации всего
new_skills = find_new_skills()

for skill in new_skills:
    content = read_skill(skill)
    embedding = zvec.encode(content)
    
    collection.insert(
        zvec.Doc(
            id=skill,
            vectors={"skill_embedding": embedding}
        )
    )

# Не оптимизируйте сразу
# collection.optimize()  # Можно, но не обязательно
```

### 3. Query Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def search_skills(query_text):
    """Кешированный поиск по навыкам."""
    query_vector = zvec.encode(query_text)
    return collection.query(
        zvec.VectorQuery("skill_embedding", vector=query_vector, topk=10)
    )
```

## OpenClaw Agent Integration

### Псевдокод для агента

```python
class ZVECSearchEngine:
    """Search engine for OpenClaw agent using ZVEC."""
    
    def __init__(self, collection_path="./skill_graphs_data"):
        self.collection = zvec.open(collection_path)
    
    def search_skills(self, query_text, topk=10, graph_filter=None):
        """
        Поиск релевантных навыков в ZVEC.
        
        Args:
            query_text: Текст запроса
            topk: Количество результатов
            graph_filter: Фильтр по графу (например, ['trading-graph'])
        
        Returns:
            Список найденных навыков
        """
        query_vector = zvec.encode(query_text)
        
        # Выполняйте поиск
        results = self.collection.query(
            zvec.VectorQuery("skill_embedding", vector=query_vector, topk=topk*2)
        )
        
        # Фильтруйте по графу если указан
        if graph_filter:
            results = [
                r for r in results
                if r.values.get('graph_name', '') in graph_filter
            ]
        
        # Верните топ-N результатов
        return results[:topk]
    
    def search_documents(self, query_text, topk=10):
        """Поиск документов в ZVEC."""
        query_vector = zvec.encode(query_text)
        
        results = self.collection.query(
            zvec.VectorQuery("doc_embedding", vector=query_vector, topk=topk)
        )
        
        return results
    
    def cross_graph_search(self, query_text, topk=5):
        """
        Кросс-графовый поиск — находит релевантные навыки
        из разных графов (trading, development, etc.)
        """
        query_vector = zvec.encode(query_text)
        
        # Выполняйте поиск
        results = self.collection.query(
            zvec.VectorQuery("skill_embedding", vector=query_vector, topk=topk*3)
        )
        
        # Группируйте по графам
        grouped_results = {}
        for result in results:
            graph_name = result.values.get('graph_name', 'unknown')
            if graph_name not in grouped_results:
                grouped_results[graph_name] = []
            grouped_results[graph_name].append(result)
        
        # Верните топ-N результатов из каждого графа
        return grouped_results
```

## Примеры использования

### 1. Поиск навыков для OpenClaw агента

```python
# Инициализируйте движок
search_engine = ZVECSearchEngine()

# Поиск релевантных навыков
query = "Как управлять рисками в трейдинге?"
results = search_engine.search_skills(query, topk=5)

# Обработка результатов
for result in results:
    print(f"{result.id} (Score: {result.score})")
    skill_content = read_skill_file(result.id)
    
    # Используйте в агенте
    openclaw_agent.process_skill(skill_content)
```

### 2. RAG с ZVEC и OpenClaw

```python
import zvec
from openclaw import LLMClient

# 1. Создайте коллекцию для RAG
rag_collection = zvec.create_and_open(
    path="./rag_data",
    schema=zvec.CollectionSchema(
        name="rag",
        vectors=zvec.VectorSchema("doc_embedding", zvec.DataType.VECTOR_FP32, 768)
    )
)

# 2. Индексируйте документы
for doc in documents:
    content = read_document(doc)
    embedding = zvec.encode(content)
    
    rag_collection.insert(
        zvec.Doc(
            id=doc.id,
            vectors={"doc_embedding": embedding}
        )
    )

# 3. RAG запрос
query = "Как использовать stop-loss стратегию в трейдинге?"
query_vector = zvec.encode(query)

# 4. Поиск релевантных документов
results = rag_collection.query(
    zvec.VectorQuery("doc_embedding", vector=query_vector, topk=5)
)

# 5. Создайте контекст
context = "\n\n".join([
    f"Document {i + 1} (Score: {r.score}):\n{read_document(r.id)}"
    for i, r in enumerate(results)
])

# 6. Запрос к LLM
llm = LLMClient()
response = llm.generate(
    prompt=f"На основе этих документов:\n{context}\n\nОтветь: {query}",
    max_tokens=1000
)

print(response)
```

## Integration Points

### OpenClaw System Components

| Компонент | Интеграция | Описание |
|-----------|-------------|-----------|
| Skill Graphs | ZVEC | Семантический поиск по навыкам |
| Agent | ZVEC Search Engine | Агент использует ZVEC для поиска |
| Knowledge Base | ZVEC | Документы индексируются в ZVEC |
| CLI | ZVEC API | `/zvec` команды для управления |

### Workflow

```
User Query
    ↓
OpenClaw Agent
    ↓
ZVEC Search Engine
    ↓
ZVEC Collection
    ↓
Semantic Search
    ↓
Relevant Skills/Documents
    ↓
Knowledge Processing
    ↓
Response to User
```

## Quick Reference

| Тип интеграции | Когда использовать | Пример |
|---------------|-----------------|--------|
| Skill Search | Поиск релевантных навыков | `search_skills("clean code")` |
| Document Search | Поиск документов | `search_documents("risk management")` |
| RAG | RAG pipeline | `rag_query("How to use stop-loss?")` |
| Cross-Graph | Поиск между графами | `cross_graph_search("testing practices")` |

## Связи

Интеграция связана с:
- [[installation]] — Установка ZVEC для интеграции
- [[collections]] — Коллекции для хранения данных
- [[query]] — Поиск в интегрированной системе
- [[performance]] — Оптимизация интеграции

## Wisdom

> "Integration is about making pieces work together, not about making pieces alone." — Unknown

ZVEC + OpenClaw = Синергия.
Семантический поиск + Граф знаний = Мощный агент.

Интегрируйте мудро.
```

**Примечание:** Этот файл — кросс-графовая ссылка на Development Graph, обеспечивающая связи между ZVEC и OpenClaw экосистемой.

---

*Полная информация о ZVEC:* [[installation]]
*Полная информация о графах навыков:* [[foundations]]