---
description: "CRUD операции с данными в ZVEC (перенаправление на Development Graph)"
version: "1.0.0"
tags: ["zvec", "data-operations", "development", "crud"]
related: ["collections", "query", "integration-openclaw"]
---

# Data Operations

Data Operations — это все операции создания, чтения, обновления и удаления данных в ZVEC коллекции. Это фундамент для любой работы с векторными данными.

## Обзор

CRUD операции — Create, Read, Update, Delete — это база любого приложения с базой данных.

> **💡 Полная информация:** Подробное описание всех операций CRUD находится в [[foundations]] (Development Graph)

## Ключевые концепции

### 1. Insert (Вставка документов)

```python
import zvec

# Простая вставка
collection.insert(
    zvec.Doc(
        id="doc_1",
        vectors={"embedding": vector_1}
    )
)

# Массовая вставка
documents = [
    zvec.Doc(id=f"doc_{i}", vectors={"embedding": vec})
    for i, vec in enumerate(vectors)
]
collection.insert(documents)
```

### 2. Update (Обновление документов)

```python
# Полное обновление
collection.update(
    "doc_1",
    zvec.Doc(
        id="doc_1",
        vectors={"embedding": updated_vector}
    )
)

# Частичное обновление
collection.update(
    "doc_1",
    zvec.Doc(
        id="doc_1",
        values={"category": "updated"}  # Обновление только скаляров
    )
)
```

### 3. Delete (Удаление документов)

```python
# Удаление по ID
collection.delete(ids="doc_1")

# Удаление по списку ID
collection.delete(ids=["doc_1", "doc_2", "doc_3"])

# Удаление по фильтру
collection.delete_by_filter(filter="category = 'old'")
```

### 4. Fetch (Получение документов)

```python
# Получение одного документа
doc = collection.fetch(ids="doc_1")

# Получение нескольких документов
docs = collection.fetch(ids=["doc_1", "doc_2", "doc_3"])

# Получение с включением значений
docs = collection.fetch(ids=["doc_1"], include_values=["content", "metadata"])
```

## Пример использования

### Полный CRUD цикл

```python
import zvec

# 1. CREATE (Создание)
collection.insert(
    zvec.Doc(
        id="user_123",
        vectors={"embedding": user_vector},
        values={"name": "John Doe", "email": "john@example.com"}
    )
)

# 2. READ (Чтение)
user = collection.fetch(ids="user_123")
print(f"User: {user.values['name']}")

# 3. UPDATE (Обновление)
collection.update(
    "user_123",
    zvec.Doc(
        id="user_123",
        values={"email": "john.updated@example.com"}
    )
)

# 4. DELETE (Удаление)
collection.delete(ids="user_123")
```

### Batch Operations (Пакетные операции)

```python
# Массовая вставка
users_batch = [
    zvec.Doc(id=f"user_{i}", vectors={"embedding": vec})
    for i, vec in enumerate(vectors)
]
collection.insert(users_batch)

# Массовое обновление
updates = [
    zvec.Doc(id=f"user_{i}", values={"active": status})
    for i, status in enumerate(status_list)
]
collection.updates(updates)

# Массовое удаление
collection.delete(ids=[f"user_{i}" for i in range(10)])
```

## Связи

Data Operations связано с:
- [[collections]] — Коллекции хранят данные
- [[query]] — Запросы для чтения данных
- [[installation]] — ZVEC обеспечивает эти операции

## Quick Reference

| Операция | Метод | Описание |
|-----------|-------|-----------|
| Insert | `insert` | Создание нового документа |
| Read | `fetch` | Получение документа по ID |
| Update | `update` | Обновление документа |
| Delete | `delete` | Удаление по ID |
| Delete | `delete_by_filter` | Удаление по условию |

## Wisdom

> "Data operations are the heartbeat of any application. Make them fast, make them reliable, make them atomic." — Unknown

Операции с данными — это пульс любого приложения.
Делайте их быстрыми, надёжными, атомарными.
