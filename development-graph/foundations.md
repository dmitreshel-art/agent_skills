---
description: "Базовые концепции и основы"
version: "1.0.0"
tags: ["basics", "fundamentals", "foundational"]
related: []
---

# Основы разработки ПО

## Обзор

Этот навык объясняет базовые концепции и основы, которые необходимы для всех типов проектов. Это фундамент для любых разработок — от скриптов до распределённых систем.

## Основные концепции

### 1. Version Control (Контроль версий)

**Что это:** Система отслеживания изменений в коде

**Зачем нужно:**
- Откатка к предыдущим версиям
- Совместная работа в команде
- История изменений
- Ветвление для фич
- Тагинг релизов

**Основные системы:**
- Git (de facto стандарт)
- Subversion (SVN)
- Mercurial (Hg)
- Bazaar (Bazaar)

**Основные команды:**
```bash
# Получить изменения
git pull

# Посмотреть изменения
git status

# Сохранить изменения
git add .
git commit -m "message"

# Откатить изменения
git checkout HEAD

# Просмотреть историю
git log --oneline
```

### 2. Testing (Тестирование)

**Что это:** Процесс проверки что код работает как ожидается

**Зачем нужно:**
- Нахождение багов до продакшена
- Уверждение качества
- Рефакторинг с защитой

**Уровни тестирования:**

| Уровень | Описание | Кто делает |
|---------|-----------|------------|
| Unit Testing | Тест отдельных функций/классов | Разработчики |
| Integration Testing | Тест взаимодействия между компонентами | Разработчики/тестировщики |
| System Testing | Тест всей системы как единого целого | QA инженеры |
| Acceptance Testing | Проверка требований и стандартов | QA/Product Owner |
| Performance Testing | Проверка скорости, нагрузки и масштабируемости | QA инженеры |

**Типы тестов:**

```python
# Unit тест (pytest)
def test_calculate_sum():
    assert calculate_sum(2, 3) == 5

# Интеграционный тест
def test_api_integration():
    response = api.get_user(1)
    assert response.status_code == 200
    assert response.data['name'] == "John"

# Производительность тест
def test_response_time():
    start = time.time()
    result = process_data(large_dataset)
    duration = time.time() - start
    assert duration < 1.0  # 1 second for large dataset
```

**Лучшие практики:**

- **Пишите тесты FIRST** — TDD (Test-Driven Development)
- **Один тест = одно утверждение** — Не проверяйте много в одном тесте
- **Давайте осмысленные имена** — Тест должен описывать что проверяет
- **Используйте AAA (Arrange-Act-Assert)** — Arrange: подготовьте данные, Act: вызовите код, Assert: проверьте результат
- **Тестируйте границы** — Empty inputs, null values, huge numbers
- **Сделайте тесты быстрыми** — Они должны работать быстро (<1 секунда)
- **Избегайте тестовые зависимости** — Каждый тест должен работать изолированно
- **Используйте fixtures** — Подготовьте тестовые данные

### 3. Code Style (Стиль кода)

**Что это:** Соглашение о том как писать код для читаемости и поддерживаемости

**Зачем нужно:**
- Единый стиль делает код лёгким для понимания
- Новые разработчики быстро встраиваются
- Код легче поддерживать и рефакторить

**Общие принципы:**

```python
# Плохой стиль
def calculateTotal(a, b, c):
    x = a + b
    y = x + c
    return y

# Хороший стиль
def calculate_total(a, b, c):
    """Вычесляет сумму трёх чисел."""
    return a + b + c
```

**Конвенции (PEP 8):**

- **Отступы:** 4 пробела
- **Максимальная длина строки:** 79 символов
- **Имена функций:** snake_case
- **Имена классов:** PascalCase
- **Константы:** UPPER_CASE

```python
# Правильные имена
class UserManager:  # Класс
    def get_user_by_id(self, user_id):  # Метод
    MAX_USERS = 100  # Константа
    def create_user(self, name, email):  # Метод
```

### 4. Debugging (Отладка)

**Что это:** Процесс нахождения и исправления ошибок в коде

**Зачем нужно:**
- Быстрое исправление багов
- Понимание того как работает код
- Уменьшение времени на решение проблем

**Техники отладки:**

**1. Print Debugging (Самый простой)**
```python
print("Debug: user_id =", user_id)
print("Debug: total =", total)
```

**Плюсы:** Очень просто, не нужно инструментов
**Минусы:** Удалён после отладки, загрязняет код

**2. Logging (Логирование)**
```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("User logged in")
logger.error("Failed to connect to database")
```

**Плюсы:** Остаются в production
**Минусы:** Может быть много логов

