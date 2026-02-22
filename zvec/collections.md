---
description: "Управление коллекциями и данными в ZVEC"
version: "1.0.0"
tags: ["zvec", "collections", "data-management", "crud"]
related: ["installation", "query", "data-operations"]
---

# Коллекции (Collections)

## Overview

Коллекция — это основной контейнер для хранения и поиска документов в ZVEC. Каждая коллекция имеет схему, определяющую типы данных и векторов.

## Создание коллекции

### Определение схемы

```python
import zvec

# Создайте схему коллекции
schema = zvec.CollectionSchema(
    name="my_collection",
    vectors=zvec.VectorSchema(
        name="embedding",          # Имя вектора
        data_type=zvec.DataType.VECTOR_FP32,  # Тип данных (FP32, FP16, FP8)
        dimensions=768              # Размерность (768, 1536, etc.)
    )
)

# Создайте и откройте коллекцию
collection = zvec.create_and_open(path="./my_collection", schema=schema)

print("Коллекция создана: my_collection")
```

### Создание с несколькими векторами

```python
import zvec

# Коллекция с несколькими векторами (dense + sparse)
schema = zvec.CollectionSchema(
    name="hybrid_collection",
    vectors=[
        # Dense вектор для семантического поиска
        zvec.VectorSchema(
            name="embedding",
            data_type=zvec.DataType.VECTOR_FP32,
            dimensions=768
        ),
        
        # Sparse вектор для ключевых слов
        zvec.SparseVectorSchema(
            name="keywords",
            data_type=zvec.DataType.VECTOR_SPARSE,
            dimensions=50000  # Размер словаря
        )
    ]
)

collection = zvec.create_and_open(path="./hybrid_collection", schema=schema)
```

## Вставка документов

### Простой Insert

```python
# Вставка одного документа
collection.insert(
    zvec.Doc(
        id="doc_1",
        vectors={
            "embedding": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
            "metadata": {"category": "tech"}
        }
    )
)
```

### Массовый Insert

```python
# Вставка нескольких документов
documents = [
    zvec.Doc(
        id="doc_2",
        vectors={
            "embedding": [0.2, 0.3, 0.4, 0.5],
            "metadata": {"category": "business"}
        }
    ),
    zvec.Doc(
        id="doc_3",
        vectors={
            "embedding": [0.3, 0.4, 0.5, 0.6],
            "metadata": {"category": "science"}
        }
    )
]

collection.insert(documents)

print(f"Вставлено {len(documents)} документов")
```

### Batch Insert с автоматическими ID

```python
# Вставка без указания ID (автоматическая генерация)
documents = [
    zvec.Doc(
        vectors={
            "embedding": [0.4, 0.5, 0.6],
            "metadata": {"category": "finance"}
        }
    ),
    zvec.Doc(
        vectors={
            "embedding": [0.5, 0.6, 0.7],
            "metadata": {"category": "healthcare"}
        }
    )
]

collection.insert(documents)
print("Документы вставлены с автоматическими ID")
```

## Обновление документов

### Обновление одного документа

```python
# Полное обновление документа
collection.update(
    "doc_1",
    zvec.Doc(
        id="doc_1",
        vectors={
            "embedding": [0.1, 0.2, 0.3, 0.4],  # Обновлённые векторы
            "metadata": {"category": "tech-updated"}  # Обновлённые метаданные
        }
    )
)
```

### Частичное обновление (Upsert)

```python
# Upsert: Insert или Update если существует
documents = [
    zvec.Doc(
        id="doc_1",
        vectors={"embedding": [0.1, 0.2, 0.3, 0.4]},
    ),
    zvec.Doc(
        id="doc_2",
        vectors={"embedding": [0.5, 0.6, 0.7, 0.8]},
    )
]

collection.upsert(documents)
print("Документы обновлены или вставлены")
```

## Удаление документов

### Удаление по ID

```python
# Удаление одного документа по ID
collection.delete(ids="doc_1")
print("Документ doc_1 удалён")

# Удаление нескольких документов
collection.delete(ids=["doc_2", "doc_3"])
print("Документы doc_2 и doc_3 удалены")
```

### Удаление по фильтру

```python
# Удаление всех документов с категорией "old"
collection.delete_by_filter(filter="metadata.category = 'old'")

print("Все старые документы удалены")
```

### Удаление по списку ID

