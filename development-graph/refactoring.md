---
description: "Паттерны рефакторинга и улучшения кода"
version: "1.0.0"
tags: ["refactoring", "maintenance", "code-quality"]
related: ["clean-code", "testing", "debugging"]
---

# Refactoring

## Overview

Refactoring is improving code structure without changing behavior. It's not about adding features or fixing bugs — it's about making code easier to understand, modify, and maintain. Good refactoring makes future changes easier and faster.

## Core Principles

### 1. Two Hats Rule

When you refactor, wear the refactoring hat:
- **Refactoring hat:** Improving structure, not changing behavior
- **Feature hat:** Adding functionality, changing behavior

Never mix them. Refactor first, then add features.

### 2. Small Steps

Refactor in small, testable increments:
- Make a small change
- Run tests
- If green, commit
- Repeat

**Never:** "I'll refactor this whole module at once"

### 3. [[testing]] Safety Net

Never refactor without tests:
- Tests catch when you accidentally change behavior
- Tests give you confidence to make changes
- Tests verify refactoring doesn't break anything

**Rule:** No tests, no refactoring.

## When to Refactor

### Good Reasons

- Code is hard to understand
- Code has duplication
- Code is hard to modify
- Code has too many responsibilities
- Tests are hard to write

### Bad Reasons

- "I don't like this style" (but it works)
- "This doesn't match my preferences"
- "Let's just clean this up" (without understanding)

**Rule:** Refactor for maintainability, not preferences.

## Common Refactorings

### 1. Extract Method

**Before:**
```python
def print_invoice(invoice):
    print(f"Invoice: {invoice.id}")
    print(f"Customer: {invoice.customer_name}")
    print(f"Date: {invoice.date}")
    total = 0
    for item in invoice.items:
        total += item.price * item.quantity
    print(f"Total: ${total}")
    # ... more code
```

**After:**
```python
def print_invoice(invoice):
    print_header(invoice)
    total = calculate_total(invoice)
    print_footer(total)

def print_header(invoice):
    print(f"Invoice: {invoice.id}")
    print(f"Customer: {invoice.customer_name}")
    print(f"Date: {invoice.date}")

def calculate_total(invoice):
    total = 0
    for item in invoice.items:
        total += item.price * item.quantity
    return total

def print_footer(total):
    print(f"Total: ${total}")
```

**Benefits:**
- Functions do one thing
- Easier to test
- Reusable components

### 2. Extract Variable

**Before:**
```python
if (order.items_count > 10 and order.total > 1000 and
    order.customer.is_vip):
    apply_discount(0.1)
```

**After:**
```python
is_large_order = order.items_count > 10
is_expensive_order = order.total > 1000
is_vip_customer = order.customer.is_vip

if is_large_order and is_expensive_order and is_vip_customer:
    apply_discount(0.1)
```

**Benefits:**
- More readable
- Self-documenting
- Easier to debug

### 3. Replace Conditional with Polymorphism

**Before:**
```python
def calculate_area(shape):
    if shape.type == 'circle':
        return 3.14 * shape.radius ** 2
    elif shape.type == 'rectangle':
        return shape.width * shape.height
    elif shape.type == 'triangle':
        return 0.5 * shape.base * shape.height
```

**After:**
```python
class Circle:
    def area(self):
        return 3.14 * self.radius ** 2

class Rectangle:
    def area(self):
        return self.width * self.height

class Triangle:
    def area(self):
        return 0.5 * self.base * self.height

# Use
area = shape.area()
```

**Benefits:**
- Eliminates conditional logic
- Easier to add new shapes
- Follows Open/Closed Principle

### 4. Rename Variable/Function

**Before:**
```python
def calc(d, r):
    return d * (1 + r/100)
```

**After:**
```python
def calculate_discounted_price(price, discount_percentage):
    return price * (1 + discount_percentage/100)
```

**Benefits:**
- Self-documenting code
- Reveals intent
- No need for comments