**3. Interactive Debugging (Интерактивная отладка)**
```python
# Python Debugger (pdb)
import pdb; pdb.set_trace()

# IDE Debugger (VS Code, PyCharm)
# Set breakpoints and step through code
```

**Плюсы:** Полный контроль над выполнением
**Минусы:** Требует навыка и IDE

### 5. Error Handling (Обработка ошибок)

**Что это:** Предвидение и изящная обработка ошибок

**Зачем нужно:**
- Предотвращение падения приложения
- Логирование ошибок для диагностики
- Пользовательские сообщения об ошибках

**Паттерны:**

**1. Try-Except (Попытка-Исключение)**
```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Specific error occurred: {e}")
    # Fallback
    result = safe_fallback()
```

**2. Context Managers (Менеджеры контекста)**
```python
# Ресурс должен быть освобождён
with open('file.txt', 'r') as f:
    content = f.read()
    # ... file automatically closed
```

### 6. Documentation (Документирование)

**Что это:** Письменное описание того, как работает код и как его использовать

**Зачем нужно:**
- Понимание кода другими разработчиками
- Обучение новых членов команды
- Архитектурные решения

**Типы документации:**

**Code Comments (Комментарии кода):**
```python
def calculate_discount(price, discount_rate):
    """
    Вычесляет скидку на основе цены.
    
    Args:
        price: Исходная цена в USD.
        discount_rate: Процент скидки (например, 0.1 для 10%).
    
    Returns:
        Скидка в USD.
    """
    return price * discount_rate
```

**Docstrings:**
```python
class UserService:
    """Сервис для работы с пользователями."""
    
    def get_user(self, user_id):
        """
        Получает пользователя по ID.
        
        Args:
            user_id: ID пользователя в базе.
        
        Returns:
            Объект пользователя.
        """
        # Implementation
```

**Readme Files (Файлы README):**
```markdown
# Проект

Простой проект для управления пользователями.

## Установка

pip install -r requirements.txt

## Использование

```bash
# Настройте конфигурацию
python setup.py

# Запустите сервер
python app.py
```

## Структура проекта

```
project/
├── src/
│   ├── __init__.py
│   ├── models/
│   ├── services/
│   └── utils/
├── tests/
│   └── README.md
├── requirements.txt
└── setup.py
```

## API Reference (Справочник API)

### 1. User API (GET /users/{id})
```python
# GET /users/123
{
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
}
```

### 2. User Creation API (POST /users)
```python
# POST /users
{
    "name": "Jane Doe",
    "email": "jane@example.com"
}

# Response 201 Created
{
    "id": 124,
    "name": "Jane Doe",
    "email": "jane@example.com"
}
```

### 3. User Update API (PUT /users/{id})
```python
# PUT /users/123
{
    "name": "John Updated",
    "email": "john.updated@example.com"
}

# Response 200 OK
{
    "id": 123,
    "name": "John Updated",
    "email": "john.updated@example.com"
}
```

### 4. User Delete API (DELETE /users/{id})
```python
# DELETE /users/123

# Response 204 No Content
```

## Best Practices (Лучшие практики)

### Для Version Control
```bash
# Сделайте частые, маленькие коммиты
# Пишите осмысленные сообщения коммитов
# Используйте ветки для фич (feature/*)
# Не коммитайте временные файлы
# Не коммитьте в master напрямую
# Используйте Pull Requests для слияния
```

### Для Тестирования
```python
# Пишите тесты FIRST (TDD)
# Тестируйте только что изменяется в коде
# Не тестируйте внешние сервисы (mock их)
# Покрыйте важные edge cases
- Делайте тесты быстрыми (<1 секунда)
- Избегайте тестовые зависимости
```

### Для Документирования
```python
# Пишите docstrings для всех функций и классов
# Комментируйте сложный алгоритмы
- Обновляйте README при изменениях
- Используйте type hints для сигнатур
- Создавайте примеры использования
```

## Quick Reference

| Тема | Рекомендация |
|-------|----------------|
| Version Control | Git + Pull Requests |
| Testing | Unit + Integration + Performance |
| Code Style | PEP 8, clear naming |
| Debugging | Logging, Interactive Debugger |
| Error Handling | Try-Except, Context Managers |
| Documentation | Docstrings + README |
| Best Practices | Write tests first, meaningful commits |

## Связи

Этот навык связан с:
- [[testing]] — Тестирование основано на этих концепциях
- [[code-review]] — Code review использует эти принципы
- [[debugging]] — Debugging использует эти концепции
- [[documentation]] — Документирование следует этим стандартам

## Wisdom

> "Код — это живой документ. Если он не читается, он не поддерживается."

Инвестируйте время в понятный, хорошо документированный код.
Это сэкономит вам время в будущем.

Ваш код = ваша документация.
Пишите для людей, которые будут читать ваш код позже.