```python
# Получите ID, затем удалите
# Это может быть эффективнее для больших удалений
ids_to_delete = ["doc_4", "doc_5", "doc_6"]

# 1. Получите документы (опционально)
documents = collection.fetch(ids=ids_to_delete)

# 2. Проверьте критерии
valid_ids = [doc.id for doc in documents if meets_criteria(doc)]

# 3. Удалите
collection.delete(ids=valid_ids)
print(f"Удалено {len(valid_ids)} документов из {len(ids_to_delete)}")
```

## Получение документов

### Получение по ID

```python
# Получение одного документа
doc = collection.fetch(ids="doc_1")
print(f"Документ: {doc}")
```

```python
# Получение нескольких документов
documents = collection.fetch(ids=["doc_1", "doc_2", "doc_3"])
for doc in documents:
    print(f"ID: {doc.id}, Категория: {doc.values.get('metadata', {}).get('category')}")
```

### Получение по Query

```python
# Поиск похожих документов и получение их
query_vector = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    include_values=True  # Включить полные значения результатов
)

for result in results:
    doc = collection.fetch(ids=result.id)
    print(f"ID: {result.id}, Score: {result.score}, Категория: {doc.values.get('metadata', {}).get('category')}")
```

## Статистика коллекции

### Просмотр информации о коллекции

```python
# Получите схему коллекции
print("Схема:")
print(collection.schema)

# Получите статистику
print("Статистика:")
stats = collection.stats()
print(stats)
```

### Статистика

```python
# Типичная статистика включает:
stats = {
    "document_count": 100000,      # Всего документов
    "index_type": "hnsw",             # Тип индекса
    "M": 16,                         # Количество соседей HNSW
    "ef_construction": 200,         # EF construction параметр
    "memory_usage": "1.2 GB",          # Использование памяти
    "index_size": "450 MB"             # Размер индекса на диске
}
```

## Оптимизация коллекции

### Создание с оптимизацией

```python
# Оптимизируйте коллекцию для производительности
schema = zvec.CollectionSchema(
    name="optimized_collection",
    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 768),
    index_config={
        "index_type": "hnsw",     # Hierarchical Navigable Small World
        "M": 16,                    # Количество соседей
        "ef_construction": 200     # EF construction параметр
    }
)

collection = zvec.create_and_open(path="./optimized", schema=schema)
```

### Оптимизация после вставки

```python
# После массовой вставки документов
collection.insert(large_batch_documents)

# Оптимизируйте коллекцию для улучшения производительности поиска
collection.optimize()

print("Коллекция оптимизирована")
```

## Транзакции

### Batch Operations с транзакциями

```python
# Вставка документов как одна транзакция
documents = [
    zvec.Doc(id="doc_1", vectors={"embedding": vector_1}),
    zvec.Doc(id="doc_2", vectors={"embedding": vector_2}),
    zvec.Doc(id="doc_3", vectors={"embedding": vector_3}),
]

collection.insert(documents)

# Если одна операция неудачна, все операции откатываются
print("Документы вставлены в транзакции")
```

## Резервное копирование

### Экспорт коллекции

```python
# Экспортируйте коллекцию для резервного копирования
collection.export_backup(path="./backup")

print("Резервная копия создана: ./backup")
```

### Импорт коллекции

```python
# Восстановите коллекцию из резервной копии
collection = zvec.open(path="./backup")

print("Коллекция восстановлена из резервной копии")
```

## Связи

Коллекции связаны с:
- [[query]] — Использование коллекций для поиска
- [[data-operations]] — Операции с данными (insert, update, delete)
- [[performance]] — Оптимизация производительности коллекций
- [[indexing]] — Индексация коллекций для быстрого поиска

## Quick Reference

| Операция | Метод | Описание |
|-----------|-------|-----------|
| Создание | `create_and_open` | Создать и открыть коллекцию |
| Вставка | `insert` | Вставить документы |
| Обновление | `update` | Обновить документ |
| Удаление | `delete` | Удалить по ID |
| Удаление | `delete_by_filter` | Удалить по фильтру |
| Получение | `fetch` | Получить по ID |
| Поиск | `query` | Поиск по сходству |
| Статистика | `stats` | Получить статистику |
| Оптимизация | `optimize` | Оптимизировать |
| Экспорт | `export_backup` | Экспорт в бэкап |
| Импорт | `open` | Импорт из бэкапа |

## Wisdom

> "Data is only as good as the collection that holds it." — Unknown

Организовуйте данные эффективно.
Оптимизируйте для производительности.
Сохраняйте резервные копии.

Хорошие данные = эффективный поиск.
