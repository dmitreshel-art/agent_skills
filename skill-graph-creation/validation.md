---
description: "Проверка качества графа и валидация связей"
version: "1.0.0"
tags: ["validation", "quality-assurance", "testing"]
related: ["graph-structure", "linking-strategies", "integration"]
---

# Валидация графа

Валидация — это подтверждение качества. Без проверки вы создадите граф с проблемами, которые будут мешать агенту и пользователям.

## Типы валидации

### 1. Структурная валидация

**Проверяет:**
- Все YAML frontmatter присутствуют
- Формат YAML корректен
- Обязательные поля заполнены

### 2. Связная валидация

**Проверяет:**
- Все wiki-links разрешаются
- Нет битых ссылок
- Нет циклических проблем

### 3. Навигационная валидация

**Проверяет:**
- INDEX.md provides вход
- Можно дойти до любой информации
- Агент может навигировать

### 4. Контентная валидация

**Проверяет:**
- Качество написания
- Конкретные примеры присутствуют
- Плохие/хорошие примеры есть

## Автоматические скрипты

### 1. Проверка YAML frontmatter

```python
#!/usr/bin/env python3
"""Validate YAML frontmatter in skill files"""

import yaml
import os

def validate_frontmatter(directory):
    """Verify all skills have required YAML fields"""
    required_fields = ['description', 'version', 'tags', 'related']
    issues = []
    
    for file in os.listdir(directory):
        if not file.endswith('.md'):
            continue
        
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for YAML delimiters
        if not content.startswith('---'):
            issues.append(f"{file}: No YAML frontmatter")
            continue
        
        # Find YAML end
        yaml_end = content.find('---', 3)
        if yaml_end == -1:
            issues.append(f"{file}: Incomplete YAML frontmatter")
            continue
        
        # Parse YAML
        yaml_content = content[3:yaml_end]
        
        try:
            data = yaml.safe_load(yaml_content)
            
            # Check required fields
            missing = [field for field in required_fields if field not in data]
            
            if missing:
                issues.append(f"{file}: Missing fields: {missing}")
            
            # Check field formats
            if 'tags' in data:
                if not isinstance(data['tags'], list):
                    issues.append(f"{file}: Tags must be a list")
            
            if 'related' in data:
                if not isinstance(data['related'], list):
                    issues.append(f"{file}: Related must be a list")
                    
        except yaml.YAMLError as e:
            issues.append(f"{file}: Invalid YAML - {e}")
        except Exception as e:
            issues.append(f"{file}: Error - {e}")
    
    if issues:
        print(f"❌ YAML Frontmatter Issues:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        files_count = len([f for f in os.listdir(directory) if f.endswith('.md')])
        print(f"✅ All {files_count} files have valid YAML frontmatter")
        return True

if __name__ == '__main__':
    import sys
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    success = validate_frontmatter(directory)
    sys.exit(0 if success else 1)
```

**Использование:**
```bash
python3 validation-scripts/frontmatter-validator.py /path/to/skill-graph/
```

### 2. Проверка wiki-links

```python
#!/usr/bin/env python3
"""Validate all wiki-links point to existing files"""

import re
import os

def validate_wiki_links(directory):
    """Verify all wiki-links point to existing files"""
    files = set(f.replace('.md', '') for f in os.listdir(directory) if f.endswith('.md'))
    all_links = []
    broken_links = []
    
    for file in os.listdir(directory):
        if not file.endswith('.md'):
            continue
        
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all wiki-links
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        
        for link in links:
            all_links.append((file, link))
            
            # Check if linked file exists
            if link not in files:
                broken_links.append((file, link))
    
    if broken_links:
        print(f"❌ Broken Wiki-Links ({len(broken_links)}):")
        for source, target in broken_links:
            print(f"  - {source} →  (не найден)")
        return False
    else:
        print(f"✅ All {len(all_links)} wiki-links valid")
        
        # Show some examples
        if all_links:
            print(f"\n📊 Примеры связей:")
            for source, target in all_links[:10]:
                print(f"  {source} → ")
        
        return True

if __name__ == '__main__':
    import sys
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    success = validate_wiki_links(directory)
    sys.exit(0 if success else 1)
```

**Использование:**
```bash
python3 validation-scripts/link-validator.py /path/to/skill-graph/
```

### 3. Поиск сиротских файлов (orphan detection)

```python
#!/usr/bin/env python3
"""Find skills not referenced by anyone"""

import re
import os

def find_orphans(directory):
    """Find skills not referenced by anyone"""
    files = set(f.replace('.md', '') for f in os.listdir(directory) if f.endswith('.md'))
    references = {f: set() for f in files}
    
    for file in os.listdir(directory):
        if not file.endswith('.md'):
            continue
        
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all wiki-links
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        
        source = file.replace('.md', '')
        
        # Track references (only to existing skills)
        for link in links:
            if link in files:
                references[link].add(source)
    
    # Find orphaned files (not referenced by anyone, except INDEX)
    orphans = sorted([f for f in files if len(references[f]) == 0 and f != 'INDEX'])
    
    if orphans:
        print(f"❌ Orphaned Skills ({len(orphans)}):")
        for orphan in orphans:
            ref_count = len(references.get(orphan, []))
            print(f"  - {orphan}.md (ссылаются {ref_count} файлов(а))")
        return False
    else:
        print(f"✅ No orphaned skills")
        
        # Show reference statistics
        print(f"\n📊 Связи:")
        for file in sorted(files):
            if file == 'INDEX':
                refs = list(references.get('INDEX', []))
                print(f"  INDEX → {', '.join(refs[:5])}...")
            else:
                ref_count = len(references.get(file, []))
                if ref_count > 0:
                    print(f"  {file} → ссылаются {ref_count} файлов(а)")
        
        return True

if __name__ == '__main__':
    import sys
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    success = find_orphans(directory)
    sys.exit(0 if success else 1)
```

