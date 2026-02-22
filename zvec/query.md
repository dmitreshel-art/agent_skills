---
description: "Векторные запросы и поиск в ZVEC"
version: "1.0.0"
tags: ["zvec", "query", "search", "retrieval"]
related: ["dense-vectors", "sparse-vectors", "collections"]
---

# Поиск и Запросы (Query)

## Overview

Поиск и запросы — это как находить релевантные документы среди миллионов векторов. ZVEC предоставляет мощный API для векторного поиска с поддержкой различных типов запросов и фильтрацией.

## Ключевые концепции

### Vector Query (Векторный запрос)

Основной метод поиска в векторных базах данных — находит документы с наиболее похожими векторами.

```python
import zvec

# Создайте векторный запрос
query_vector = [0.12, -0.23, 0.45, 0.89]  # 4-мерный вектор

# Выполняйте поиск
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10)
)

# Результаты: документы с similarity scores
for result in results:
    print(f"ID: {result.id}, Score: {result.score}")
```

### Multi-Vector Query (Многовекторный запрос)

Одновременный поиск по нескольким векторам — для более точных результатов.

```python
# Поиск по нескольким признакам
results = collection.query(
    zvec.VectorQuery(
        "embedding",              # Название вектора
        vector=[vec1, vec2, vec3],  # 3 разных вектора
        topk=10
    )
)
```

### Filtered Query (Фильтрованный запрос)

Комбинируйте векторный поиск с фильтрами для точных результатов.

```python
# Фильтры в SQL-подобном синтаксисе
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    filter="publish_year >= 2020"  # Только документы после 2020
)

# Комбинированные фильтры
results = collection.query(
    zvec.VectorQuery(
        "embedding",
        vector=query_vector,
        topk=10
    ),
    filter="publish_year >= 2020 AND category IN ('tech', 'business')"  # Только тех/бизнес документы
)
```

## Типы запросов

### 1. Basic Similarity Search

Базовый поиск по сходству.

```python
# Простая nearest-neighbour search
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10)
)

# Результат: топ-10 самых похожих документов
```

### 2. Ranged Search (Поиск по диапазону)

Ограничение поиска по similarity score.

```python
# Ищите только документы с score >= порога
results = collection.query(
    zvec.VectorQuery(
        "embedding",
        vector=query_vector,
        topk=10,
        min_score=0.7  # Только score >= 0.7
    )
)
```

### 3. HNSW Search

Использование иерархической навигации для ускорения поиска на больших данных.

```python
# HNSW включён по умолчанию
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10)
)
```

### 4. IVF Search (Inverted File Index)

Поиск через инвертированный файловый индекс для масштабируемости.

```python
# IVF для очень больших коллекций
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    index_config={
        "index_type": "ivf",
        "nlist": 1024,  # Количество центроидов
        "nprobe": 64    # Количество проверяемых центроидов
    }
)
```

## Параметры запросов

### topk (Количество результатов)

```python
# Количество документов для возврата
topk = 10  # Вернёт топ-10

results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=topk)
)

# Результат: максимум 10 документов
```

### min_score (Минимальный score)

```python
# Фильтрация по минимальному similarity score
min_score = 0.7

results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10, min_score=min_score)
)
```

### include_values (Включить значения)

```python
# Включите или исключите значения в результаты
results = collection.query(
    zvec.VectorQuery(
        "embedding",
        vector=query_vector,
        topk=10,
        include_values=["content", "metadata"]  # Возвратить дополнительно поля
    )
)

# Результат: результат включает дополнительные поля
for result in results:
    print(f"Content: {result.values['content']}")
    print(f"Metadata: {result.values['metadata']}")
```

## Sparse Vector Queries

### BM25 Query (TF-IDF)

Поиск по ключевым словам с TF-IDF весами.

```python
# Поиск по одному слову
results = collection.query(
    zvec.SparseQuery(
        "bm25",           # Имя вектора
        vector={"word": 2.5}  # Sparse вектор с весом 2.5
        topk=10
    )
)
```

### Multi-Term Query

Поиск по нескольким словам одновременно.

```python
# Поиск по нескольким словам
results = collection.query(
    zvec.SparseQuery(
        "bm25",
        vector={
            "word1": 2.5,
            "word2": 1.8,
            "word3": 3.2
        },
        topk=10
    )
)
```

### Phrase Search

Поиск по фразе (несколько слов вместе).

