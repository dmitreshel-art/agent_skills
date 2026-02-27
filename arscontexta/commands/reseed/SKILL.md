---
name: arscontexta:reseed
description: Re-derive your knowledge system from first principles. Use when drift accumulates, needs change, or you want to refresh the foundational architecture.
---

# Reseed — Re-derive from First Principles

Rebuild your knowledge system architecture while preserving your notes.

## Usage

```
/arscontexta:reseed
```

## When to Reseed

Reseed when:

1. **Drift accumulation** — Your system has drifted from its purpose
2. **Domain shift** — Your work focus has changed significantly
3. **Scale changes** — Vault grew beyond original structure design
4. **Frustration** — The system feels wrong, not helpful
5. **Staleness** — Haven't used the system in months

Signs of drift:
- Can't find notes that should be there
- MOCs don't reflect current mental model
- Processing feels like chores, not flow
- Structure fights your thinking

## The Reseed Process

### Phase 1: Backup

Create timestamped backup:

```
Creating backup...
✓ Vault backed up to .ars-backups/2024-01-15-reseed/
  - All notes preserved
  - MOCs preserved
  - ops/ preserved
  - Configuration saved
```

### Phase 2: Preserve

Identify what to keep:

```
Preserving:
✓ All notes in [notes-space]/
✓ Session history in ops/sessions/
✓ Processing queue

Will regenerate:
- self/ (identity, methodology, goals)
- MOCs/ (navigation structure)
- templates/ (schemas may update)
- hooks.json
```

### Phase 3: Re-interview

Run abbreviated setup conversation:

```
RESEED INTERVIEW

Current configuration:
- Domain: software-architecture
- Atomicity: HIGH
- Connectivity: HIGH
- Structure: MEDIUM
- Processing: MEDIUM
- Automation: HEAVY

1. Has your domain or focus changed?
   [Current: software architecture with decision focus]
   
   You: I've shifted more toward system design and documentation.
        Less about individual decisions, more about holistic patterns.

2. How has your note-taking evolved?
   
   You: I'm more narrative now. I write longer notes that tell stories.
        The atomic style felt too fragmented.

3. What's working? What's not?
   
   You: MOCs are great. But I have too many templates I never use.
        And the hooks feel intrusive.

4. Any new challenges?
   
   You: I want to track design evolution over time better.
        Version history matters more now.
```

### Phase 4: Re-derive

Map new signals to dimensions:

```
NEW DERIVATION:

Changes detected:
- Atomicity: HIGH → MEDIUM (narrative preference)
- Temporal: MEDIUM → HIGH (version tracking need)
- Automation: HEAVY → MEDIUM (reduce intrusiveness)
- Domain: "software-architecture" → "system-design-documentation"

Unchanged:
- Connectivity: HIGH (still need relationships)
- Structure: MEDIUM (hierarchy appropriate)
- Processing: MEDIUM (pipeline depth good)
- Navigation: BOTH (search + browse + links)
```

### Phase 5: Propose

Show changes:

```
PROPOSED CHANGES:

Space Structure:
- Rename "decisions/" → "designs/" (broader scope)
- Add "evolution/" for version tracking
- Simplify templates (12 → 4)

MOCs:
- Rename MOCs/decisions.md → MOCs/designs.md
- Add MOCs/evolution.md for version history
- Consolidate sparse MOCs

Hooks:
- Reduce validation intensity
- Remove auto-commit (manual preferred)
- Keep session capture

Templates:
- Remove unused templates (6 decision variants → 1 flexible design template)
- Add evolution-tracking fields
- Add narrative-friendly schema

Your notes will be preserved. MOCs will be regenerated.
Proceed? [y/n/diff]
```

### Phase 6: Regenerate

Apply changes:

```
REGENERATING...

✓ self/ regenerated with new identity
✓ MOCs regenerated (4 → 3, consolidated)
✓ templates simplified (12 → 4)
✓ hooks.json updated
✓ AGENTS.md updated

Preserved:
✓ All 347 notes in designs/ (renamed from decisions/)
✓ ops/sessions history (23 sessions)
✓ queue state (3 pending)

Migration:
✓ Renamed decisions/ → designs/
✓ Updated wiki links in 156 notes
✓ Added evolution/ folder
✓ Created evolution MOC

Backup saved to: .ars-backups/2024-01-15-reseed/

Reseed complete. Restart OpenClaw to activate new hooks.
```

## Rollback

If something goes wrong:

```
/arscontexta:reseed --rollback [timestamp]
```

Rollback restores from backup:

```
Rolling back to 2024-01-15-reseed...

✓ Restored self/
✓ Restored MOCs/
✓ Restored templates/
✓ Restored hooks.json
✓ Reverted designs/ → decisions/

Rollback complete.
```

## Partial Reseed

Reseed specific aspects:

```
/arscontexta:reseed --mocs-only
```
Regenerate MOCs only, keep everything else.

```
/arscontexta:reseed --hooks-only
```
Reconfigure hooks only.

```
/arscontexta:reseed --templates-only
```
Regenerate templates only.

```
/arscontexta:reseed --identity-only
```
Refresh self/ only (identity, methodology, goals).

## Reseed vs Add-Domain

| Scenario | Command |
|----------|---------|
| Needs fundamentally changed | `/arscontexta:reseed` |
| Adding new domain alongside | `/arscontexta:add-domain` |
| Small tweaks to structure | `/arscontexta:architect` |
| Just updating MOCs | `/reflect` |

## Frequency

- **Too often** (weekly): You're not giving the system a chance to work
- **Healthy** (quarterly/biannually): Reflecting changed needs
- **Never** (years): Possible drift accumulation

Consider reseeding when:
- Your work has changed significantly
- The system feels wrong
- You've stopped using it actively