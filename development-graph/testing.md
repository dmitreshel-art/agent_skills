---
description: "Стратегии тестирования и лучшие практики"
version: "1.0.0"
tags: ["testing", "quality-assurance", "best-practices"]
related: ["debugging", "code-review", "foundations"]
---

# Тестирование (Testing)

## Overview

Тестирование — это процесс проверки что код работает как ожидается. Это критически важный навык для всех разработчиков — от новичков до экспертов. Хорошее тестирование повышает качество кода, уверенность в изменениях и предотврашает регрессии.

## Ключевые принципы

### 1. Test-Driven Development (TDD)

**Что это:** Сначала пишете тест, потом код

**Зачем нужно:**
- Лучшее понимание требований
- Более чистый код (тесты как документация)
- Снижение количества багов
- Уверенность в рефакторинге

**Как работает:**
```python
# TDD Cycle

# 1. Red: Пишем тест (FAILING)
def test_calculate_total():
    assert calculate_total(100, 0.1) == 10

# 2. Green: Пишем код (MINIMAL)
def calculate_total(price, discount_rate):
    return price * (1 - discount_rate)

# 3. Refactor: Улучаем код (OPTIMIZED)
def calculate_total(price, discount_rate):
    return price * (1 - discount_rate)  # Could optimize caching
```

### 2. AAA Pattern (Arrange-Act-Assert)

**Что это:** Структурированный подход к тестированию

**Как работает:**
- **Arrange (Подготовка):** Подготовьте тестовые данные
- **Act (Действие):** Вызовите кода
- **Assert (Утверждение):** Проверьте результат

**Пример:**
```python
# Плохо: Все в одном
def test_calculate():
    assert calculate(1, 2, '+') == 3

# Хорошо: Чёткая структура
def test_calculate():
    # Arrange
    a, b, operator = 1, 2, '+'
    expected = 3
    
    # Act
    result = calculate(a, b, operator)
    
    # Assert
    assert result == expected
```

### 3. Пишите тесты FIRST

**Правило:** Перед тем как писать код, напишите тест для него

**Пример:**
```python
# Плохо: Сначала код, потом тесты
def process_payment(amount):
    # ... 50 lines of code
    return result

def test_process_payment():
    # Test added later
    assert process_payment(100) == 90

# Хорошо: Сначала тест, потом код
def test_process_payment():
    assert process_payment(100) == 90

def process_payment(amount):
    if amount < 0:
        return 0
    return amount * 0.9  # 10% fee
```

### 4. Один тест = одно утверждение

**Плохо:**
```python
def test_calculate_total_and_discount():
    # Проверяет несколько вещей
    total = calculate_total([100, 200])
    discount = calculate_discount(100, 0.1)
    assert total == 300 and discount == 90
```

**Хорошо:**
```python
def test_calculate_total():
    total = calculate_total([100, 200])
    assert total == 300

def test_calculate_discount():
    discount = calculate_discount(100, 0.1)
    assert discount == 90
```

### 5. Тестируйте только то, что меняется

**Правило:** Не тестируйте код, который вы не меняете

**Пример:**
```python
# Плохо: Тестирование внешней библиотеки
def test_external_library():
    result = external_library.calculate_something()
    assert result == expected  # Не ваш код, не тестите
```

**Хорошо:**
```python
# Проверяйте только ваш код
def test_my_function():
    result = my_calculate(100, 0.1)
    assert result == expected
```

## Типы тестов

### Unit Testing (Юнит-тестирование)

**Что это:** Тестирование отдельных функций или классов

**Когда использовать:**
- Для изолированной бизнес-логики
- Для алгоритмов (математика, обработка данных)
- Для утилитных функций

**Пример:**
```python
import pytest

def calculate_discount(price, discount_rate):
    """Вычисляет скидку."""
    return price * discount_rate

def test_calculate_discount_10_percent():
    """Проверяет 10% скидку."""
    result = calculate_discount(100, 0.1)
    assert result == 10.0

def test_calculate_discount_zero_rate():
    """Проверяет 0% скидку."""
    result = calculate_discount(100, 0.0)
    assert result == 0.0

def test_calculate_discount_negative_price():
    """Проверяет обработку отрицательных цен."""
    with pytest.raises(ValueError):
        calculate_discount(-100, 0.1)
```

### Integration Testing (Интеграционное тестирование)

**Что это:** Тестирование взаимодействия между компонентами

**Когда использовать:**
- Для проверки что модули работают вместе
- Для проверки API endpoints
- Для проверки database queries

**Пример:**
```python
import pytest
from myapp.database import Database
from myapp.services import UserService

def test_user_creation_flow():
    """Проверяет создание пользователя."""
    db = Database(":memory:")
    service = UserService(db)
    
    # Создаём пользователя
    user = service.create_user("test@example.com", "password")
    assert user.id is not None
    
    # Проверяем что пользователь сохранён
    saved_user = service.get_user(user.id)
    assert saved_user.email == "test@example.com"
```

### End-to-End Testing (E2E)

**Что это:** Тестирование полного потока через систему

**Когда использовать:**
- Для проверки критических пользовательских путей
- Для проверки интеграции между сервисами
- Для проверки UI workflows

**Пример:**
```python
def test_user_login_flow():
    """Проверяет процесс логина пользователя."""
    # 1. Открываем страницу
    login_page = open("/login")
    assert login_page.status_code == 200
    
    # 2. Вводим данные
    login_page.enter_email("test@example.com")
    login_page.enter_password("password")
    assert not login_page.email_has_errors()
    
    # 3. Кликаем логин
    login_page.click_login()
    assert login_page.url == "/dashboard"
    
    # 4. Проверяем что пользователь авторизован
    assert login_page.is_authenticated()
```

## Best Practices