**Использование:**
```bash
python3 validation-scripts/orphan-detector.py /path/to/skill-graph/
```

## Чеклист качества

### Перед публикацией графа

```markdown
## Структурная валидация
- [ ] Все файлы имеют YAML frontmatter
- [ ] Все YAML frontmatter валидны
- [ ] Обязательные поля присутствуют
- [ ] Форматы полей корректны

## Связная валидация
- [ ] Все wiki-links разрешаются
- [ ] Нет битых ссылок
- [ ] Нет сиротских файлов
- [ ] Связи бидирекционные где возможно

## Навигационная валидация
- [ ] INDEX.md provides вход
- [ ] Навигация к любому навыку ≤3 клика
- [ ] Агент может найти информацию

## Контентная валидация
- [ ] Навыки имеют 3-5 секций
- [ ] Примеры присутствуют
- [ ] Плохие/хорошие примеры есть
- [ ] Длина навыков 500-1000 слов

## Интеграция
- [ ] AGENT-GUIDE.md обновлён
- [ ] README.md обновлён
- [ ] Связи с другими графами добавлены
```

## Частые проблемы

### 1. Отсутствующий YAML frontmatter

**Симптом:** Файл начинается с заголовка, не `---`
**Решение:** Добавьте YAML frontmatter

```yaml
---
description: "Описание навыка"
version: "1.0.0"
tags: ["tag1", "tag2"]
related: ["skill-1", "skill-2"]
---
```

### 2. Битые wiki-links

**Симптом:** `` ссылка
**Решение:** Исправьте или удалите ссылку

**Автоматическая проверка:** Используйте link-validator.py

### 3. Сиротский файл

**Симптом:** Файл не ссылается ни на один навык (кроме INDEX)
**Решение:** Добавьте связи в Related секцию других навыков

**Автоматическая проверка:** Используйте orphan-detector.py

### 4. Длинные навыки

**Симптом:** Навык > 2000 слов
**Решение:** Разбейте на 2-3 навыка

**Правило:** 500-1000 слов — оптимум.

### 5. Мало связей

**Симптом:** Навык имеет 0-2 связи
**Решение:** Добавьте связи в Related секцию

**Правило:** 6-10 связей — оптимум.

## Тестирование агента

### Навигационный тест

**Вопрос:** "Как написать чистый код?"

**Ожидаемый путь:**
1. Агент читает INDEX.md
2. Находит `[[clean-code]]`
3. Сканирует YAML frontmatter
4. Читает целевые секции
5. Предоставляет конкретные примеры
6. Следует по связи на `[[refactoring]]`

**Проверка:** Агент не читает весь файл.

### Связный тест

**Вопрос:** "Как рефакторинг связан с чистым кодом?"

**Ожидаемый путь:**
1. Агент читает clean-code.md
2. Находит `[[refactoring]]` в Related
3. Переходит на refactoring.md
4. Объясняет связь

**Проверка:** Связи работают корректно.

## Лучшая практика

### Валидируйте регулярно

**Частота:** После каждого изменения

**Что проверять:**
- YAML frontmatter
- Wiki-links
- Связность графа

**Скрипты:**
```bash
# После изменений в skill-graphs/my-graph/
python3 validation-scripts/frontmatter-validator.py skill-graphs/my-graph/
python3 validation-scripts/link-validator.py skill-graphs/my-graph/
python3 validation-scripts/orphan-detector.py skill-graphs/my-graph/
```

### Валидируйте перед публикацией

**Пререлизный чеклист:**
- [ ] Запустите все 3 скрипта
- [ ] Протестируйте навигацию
- [ ] Проверьте качество контента
- [ ] Убедитесь что агент работает

### Исправляйте сразу

**Не откладывай:** Найдите проблему → исправьте сейчас

**Почему:** Маленькие проблемы растут в большие.

## Quick Reference

| Тип проверки | Скрипт | Что проверяет |
|------------|----------|----------------|
| YAML frontmatter | frontmatter-validator.py | Формат и обязательные поля |
| Wiki-links | link-validator.py | Разрешаемость ссылок |
| Orphans | orphan-detector.py | Ссылаемость файлов |
| Навигация | Ручной тест | Агент может находить информацию |
| Контент | Ручной обзор | Качество и полнота |

## Метрики качества

### Хорошие показатели

| Метрика | Хорошо | Отлично |
|---------|--------|----------|
| YAML валидность | 100% | 100% |
| Wiki-links валидность | 100% | 100% |
| Связность | 80%+ связаны | 95%+ связаны |
| Средняя длина навыка | 600-800 слов | 500-700 слов |
| Среднее связей | 6-10 | 8-10 |

### Плохие индикаторы

| Метрика | Плохо | Критично |
|---------|--------|----------|
| YAML валидность | <95% | <90% |
| Wiki-links валидность | <95% | <90% |
| Связность | <60% | <40% |
| Средняя длина навыка | >1500 слов | >2000 слов |
| Среднее связей | <3 | <2 |

## Связи

Валидация связана с:
- [[graph-structure]] — Организация влияет на валидацию
- [[linking-strategies]] — Связи нужно проверять
- [[content-writing]] — Качество нужно проверять
- [[integration]] — Валидация перед интеграцией

## Wisdom

> "Quality is not an accident. It's the result of intention, attention, and validation."

Не надейся на качество.
Проверяйте её.
Обеспечивайте её.

Автоматические скрипты = быстрая проверка.
Ручной обзор = глубокая проверка.
Комбинируйте.
Итог = качество.
