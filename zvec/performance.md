---
description: "Производительность и оптимизация в ZVEC"
version: "1.0.0"
tags: ["zvec", "performance", "optimization", "benchmarking"]
related: ["collections", "indexing", "query"]
---

---
description: "Производительность и оптимизация в ZVEC"
version: "1.0.0"
tags: ["zvec", "performance", "optimization", "benchmarking"]
related: ["collections", "indexing", "query"]
---

# Производительность (Performance)

## Overview

Производительность ZVEC — это как быстро и эффективно система обрабатывает данные. ZVEC оптимизирован для sub-millisecond задержек и миллисекундного поиска на миллиарды векторов.

## Ключевые показатели

### Latency (Задержка)

```python
import time

# Измерение времени запроса
start = time.time()
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10)
duration = time.time() - start

latency_ms = duration * 1000
print(f"Query latency: {latency_ms:.2f}ms")
```

**Целевые показатели:**
- **Excellent:** < 1ms
- **Good:** 1-5ms
- **Acceptable:** 5-10ms
- **Poor:** > 10ms

### Throughput (Пропускная способность)

```python
# Количество запросов в секунду
import time

def measure_throughput(collection, query_vectors):
    start = time.time()
    
    for query_vector in query_vectors:
        results = collection.query(
            zvec.VectorQuery("embedding", vector=query_vector, topk=10)
        )
    
    duration = time.time() - start
    queries_per_second = len(query_vectors) / duration
    
    return queries_per_second

throughput = measure_throughput(collection, query_vectors)
print(f"Throughput: {throughput:.2f} queries/sec")
```

**Ориентировка:**
- **Excellent:** > 1000 queries/sec
- **Good:** 500-1000 queries/sec
- **Acceptable:** 100-500 queries/sec
- **Poor:** < 100 queries/sec

## Индексация

### HNSW (Hierarchical Navigable Small World)

```python
import zvec

# Определите HNSW параметры
schema = zvec.CollectionSchema(
    name="hnsw_optimized",
    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 768),
    index_config={
        "index_type": "hnsw",        # Hierarchical Navigable Small World
        "M": 16,                      # Количество соседей для построения графа
        "ef_construction": 200    # Количество соседей для построения
    }
)

collection = zvec.create_and_open(path="./hnsw_collection", schema=schema)
```

**HNSW Параметры:**

| Параметр | Описание | Рекомендация |
|----------|-----------|----------------|
| M | Количество соседей | 16-32 для хорошего баланса скорости/точности |
| ef_construction | EF для построения | 200-400 для больших данных |
| ef_runtime | EF для поиска (по умолчанию = ef_construction) | Может быть выше для точности |

### IVF (Inverted File Index)

```python
import zvec

# Определите IVF параметры
schema = zvec.CollectionSchema(
    name="ivf_optimized",
    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 768),
    index_config={
        "index_type": "ivf",         # Inverted File Index
        "nlist": 1024,               # Количество центроидов
        "nprobe": 16                 # Количество центроидов для проверки
    }
)

collection = zvec.create_and_open(path="./ivf_collection", schema=schema)
```

**IVF Параметры:**

| Параметр | Описание | Рекомендация |
|----------|-----------|----------------|
| nlist | Количество центроидов | 1024-4096 для больших данных |
| nprobe | Количество центроидов для проверки | 16-64 для баланса |

## Масштабируемость

### Размеры коллекций

```python
# Маленькая коллекция (<10K векторов)
small_collection = zvec.create_and_open(path="./small", schema=schema)

# Средняя коллекция (10K-100K векторов)
medium_collection = zvec.create_and_open(path="./medium", schema=schema)

# Большая коллекция (100K-1M векторов)
large_collection = zvec.create_and_open(path="./large", schema=schema)

# Очень большая коллекция (1M-10M векторов)
xlarge_collection = zvec.create_and_open(path="./xlarge", schema=schema)
```

**Производительность по размерам:**

| Размер | Queries/sec | Latency (p99) | Memory |
|--------|---------------|---------------|---------|
| < 10K | > 2000 | < 2ms | < 100MB |
| 10K-100K | 500-1000 | 2-5ms | 1-2GB |
| 100K-1M | 100-500 | 5-10ms | 5-10GB |
| 1M-10M | 10-100 | 10-50ms | 20-100GB |