### 1. Используйте понятные имена тестов

**Плохо:**
```python
def test1():
    pass
def test2():
    pass
```

**Хорошо:**
```python
def test_calculate_discount_positive():
    """Тест положительной скидки."""
    pass

def test_calculate_discount_negative():
    """Тест обработки отрицательных значений."""
    pass
```

### 2. Делайте тесты быстрыми

**Правило:** Тесты должны работать <1 секунда

**Плохо:**
```python
def test_slow_operation():
    """Этот тест работает 10 секунд."""
    time.sleep(10)
    assert True  # Slow test
```

**Хорошо:**
```python
def test_fast_operation():
    """Этот тест работает 0.01 секунды."""
    assert complex_calculation() == expected
```

### 3. Используйте fixtures для тестовых данных

**Пример:**
```python
import pytest

@pytest.fixture
def user_data():
    """Тестовые данные пользователя."""
    return {
        'email': 'test@example.com',
        'password': 'securepassword',
        'discount_rate': 0.1
    }

def test_user_registration(user_data):
    """Тест регистрации пользователя."""
    result = register_user(user_data['email'], user_data['password'])
    assert result.success is True

def test_user_discount(user_data):
    """Тест скидки пользователя."""
    discount = calculate_discount(100, user_data['discount_rate'])
    assert discount == 10.0
```

### 4. Mock внешние зависимости

**Пример:**
```python
import pytest
from unittest.mock import Mock, patch

def test_api_call_with_mock():
    """Тест API вызова с mock."""
    # Mock database
    mock_db = Mock()
    mock_db.get_user.return_value = Mock(email="test@example.com")
    
    # Test with mock
    with patch('myapp.database.Database', return_value=mock_db):
        service = UserService()
        user = service.get_user(1)
        assert user.email == "test@example.com"
```

### 5. Тестируйте error handling

**Пример:**
```python
def test_calculate_discount_invalid_rate():
    """Тест обработки недопустимой ставки скидки."""
    with pytest.raises(ValueError):
        calculate_discount(100, 1.5)  # 150% скидка

def test_database_connection_error():
    """Тест обработки ошибки подключения к базе."""
    with pytest.raises(ConnectionError):
        service = UserService("invalid_connection_string")
        user = service.get_user(1)
```

### 6. Используйте parametrized тесты

**Пример:**
```python
import pytest

@pytest.mark.parametrize("price,discount_rate,expected", [
    (100, 0.1, 10.0),
    (200, 0.15, 30.0),
    (300, 0.2, 60.0),
])
def test_calculate_discount_parameterized(price, discount_rate, expected):
    """Параметризованный тест скидки."""
    result = calculate_discount(price, discount_rate)
    assert result == expected
```

### 7. Тестируйте edge cases

**Пример:**
```python
def test_calculate_discount_zero_price():
    """Тест нулевой цены."""
    result = calculate_discount(0, 0.1)
    assert result == 0.0

def test_calculate_discount_very_large_value():
    """Тест очень большого значения."""
    result = calculate_discount(1_000_000, 0.1)
    assert result == 100_000.0

def test_calculate_discount_negative_value():
    """Тест отрицательного значения."""
    with pytest.raises(ValueError):
        calculate_discount(-100, 0.1)
```

### 8. Организуйте тесты в папки

**Структура:**
```
tests/
├── unit/
│   ├── test_calculate_discount.py
│   ├── test_calculate_total.py
│   └── test_user_service.py
├── integration/
│   ├── test_user_flow.py
│   └── test_database_queries.py
├── e2e/
│   ├── test_login_flow.py
│   └── test_checkout_flow.py
└── fixtures/
    ├── user_data.py
    └── test_data.py
```

### 9. Запускайте тесты автоматически

**Пример (pytest):**
```bash
# Запустить все тесты
pytest

# Запустить только unit тесты
pytest tests/unit/

# Запустить только конкретный файл
pytest tests/unit/test_calculate_discount.py

# Запустить с verbose output
pytest -v

# Запустить с coverage report
pytest --cov=myapp tests/
```

**Пример (unittest):**
```bash
# Запустить все тесты
python -m unittest discover

# Запустить конкретный тест
python -m unittest tests.unit.test_calculate_discount

# Запустить с verbose
python -m unittest tests.unit.test_calculate_discount -v
```

### 10. Покрытие кода тестами

**Цель:** Как можно больше кода покрыто тестами

**Пример pytest:**
```bash
# Сгенерировать coverage report
pytest --cov=myapp --cov-report=html tests/

# Проверить процент покрытия
pytest --cov=myapp --cov-fail-under=90 tests/
```

**Пример coverage:**
```python
# Файл .coveragerc
[run]
omit = tests/*
```

## Quick Reference

| Тип теста | Когда использовать | Пример |
|-----------|-----------------|--------|
| Unit | Изолированная функция | `def calculate_discount()` |
| Integration | Модули работают вместе | `UserService + Database` |
| E2E | Полный поток | Login → Dashboard |
| Parametrized | Множества входов | `@pytest.mark.parametrize` |

## Связи

Тестирование связано с:
- [[foundations]] — Тесты основаны на базовых концепциях
- [[code-review]] — Тесты проверяют код-review findings
- [[debugging]] — Тесты помогают находить bugs
- [[refactoring]] — Тесты защищают от регрессий при рефакторинге

## Wisdom

> "Testing shows the presence, not the absence, of bugs." — Edsger Dijkstra

Не тестируйте чтобы всё работало.
Тестируйте чтобы код ломался ожидаемо.
Найдите bugs до того как они найдут ваши пользователи.

Тесты — это ваши страховщики.
Хорошие тесты = спокойная работа.

Пишите тесты первым.
Код будет следовать.
Качество улучшится.
