---
description: "Разрежные векторные представления в ZVEC"
version: "1.0.0"
tags: ["zvec", "sparse-vectors", "embeddings", "foundational"]
related: ["installation", "dense-vectors", "query", "collections"]
---

# Разрежные (Sparse) Векторы

## Что такое Sparse Векторы?

Sparse векторы — это высокой размерности векторы, где **только ключевые элементы активны**, а большинство — нулевые. Это другая форма векторных представлений, оптимизированная для поиска по ключевым словам и эффективного хранения.

## Ключевые характеристики

### Высокая размерность

```python
# Sparse вектор над словарём из 50,000 слов
sparse_vector = {
    "король": 2.31,       # "king" имеет высокий вес
    "живёт": 1.85,      # "lives" имеет вес
    "во": 0.92,         # "in" имеет низкий вес
    "дворце": 1.45,      # "palace" имеет высокий вес
    # ... остальные 49,996 размерностей неявно равны 0
}

# Всего: 50,000 словарь, но только ~5-10 слов активны в этом документе
# Размерность: 50,000 (по словарю), но эффективнее для хранения
```

### Ключевые слова

- **Описательный характер** — только важные слова
- **Весовые значения** — отражают важность
- **Разреженность** — ~95-99% элементов нулевые
- **Эффективность хранения** — только активные элементы хранятся явно

### Вычисления

```python
# Вес слова (например, BM25)
weight = idf(term) * tf(document, term)

# Sparse вектор
sparse_vector[term] = weight

# Пример:
# term = "король" с весом 2.31 в документе
# sparse_vector["король"] = 2.31
# sparse_vector["другое слово"] = 0 (не в документе)
```

## Sparse vs Dense

| Характеристика | Sparse Векторы | Dense Векторы |
|---------------|----------------|-----------------|
| Размерность | Высокая (50,000+) | Средняя (384, 768) |
| Размерность | Большинство нулевые | Почти все активны |
| Интерпретация | Прямая (слово → вес) | Неясная (семантика) |
| Использование | Поиск по ключам | Семантический поиск |
| Память | Эффективнее | Больше для хранения |
| Вычисления | Медленнее, но эффективнее | Быстрее, но памяти больше |
| Лучше для | Текстовые запросы | Визуальные/семантические |

## Преимущества

### ✅ Эффективное хранение

```python
# Dense: 768 floats × 4 bytes = 3 KB per vector
dense_storage = 768 * 4  # 3072 bytes

# Sparse: 10 active terms × 4 bytes = 40 bytes
sparse_storage = 10 * 4  # 40 bytes

# Sparse в 100+ раз компактнее!
storage_ratio = dense_storage / sparse_storage
# ~77x more efficient
```

### ✅ Быстрый текстовый поиск

```python
# Поиск по ключевым словам — мгновенно
# Sparse вектор = индекс по слову

sparse_vector["король"] = 2.31
search_results = collection.query_by_key("король", topk=10)
```

### ✅ Подходит для больших словарей

```python
# Эффективно работает с большими словарями
# Даже при 100K, 1M слов sparse векторы работают хорошо

# Оптимизация через хеширование
# Быстрый lookup по term index → hash table
```

### ✅ Интерпретируемость

```python
# Sparse вектор легко интерпретируется
# Каждый активный элемент → понятное слово с весом
# Вес показывает важность слова в документе

# Пример:
sparse_vector = {
    "король": 2.31,     # Очень важно
    "живёт": 1.85,      # Важно
    "во": 0.92          # Менее важно
    "дворце": 1.45       # Важно
    # ... остальные 0
}

# Высокие веса → ключевые темы документа
# Можно понять主要内容 без сложного анализа
```

## Недостатки

### ❌ Нет семантики

```python
# Sparse вектор:
sparse_vector["король"] = 2.31
sparse_vector["монарх"] = 0 (не в документе)

# Dense вектор:
dense_vector[0] = 0.012  # Понимает "король" как концепт
dense_vector[1] = 0.001  # Понимает "монарх" как концепт

# Sparse вектор не понимает что "король" ~ "монарх"
# Нет семантического понимания связей между словами
```

### ❌ Ограниченный поисковый простор

