---
description: "Правила именования файлов, навыков и тегов"
version: "1.0.0"
tags: ["naming", "conventions", "standards"]
related: ["graph-structure", "content-writing", "linking-strategies"]
---

# Именование соглашения

Хорошые имена — это мгновенное понимание. Плохие имена создают путаницу. Последовательные имена делают граф проходимым.

## Именование файлов

### Правила для файлов навыков

```bash
# ХОРОШО
clean-code.md
testing.md
debugging.md
code-review.md
refactoring.md
architecture.md
documentation.md
version-control.md

# ПЛОХО
Clean Code.md
TESTING.md
Debugging.md
code_review.md
Refactoring.md
Architecture.md
Doc.md
vc.md
```

### Конвенции

1. **Нижний регистр** — Всегда
2. **Гифисы между словами** — не пробелы
3. **Краткие и осмысленные** — не аббревиатуры
4. **Английские слова** — для URL и cross-платформенности
5. **Нет специальных символов** — кроме дефиса
6. **Максимум 50 символов** — для читаемости

### Почему эти правила?

| Правило | Проблема при нарушении | Решение |
|---------|------------------------|----------|
| Нижний регистр | case-sensitive файловые системы | Всегда нижний |
| Гифисы | Пробелы в URL/путях | Используйте дефисы |
| Осмысленность | Неясно о чём файл | Описательные имена |
| Английские слова | Проблемы с кодировками | Используйте английский |
| Нет спец. символов | Символы в путях | Только a-z, 0-9, - |

## Именование навыков

### В wiki-links

```markdown
# Объявление

См. [[clean-code]] для принципов.
См. [[testing]] для стратегии.
```

**В YAML frontmatter:**
```yaml
---
related: ["clean-code", "testing", "debugging"]
---
```

**Правило:** То же имя файла = имя в wiki-link.

### В тегах

```yaml
---
tags: ["clean-code", "fundamentals", "code-quality"]
---
```

**Правило:** Короткие, описательные теги (1-2 слова).

## Именование графов

### Папка графа

```bash
# ХОРОШО
trading-graph/
development-graph/
marketing-graph/
medical-graph/

# ПЛОХО
TradingGraph/
development_graph/
marketingGraph/
med/
```

### Правила

1. **Нижний регистр**
2. **Гифис между словами**
3. **Описательное название темы**
4. **Суффикс `-graph`** — для ясности

### Почему -graph суффикс?

**Без суффикса:**
```
trading/
development/
marketing/
```

**С суффиксом:**
```
trading-graph/         ← Ясно что это граф
development-graph/     ← Ясно что это граф
marketing-graph/       ← Ясно что это граф
```

## Именование в YAML frontmatter

### Description (обязательно)

```yaml
---
description: "Принципы чистого кода и практики написания"
```

**Правила:**
- Одно предложение
- Максимум 50-60 символов
- Описывает суть навыка
- Русский или английский (последовательно в графе)

**Примеры:**
```yaml
description: "Принципы чистого кода"  # Хорошо
description: "Про код"  # Плохо (слишком общее)
description: "Краткое описание принципа написания чистого кода и лучших практик"  # Плохо (слишком длинно)
```

### Version (обязательно)

```yaml
---
version: "1.0.0"
```

**Правила:**
- Семантическая версия (Semantic Versioning)
- `MAJOR.MINOR.PATCH` формат
- Начните с `1.0.0`

**Когда увеличивать:**
- MAJOR: Фундаментальное изменение
- MINOR: Добавление секции или принципа
- PATCH: Исправление ошибок или улучшения

### Tags (обязательно)

```yaml
---
tags: ["clean-code", "fundamentals", "code-quality"]
```

**Правила:**
- 3-5 тегов
- Короткие (1-2 слова)
- Описательные
- Нижний регистр
- Английские слова (для cross-поиска)

**Хорошие теги:**
```yaml
tags: ["testing", "quality-assurance"]
tags: ["refactoring", "maintenance", "code-improvement"]
tags: ["debugging", "problem-solving", "troubleshooting"]
```

**Плохие теги:**
```yaml
tags: ["tst"]  # Аббревиатура
tags: ["a", "b", "c"]  # Бессмысленные
tags: ["verylongtagname", "anotherverylongtagname"]  # Слишком длинные
```

### Related (обязательно)

```yaml
---
related: ["clean-code", "testing", "debugging"]
```

**Правила:**
- 3-5 ссылок
- На реально существующие файлы
- На связанные концепции
- Избегайте циклов (A → B → A)

