---
description: "Установка и настройка ZVEC"
version: "1.0.0"
tags: ["zvec", "installation", "python", "nodejs"]
related: ["dense-vectors", "sparse-vectors", "query"]
---

# Установка ZVEC

## Что такое ZVEC?

ZVEC — это open-source, in-process векторная база данных от Alibaba для быстрого семантического поиска. Работает без серверов, демонов или внешней инфраструктуры.

## Ключевые особенности

- ⚡ **Блестящая скорость** — миллионы векторов за миллисекунды
- ⚡ **Низкая задержка** — sub-millisecond latency для ответов
- 🧩 **Простой в использовании** — `pip install zvec` и работает
- ✨ **Dense + Sparse** — поддержка обоих типов векторов
- 🎯 **Гибридный поиск** — семантика + структурированные фильтры
- 📱 **Работает везде** — Jupyter, сервера, CLI, edge устройства

## Установка

### Python

**Требования:**
- Python 3.10 или новее
- Linux, macOS, или Windows (x86_64/ARM64)

**Команда:**
```bash
pip install zvec
```

**Проверка установки:**
```bash
# Проверьте версию
python -c "import zvec; print(zvec.__version__)"

# Запустите быстрый тест
python -c "import zvec; print('ZVEC installed successfully!')"
```

### Node.js

**Требования:**
- Node.js 16 или новее
- Современный браузер

**Команда:**
```bash
npm install @zvec/zvec
```

**Проверка установки:**
```bash
# Проверьте в package.json
node -e "console.log(require('@zvec/zvec').version)"
```

## Быстрый старт

### Минимальный пример (Python)

```python
import zvec

# 1. Создайте схему коллекции
schema = zvec.CollectionSchema(
    name="example",
    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 4)
)

# 2. Создайте коллекцию
collection = zvec.create_and_open(path="./zvec_example", schema=schema)

# 3. Вставьте документы
collection.insert([
    zvec.Doc(id="doc_1", vectors={"embedding": [0.1, 0.2, 0.3, 0.4]}),
    zvec.Doc(id="doc_2", vectors={"embedding": [0.2, 0.3, 0.4, 0.1]}),
    zvec.Doc(id="doc_3", vectors={"embedding": [0.3, 0.2, 0.1, 0.2]}),
])

# 4. Поиск по сходству
results = collection.query(
    zvec.VectorQuery("embedding", vector=[0.35, 0.25, 0.3, 0.15], topk=10)
)

# 5. Результаты
for result in results:
    print(f"ID: {result.id}, Score: {result.score}")
```

### Минимальный пример (Node.js)

```javascript
const { Collection, Doc, VectorQuery } = require('@zvec/zvec');

async function main() {
    // 1. Создайте схему
    const schema = new Collection({
        name: 'example',
        vectors: new VectorSchema('embedding', DataType.VECTOR_FP32, 4)
    });

    // 2. Создайте коллекцию
    const collection = await createAndOpen('./zvec_example', schema);

    // 3. Вставьте документы
    await collection.insert([
        new Doc({
            id: 'doc_1',
            vectors: { embedding: [0.1, 0.2, 0.3, 0.4] }
        }),
        new Doc({
            id: 'doc_2',
            vectors: { embedding: [0.2, 0.3, 0.4, 0.1] }
        })
    ]);

    // 4. Поиск по сходству
    const results = await collection.query(
        new VectorQuery('embedding', [0.35, 0.25, 0.3, 0.15], 10)
    );

    // 5. Результаты
    for (const result of results) {
        console.log(`ID: ${result.id}, Score: ${result.score}`);
    }
}
```

## Конфигурация

### Оптимизация производительности

```python
import zvec

# Создайте коллекцию с оптимизированной схемой
schema = zvec.CollectionSchema(
    name="optimized",
    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 768),
    index_config={
        "index_type": "hnsw",
        "M": 16,  # Количество соседей
        "ef_construction": 200
    }
)

collection = zvec.create_and_open(path="./optimized", schema=schema)
```

