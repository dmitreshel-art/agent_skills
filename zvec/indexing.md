---
description: "Индексация коллекций для быстрого поиска в ZVEC"
version: "1.0.0"
tags: ["zvec", "indexing", "performance", "optimization"]
related: ["collections", "query", "performance"]
---

# Индексация (Indexing)

## Overview

Индексация — это процесс создания структур данных для ускорения поиска. Без индексов, поиск был бы медленным (O(n) для N документов). С индексами, поиск становится быстрым (O(log n)).

## Ключевые концепты

### 1. Index Types (Типы индексов)

```python
import zvec

# HNSW — Hierarchical Navigable Small World
schema = zvec.CollectionSchema(
    name="hnsw_collection",
    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 768),
    index_config={
        "index_type": "hnsw",          # Hierarchical Navigable Small World
        "M": 16,                        # Количество соседей
        "ef_construction": 200         # EF для построения
    }
)

# IVF — Inverted File Index
schema = zvec.CollectionSchema(
    name="ivf_collection",
    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 768),
    index_config={
        "index_type": "ivf",          # Inverted File Index
        "nlist": 1024,                # Количество центроидов
        "nprobe": 64                   # Количество центроидов для проверки
    }
)

collection = zvec.create_and_open(path="./indexed", schema=schema)
```

**Когда использовать:**

| Тип индекса | Для чего | Память | Скорость |
|-------------|----------|--------|---------|
| HNSW | Семантический поиск | Умеренная | Быстрый |
| IVF | Очень большие данные | Большая | Очень быстрый |
| Brute Force | Маленькие данные (<1K) | Минимум | Медленный |

### 2. Index Construction (Построение индекса)

```python
# Индекс создаётся автоматически при вставке
collection.insert([
    zvec.Doc(id="doc_1", vectors={"embedding": vector_1}),
    zvec.Doc(id="doc_2", vectors={"embedding": vector_2}),
    zvec.Doc(id="doc_3", vectors={"embedding": vector_3}),
])

# Индекс построен в памяти и готов к поиску
```

### 3. Index Parameters (Параметры индекса)

```python
# HNSW параметры
schema = zvec.CollectionSchema(
    name="hnsw_optimized",
    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 768),
    index_config={
        "index_type": "hnsw",
        "M": 32,                      # Больше M = быстрее построение, больше памяти
        "ef_construction": 400      # Больше ef = выше точность, больше памяти
        "ef_search": 100             # Параметр для поиска (по умолчанию = ef_construction)
    }
)

collection = zvec.create_and_open(path="./hnsw_optimized", schema=schema)
```

**Рекомендации:**

| Параметр | Маленькие данные | Средние данные | Большие данные |
|----------|---------------|--------------|---------------|
| M (HNSW) | 16 | 24-32 | 48-64 |
| ef_construction (HNSW) | 100 | 200-400 | 400-1000 |
| nlist (IVF) | 128 | 512-1024 | 4096-8192 |

### 4. Index Maintenance (Поддержка индекса)

```python
# Оптимизация индекса после массовых вставок
collection.optimize()

# Восстановление индекса после сбоя
collection.reindex()

# Статистика индекса
index_stats = collection.stats()
print(f"Index health: {index_stats}")
```

## Оптимизация производительности

### 1. Pre-indexing (Предварительная индексация)

```python
# Создайте индекс до вставки данных
schema = zvec.CollectionSchema(
    name="preindexed_collection",
    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 768),
    index_config={
        "index_type": "hnsw",
        "M": 32,
        "ef_construction": 200
    }
)

collection = zvec.create_and_open(path="./preindexed", schema=schema)

# Вставляйте данные пачками
batch_size = 1000
for i in range(0, len(documents), batch_size):
    batch = documents[i:i + batch_size]
    collection.insert(batch)
```

### 2. Lazy Indexing (Ленивая индексация)

```python
# Индексируйте по требованию, а не сразу
class LazyIndexer:
    def __init__(self, schema, path):
        self.schema = schema
        self.path = path
    
    def index_document(self, doc):
        """Индексируйте документ по требованию."""
        collection = zvec.open(self.path)
        collection.insert(doc)
        return

indexer = LazyIndexer(schema=schema, path="./lazy")

# Индексируйте по требованию
for doc in documents:
    indexer.index_document(doc)
```

### 3. Incremental Indexing (Инкрементная индексация)

```python
# Добавляйте новые данные без переиндексации всего
existing_collection = zvec.open(path="./existing")

new_docs = [
    zvec.Doc(id=f"new_doc_{i}", vectors={"embedding": vec})
    for i, vec in enumerate(new_vectors)
]

existing_collection.insert(new_docs)

# Оптимизируйте только часть индекса
existing_collection.partial_reindex(new_docs)
```

## Мониторинг индекса

### Проверка здоровья индекса

```python
# Получите статистику индекса
stats = collection.stats()

print(f"Документов: {stats['document_count']}")
print(f"Размер индекса: {stats['index_size_mb']}MB")
print(f"Время построения: {stats['index_build_time_ms']}ms")
print(f"Среднее время поиска: {stats['avg_search_latency_ms']}ms")
```

### Анализ производительности

```python
import time
import numpy as np

# Измерьте время поиска
query_times = []

for query_vector in query_vectors:
    start = time.time()
    
    results = collection.query(
        zvec.VectorQuery("embedding", vector=query_vector, topk=10)
    )
    
    duration = time.time() - start
    query_times.append(duration)

# Анализ
print(f"Среднее время: {np.mean(query_times) * 1000:.2f}ms")
print(f"P95: {np.percentile(query_times, 95) * 1000:.2f}ms")
print(f"P99: {np.percentile(query_times, 99) * 1000:.2f}ms")
```

## Обновление индекса

### Reindexing (Переиндексация)

```python
# Полная переиндексация
collection.reindex()

print("Индекс перестроен")
```

### Partial Reindexing (Частичная переиндексация)

```python
# Переиндексируйте только часть данных
collection.partial_reindex(
    filter="publish_year >= 2023"  # Только новые документы
)
```

### Adding New Vectors

```python
# Добавьте новые векторы без перестройки всего индекса
new_documents = [
    zvec.Doc(id=f"doc_{i}", vectors={"embedding": vec})
    for i, vec in enumerate(new_vectors)
]

collection.insert(new_documents)
print("Новые векторы добавлены")
```

## Связи

Индексация связана с:
- [[collections]] — Коллекции используют индексы для поиска
- [[query]] — Поиск использует индексы для быстрого доступа
- [[performance]] — Индексация критична для производительности

## Quick Reference

| Операция | Метод | Когда использовать |
|-----------|-------|-----------------|
| Создание индекса | `create_and_open` + index_config | При создании коллекции |
| Оптимизация | `optimize` | После массовых вставок |
| Переиндексация | `reindex` | После значительных изменений |
| Частичное обновление | `insert` | Для добавления новых данных |
| Статистика | `stats` | Для мониторинга |

## Wisdom

> "Good indexing is the difference between a search that works and a search that works at scale." — Unknown

Индексируйте для масштабируемости.
Оптимизируйте для производительности.
Мониторьте здоровье индекса.

Без индексов — медленно.
С хорошими индексами — быстро.

ZVEC даёт вам мощные индексы.
Используйте их мудро.
