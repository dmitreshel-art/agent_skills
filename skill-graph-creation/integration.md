---
description: "Интеграция нового графа в систему OpenClaw"
version: "1.0.0"
tags: ["integration", "system", "deployment"]
related: ["graph-structure", "validation", "naming-conventions"]
---

# Интеграция графа

Граф создан, валидирован, готов... Теперь нужно подключить его к системе. Интеграция делает граф доступным для агента и пользователей.

## Типы интеграции

### 1. Локальная интеграция

**Что:** Граф существует в `skill-graphs/`
**Доступность:** Агент может использовать его
**Работает:** Немедленно

### 2. Агентная интеграция

**Что:** Агент знает когда использовать граф
**Доступность:** Автоматическое нахождение
**Работает:** После обновления AGENT-GUIDE.md

### 3. Документационная интеграция

**Что:** Пользователь знает о существовании графа
**Доступность:** Чтение README.md
**Работает:** После обновления README.md

## Обновление AGENT-GUIDE.md

### Что добавить

В `skill-graphs/AGENT-GUIDE.md` добавьте:

```markdown
## Создание новых графов

When user wants to create a new skill graph:
1. Direct to `skill-graph-creation/INDEX.md`
2. Follow step-by-step creation process
3. Use templates from [[content-writing]]
4. Establish links using [[linking-strategies]]
5. Validate using scripts from [[validation]]
6. Integrate with [[integration]]
```

### Где разместить

В секции "Текущие графы" или аналогичной:

```markdown
## Текущие графы

### skill-graph-creation

**Точка входа:** `skill-graphs/skill-graph-creation/INDEX.md`

**Роль:** Мета-граф для создания новых графов

**Шаги:**
- [[graph-structure]] — Организация файлов
- [[content-writing]] — Написание навыков
- [[linking-strategies]] — Создание связей
- [[naming-conventions]] — Правила именования
- [[validation]] — Проверка качества
- [[integration]] — Подключение к системе

**Результат:** Возможность создавать новые графы!

### trading-graph
[существующие данные...]

### development-graph
[существующие данные...]

### [your-new-graph]
[ваши данные...]
```

## Обновление README.md

### Что добавить

В `skill-graphs/README.md` добавьте раздел:

```markdown
## Создание новых графов

### Быстрый старт

Для создания нового графа используйте мета-граф `skill-graph-creation/`:

```bash
# 1. Организация
См. [[graph-structure]] → создание INDEX.md и файлов

# 2. Написание
См. [[content-writing]] → шаблоны и практики

# 3. Связи
См. [[linking-strategies]] → создание wiki-links

# 4. Именование
См. [[naming-conventions]] → правила файлов и тегов

# 5. Валидация
См. [[validation]] → проверка качества

# 6. Интеграция
См. [[integration]] → подключение к системе
```

### Где разместить

После секции "Как использовать" или "Пример: Граф трейдинга":

```markdown
## Создание новых графов

Для создания нового графа используйте мета-граф `skill-graph-creation/`:

1. **Организация:** См. [[graph-structure]] для структуры файлов
2. **Написание:** См. [[content-writing]] для лучших практик
3. **Связи:** См. [[linking-strategies]] для создания связей
4. **Именование:** См. [[naming-conventions]] для правил
5. **Валидация:** См. [[validation]] для проверки качества
6. **Интеграция:** См. [[integration]] для подключения

### Шаблоны

См. [[content-writing]] для готовых шаблонов INDEX.md и навыков.

### Примеры созданных графов

- **trading-graph** — Граф трейдинга (15 навыков, 72 связи)
- **development-graph** — Граф разработки (9 навыков, 72 связи)
- **skill-graph-creation** — Мета-граф (6 навыков, как создать новые графы)
```

## Добавление в систему

### Git commit

**Перед коммитом проверьте:**
- [ ] Все файлы созданы
- [ ] Валидация пройдена
- [ ] AGENT-GUIDE.md обновлён
- [ ] README.md обновлён
- [ ] Протестировано

**Коммит:**
```bash
git add skill-graphs/
git commit -m "feat(skill-graphs): add [your-graph-name] skill graph

- Added [number] interconnected skills
- Organized with [X] domains
- Validated with automation scripts
- Integrated with AGENT-GUIDE and README"
```

## Тестирование интеграции

### Ручное тестирование агента

**Шаг 1: Простый запрос**
```
Пользователь: Что есть в [your-graph]?

Ожидаемый результат: Агент читает INDEX.md,
                           сканирует YAML frontmatter,
                           предоставляет обзор.
```

**Шаг 2: Запрос с навигацией**
```
Пользователь: Расскажи про [specific-skill] из [your-graph].

Ожидаемый результат: Агент следует wiki-link,
                           читает навык,
                           предоставляет целевые знания.
```

**Шаг 3: Запрос с глубиной**
```
Пользователь: Как [X] связан с [Y] в [your-graph]?

Ожидаемый результат: Агент следует связи,
                           объясняет взаимосвязь.
```

### Атоматическая проверка

```python
#!/usr/bin/env python3
"""Test agent navigation in skill graph"""

import os
import re

