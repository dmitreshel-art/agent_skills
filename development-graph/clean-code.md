---
description: "Принципы чистого кода и практики написания кода"
version: "1.0.0"
tags: ["clean-code", "fundamentals", "code-quality"]
related: ["refactoring", "testing", "code-review"]
---

# Clean Code

## Overview

Clean code is code that is easy to understand, easy to modify, and does what it's supposed to do. It's not about style — it's about communication. Code is read far more often than it's written, so write for the reader.

## Core Principles

### 1. Meaningful Names

Names should reveal intent:

**Bad:**
```python
def d(x):
    return x * 86400
```

**Good:**
```python
def days_to_seconds(days):
    return days * 86400
```

**Rules:**
- Use intention-revealing names
- Avoid disinformation (don't call a list `user_list` if it's not a list)
- Make meaningful distinctions (avoid `a1`, `a2`, `a3`)
- Use pronounceable names
- Use searchable names (avoid single letters)

### 2. Functions Should Do One Thing

**Bad:**
```python
def process_user(user_data):
    # Validate user
    if not user_data.get('email'):
        raise ValueError('Email required')

    # Transform data
    user_data['email'] = user_data['email'].lower()

    # Save to database
    db.save(user_data)

    # Send email
    email_service.send(user_data)
```

**Good:**
```python
def validate_user(user_data):
    if not user_data.get('email'):
        raise ValueError('Email required')

def transform_user(user_data):
    user_data['email'] = user_data['email'].lower()
    return user_data

def save_user(user_data):
    db.save(user_data)

def send_welcome_email(user_data):
    email_service.send(user_data)

def process_user(user_data):
    validate_user(user_data)
    user_data = transform_user(user_data)
    save_user(user_data)
    send_welcome_email(user_data)
```

**Rules:**
- Functions should be small (fewer than 20 lines is a good target)
- Functions should do one thing
- One level of abstraction per function

### 3. Comments vs Code

**Bad:**
```python
# Check if user is eligible for discount
if user.age >= 65 and user.has_membership:
    user.apply_discount(0.1)  # 10% discount
```

**Good:**
```python
if user.is_eligible_for_senior_discount():
    user.apply_discount(0.1)
```

**Rule:** Comments should explain *why*, not *what*. If you need comments to explain what code does, rewrite the code.

### 4. Error Handling

**Bad:**
```python
def process_payment(amount):
    result = payment_gateway.charge(amount)
    return result
```

**Good:**
```python
def process_payment(amount):
    try:
        result = payment_gateway.charge(amount)
        if result.is_successful():
            return result
        else:
            raise PaymentError(result.error_message)
    except PaymentGatewayError as e:
        logger.error(f"Payment failed: {e}")
        raise PaymentError("Unable to process payment")
```

**Rules:**
- Don't swallow exceptions
- Provide meaningful error messages
- Log errors for debugging
- Fail fast with clear errors

## Common Mistakes

### 1. Magic Numbers

**Bad:**
```python
if score > 95:
    grade = 'A'
elif score > 85:
    grade = 'B'
```

**Good:**
```python
GRADE_A_THRESHOLD = 95
GRADE_B_THRESHOLD = 85

if score > GRADE_A_THRESHOLD:
    grade = 'A'
elif score > GRADE_B_THRESHOLD:
    grade = 'B'
```

### 2. Deep Nesting

**Bad:**
```python
if user:
    if user.is_active:
        if user.has_permission:
            if user.has_subscription:
                process(user)
```

**Good:**
```python
if not user:
    return

if not user.is_active:
    return

if not (user.has_permission and user.has_subscription):
    return

process(user)
```

### 3. DRY Violations

**Bad:**
```python
def send_email_to_user(user):
    email = Email()
    email.to = user.email
    email.from_ = 'noreply@company.com'
    email.subject = 'Welcome'
    email.body = 'Hello!'
    email.send()

def send_email_to_admin(user):
    email = Email()
    email.to = user.email
    email.from_ = 'noreply@company.com'
    email.subject = 'Alert'
    email.body = 'Warning!'
    email.send()
```

**Good:**
```python
def send_email(to, subject, body):
    email = Email()
    email.to = to
    email.from_ = 'noreply@company.com'
    email.subject = subject
    email.body = body
    email.send()

def send_email_to_user(user):
    send_email(user.email, 'Welcome', 'Hello!')

def send_email_to_admin(user):
    send_email(user.email, 'Alert', 'Warning!')
```

## Integration

Clean code connects to:
- [[refactoring]] — Refactoring improves code quality
- [[testing]] — Clean code is easier to test
- [[code-review]] — Code reviews enforce clean standards
- [[debugging]] — Clean code is easier to debug

## Quick Reference

| Principle | Key Rule |
|-----------|-----------|
| Meaningful Names | Reveal intent, be pronounceable |
| One Thing | Functions do one thing only |
| Comments | Explain why, not what |
| Error Handling | Don't swallow, provide context |
| DRY | Don't repeat yourself |
| Magic Numbers | Use named constants |

## When to Apply

Always write clean code:
- New features
- Bug fixes (don't introduce bad code when fixing bugs)
- Refactoring (the whole point)
- Code reviews (enforce standards)

## Wisdom

> "Any fool can write code that a computer can understand. Good programmers write code that humans can understand." — Martin Fowler

Write for humans.
Machines are easy.
Humans are hard.

Make it readable.
