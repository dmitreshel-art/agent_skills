---
description: "Техники отладки и решения проблем"
version: "1.0.0"
tags: ["debugging", "problem-solving", "troubleshooting"]
related: ["testing", "code-review", "foundations"]
---

# Отладка (Debugging)

## Overview

Отладка — это процесс нахождения и исправления ошибок в коде. Это критически важный навык для всех разработчиков — от новичков до экспертов. Хорошие навыки отладки могут сэкономить вам часы работы.

## Ключевые принципы

### 1. Научайтесь использовать Debugger вместо Print

**Плохо:**
```python
def process_data(data):
    for item in data:
        if item['value'] > 100:
            print("Processing:", item)
            # ... more code
```

**Хорошо:**
```python
def process_data(data):
    for item in data:
        if item['value'] > 100:
            breakpoint()  # Stops here, you can inspect variables
            result = complex_calculation(item)
        return result
```

**Правило:** Если вам нужно узнать значение переменной, используйте debugger, а не print.

### 2. Разделяйте проблему на части

**Плохо:**
```python
# Try to fix everything at once
def fix_all_the_things():
    # ... 100 lines of code
```

**Хорошо:**
```python
def test_specific_case():
    # Test only this specific scenario
    assert result == expected
```

**Правило:** Минимизируйте объём кода, который вы тестируете за один раз.

### 3. Записывайте то, что вы уже попытались

**Плохо:**
```python
# Try random fixes
# I wonder if this variable is None?
# Let's try changing it
# Let's try another approach
# (10 minutes later) Oops, I forgot what worked
```

**Хорошо:**
```python
# Debugging notes
# 2024-02-22: Tried changing variable type - didn't work
# 2024-02-22: Added null check - fixed the bug
```

**Правило:** Отслеживайте ваши попытки. Это сэкономит вам время в будущем.

## Инструменты отладки

### 1. Print Debugging (Простейший)

**Когда использовать:**
- Быстрая проверка значений
- Логирование хода выполнения
- Понимание базового флоу

**Пример:**
```python
def calculate_discount(price, discount_rate):
    print(f"DEBUG: price={price}, discount={discount_rate}")
    discounted = price * discount_rate
    print(f"DEBUG: discounted={discounted}")
    return discounted
```

**Плюсы:** Самый простой, не требует настроек
**Минусы:** Не позволяет пошаговую отладку, засоряет логи

### 2. Interactive Debugger (Интерактивный отладчик)

**Когда использовать:**
- Исследование состояния переменных
- Пошаговое выполнение кода
- Понимание сложной логики

**Инструменты:**

**Python Debugger (pdb):**
```bash
# Запуск скрипта с debugger
python -m pdb script.py

# Или встроить в код
import pdb; pdb.set_trace()  # Stops here
```

**IPython Debugger (ipdb):**
```python
# Установите
pip install ipdb

# Используйте
import ipdb; ipdb.set_trace()
```

**VS Code Debugger:**
```python
# VS Code автоматически интегрирован
# Установите точку останова (breakpoint) нажимая на слева от номера строки
# Нажмите F5 для запуска debug mode
# Используйте Debug Console для проверки переменных
```

**PyCharm Debugger:**
- Full-featured IDE debugger
- Variable inspection, call stack, breakpoints
- Step into, step over, continue buttons

### 3. Logging (Логирование)

**Когда использовать:**
- Отслеживание выполнения кода в production
- Понимание ошибок, когда они происходят
- Анализ производительности

**Пример:**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_user(user_id):
    logger.info(f"Processing user {user_id}")
    
    try:
        result = risky_operation(user_id)
        logger.info(f"Success: {result}")
    except Exception as e:
        logger.error(f"Failed for user {user_id}: {e}")
        logger.error(f"Traceback: {e.__traceback__}")
```

**Уровни логирования:**
- **DEBUG:** Подробная информация (для разработки)
- **INFO:** Общая информация (запуск, завершение)
- **WARNING:** Потенциальные проблемы
- **ERROR:** Ошибки, которые прерывают выполнение
- **CRITICAL:** Критические проблемы

### 4. Assertion Testing (Проверка утверждений)

**Когда использовать:**
- Проверка предусловий
- Верификация инвариантов
- Валидация входных данных

**Пример:**
```python
def calculate_discount(price, discount_rate):
    assert price > 0, "Price must be positive"
    assert 0 <= discount_rate <= 1, "Discount rate must be between 0 and 1"
    
    discounted = price * discount_rate
    assert discounted >= 0, "Discounted price cannot be negative"
    
    return discounted
