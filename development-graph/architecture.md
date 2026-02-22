---
description: "Архитектурные принципы и системный дизайн"
version: "1.0.0"
tags: ["architecture", "design", "system-design"]
related: ["clean-code", "refactoring", "testing"]
---

# Architecture

## Overview

Architecture is the high-level structure of your system. It determines how components interact, how the system scales, and how easy it is to change. Good architecture makes development easier; bad architecture makes everything harder.

## Core Principles

### 1. Separation of Concerns

Different components should have different responsibilities:

**Bad:**
```python
class OrderProcessor:
    def process(self, order):
        # Business logic
        total = calculate_total(order)

        # Database access
        db.save(order)

        # Email sending
        email_service.send(order)

        # Logging
        logger.log(f"Processed {order.id}")
```

**Good:**
```python
class OrderProcessor:
    def __init__(self, db, email_service, logger):
        self.db = db
        self.email = email_service
        self.logger = logger

    def process(self, order):
        total = self.calculate_total(order)
        self.db.save(order)
        self.email.send(order)
        self.logger.log(f"Processed {order.id}")
```

**Benefits:**
- Components are focused
- Easier to test
- Easier to change

### 2. Dependency Inversion

Depend on abstractions, not concretions:

**Bad:**
```python
class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # Hard dependency

    def get_user(self, id):
        return self.db.query(f"SELECT * FROM users WHERE id = {id}")
```

**Good:**
```python
class UserService:
    def __init__(self, db):  # Depends on interface
        self.db = db

    def get_user(self, id):
        return self.db.get_user(id)
```

**Benefits:**
- Can swap implementations
- Easier to test (use mock DB)
- More flexible

### 3. Single Responsibility

Each component should have one reason to change:

**Bad:**
```python
class User:
    def save(self):  # Persistence concern
        db.save(self)

    def send_email(self):  # Notification concern
        email_service.send(self)

    def validate(self):  # Validation concern
        if not self.email:
            raise ValueError()
```

**Good:**
```python
class User:
    def validate(self):
        if not self.email:
            raise ValueError()

class UserRepository:
    def save(self, user):
        db.save(user)

class NotificationService:
    def send(self, user):
        email_service.send(user)
```

## Architectural Patterns

### Layered Architecture

```
┌─────────────────────────────────┐
│   Presentation Layer           │  UI/API
├─────────────────────────────────┤
│   Business Logic Layer         │  Core logic
├─────────────────────────────────┤
│   Data Access Layer           │  Database
└─────────────────────────────────┘
```

**Rules:**
- Presentation doesn't access database directly
- Business logic doesn't depend on UI
- Each layer only depends on layer below

### Microservices

```
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Service │  │ Service │  │ Service │
│    A    │  │    B    │  │    C    │
└────┬────┘  └────┬────┘  └────┬────┘
     │             │             │
     └─────────────┴─────────────┘
              API Gateway
```

**Benefits:**
- Independent deployments
- Technology diversity
- Scalability per service

**Challenges:**
- Increased complexity
- Network communication
- Data consistency

### Event-Driven Architecture

```
Producer → Event Bus → Consumer
   ↓                        ↓
OrderCreated          UpdateInventory
                    SendEmail
                    UpdateAnalytics
```

**Benefits:**
- Decoupled components
- Asynchronous processing
- Easy to extend

**Challenges:**
- Event ordering
- Error handling
- Debugging complexity

## When to Think About Architecture

### Good Times

- Starting a new project
- Adding major features
- Experiencing performance issues
- System becoming hard to modify

### Bad Times

- Micro-optimizing
- During bug fixes
- For small, temporary code

**Rule:** Architecture matters for systems that will grow and change.

## Common Architectural Mistakes

### 1. Premature Optimization

**Bad:** Designing for millions of users when you have 10
**Good:** Design for what you need now, make it flexible

**Why:** Complexity for complexity's sake.

### 2. Over-Engineering

**Bad:** Microservices for a simple CRUD app
**Good:** Monolith for a simple app, evolve when needed

**Why:** Microservices add complexity, they don't simplify.

### 3. Tight Coupling

**Bad:** Every component knows about every other component
**Good:** Components interact through well-defined interfaces

**Why:** Tight coupling makes changes ripple everywhere.

## Integration

Architecture connects to:
- [[clean-code]] — Good architecture makes clean code easier
- [[refactoring]] — Architecture guides refactoring decisions
- [[testing]] — Good architecture is easier to test
- [[documentation]] — Architecture needs to be documented

## Quick Reference

| Pattern | Best For | Trade-offs |
|---------|-----------|-------------|
| Layered | Simple apps | Easy to understand, can become rigid |
| Microservices | Large, complex systems | Scalable, complex |
| Event-Driven | Async processing | Decoupled, hard to debug |

## Architecture Decisions

### Record Your Decisions

Use Architecture Decision Records (ADRs):

```markdown
# ADR-001: Use PostgreSQL for Database

## Status
Accepted

## Context
We need a database for our application.

## Decision
Use PostgreSQL.

## Consequences
- Positive: Mature, well-supported
- Positive: Advanced features (JSON, etc.)
- Negative: Vertical scaling limited
```

**Benefits:**
- Documents why decisions were made
- Helps future understanding
- Considers trade-offs

## Scalability

### Vertical Scaling

Add more resources to single server:
- Faster CPU
- More RAM
- Better storage

**Pros:** Simpler, no code changes
**Cons:** Limited by single machine

### Horizontal Scaling

Add more servers:
- Load balancer
- Multiple instances
- Distributed systems

**Pros:** Unlimited scaling
**Cons:** More complex, needs design

## When to Simplify

If architecture is causing more problems than it solves:

- Can't understand your own code
- Every change breaks multiple components
- Team velocity is slow
- [[debugging]] is painful

Then simplify. Complexity for complexity's sake is anti-pattern.

## Wisdom

> "Premature optimization is the root of all evil." — Donald Knuth

Build what you need.
Make it flexible.
Don't over-engineer.

Architecture enables development.
It shouldn't hinder it.

## Common Heuristics

- **KISS:** Keep It Simple, Stupid
- **YAGNI:** You Aren't Gonna Need It
- **DRY:** Don't Repeat Yourself
- **SOLID:** Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion

Apply these principles consistently.