### 5. Remove Dead Code

**Before:**
```python
def process_order(order):
    # Old discount logic
    # if order.has_old_discount:
    #     apply_legacy_discount()

    if order.has_discount:
        apply_discount(order.discount)
```

**After:**
```python
def process_order(order):
    if order.has_discount:
        apply_discount(order.discount)
```

**Benefits:**
- Less code to maintain
- Less confusion
- Cleaner codebase

## Code Smells and Solutions

### Long Function

**Smell:** Function > 20 lines, multiple responsibilities
**Solution:** [[refactoring]] into smaller functions

### Duplicated Code

**Smell:** Same code in multiple places
**Solution:** [[refactoring]], create helper functions

### Long Parameter List

**Smell:** Function has 5+ parameters
**Solution:** Pass object instead, use parameter object

### Comments Where Code Should Be Clear

**Smell:** Code needs comments to be understood
**Solution:** Rewrite code to be self-documenting (see [[clean-code]])

### Large Class

**Smell:** Class has too many responsibilities
**Solution:** [[refactoring]], split into smaller classes

## Refactoring Workflow

### 1. Identify the Problem

- Code is hard to understand
- Code has duplication
- Code is hard to test
- Code has a code smell

### 2. Write a Test (if none exists)

```python
def test_refactoring_doesnt_change_behavior():
    result_before = process_order(order)
    refactor_code()
    result_after = process_order(order)
    assert result_before == result_after
```

### 3. Apply Refactoring

- Make small, incremental change
- Run tests after each change
- Commit if green

### 4. Verify

- Run all tests
- Check for regressions
- Verify code is better

## Integration

Refactoring connects to:
- [[clean-code]] — Refactoring implements clean code
- [[testing]] — Tests enable safe refactoring
- [[debugging]] — Refactored code is easier to debug
- [[code-review]] — Reviews identify refactoring opportunities

## Quick Reference

| Refactoring | When to Use | Benefit |
|-------------|--------------|----------|
| Extract Method | Long function | Smaller, focused functions |
| Extract Variable | Complex expression | More readable |
| Rename Variable | Unclear name | Self-documenting |
| Replace Condition with Polymorphism | Long switch/if | Eliminates conditionals |
| Remove Dead Code | Unused code | Cleaner codebase |

## Common Mistakes

### 1. Refactoring Without Tests

**Bad:** Change code structure without tests
**Good:** Write tests first, then refactor

**Why:** Tests catch when you accidentally change behavior.

### 2. Too Much at Once

**Bad:** "I'll refactor this whole module"
**Good:** "I'll refactor this function today, this method tomorrow"

**Why:** Small steps are safer and easier to review.

### 3. Refactoring to "Perfect" Code

**Bad:** Trying to make code perfect
**Good:** Making code good enough

**Why:** Perfect is the enemy of good.

## Anti-Patterns

### Don't:

- Refactor while fixing a bug (two hats!)
- Refactor without understanding why code exists
- Refactor to match your style preferences
- Refactor code that works and is rarely touched

## Best Practices

1. **Test Driven Refactoring**
   - Write failing test for current behavior
   - Refactor code
   - Test should still pass

2. **Small Commits**
   - One refactoring per commit
   - Easy to review
   - Easy to revert

3. **Document Decisions**
   - Why did you refactor this way?
   - What alternatives did you consider?
   - See [[documentation]]

4. **Measure Impact**
   - Is code more readable?
   - Is it easier to test?
   - Is it easier to modify?

## When NOT to Refactor

- Code that works and is rarely touched
- Code about to be replaced
- Code you don't understand (learn first)
- Without tests (write tests first)

## Wisdom

> "Any code of your own that you haven't looked at for six or more months might as well have been written by someone else." — Eagleson's Law

Refactor when you can't understand your own code.

Make it readable.
Make it maintainable.
Make it simple.

That's what [[clean-code]] is all about.

Refactoring is the tool.
Use it.
