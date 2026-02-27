---
name: reflect
description: Find connections and update MOCs. Phase 3 of the processing pipeline. Analyzes notes, discovers relationships, and maintains navigation.
---

# Reflect — Find Connections

Discover relationships and update Maps of Content.

## Usage

```
/reflect [note]
/reflect --recent
/reflect --mocs
/reflect --orphans
```

## What It Does

Reflect performs the relationship work:

1. **Scans recent notes** — Identifies new content
2. **Finds connections** — Discovers relationships via semantic analysis
3. **Suggests links** — Proposes wiki links between related notes
4. **Updates MOCs** — Maintains navigation hubs
5. **Detects orphans** — Finds notes without incoming links

## Process

### Connection Discovery

```
Analyzing notes/decisions/data-ownership.md...

Text: "Each service should own its data"
Keywords: service, data, ownership, microservices

Semantic search found 4 related notes:
1. notes/decisions/api-gateway.md (similarity: 0.87)
   - Both discuss service isolation
   - Suggestion: [[Data Ownership]] ↔ [[API Gateway Pattern]]

2. notes/patterns/database-per-service.md (similarity: 0.82)
   - Same concept, different framing
   - Suggestion: Merge or link?

3. notes/trade-offs/distributed-transactions.md (similarity: 0.71)
   - Contrasting approach
   - Suggestion: Link as trade-off

4. notes/learnings/monolith-breakdown.md (similarity: 0.65)
   - Related experience
   - Suggestion: Link as supporting context

Add suggested links? [all/select/skip]
```

### MOC Updates

```
Updating MOCs...

MOC: decisions.md
+ [[Data Ownership]] — Services own their data
+ [[API Gateway Pattern]] — Entry point for services
  
MOC: patterns.md
+ [[CQRS]] — Separate read/write models
+ [[Saga Pattern]] — Distributed transactions

MOC: trade-offs.md
(no new entries — existing notes linked)

3 MOCs updated with 4 new entries.
```

### Orphan Detection

```
Scanning for orphans (notes with no incoming links)...

Found 8 orphans:
1. notes/patterns/saga.md
   - Created 2 days ago
   - Suggest linking from: [[Data Ownership]], [[Distributed Transactions]]
   
2. notes/learnings/postmortem-001.md
   - Created 5 days ago
   - Suggest linking from: [[Incidents]], [[Lessons Learned]]

... (6 more)

Link orphans? [all/select/skip]
```

## Modes

### Single Note

```
/reflect notes/decisions/data-ownership.md
```

Reflect on one specific note.

### Recent Notes

```
/reflect --recent
```

Reflect on notes created in the last N days.

```
Reflecting on 12 notes from the last 7 days...

Connections found: 23
MOCs updated: 3
Orphans linked: 2
```

### MOC-Only

```
/reflect --mocs
```

Update MOCs without scanning for connections. Fast refresh.

```
Refreshing MOCs...

hub.md: ✓ 15 entries, last updated 2 days ago
decisions.md: +2 entries, updated
patterns.md: ✓ 8 entries, no changes
trade-offs.md: ✓ 5 entries, no changes

MOC refresh complete.
```

### Orphans Only

```
/reflect --orphans
```

Focus on finding and linking orphan notes.

## MOC Maintenance

Reflect maintains MOC structure:

### Hub MOC

```
# Decisions Hub

> Architecture decisions and their reasoning

## Recent
- [[Data Ownership]] — Services own their data
- [[API Gateway Pattern]] — Entry point for services

## Active Topics
- [[Microservices Architecture]] (5 decisions)
- [[Data Architecture]] (3 decisions)
- [[API Design]] (2 decisions)

## Related MOCs
- [[Patterns MOC]]
- [[Trade-offs MOC]]
```

### Topic MOCs

```
# Microservices Architecture

> Decisions and patterns related to microservices

## Decisions
- [[Data Ownership]]
- [[API Gateway Pattern]]
- [[Service Discovery]]

## Patterns
- [[CQRS]]
- [[Saga Pattern]]

## Trade-offs
- [[Distributed Transactions]]
- [[Service Mesh Complexity]]

## Related
- [[Monolith Breakdown]]
```

## Connection Types

Reflect recognizes different relationship types:

| Type | Marker | Description |
|------|--------|-------------|
| Supports | `→` | This note supports that one |
| Contrasts | `↔` | These notes contrast |
| Extends | `+` | This note extends that one |
| Questions | `?` | This note questions that one |
| Example | `ex:` | This is an example of that |

```markdown
## Connections
- → [[API Gateway Pattern]] (supports service isolation)
- ↔ [[Distributed Transactions]] (trade-off)
- ? [[Database Sharing]] (challenges this approach)
- ex: [[Payment System Data Model]] (example)
```

## Semantic Search Integration

When Agent Memory System is available:

```
Using semantic search for connection discovery...
Agent Memory System: ✓ Connected

Found connections beyond keyword matching:
- "service isolation" semantically similar to "bounded context"
- [[Bounded Context]] — related pattern from DDD
```

## When to Use

- After running `/reduce`
- When MOCs feel outdated
- Weekly as part of regular maintenance
- Before running `/reweave`

## Workflow

```
Capture → Record → Reduce → [Reflect] → Reweave → Verify
                              ↑
                          YOU ARE HERE
```