```

**Правило:** Используйте assertions для проверки предположений, но не для логики управления (используйте if/else).

### 5. Unit Testing (Юнит-тестирование)

**Когда использовать:**
- Проверка отдельных функций/классов
- Валидация поведения на граничных значения
- Снижение сложности через маленькие тесты

**Пример:**
```python
import pytest

def test_calculate_discount_positive_price():
    result = calculate_discount(100, 0.1)
    assert result == 90.0

def test_calculate_discount_negative_price():
    result = calculate_discount(-100, 0.1)
    assert result == -10.0

def test_calculate_discount_zero_price():
    result = calculate_discount(0, 0.1)
    assert result == 0.0

def test_calculate_discount_full_discount():
    result = calculate_discount(100, 1.0)
    assert result == 0.0
```

**Правило:** Пишите тесты до того, как напишете код. Это поможет вам быстро обнаружить регрессии.

### 6. Remote Debugging (Удалённая отладка)

**Когда использовать:**
- Отладка кода на удалённом сервере
- Отладка кода в контейнере
- Отладка кода в production среде

**Инструменты:**

**VS Code Remote Debugging:**
```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "remote-server.com",
                "port": 22,
                "user": "username",
                "password": "${command:Ask for password}"
            },
            "path": "${workspaceFolder}/app.py",
            "justMyCode": false
        }
    ]
}
```

**PyCharm Remote Debugging:**
- Настройте remote interpreter
- Установите breakpoint
- Запустите в debug mode

**Remote PDB (RPDB):**
```python
# Установите
pip install rpdb

# В коде добавьте
import rpdb; rpdb.set_trace()
```

**Ключ:** Всегда используйте logging для удалённой отладки, так как интерактивный debugger может быть недоступен.

## Стратегии отладки

### 1. Бинарный поиск (Binary Search)

Сужайте область проблемы пополам:

```python
# Проблема: Функция возвращает неправильный результат
# Возможные причины: 
# 1. Входные данные неверны
# 2. Алгоритм неверен
# 3. Проблема в логике
# 4. Проблема в математике

# Начните с проверки входных данных
assert input_data is not None
assert len(input_data) > 0

# Затем проверяйте каждый шаг алгоритма
step1_result = calculate_step1(input_data)
assert step1_result is not None
step2_result = calculate_step2(step1_result)
assert step2_result is not None
```

### 2. Минимализация воспроизводимости

Создайте минимальный пример, который воспроизводит проблему:

```python
# Минимальный пример вместо сложного приложения
def test_bug():
    data = {"value": 150, "discount_rate": 0.1}
    result = calculate_discount(data["value"], data["discount_rate"])
    print(f"Result: {result}")
    assert result == 135.0  # Should be 135
```

**Преимущество:** Если минимальный пример работает, значит проблема в других частях кода.

### 3. Rubber Ducking (Объяснение кода резиновой уточке)

Объясните код вслух простыми словами или с бумажкой:

**Пример:**
```python
# Объясните вслух:
"Эта функция вычисляет скидку на основе цены. Сначала проверяется, что цена положительная, затем применяется процент скидки."

# Объясните с бумажкой:
"""
Функция: calculate_discount(price, discount_rate)

Входные параметры:
- price: исходная цена в USD (должна быть > 0)
- discount_rate: процент скидки (от 0 до 1)

Алгоритм:
1. Валидация входных данных:
   - Проверяется, что цена > 0
   - Проверяется, что скидка в допустимом диапазоне (0-1)
   
2. Вычисление:
   - Умножаем цену на ставку скидки
   - Возвращаем результат

Результат:
- Скидённая цена = original_price × (1 - discount_rate)

Пример:
calculate_discount(100, 0.1) → 90.0 (10% скидка от $100)
calculate_discount(200, 0.25) → 150.0 (25% скидка от $200)

Edge cases:
- Цена 0 или отрицательная → raises assertion
- Скидка 0% → возвращается 0 (но валидация предупреждает)
- Скидка 100% → возвращается 0 (бесплатно)
"""
```

**Преимущество:** Это помогает вам лучше понять свою логику.

## Частые ошибки и их решения

### 1. Ошибка: NoneType / TypeError

**Симптом:** `TypeError: 'NoneType' object is not callable`

**Возможные причины:**
1. Переменная None вместо ожидаемого объекта
2. Функция возвращает None, но вы не проверяете
3. Аргумент функции неправильного типа

**Решение:**
```python
# Добавьте проверку
def process_data(data):
    if data is None:
        raise ValueError("Data cannot be None")
    
    if not isinstance(data, dict):
        raise TypeError(f"Expected dict, got {type(data)}")
    
    # ... process data