def test_agent_navigation(graph_path):
    """Test that agent can navigate skill graph"""
    
    # 1. Check INDEX exists
    index_path = f"{graph_path}/INDEX.md"
    if not os.path.exists(index_path):
        print(f"❌ INDEX.md not found")
        return False
    
    print("✅ INDEX.md exists")
    
    # 2. Parse INDEX and get skill links
    with open(index_path, 'r') as f:
        index_content = f.read()
    
    skills = re.findall(r'\[\[([^\]]+)\]\]', index_content)
    print(f"✅ Found {len(skills)} skills in INDEX")
    
    # 3. Check all skills exist
    for skill in skills[:5]:  # Test first 5
        skill_path = f"{graph_path}/{skill}.md"
        if not os.path.exists(skill_path):
            print(f"❌ Skill not found: {skill}")
            return False
    
    print(f"✅ Sample skills exist")
    
    # 4. Check YAML frontmatter
    yaml_delimiter = '---'
    yaml_count = 0
    
    for skill in skills[:5]:
        skill_path = f"{graph_path}/{skill}.md"
        with open(skill_path, 'r') as f:
            content = f.read()
        
        if content.startswith(yaml_delimiter):
            yaml_count += 1
    
    if yaml_count < len(skills[:5]):
        print(f"⚠️  Only {yaml_count}/{len(skills[:5])} skills have YAML")
    else:
        print(f"✅ Skills have YAML frontmatter")
    
    print("\n✅ Agent navigation looks functional")
    return True

if __name__ == '__main__':
    import sys
    graph = sys.argv[1] if len(sys.argv) > 1 else 'skill-graphs/trading-graph'
    success = test_agent_navigation(graph)
    sys.exit(0 if success else 1)
```

**Использование:**
```bash
python3 test-agent-navigation.py skill-graphs/[your-graph]/
```

## Частые проблемы интеграции

### 1. Агент не находит граф

**Симптом:** Агент не использует новый граф
**Причины:**
- AGENT-GUIDE.md не обновлён
- Инструкции неполные
- Граф не в `skill-graphs/`

**Решение:**
1. Проверьте AGENT-GUIDE.md
2. Убедитесь что граф в skill-graphs/
3. Протестируйте с ручным запросом

### 2. Битые ссылки после интеграции

**Симптом:** `` ссылка не работает
**Причины:**
- Ошибка при обновлении AGENT-GUIDE.md
- Невалидные wiki-links в новом графе

**Решение:**
1. Запустите link-validator.py
2. Исправьте битые ссылки
3. Перекоммитте

### 3. Навыки не подключены

**Симптом:** Новые навыки не связаны с системой
**Причины:**
- Related секции пустые
- Нет связей с INDEX.md

**Решение:**
1. Проверьте Related секции
2. Добавьте связи где нужно
3. Создайте MOC если много навыков

## Деплоймент стратегии

### Разработка

**Где:** Локальный workspace
**Действия:**
1. Создайте файлы
2. Валидируйте
3. Тестируйте
4. Коммитте

### Публикация

**Где:** Git repository
**Действия:**
1. Push изменений
2. Create PR/MR (если нужно)
3. Review и merge

### Доставка

**Где:** Production (если применимо)
**Действия:**
1. Убедитесь что агент имеет доступ
2. Протестируйте на реальных запросах
3. Мониторируйте использование

## Quick Reference

| Тип интеграции | Файл | Что делать |
|--------------|-------|-----------|
| Агентная | AGENT-GUIDE.md | Добавьте секцию использования |
| Документационная | README.md | Добавьте описание и примеры |
| Локальная | (ни чего не нужно) | Граф доступен сразу |
| Git | Git commit | Зафиксируйте изменения |

## Чеклист интеграции

### Перед коммитом

- [ ] Все навыки созданы
- [ ] YAML frontmatter валиден
- [ ] Wiki-links валидны
- [ ] Нет сиротских файлов
- [ ] Валидация пройдена
- [ ] AGENT-GUIDE.md обновлён
- [ ] README.md обновлён
- [ ] Протестировано агентом
- [ ] Готов к коммиту

### После коммита

- [ ] Changes pushed to remote
- [ ] Create PR/MR если нужно
- [ ] Reviewed (если применимо)
- [ ] Merged
- [ ] Verify in production

## Лучшая практика

### Инкрементная интеграция

Не обновляйте всё сразу:

**Плохо:**
```bash
# Меняет всё сразу
git add .
git commit -m "Update everything"
```

**Хорошо:**
```bash
# Инкрементные изменения
git add skill-graphs/my-graph/
git commit -m "feat: add my-graph (part 1)"

git add AGENT-GUIDE.md
git commit -m "docs: update AGENT-GUIDE with my-graph"
```

### Валидация после каждого изменения

**Правило:** После каждого изменения → валидация

**Почему:** Маленькие проблемы легче фиксать чем большие.

### Сообщайте изменения

**Правило:** Сообщайте об интеграции

**Где:**
- README.md (добавление)
- AGENT-GUIDE.md (добавление)
- Чат (сообщите что новый граф доступен)

## Связи

Интеграция связана с:
- [[graph-structure]] — Организация для интеграции
- [[validation]] — Валидация перед интеграцией
- [[naming-conventions]] — Имена для интеграции
- [[content-writing]] — Документация для README

## Wisdom

> "Integration is the bridge between creation and usage. Poor integration = wasted creation."

Созданный граф без интеграции = бесполезен.
Хорошая интеграция = мгновенная полезность.

Интегрируйте тщательно.
Документируйте изменения.
Валидируйте перед коммитом.

Граф создан → валидирован → интегрирован → используем.
Всё три этапа важны.