### Batch Operations

```python
# Вставка документов пачками (bulk insert)
batch_size = 1000

for i in range(0, len(documents), batch_size):
    batch = documents[i:i + batch_size]
    collection.insert(batch)

print(f"Вставлено {len(documents)} документов пачками по {batch_size}")
```

## Оптимизация памяти

### Vector Types (Типы векторов)

```python
import zvec

# Используйте более компактные типы
schema = zvec.CollectionSchema(
    name="memory_optimized",
    vectors=[
        # FP16 вместо FP32 (50% меньше памяти)
        zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP16, 768),
        
        # FP8 для ещё меньше памяти (но потеря точности)
        zvec.VectorSchema("compressed", zvec.DataType.VECTOR_FP8, 768),
        
        # Sparse векторы для text data (эффективнее для больших словарей)
        zvec.SparseVectorSchema("keywords", zvec.DataType.VECTOR_SPARSE, 50000)
    ]
)

collection = zvec.create_and_open(path="./memory_optimized", schema=schema)
```

**Память по типам:**

| Тип | Память на вектор (768D) | Точность | Использование |
|-----|---------------------|---------|-------------|
| FP32 | 3KB | Высокая | General purpose |
| FP16 | 1.5KB | Хорошая | Визуальные данные |
| FP8 | 750B | Средняя | Кэшируемые данные |
| Sparse | 200KB | Зависит | Text search |

### Product Quantization (Квантование произведений)

```python
# Используйте PQ (Product Quantization) для большого сокращения памяти
# Разделите векторы на под-векторы (sub-vectors) и квантуйте их

schema = zvec.CollectionSchema(
    name="pq_optimized",
    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 768),
    index_config={
        "index_type": "pq",          # Product Quantization
        "M": 256,                  # Количество центроидов для квантования
        "ef_construction": 128,  # EF для построения
    }
)

collection = zvec.create_and_open(path="./pq_collection", schema=schema)
```

**Плюсы PQ:**
- 75-90% меньше памяти
- Сравнимая скорость поиска
- Подходит для больших коллекций

**Минусы PQ:**
- Небольшая потеря точности
- Больше сложность оптимизации

## Оптимизация запросов

### 1. Используйте кеширование

```python
import time
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_embedding(text):
    """Кешированная функция для эмбеддинга."""
    return embedding_model.encode(text)

# Используйте в запросах
def search_with_cache(query_text):
    query_vector = cached_embedding(query_text)
    
    results = collection.query(
        zvec.VectorQuery("embedding", vector=query_vector, topk=10)
    )
    
    return results
```

### 2. Уменьшите topk

```python
# Запрашивайте только необходимые результаты
# Если для UI нужно только топ-5, не запрашивайте топ-10

results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=5)  # Вместо 10
)
```

### 3. Используйте фильтрацию

```python
# Фильтруйте результаты до получения большего topk
# Это уменьшает объём данных для обработки

results = collection.query(
    zvec.VectorQuery("embedding", vector=query_vector, topk=10),
    filter="publish_year >= 2023 AND category IN ('tech', 'business')"  # Умные фильтры
)
```

## Мониторинг производительности

### Метрики для отслеживания

```python
import time

class PerformanceMonitor:
    def __init__(self, collection):
        self.collection = collection
        self.query_times = []
        self.insert_times = []
    
    def measure_query(self, query_vector):
        start = time.time()
        results = self.collection.query(
            zvec.VectorQuery("embedding", vector=query_vector, topk=10)
        )
        duration = time.time() - start
        
        self.query_times.append(duration)
        return results
    
    def measure_insert(self, doc):
        start = time.time()
        self.collection.insert(doc)
        duration = time.time() - start
        
        self.insert_times.append(duration)
    
    def get_stats(self):
        """Получите статистику."""
        import numpy as np
        
        query_times = np.array(self.query_times)
        insert_times = np.array(self.insert_times)
        
        stats = {
            "query_latency_p50": np.percentile(query_times, 50),
            "query_latency_p99": np.percentile(query_times, 99),
            "query_latency_max": np.max(query_times),
            "insert_latency_avg": np.mean(insert_times),
            "query_throughput": 1.0 / np.mean(query_times)
        }
        
        return stats

# Использование
monitor = PerformanceMonitor(collection)

# Выполняйте операции с измерением
results = monitor.measure_query(query_vector)
doc = zvec.Doc(id="doc_1", vectors={"embedding": vector_1})
monitor.measure_insert(doc)

# Получите статистику
stats = monitor.get_stats()
print(stats)
```