```

### 2. Ошибка: KeyError

**Симптом:** `KeyError: 'user_name'`

**Возможные причины:**
1. Ключ отсутствует в словаре
2. Опечатка в ключе
3. Несогласованное именование

**Решение:**
```python
# Безопасный доступ к ключу с дефолтом
username = user_data.get('username', 'Unknown')

# Или проверьте наличие ключа
if 'user_name' in user_data:
    username = user_data['user_name']
else:
    username = user_data.get('username', 'Unknown')
```

### 3. Ошибка: AttributeError

**Симптом:** `AttributeError: 'str' object has no attribute 'strip'`

**Возможные причины:**
1. Переменная не того типа, который вы ожидаете
2. Метод/атрибут не существует
3. Неправильное понимание API

**Решение:**
```python
# Проверьте тип перед использованием
if isinstance(value, str):
    cleaned = value.strip()
else:
    cleaned = str(value)

# Или используйте getattr с дефолтом
attr_value = getattr(obj, 'attribute_name', default_value)
```

### 4. Ошибка: IndexError / ValueError

**Симптомы:**
- `IndexError: list index out of range`
- `ValueError: invalid literal for int() with base 10`

**Возможные причины:**
1. Индекс массива превышает длину
2. Плохая валидация входных данных
3. Неверная математика

**Решение:**
```python
# Проверьте длину перед доступом
if index < len(array):
    value = array[index]
else:
    raise IndexError(f"Index {index} out of range for array of length {len(array)}")

# Валидация входных данных
try:
    value = int(string_value)
except ValueError as e:
    raise ValueError(f"Invalid integer value: {string_value}") from e
```

### 5. Ошибка: Logic Error

**Симптом:** Код работает, но результат неправильный

**Возможные причины:**
1. Неверный алгоритм
2. Неправное понимание требований
3. Проблема в формуле
4. Граничные условия не обработаны

**Решение:**
```python
# Добавьте юнит-тесты для проверки логики
import unittest

class TestDiscountCalculation(unittest.TestCase):
    def test_positive_discount(self):
        result = calculate_discount(100, 0.1)
        self.assertEqual(result, 90.0)
    
    def test_full_discount(self):
        result = calculate_discount(100, 1.0)
        self.assertEqual(result, 0.0)
    
    def test_zero_discount(self):
        result = calculate_discount(100, 0.0)
        self.assertEqual(result, 100.0)

# Запуск тестов
if __name__ == '__main__':
    unittest.main()
```

### 6. Ошибка: Timeout / Infinite Loop

**Симптом:** Программа зависает или выполняется слишком долго

**Возможные причины:**
1. Бесконечный цикл
2. Неэффективный алгоритм (O(n²))
3. Блокировка на внешнем ресурсе
4. Очень большие данные

**Решение:**
```python
# Добавьте timeout
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Function took too long")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)  # 10 seconds timeout

# Или оптимизируйте алгоритм
# Вместо O(n²) используйте O(n log n)
# Вместо вложенных циклов используйте list comprehensions
```

## Лучшие практики

### 1. Используйте Debugger, а не Guessing

**Плохо:**
```python
# Догадка
result = (value + 100) / 2  # Я думаю это должно работать
```

**Хорошо:**
```python
# Использование debugger
def calculate_result(value):
    breakpoint()  # Здесь остановитесь и проверьте value
    result = complex_calculation(value)
    return result
