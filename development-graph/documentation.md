---
description: "Стандарты документирования и обмена знаниями"
version: "1.0.0"
tags: ["documentation", "knowledge-sharing", "best-practices"]
related: ["code-review", "clean-code", "testing"]
---

# Documentation

## Overview

Documentation is not a separate activity — it's part of writing code. Good documentation helps teammates understand your work, helps future-you understand what past-you wrote, and helps users use your software. Documentation is your time machine to the future.

## Core Principles

### 1. Document Why, Not What

**Bad:**
```python
# This function calculates the total price
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total
```

**Good:**
```python
def calculate_total(items):
    """
    Calculate total price including taxes and discounts.

    Applies local tax rate based on user location and any
    active discounts from the user's account.

    Args:
        items: List of OrderItem objects

    Returns:
        Total price as float, including tax and discounts
    """
    tax_rate = get_tax_rate(user.location)
    discount = get_user_discount(user.id)
    total = sum(item.price for item in items)
    return total * (1 + tax_rate) * (1 - discount)
```

**Rule:** Code explains what. Docs explain why.

### 2. Keep Documentation Close to Code

**Bad:**
- Documentation in separate Wiki
- Documentation in Word docs
- Documentation that drifts from code

**Good:**
- Docstrings in code
- README in repository
- Code comments inline

**Rule:** Documentation lives with the code it describes.

### 3. Assume the Reader Is Busy

Make it scannable:
- Clear headings
- Code examples
- Visual aids when helpful
- Examples, not just theory

## Types of Documentation

### 1. Code Documentation

**Docstrings:**
```python
def send_email(to, subject, body):
    """
    Send an email to the specified recipient.

    Handles retries and logging automatically.

    Args:
        to: Recipient email address
        subject: Email subject line
        body: Email body content

    Returns:
        True if sent successfully, False otherwise

    Raises:
        ValueError: If email address is invalid
    """
    # Implementation
```

**Comments:**
```python
# Use retry logic because email service is unreliable
# Max 3 retries with exponential backoff
for attempt in range(3):
    try:
        send_via_smtp()
        break
    except SMTPError:
        time.sleep(2 ** attempt)
```

### 2. Project Documentation

**README.md:**
```markdown
# Project Name

Brief description of what this project does.

## Installation
Steps to install.

## Usage
How to use the project.

## Examples
Code examples showing usage.

## Contributing
How to contribute.

## License
License information.
```

**ARCHITECTURE.md:**
```markdown
# Architecture

System architecture and design decisions.

## Components
- Component A: Does X
- Component B: Does Y

## Data Flow
How data flows through system.

## Trade-offs
Design decisions and why we made them.
```

### 3. API Documentation

**Endpoint Documentation:**
```markdown
## Create User

### POST /api/users

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepass123"
}
```

**Response:**
```json
{
  "id": "123",
  "email": "user@example.com",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Errors:**
- 400: Invalid email format
- 409: Email already exists
```

## Documentation Best Practices

### 1. Start with README

Every project should have:
- What it does
- Why it exists
- How to install
- How to use
- How to contribute

### 2. Keep It Up to Date

**Problem:** Documentation drifts from code
**Solution:** Update docs with code changes

**In [[code-review]]:** Check if docs need updating

### 3. Use Examples

**Bad:**
```
The function processes user data.
```

**Good:**
```python
# Example usage
user = UserService().get_user("123")
print(user.email)  # user@example.com
```

### 4. Assume Knowledge Level

- Internal docs: Assume developer knows the stack
- External docs: Assume user knows basic programming
- API docs: Assume user knows REST/HTTP basics

## Common Mistakes

### 1. Over-Documenting Obvious Code

**Bad:**
```python
# Set variable i to 0
i = 0

# Loop through list
for item in items:
    print(item)
```

**Rule:** Don't document the obvious. Code should be self-documenting (see [[clean-code]]).

### 2. Outdated Documentation

**Bad:** Docs say function takes 2 args, it now takes 3
**Good:** Update docs when code changes

**Rule:** Documentation drift is worse than no documentation.

### 3. No Examples

**Bad:** "The function calculates totals"
**Good:** "The function calculates totals. Example:..."

**Rule:** Show, don't just tell.

## Documentation Workflow

### 1. Plan Documentation

Before writing code, plan what docs you need:
- User-facing docs?
- API docs?
- Internal architecture docs?

### 2. Write While Coding

Don't wait until the end:
- Write docstrings when writing functions
- Update README when adding features
- Document decisions when making them

### 3. Review Documentation

In [[code-review]]:
- Are docstrings present?
- Are they accurate?
- Are examples helpful?

### 4. Maintain Documentation

Keep docs in sync with code:
- Update when code changes
- Remove obsolete docs
- Fix inaccuracies

## Integration

Documentation connects to:
- [[code-review]] — Reviews catch missing docs
- [[clean-code]] — Self-documenting code needs less docs
- [[testing]] — Tests can serve as documentation
- [[architecture]] — Architecture needs documentation

## Quick Reference

| Doc Type | Audience | Content |
|-----------|-----------|----------|
| Docstrings | Developers | Function/class purpose, args, returns |
| README | Everyone | Project overview, installation, usage |
| API Docs | API Users | Endpoints, requests, responses, errors |
| Architecture Docs | Developers | System design, components, decisions |

## Tools

### Documentation Generators
- **Sphinx:** Python documentation
- **Swagger/OpenAPI:** API documentation
- **JSDoc:** JavaScript documentation

### Documentation Hosting
- **GitHub Pages:** Static sites from repos
- **Read the Docs:** Documentation hosting
- **Notion:** Internal knowledge base

## When to Document

**Always:**
- Public APIs
- Complex algorithms
- Non-obvious business logic
- Architecture decisions

**Sometimes:**
- Helper functions
- Configuration options
- Error handling patterns

**Rarely:**
- Trivial code (getters, setters)
- Obvious operations
- Temporary code

## Wisdom

> "Code is like humor. When you have to explain it, it's bad." — Cory House

Write self-documenting code first.
Then document the non-obvious.

Documentation is the README to your code.
Make it helpful.

## Documentation Anti-Patterns

Don't:
- Document obvious code
- Let docs drift from code
- Write docs without examples
- Assume reader knows everything
- Skip docs for "temporary" code

Remember: Future-you will thank present-you.