```python
# Sparse вектор можно искать только по точным словам
# Поиск "король" найдёт документы, где есть слово "король"
# Но не найдёт "царь", "правитель", "королева"

# Dense вектор понимает семантику
# Вектор "король" близок к "царь", "правитель"
```

### ❌ Сложные вычисления

```python
# Sparse вектор требуют специальных алгоритмов
# TF-IDF, BM25, cosine similarity для sparse
# Не могут использовать стандартные distance метрики

# Пример:
# Dense: cosine_similarity(vec1, vec2)
# Sparse: BM25 scoring (complex)
```

## Когда использовать Sparse Векторы

### ✅ Для текстового поиска

```python
# Отлично подходит для документного поиска
# Поиск по ключевым словам → быстрая и точная

# Пример: поиск по юридическим документам
sparse_vector = {
    "налог": 3.5,      # Очень важно
    "договор": 2.1,     # Важно
    "процент": 0.8,      # Менее важно
    "ставка": 1.2       # Важно
}

# Поиск: "налоговый договор" → найдёт документы, где есть эти слова
```

### ✅ Для больших словарей

```python
# Sparse векторы эффективно работают с большими словарями
# Даже при 100K, 1M слов

# Оптимизация:
# - Compress sparse vectors (store only active terms)
# - Use integer encoding for terms (0-49999)
# - Use hash tables for fast lookup
```

### ✅ Для рекомендательных систем

```python
# TF-IDF sparse vectors для рекомендаций
# Похожие документы → похожие sparse векторы

# Пример:
# Пользователь купил книгу A → sparse_vector содержит термы книги A
# Пользователь купил книгу B → sparse_vector похож на A
# Рекомендация: книга B
```

## Sparse Векторы в ZVEC

### Создание коллекции

```python
import zvec

# Определите схему для sparse векторов
schema = zvec.CollectionSchema(
    name="sparse_collection",
    vectors=zvec.SparseVectorSchema(
        name="bm25",
        data_type=zvec.DataType.VECTOR_SPARSE,  # Sparse vector type
        dimensions=50000  # Vocabulary size
    )
)

collection = zvec.create_and_open(path="./sparse_data", schema=schema)
```

### Вставка документов

```python
# Вставляйте документы с sparse векторами
documents = [
    zvec.Doc(
        id="doc_1",
        sparse_vectors=zvec.SparseVectorValue(
            name="bm25",
            vector={
                "король": 2.31,
                "жизнь": 1.85,
                "правитель": 1.45
            }
        )
    ),
    zvec.Doc(
        id="doc_2",
        sparse_vectors=zvec.SparseVectorValue(
            name="bm25",
            vector={
                "император": 3.2,
                "королева": 1.85,
                "власть": 1.9
            }
        )
    )
]

collection.insert(documents)
```

### Поиск по sparse векторам

```python
# Поиск по ключевым словам
results = collection.query(
    zvec.VectorQuery(
        name="bm25",
        vector={
            "король": 2.31
        }
    ),
    topk=10
)

# Поиск по нескольким словам
results = collection.query(
    zvec.VectorQuery(
        name="bm25",
        vector={
            "король": 2.31,
            "жизнь": 1.85
        }
    ),
    topk=10
)
```

## Оптимизация Sparse Векторов

### 1. Используйте Integer Encoding

```python
# Вместо строковых ключей используйте целые числа
# 0-49999 = 50K словарь
# Компактнее и быстрее для lookup

term_mapping = {
    "король": 124,    # Индекс в словаре
    "жизнь": 4512,
    "правитель": 9234,
}

sparse_vector = [term_mapping[word] * weight for word in document_terms]
```

### 2. Компрессия векторов

```python
# Храните только активные элементы
active_terms = [term for term, weight in sparse_vector.items() if weight > 0]
compressed_vector = {term: weight for term in active_terms}

# Храните inactive terms отдельно (или не храните вообще)
inactive_terms = [term for term in sparse_vector.keys() if sparse_vector[term] == 0]
```

### 3. Используйте Bitmap