### Real-time мониторинг

```python
# Добавьте метрики в вашу систему (Prometheus, Grafana)
from prometheus_client import PrometheusClient

prometheus = PrometheusClient()

# Измеряйте запросы
def query_with_metrics(query_vector):
    start = time.time()
    
    results = collection.query(
        zvec.VectorQuery("embedding", vector=query_vector, topk=10)
    )
    
    duration = time.time() - start
    
    # Отправьте в Prometheus
    prometheus.histogram('zvec_query_duration_seconds', duration)
    prometheus.summary('zvec_query_duration_seconds', duration)
    
    return results
```

## Профилирование

### Профилирование Python кода

```python
import cProfile
import pstats
import io

# Запустите profiling
pr = cProfile.Profile()

# Выполните код
pr.enable()

# ... ваш код с ZVEC операциями ...

pr.disable()

# Выведите результаты
s = io.StringIO()
ps = pstats.Stats(pr).sort_stats('cumtime')
ps.print_stats(s)

# Сохраните в файл для анализа
with open('profile_results.txt', 'w') as f:
    f.write(s.getvalue())
```

### Анализ горячих точек (Hotspots)

```python
# Найдите медленные части кода
# 1. Логируйте время каждой операции
# 2. Идентифицируйте медленные операции
# 3. Оптимизируйте их

# Пример
import time

def slow_operation(data):
    """Моделирование медленной операции."""
    start = time.time()
    
    # ... медленная операция ...
    time.sleep(0.1)  # Симуляция
    
    duration = time.time() - start
    
    if duration > 1.0:  # > 1 секунда = медленно
        print(f"⚠️  Slow operation: {duration:.2f}s")
    
    return result

def fast_operation(data):
    """Оптимизированная версия."""
    start = time.time()
    
    # ... быстрая операция ...
    duration = time.time() - start
    
    if duration > 0.5:  # > 0.5 секунды = медленно
        print(f"✅ Fast operation: {duration:.2f}s")
    
    return result
```

## Конфигурация для разных workload'ов

### Лёгкий Workload

```python
# Для лёгких запросов (< 1000 qps)
schema = zvec.CollectionSchema(
    name="lightweight",
    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 768),
    index_config={
        "index_type": "hnsw",
        "M": 16,
        "ef_construction": 100
    }
)

collection = zvec.create_and_open(path="./lightweight", schema=schema)
```

### Средний Workload

```python
# Для средних запросов (1000-5000 qps)
schema = zvec.CollectionSchema(
    name="medium",
    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 768),
    index_config={
        "index_type": "hnsw",
        "M": 32,
        "ef_construction": 200
    }
)

collection = zvec.create_and_open(path="./medium", schema=schema)
```

### Heavy Workload

```python
# Для тяжёлых запросов (> 5000 qps)
schema = zvec.CollectionSchema(
    name="heavy",
    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 768),
    index_config={
        "index_type": "ivf",
        "nlist": 4096,
        "nprobe": 64
    }
)

collection = zvec.create_and_open(path="./heavy", schema=schema)
```

## Связи

Производительность связана с:
- [[collections]] — Коллекции содержат данные для оптимизации
- [[indexing]] — Индексация влияет на производительность поиска
- [[query]] — Поисковые операции измеряются производительности
- [[data-operations]] — Вставка/обновление данных

## Quick Reference

| Метрика | Хорошее значение | Плохое значение |
|---------|---------------|--------------|
| Latency (p99) | < 5ms | > 50ms |
| Throughput | > 1000 qps | < 100 qps |
| Memory | < 10GB | > 50GB |
| CPU Usage | < 70% | > 90% |

## Wisdom

> "Premature optimization is the root of all evil." — Donald Knuth

Оптимизируйте то, что медленно.
Измеряйте перед оптимизацией.
Не оптимизируйте слишком рано.

Производительность = скорость + эффективность.
Оптимизируйте для скорости, но не теряйте надёжность.

ZVEC даёт вам контроль над производительностью.
Используйте его мудро.
