---
name: remember
description: Mine session learnings. Captures what was learned, decided, or discovered during a session and creates atomic notes from session state.
---

# Remember — Capture Session Learnings

Extract insights from the current session.

## Usage

```
/remember
/remember --auto
/remember --prompt
```

## What It Does

Remember captures session-level insights:

1. **Identifies learnings** — What did you learn or discover?
2. **Extracts decisions** — What did you decide?
3. **Notes questions** — What remains open?
4. **Creates notes** — Atomic notes from session content
5. **Updates MOCs** — Maintains navigation

## Process

### Session Review

```
REMEMBERING SESSION: 2024-01-15

Scanning session for learnings...

Found:
- 3 decisions made
- 5 patterns discussed
- 2 trade-offs identified
- 4 questions raised

Extract into notes?
```

### Extraction

```
EXTRACTING LEARNINGS:

1. Decision: Use event sourcing for audit trail
   Context: Discussion about payment system
   Create note? [Y/n]
   > Y
   → Created: notes/decisions/event-sourcing-audit.md

2. Pattern: Saga pattern for distributed transactions
   Context: Microservices discussion
   Create note? [Y/n]
   > Y
   → Created: notes/patterns/saga-distributed.md

3. Trade-off: Consistency vs availability
   Context: CAP theorem application
   Create note? [Y/n]
   > Y
   → Created: notes/trade-offs/consistency-availability.md

4. Question: How to handle saga compensation?
   Context: Open question from discussion
   Create note? [Y/n]
   > Y
   → Created: notes/questions/saga-compensation.md

4 notes created from session.
```

### Session Summary

```markdown
# Session 2024-01-15

## Learnings
- Event sourcing provides complete audit trail
- Saga pattern enables distributed transactions
- CAP theorem applies to payment system design

## Decisions
- Use event sourcing for payment system
- Implement saga pattern for transactions

## Questions
- How to handle saga compensation failures?

## Notes Created
- [[Event Sourcing for Audit]]
- [[Saga Pattern for Distributed Transactions]]
- [[Consistency vs Availability Trade-off]]
- [[Saga Compensation Question]]

## Follow-up
- Research saga compensation strategies
- Evaluate event sourcing frameworks
```

## Modes

### Interactive

```
/remember
```

Review and confirm each extraction.

### Auto

```
/remember --auto
```

Automatically extract and create notes without confirmation.

```
Auto-remembering session...

Created 4 notes:
- notes/decisions/event-sourcing-audit.md
- notes/patterns/saga-distributed.md
- notes/trade-offs/consistency-availability.md
- notes/questions/saga-compensation.md

Updated MOCs:
- decisions.md: +1
- patterns.md: +1
- trade-offs.md: +1
```

### Prompted

```
/remember --prompt
```

Prompt for specific learnings:

```
What did you learn this session?
> Event sourcing provides complete audit trail for payments

Any decisions made?
> Yes, we decided to use event sourcing for the payment system

Any open questions?
> How to handle saga compensation failures

Creating notes from your input...
```

## Extraction Categories

| Category | Triggers |
|----------|----------|
| Decision | "decided", "chose", "will use", "went with" |
| Pattern | "pattern", "approach", "method", "technique" |
| Trade-off | "trade-off", "versus", "vs", "but", "however" |
| Question | "question", "wonder", "how do we", "what if" |
| Learning | "learned", "discovered", "realized", "found that" |
| Insight | "insight", "aha", "interesting", "key point" |

## Session Capture Hook

Remember integrates with the session capture hook:

```
SESSION CAPTURE HOOK

On session stop, automatically:
1. Scan for unlearned content
2. Prompt: "Session ending. Run /remember?"
3. If yes, extract learnings
4. Save session summary to ops/sessions/
```

## Integration with Pipeline

Remember is often the **Record** phase:

```
[Remember] → Reduce → Reflect → Reweave → Verify → Rethink
     ↑
  YOU ARE HERE
```

But it can also run standalone:

- End of session: capture what was learned
- Before closing: don't lose insights
- After discovery: solidify new knowledge

## Session Files

Sessions are saved to `ops/sessions/`:

```markdown
# ops/sessions/2024-01-15-payment-design.md

## Summary
Discussed payment system architecture decisions.

## Duration
45 minutes

## Learnings Extracted
- [[Event Sourcing for Audit]]
- [[Saga Pattern for Distributed Transactions]]
- [[Consistency vs Availability Trade-off]]

## Open Questions
- [[Saga Compensation Question]]

## Participants
- Primary user

## Follow-up Actions
- Research saga compensation
- Evaluate event sourcing frameworks
```

## When to Use

- End of a work session
- After making decisions
- When you've learned something new
- Before closing the vault
- Periodically during long sessions

## Automatic Reminders

```
SESSION DURATION: 2 hours

You've been working for a while.
Run /remember to capture session learnings?

[Y/now/later]
```

## Research Grounding

```
REMEMBER derives from:

- COR-001: Record — capture during experience
- COR-004: Reflect — connect to prior knowledge
- AGT-002: Session boundaries — each session is finite
- EVE-001: Evergreen notes — written for future self

Without session capture, insights fade.
With remember, the knowledge graph grows from every session.
```