```

### 2. Пишите Debuggable Code (Отлаживаемый код)

**Плохо:**
```python
# Слишком сложное, трудно понять
def calculate_total(items):
    result = 0
    for item in items:
        result += item['value'] * item['discount'] * item.get('tax', 1.0) * (1 - item.get('discount_rate', 0.0)) / (1 + item.get('markup', 0.0)) * (1 - item.get('shipping', 0.0))
    return result
```

**Хорошо:**
```python
# Разбейте на понятные части
def calculate_item_total(item):
    """Calculate total for a single item."""
    price = item['value']
    discount = price * item['discount_rate']
    tax = discount * item.get('tax', 0.0)
    shipping = item.get('shipping', 0.0)
    return price + tax + shipping

def calculate_total(items):
    """Calculate total for all items."""
    return sum(calculate_item_total(item) for item in items)
```

**Преимущества:**
- Легче понять
- Легче протестировать
- Легче найти ошибки

### 3. Минимизируйте State (Состояние)

**Плохо:**
```python
# Глобальные переменные
result_cache = {}
is_initialized = False

def process_user(user_id):
    global is_initialized
    if not is_initialized:
        result_cache = load_cache()
        is_initialized = True
    # ... process user
```

**Хорошо:**
```python
# Передавайте состояние явно
def process_user(user_id, cache=None):
    if cache is None:
        cache = load_cache()
    # ... process user with cache
    return result
```

**Преимущества:**
- Нет скрытых зависимостей
- Легче тестировать
- Нет race conditions в concurrent коде

### 4. Добавляйте Logging

**Пример:**
```python
import logging

logger = logging.getLogger(__name__)

def process_payment(payment):
    logger.info(f"Processing payment: {payment['id']}")
    
    try:
        result = charge_payment(payment)
        logger.info(f"Payment successful: {result}")
        return result
    except InsufficientFundsError as e:
        logger.error(f"Insufficient funds: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
```

**Рекомендация:** Используйте logging вместо print statements.

### 5. Пишите Unit Tests

**Пример:**
```python
import pytest

def test_calculate_discount_zero_discount():
    """Test zero discount edge case."""
    result = calculate_discount(100, 0.0)
    assert result == 100.0

def test_calculate_discount_negative_price():
    """Test negative price edge case."""
    with pytest.raises(ValueError):
        calculate_discount(-100, 0.1)
```

**Рекомендация:** Покрывайте edge cases тестами.

### 6. Изолируйте проблемы

Создайте минимальный пример, который воспроизводит проблему:

```python
def test_bug_scenario():
    """Test the bug in isolation."""
    # This isolates the bug from the rest of the code
    setup_scenario()
    trigger_bug()
    assert bug_reproduced()
```

**Преимущества:**
- Легче понять проблему
- Легче исправить
- Легче убедиться, что исправление работает

## Интеграция

Отладка связана с:
- [[testing]] — Unit tests help catch bugs early
- [[code-review]] — Code review helps identify difficult-to-debug code
- [[foundations]] — Strong foundations make code easier to debug
- [[performance]] — Performance monitoring helps identify bottlenecks

## Quick Reference

| Инструмент | Когда использовать | Пример |
|-----------|---------------|--------|
| Print Debugging | Быстрая проверка значений | `print(f"DEBUG: {var}")` |
| Interactive Debugger | Исследование состояния | `breakpoint()` или IDE debugger |
| Logging | Production logging | `logger.error(f"Error: {e}")` |
| Assertions | Проверка предусловий | `assert price > 0` |
| Unit Tests | Проверка функций | `pytest test_function()` |
| Remote Debugging | Удалённая отладка | VS Code Remote, PyCharm Remote |

## Связи

Этот навык связан с:
- [[testing]] — Unit tests prevent bugs
- [[code-review]] — Code review catches debugging issues
- [[foundations]] — Strong foundations reduce bugs
- [[performance]] — Performance monitoring helps identify bottlenecks
- [[documentation]] — Good documentation explains debugging approaches

## Wisdom

> "Debugging is twice as hard as writing the code in the first place. So if you're as clever as possible when you write the code, you will, by definition, be too smart to debug it." — Brian Kernighan

Пишите отлаживаемый код.
Тестируйте часто.
Документируйте свои findings.

Это сэкономит вам часы отладки.