```python
# Для очень разреженных векторов используйте bitmap
# 1 bit per element → 8x сжатие

# Пример:
# Sparse vector: 50K dimensions, 100 active terms
# Dense: 50K floats × 4 bytes = 200KB
# Sparse bitmap: 50K bits = 6.25KB
```

## Смешанные Векторы (Hybrid)

### Dense + Sparse

```python
import zvec

# Комбинируйте dense и sparse векторы
# Dense для семантики, sparse для ключевых слов

schema = zvec.CollectionSchema(
    name="hybrid_collection",
    vectors=[
        zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 768),  # Dense
        zvec.SparseVectorSchema("bm25", zvec.DataType.VECTOR_SPARSE, 50000)   # Sparse
    ]
)

collection = zvec.create_and_open(path="./hybrid_data", schema=schema)

# Вставка документов
collection.insert(
    zvec.Doc(
        id="doc_1",
        vectors={
            "embedding": dense_vector_1,
            "bm25": sparse_vector_1
        }
    )
)
```

### Поиск по гибридным векторам

```python
# Комбинируйте плотный и разреженный поиск
results = collection.query(
    zvec.VectorQuery(
        name="embedding",  # Dense search
        vector=query_dense_vector
    ),
    zvec.VectorQuery(
        name="bm25",  # Sparse filter
        vector={
            "король": 2.31,
            "жизнь": 1.85
        }
    )
)
)
```

## Рекомендации по производительности

### Для Text Search

```python
# 1. Используйте sparse векторы для ключевых слов
# 2. Комбинируйте с dense векторами для семантического понимания
# 3. Используйте TF-IDF или BM25 для весов
# 4. Оптимизируйте словарь (оставьте только важные слова)
# 5. Используйте integer encoding для терминов
```

### Для Memory Optimization

```python
# 1. Ограничьте словарь (50K-100K вместо 1M)
# 2. Используйте 8-bit floats вместо 32-bit
# 3. Компрессуйте sparse векторы (храните только активные)
# 4. Используйте bitmap для очень разреженных данных
```

## Пример: Text Search Engine

```python
import zvec

# Создайте коллекцию для текстового поиска
schema = zvec.CollectionSchema(
    name="text_search",
    vectors=zvec.SparseVectorSchema(
        name="bm25",
        data_type=zvec.DataType.VECTOR_SPARSE,
        dimensions=50000  # Vocabulary size
    )
)

collection = zvec.create_and_open(path="./text_search", schema=schema)

# Индексируйте документы
for doc in documents:
    # Генерируйте sparse вектор (TF-IDF)
    sparse_vector = generate_bm25_vector(doc)
    
    collection.insert(
        zvec.Doc(
            id=doc.id,
            sparse_vectors=zvec.SparseVectorValue(
                name="bm25",
                vector=sparse_vector
            )
        )
    )

# Поиск
query_terms = extract_terms("поиск по документам")
query_vector = bm25_vector(query_terms)

results = collection.query(
    zvec.VectorQuery(
        name="bm25",
        vector=query_vector
    ),
    topk=10
)

# Результаты: документы с наиболее релевантными словами
for result in results:
    print(f"Document: {result.id}, Score: {result.score}")
```

## Связи

Sparse векторы связаны с:
- [[dense-vectors]] — Альтернатива для понимания разницы
- [[query]] — Использование sparse векторов для запросов
- [[collections]] — Работа с sparse коллекциями
- [[installation]] — Установка ZVEC
- [[performance]] — Оптимизация sparse векторов

## Quick Reference

| Тип | Размерность | Память | Использование |
|-----|-----------|--------|-------------|
| Sparse (10K terms) | 50K (100 active) | ~2KB | Текстовый поиск |
| Sparse (100K terms) | 100K (500 active) | ~10KB | Большой корпус |
| Sparse (1M terms) | 1M (2K active) | ~20KB | Очень большой корпус |

## Wisdom

> "In data sparse, structure matters more than density." — Unknown

Разреженность — это сила.
Sparse векторы — это умный компромисс:
- Отказ от семантики ради эффективности
- Экономия памяти и вычислений
- Интерпретируемость через веса

Для текстового поиска — безупорно.
Для семантического понимания — dense векторы.

Выберите правильный инструмент для задачи.
Sparse для точности, dense для смысла.
