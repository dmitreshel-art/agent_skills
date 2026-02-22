---
description: "Фильтрация результатов поиска в ZVEC"
version: "1.0.0"
tags: ["zvec", "filtering", "query", "data-operations"]
related: ["data-operations", "query", "collections"]
---

# Filtering (Фильтрация)

## Overview

Фильтрация — это ограничение результатов поиска для получения более релевантных документов. Вместо "похожие документы", вы получаете "похожие документы, которые удовлетворяют вашим критериям".

## Ключевые концепции

### SQL-подобные фильтры

Фильтры в ZVEC используют SQL-подобный синтаксис:

```python
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    filter="publish_year >= 2020"  # Только новые документы
)
```

### Типы фильтров

| Тип | Пример | Описание |
|-----|---------|-----------|
| Equality | `category = 'tech'` | Точное совпадение |
| Comparison | `price > 100` | Сравнение |
| Range | `year BETWEEN 2020 AND 2023` | Диапазон |
| Set membership | `category IN ('tech', 'business')` | Несколько значений |
| Logical | `year >= 2020 AND category = 'tech'` | Комбинация |

## Операции с фильтрацией

### Фильтрация по числовым полям

```python
import zvec

# Фильтрация по цене
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    filter="price > 100"  # Только документы с ценой > $100
)

# Фильтрация по диапазону
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    filter="price BETWEEN 50 AND 150"  # Цена между $50 и $150
)
```

### Фильтрация по строкам

```python
# Точное совпадение
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    filter="category = 'tech'"  # Только технологические документы
)

# Частичное совпадение (LIKE)
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    filter="title LIKE '%Python%'"
)

# IN оператор (несколько значений)
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    filter="category IN ('tech', 'business', 'science')"
)
```

### Логические фильтры

```python
# AND — все условия должны выполняться
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    filter="category = 'tech' AND publish_year >= 2020"
)

# OR — хотя бы одно условие
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    filter="category = 'tech' OR category = 'business'"
)

# NOT — условие не должно выполняться
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    filter="NOT category = 'archived'"
)

# Комбинация AND/OR с группировкой
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    filter="(category = 'tech' OR category = 'business') AND publish_year >= 2020"
)
```

## Гибридный поиск (Semantic + Filtering)

### Комбинация с векторным поиском

```python
# 1. Semantic search
query_vector = zvec.encode("поиск по смыслу")

results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=100),  # Получаем 100 кандидатов
    filter="category = 'tech' AND publish_year >= 2020"
)

# 2. Post-processing фильтрация
filtered_results = [r for r in results if r.score > 0.7]  # Высокая схожесть
filtered_results = sorted(filtered_results, key=lambda x: x.values.get('popularity', 0), reverse=True)  # Сортировка по популярности

# 3. Реранжирование
final_results = filtered_results[:10]  # Берём топ-10
```

### Многоуровневая фильтрация

```python
# Первый уровень: Сильные фильтры (SQL)
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=50),
    filter="category = 'tech' AND price > 100"
)

# Второй уровень: Слабые фильтры (post-processing)
level1_results = results
level2_filtered = [r for r in level1_results if r.values.get('rating', 0) >= 4]

# Третий уровень: Кастомный бизнес-логика
final_results = sorted(
    level2_filtered,
    key=lambda x: calculate_relevance(x)
)[:10]
```

## Предфильтрация

### Кеширование популярных запросов

```python
import zvec

# Кешируйте результаты популярных запросов
query_cache = {}

def search_with_cache(query_vector, query_terms):
    cache_key = tuple(query_vector[:10])  # Первые 10 значений
    
    if cache_key in query_cache:
        return query_cache[cache_key]
    
    # Выполняем поиск
    results = collection.query(
        zvec.VectorQuery("embedding", vector=query_vector, topk=10),
        filter="category IN (select_categories(query_terms))"
    )
    
    # Кешируем результат
    query_cache[cache_key] = results
    return results

def select_categories(terms):
    """Выбор категории на основе терминов."""
    if 'tech' in terms:
        return ['tech']
    elif 'business' in terms:
        return ['business']
    else:
        return ['tech', 'business', 'science']
```

### Географические и временные фильтры

```python
# Временные фильтры
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    filter="publish_date >= '2024-01-01' AND publish_date <= '2024-12-31'"
)

# Временной диапазон
from datetime import datetime, timedelta

last_30_days = datetime.now() - timedelta(days=30)
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    filter=f"publish_date >= '{last_30_days.date()}'"
)
```

## Сложные фильтры

### Faceted Search (Фацетный поиск)

```python
import zvec

# Фацетный поиск с несколькими фильтрами
def faceted_search(category, price_range, year_range):
    """Выполняет фацетный поиск с несколькими критериями."""
    
    results = collection.query(
        zvec.VectorQuery("embedding", vector=query_vector, topk=50),
        filter=f"""
            category = '{category}'
            AND price >= {price_range[0]}
            AND price <= {price_range[1]}
            AND publish_year >= {year_range[0]}
            AND publish_year <= {year_range[1]}
        """
    )
    
    # Альтернативная фильтрация
    filtered = [
        r for r in results
        if r.values.get('rating', 0) >= 4
    ]
    
    return sorted(filtered, key=lambda x: x.score, reverse=True)[:10]

# Использование
results = faceted_search('tech', [100, 500], [2020, 2023])
```

## Оптимизация фильтрации

### Использование индексов

```python
# Создайте индекс на часто фильтруемых полях
# ZVEC автоматически оптимизирует фильтры при вставке

# При создании коллекции
schema = zvec.CollectionSchema(
    name="optimized_collection",
    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 768),
    indexes=[
        zvec.IndexSchema("category", zvec.DataType.STRING),  # Индекс на категорию
        zvec.IndexSchema("publish_year", zvec.DataType.INT32)     # Индекс на год
    ]
)

collection = zvec.create_and_open(path="./optimized", schema=schema)
```

### Предвычисление значений

```python
# Предвычисляйте часто используемые значения
popular_categories = ['tech', 'business', 'science']
popular_years = [2020, 2021, 2022, 2023]

# Создайте кешированные фильтры
cached_filters = {
    'tech_only': "category IN ('tech', 'science')",
    'recent_years': f"publish_year >= {min(popular_years)}"
}
```

## Связи

Фильтрация связано с:
- [[data-operations]] — Операции CRUD используют фильтры
- [[query]] — Поиск часто комбинируется с фильтрацией
- [[collections]] — Коллекции обеспечивают фильтрацию

## Quick Reference

| Тип фильтра | Синтаксис | Пример |
|-------------|----------|--------|
| Equality | `field = 'value'` | `category = 'tech'` |
| Comparison | `field > 100` | `price > 100` |
| Range | `BETWEEN a AND b` | `price BETWEEN 50 AND 100` |
| Set | `IN (...)` | `category IN ('tech', 'business')` |
| Logical | `AND, OR, NOT` | `year >= 2020 AND status = 'active'` |

## Wisdom

> "Filtering is about relevance, not restriction. Good filters find what users want, not what they don't." — Unknown

Фильтрация — это баланс.
Не слишком строго → потеряете результаты
Не слишком слабо → получаете мусор

Найдите золотую середину.
Точные результаты.
Релевантные фильтры.

Фильтрация улучшает поиск.
