---
name: reweave
description: Backward pass — update older notes with new context. Phase 4 of the processing pipeline. Ensures existing notes benefit from new knowledge.
---

# Reweave — Update with New Context

Backward link propagation. Old notes gain new connections.

## Usage

```
/reweave [note]
/reweave --recent
/reweave --target [older-note]
/reweave --bidirectional
```

## What It Does

Reweave performs the backward pass:

1. **Identifies new context** — What did you learn recently?
2. **Scans older notes** — What should be updated?
3. **Propagates connections** — Links new insights to old notes
4. **Updates summaries** — Adds newly relevant context
5. **Maintains consistency** — Ensures knowledge graph integrity

## The Problem It Solves

When you learn something new, it often relates to older notes:

```
Timeline:
├── Day 1: Create [[Database Design]] (decision: use PostgreSQL)
├── Day 15: Create [[Data Ownership]] (pattern: services own data)
├── Day 20: Learn: "Data ownership affects database design"
│
└── Problem: [[Database Design]] doesn't know about [[Data Ownership]]
    Solution: Reweave updates [[Database Design]] with new context
```

## Process

### Forward Analysis

```
Analyzing recent notes (last 7 days)...

New context identified:
1. notes/decisions/data-ownership.md
   - Key concept: "Services own their data"
   - Affected topics: database design, API boundaries, transactions
   
2. notes/patterns/cqrs.md
   - Key concept: "Separate read/write models"
   - Affected topics: data architecture, performance, consistency
```

### Backward Scan

```
Scanning older notes for relevance...

Found 5 older notes that relate to new context:

notes/decisions/database-design.md (15 days old)
- Contains: "PostgreSQL for all services"
- Conflict: Data ownership suggests separate databases
- Action: Add connection, note tension

notes/patterns/api-gateway.md (10 days old)
- Contains: "Gateway routes to services"
- Support: Data ownership reinforces gateway need
- Action: Add backlink

notes/learnings/monolith-lessons.md (30 days old)
- Contains: "Shared database caused coupling"
- Support: Validates data ownership
- Action: Add "see also" connection
```

### Propagation

```
Updating: notes/decisions/database-design.md

Adding context section:
## New Developments (2024-01-20)

The [[Data Ownership]] decision affects this earlier choice.
Consider: Database-per-service pattern?
See also: [[Database per Service Pattern]]

Tension noted: Current decision uses shared database;
New pattern suggests dedicated databases per service.

Update note status? [decision → revisiting]
> Y
```

### Bidirectional Mode

```
/reweave --bidirectional

Creates links in both directions:

notes/decisions/database-design.md
+ ## See Also
+ [[Data Ownership]] — challenges shared database approach

notes/decisions/data-ownership.md
+ ## Related Decisions
+ [[Database Design]] — earlier decision, may need revision

Bidirectional links create stronger knowledge graph.
```

## Modes

### Single Note

```
/reweave notes/decisions/data-ownership.md
```

Reweave from one specific note to older notes.

### Recent Context

```
/reweave --recent
```

Take all notes from last 7 days and reweave them into older notes.

```
Reweaving 8 recent notes into vault...

Notes updated: 12
Connections added: 18
Tensions identified: 2
- [[Database Design]] ↔ [[Data Ownership]]
- [[API Versioning]] ↔ [[Schema Evolution]]
```

### Target Mode

```
/reweave --target notes/decisions/database-design.md
```

Find all new notes that should connect to a specific older note.

```
Scanning for notes that relate to [[Database Design]]...

Found 4 recent notes:
1. [[Data Ownership]] — direct relationship
2. [[CQRS]] — affects read/write separation
3. [[Saga Pattern]] — affects transaction handling
4. [[Service Discovery]] — indirect relationship

Add connections? [all/select/skip]
```

### Bidirectional

```
/reweave --bidirectional
```

Create links in both directions for stronger graph.

## Update Types

### Addition

New information supports old note:

```markdown
## Developments
+ 2024-01-20: [[Data Ownership]] validates this approach
```

### Tension

New information conflicts with old note:

```markdown
## Tensions
+ 2024-01-20: [[Data Ownership]] challenges shared database
  Consider revisiting this decision
```

### Refinement

New information adds nuance:

```markdown
## Refinements
+ 2024-01-20: [[CQRS]] suggests separating read replicas
  Original decision assumed single model
```

### Context

New information provides context:

```markdown
## See Also
+ [[Monolith Lessons]] — why we made this choice
```

## Tension Detection

Reweave identifies when new knowledge contradicts old:

```
TENSION DETECTED:

Old: notes/decisions/database-design.md
  "Use PostgreSQL with shared database for all services"

New: notes/decisions/data-ownership.md
  "Each service owns its data, no shared databases"

These decisions conflict. Options:
1. Add tension note to both
2. Mark older decision as "revisiting"
3. Create new note to track conflict

Action: [tension/revisiting/ignore]
```

## When to Use

- After running `/reflect`
- When learning something that changes perspective
- Before running `/verify`
- Weekly as part of regular processing

## Workflow

```
Capture → Record → Reduce → Reflect → [Reweave] → Verify
                                         ↑
                                     YOU ARE HERE
```

## Research Grounding

```
REWEAVE derives from:

- EVE-004: Iterative refinement (notes evolve over time)
- ZET-002: Connection over categorization
- NET-002: Betweenness centrality (connecting clusters adds value)

Without reweaving, new knowledge stays isolated.
With reweaving, the entire knowledge graph evolves.
```