```python
# Поиск по фразе
results = collection.query(
    zvec.SparseQuery(
        "bm25",
        vector={
            "мама": 2.5,
            "мыла": 1.8
            "рама": 3.2
        },
        topk=10
    )
)
```

## Hybrid Search

Комбинируйте векторный поиск с текстовым фильтрами.

### Dense + Sparse

```python
# Комбинированный поиск
results = collection.query(
    zvec.VectorQuery(
        "embedding",              # Dense vector
        vector=[0.12, -0.23, 0.45],  # Dense vector
        topk=10
    ),
    filter="category IN ('tech', 'business')"  # Sparse фильтр по категориям
)
```

### Reranking (Переранжирование)

```python
# Первичный поиск
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=50)
)

# Переранжирование по дополнительным факторам
reranked = []
for result in results:
    # Учитывайте не только similarity score, но и другие факторы
    rerank_score = result.score * result.values.get('popularity', 1.0)
    reranked.append((rerank_score, result))

# Сортируйте по переранжированному score
reranked.sort(reverse=True, key=lambda x: x[0])

# Возмите топ-10
top_10 = [item[1] for item in reranked[:10]]
```

## Оптимизация производительности

### 1. Используйте подходящий алгоритм

```python
# Для маленьких данных: Brute force
# Для средних данных: HNSW (по умолчанию)
# Для очень больших данных: IVF + HNSW
```

### 2. Оптимизируйте топк (topk)

```python
# Не запрашивайте больше результатов, чем нужно
# Маленький topk = быстрые запросы
# Большой topk = медленные запросы

topk = 10  # Хороший баланс скорости и качества
```

### 3. Используйте кеширование

```python
import time

# Кешируйте популярные запросы
query_cache = {}

def search_with_cache(query_vector):
    cache_key = tuple(query_vector)
    
    if cache_key in query_cache:
        print("Cache hit!")
        return query_cache[cache_key]
    
    results = collection.query(
        zvec.VectorQuery("embedding", vector=query_vector, topk=10)
    )
    
    query_cache[cache_key] = results
    return results
```

## Best Practices

### 1. Начните с малого топка

```python
# Сначала получите топ-10 результатов
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10)
)

# Если пользователь хочет больше, запустите ещё запросы
if len(results) == 10:
    results.extend(
        collection.query(
            zvec.VectorQuery("embedding", vector=query_vector, topk=10, skip=10)
        )
    )
```

### 2. Комбинируйте типы запросов

```python
# Сначала sparse поиск по ключевым словам
sparse_results = collection.query(
    zvec.SparseQuery("bm25", vector={"word": 2.5}, topk=10)
)

# Затем dense поиск по семантике
dense_results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10)
)

# Комбинируйте результаты
combined = {}
for result in sparse_results:
    combined[result.id] = result.score + dense_results.get(result.id, 0)
```

### 3. Используйте фильтры для точности

```python
# Точные запросы за счёт фильтрации
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    filter="publish_year >= 2023 AND category = 'tech'"
)

# Результаты: точные и релевантные
```

### 4. Параллельные запросы

```python
import concurrent.futures

def parallel_search(collection, queries):
    """Параллельное выполнение нескольких запросов"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for query_vector in queries:
            future = executor.submit(
                collection.query,
                zvec.VectorQuery("embedding", vector=query_vector, topk=10)
            )
            futures.append(future)
        
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.extend(future.result())
    
    return results
```

## Связи

Поиск связан с:
- [[dense-vectors]] — Для плотных векторных запросов
- [[sparse-vectors]] — Для разреженных векторных запросов
- [[collections]] — Хранилище данных для поиска
- [[performance]] — Оптимизация производительности поиска

## Quick Reference

| Тип запроса | Когда использовать | Пример |
|-------------|-----------------|--------|
| Dense Query | Семантический поиск | `query(vector)` |
| Sparse Query | Поиск по словам | `sparse_query(vector)` |
| Hybrid Query | Семантика + фильтры | `query(vector, filter="...")` |
| Multi-Vector | Несколько признаков | `query([v1, v2, v3])` |

## Wisdom

> "Search is about finding the needle in the haystack, not finding the perfect needle."

Поиск — это приближение.
Хорош enough результатов лучше, чем идеальный поиск, который занимает вечность.

Используйте топк, фильтры и кеширование для быстрого и точного поиска.
