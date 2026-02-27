---
name: reduce
description: Extract insights from sources. Phase 2 of the processing pipeline. Takes inbox items and distills them into atomic notes with proper categorization.
---

# Reduce — Extract Insights

Distill raw captures into atomic, well-categorized notes.

## Usage

```
/reduce [source]
/reduce notes/inbox/article-capture.md
/reduce --all-inbox
/reduce --from-url "https://..."
```

## What It Does

Reduce takes raw captured content and:

1. **Extracts key ideas** — Identifies atomic concepts
2. **Creates categorization** — Assigns domain-specific categories
3. **Links to existing notes** — Finds connections
4. **Ensures atomicity** — Splits if necessary
5. **Adds to MOCs** — Updates navigation

## Process

### Input: Raw Capture

```markdown
# Random thoughts on microservices

Read that article about breaking monoliths. They said 
each service should own its data. Makes sense but then
how do you do joins? Maybe CQRS? Also mentioned saga 
pattern for transactions. Need to think about how this
applies to our payment system.

Also saw something about service mesh - istio? linkerd?
Seems like a lot of complexity but maybe worth it for
observability.
```

### Output: Atomic Notes

**notes/decisions/data-ownership.md**:
```markdown
---
_schema: decision
_status: exploring
_context: microservices architecture
---

# Each Service Owns Its Data

## Summary
In microservices architecture, each service should 
own and manage its own data, with no direct database 
sharing.

## Context
Breaking down a monolith; considering data boundaries.

## Implications
- No cross-service joins
- Need alternative patterns (CQRS, saga)
- Service boundaries become data boundaries

## Questions
- How does this affect our payment system?

## Connections
- [[CQRS Pattern]]
- [[Saga Pattern for Transactions]]
- [[Microservices Trade-offs]]
```

**notes/patterns/cqrs.md**:
```markdown
---
_schema: pattern
_status: candidate
---

# CQRS (Command Query Responsibility Segregation)

## Summary
Separate read and write models for complex domains.

## Context
Useful when read and write patterns differ significantly.

## Related
- [[Data Ownership]]
- [[Saga Pattern]]
```

## Domain-Specific Extraction

Reduce adapts to your domain vocabulary:

| Domain | Extraction Categories |
|--------|----------------------|
| Research | Claims, Evidence, Methods, Questions |
| Software Architecture | Decisions, Patterns, Trade-offs, Principles |
| Personal | Reflections, Learnings, Intentions, Gratitude |
| Business | Insights, Actions, Metrics, Risks |
| Writing | Ideas, Quotes, Threads, Drafts |

## Modes

### Single Item

```
/reduce notes/inbox/capture-2024-01-15.md
```

Process one inbox item.

### All Inbox

```
/reduce --all-inbox
```

Process all pending inbox items. Shows progress:

```
Processing inbox/ (5 items):
✓ capture-001.md → 2 notes created
✓ capture-002.md → 1 note created
✓ capture-003.md → skipped (empty)
✓ capture-004.md → 3 notes created
✓ capture-005.md → needs review (unclear)

4 processed, 6 notes created, 1 needs review.
```

### From URL

```
/reduce --from-url "https://blog.example.com/article"
```

Fetches content, creates inbox item, then reduces.

### Interactive Mode

```
/reduce --interactive notes/inbox/capture.md
```

Asks for confirmation on each extraction:

```
Extracting: "Each service should own its data"

Category: Decision [D] / Pattern [P] / Trade-off [T]
> D

Title: "Each Service Owns Its Data" [enter to confirm]
> Data Ownership in Microservices

Create as atomic note? [Y/n]
> Y

Add connection to existing note? [[microservices-overview]]
> Y

Proceed? [Y/n]
```

## Schema Enforcement

Reduce ensures schema compliance:

```
Schema check for notes/decisions/data-ownership.md:
✓ _schema: decision
✓ _status: exploring
✓ Summary present
⚠ Context missing → added from extraction

Note created with full schema compliance.
```

## Connection Detection

```
Analyzing connections...
Found 3 potential links:
1. [[Microservices Overview]] (shared context)
2. [[Database Architecture]] (related concept)
3. [[Payment System Design]] (mentioned)

Add all? [Y/n/select]
```

## Queue Integration

Reduce updates the processing queue:

```
Queue updated:
- notes/inbox/capture.md → PROCESSING → COMPLETE
- Created: notes/decisions/data-ownership.md (PENDING reflect)
- Created: notes/patterns/cqrs.md (PENDING reflect)
```

## When to Use

- After capturing to inbox
- When inbox has accumulated items
- Before running `/reflect`
- Weekly as part of regular processing

## Workflow

```
Capture → Record → [Reduce] → Reflect → Reweave → Verify
                      ↑
                   YOU ARE HERE
```