### Мониторинг

```python
import zvec

# Получите статистику коллекции
print(collection.stats())

# Проверьте использование ресурсов
```

## Устранение неполадок

### Проблема: ModuleNotFoundError

**Решение:**
```bash
# Переустановите zvec
pip uninstall zvec
pip install zvec
```

### Проблема: Ошибка импорта

**Решение:**
```python
# Проверьте что все зависимости установлены
pip list | grep zvec

# Или переустановите
pip install --force-reinstall zvec
```

### Проблема: Низкая производительность

**Возможные причины:**
1. Не оптимизирована схема индекса
2. Мало оперативной памяти
3. Медленный диск

**Решения:**
1. Используйте HNSW индекс (параметр M=16)
2. Увеличьте память на сервере
3. Перенесите данные на SSD/NVMe

## Следующие шаги

После успешной установки:

1. [[zvec-basics]] — Узнайте основы векторных баз данных
2. [[dense-vectors]] — Изучите плотные векторы
3. [[sparse-vectors]] — Изучите разрежные векторы
4. [[collections]] — Создайте коллекцию для ваших данных
5. [[query]] — Начните искать по сходству

## Интеграция с существующими системами

### Python приложения

```python
# ZVEC как встроенный модуль
import zvec

# Интеграция с фреймворками
# Flask, FastAPI, Django и т.д.
```

### CLI инструменты

```bash
# Создайте коллекцию
zvec create my_collection ./data

# Ищите по сходству
zvec search my_collection ./query_data.json

# Статистика
zvec stats my_collection
```

## Резервное копирование и восстановление

```python
import zvec

# Экспорт коллекции
zvec export my_collection ./backup

# Восстановление из резервной копии
collection = zvec.open("./backup")
```

## Документация

- **Главная страница:** https://zvec.org/en/
- **Документация:** https://zvec.org/en/docs/
- **Quickstart:** https://zvec.org/en/docs/quickstart/
- **Концепты:** https://zvec.org/en/docs/concepts/
- **GitHub:** https://github.com/alibaba/zvec
- **Discord:** https://discord.gg/rKddFBBu9z

## Вопросы и ответы

### Частые вопросы

**Q: Работает ли ZVEC без интернета?**
A: Да! ZVEC полностью in-process — работает локально без сетевого подключения.

**Q: Нужен ли сервер?**
A: Нет. ZVEC работает в памяти процесса, сервер не требуется.

**Q: Сколько памяти нужно?**
A: Зависит от размера данных. Примерно 1GB на 1 миллион векторов (768D dense vectors).

**Q: Какую Python версию использовать?**
A: Python 3.10+ для полной поддержки. Python 3.11+ рекомендован для лучшей производительности.

**Q: Поддерживает ли ZVEC Windows?**
A: Официальная поддержка только Linux и macOS. На Windows может работать, но не тестирован.

**Q: Как оптимизировать производительность?**
A: 1. Используйте HNSW индекс (параметр M=16)
2. Оптимизируйте параметры ef_construction
3. Рассмотрите sparse векторы для больших данных

## Краткое резюме

ZVEC — это:
- ✅ Open-source и бесплатный
- ⚡ Сверхбыстрая векторная база данных
- 🧩 Прост в установке и использовании
- 📱 Работает везде: Python, Node.js, CLI
- ✨ Поддержка dense + sparse векторов
- 🎯 Гибридный поиск с фильтрами
- 🔧 Масштабируется до миллиардов векторов

**Начните:** [[zvec-basics]] → Основы

**Дальше:** После основ — [[collections]] → [[query]]

## Интеграция с OpenClaw

Когда ZVEC установлен, вы можете:

1. Использовать его в ваших проектах через Python API
2. Создавать векторные embeddings для ваших документов
3. Интегрировать с существующими базами данных
4. Строить RAG (Retrieval-Augmented Generation) приложения

ZVEC даёт вам мощный инструмент для векторного поиска без сложности управления инфраструктурой.

Установлено и готово к использованию! 🎉