**Хорошие связи:**
```yaml
related: ["clean-code", "refactoring", "testing"]
# clean-code: Базовый принцип
# refactoring: Применяет clean-code
# testing: Валидирует clean-code
```

**Плохие связи:**
```yaml
related: ["skill-1", "skill-2", "skill-3"]
# Бессмысленные имена
related: ["a", "b", "c"]
# Аббревиатуры
```

## Именование в контенте

### Заголовки секций

```markdown
# Название навыка

## Overview

## Core Principles

### 1. Principle Name

#### Subsection (если нужно)

## Common Mistakes

## Quick Reference

## Integration
```

**Правила:**
- H1 = название навыка
- H2 = основные секции
- H3 = принципы/ошибки
- H4 = подсекции (если нужно)

### Именование принципов

**Хорошо:**
```markdown
### 1. Meaningful Names
### 2. Functions Should Do One Thing
### 3. Comments vs Code
```

**Плохо:**
```markdown
### 1. Rules for names
### 2. Single Responsibility
### 3. Documentation
```

**Правило:** Имена принципов должны быть описательными.

## Локализация

### Русский vs Английский

**Решайте заранее:**
- Весь граф русский ИЛИ весь граф английский
- Не смешивайте языки

**Почему:**
- Агент будет последователен
- Поиск будет эффективнее
- Читатель не запутается

### Если оба языка

Используйте разные графы:
```
trading-graph-ru/    (русская версия)
trading-graph-en/    (английская версия)
```

## Частые ошибки

### 1. Неописательные имена

**Плохо:**
```bash
stuff.md
things.md
info.md
data.md
```

**Хорошо:**
```bash
principles.md
techniques.md
best-practices.md
strategies.md
```

### 2. Слишком длинные имена

**Плохо:**
```bash
extremely_long_and_descriptive_file_name_that_explains_everything.md
```

**Хорошо:**
```bash
principles.md
strategies.md
patterns.md
```

### 3. Смешивание регистра

**Плохо:**
```bash
Clean-code.md
TESTING.md
Debugging.md
```

**Хорошо:**
```bash
clean-code.md
testing.md
debugging.md
```

### 4. Специальные символы

**Плохо:**
```bash
file@name.md
file&name.md
file_name!.md
file#name.md
```

**Хорошо:**
```bash
file-name.md
```

## Quick Reference

| Элемент | Правило | Пример |
|---------|---------|--------|
| Файл навыка | Нижний регистр, гифисы | clean-code.md |
| Папка графа | Тема + -graph | trading-graph |
| Wiki-link | Имя файла без .md | [[clean-code]] |
| Description | Одно предложение, <60 символов | "Принципы чистого кода" |
| Version | MAJOR.MINOR.PATCH | 1.0.0 |
| Tags | 3-5 коротких слов, нижний регистр | ["clean-code", "fundamentals"] |
| Related | 3-5 валидных ссылок | ["clean-code", "testing"] |

## Скрипт для проверки имен

```python
import re

def validate_names(directory):
    """Validate file naming conventions"""
    valid_pattern = re.compile(r'^[a-z0-9-]+\.md$')
    
    for file in os.listdir(directory):
        if file.endswith('.md'):
            if not valid_pattern.match(file):
                print(f"❌ Invalid name: {file}")
                return False
    
    print(f"✅ All names valid")
    return True
```

## Лучшие практики

### Будьте последовательными

**Правило:** Выберите соглашение и придерживайтесь

```bash
# Всегда нижний регистр
clean-code.md
testing.md
debugging.md

# Всегда английские теги
tags: ["clean-code", "testing"]

# Всегда гифисы
my-skill.md
```

### Будьте описательными

Избегайте:
- Аббревиатур (кроме широко известных)
- Слишком общих слов
- Слишком длинных названий

Используйте:
- Конкретные термины
- Понятные концепции
- Описательные фразы

### Будьте краткими

**Максимум:** 50 символов для файлов
**Максимум:** 2 слова для тегов
**Максимум:** 60 символов для description

## Связи

Именование связано с:
- [[graph-structure]] — Как организовывать файлы
- [[content-writing]] — Как называть секции
- [[linking-strategies]] — Как связывать навыки

## Wisdom

> "Names are the first thing people see. Good names create good first impressions. Great names create instant understanding."

Имя — это первое впечатление.
Делайте его хорошим.
Делайте его описательным.
Делайте его последовательным.

Плохие имена = путаница.
Хорошие имена = ясность.
Ясность = понимание.
Понимание = полезность.
