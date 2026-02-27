---
name: verify
description: Combined quality check — schema compliance, link integrity, note health. Phase 5 of the processing pipeline. Ensures knowledge graph quality.
---

# Verify — Quality Check

Ensure your vault meets quality standards.

## Usage

```
/verify [note]
/verify --all
/verify --schema
/verify --links
/verify --health
```

## What It Does

Verify runs comprehensive quality checks:

1. **Schema compliance** — Notes follow their declared schemas
2. **Link integrity** — Wiki links point to existing notes
3. **Note health** — Content quality, completeness, freshness
4. **MOC health** — Navigation structure is current

## Checks

### Schema Compliance

```markdown
SCHEMA CHECK

notes/decisions/data-ownership.md:
✓ _schema: decision (valid)
✓ _status: exploring (valid enum)
✓ Summary: present
✓ Context: present
✓ Connections: 3 links
✓ Questions: 1 item
✓ All required fields present

notes/patterns/saga.md:
✓ _schema: pattern
⚠ _status: missing (default: candidate)
✓ Summary: present
⚠ Context: missing
✓ Related: 2 links

notes/inbox/capture-001.md:
⚠ No _schema declared
⚠ No structure detected
→ Consider running /reduce first
```

### Link Integrity

```markdown
LINK CHECK

Total wiki links: 156
Internal links: 142
External links: 14

Broken links: 2
1. notes/decisions/api-gateway.md
   [[Service Discovery]] → Note not found
   Suggestions: [[Service Discovery Pattern]], [[DNS-based Discovery]]
   
2. MOCs/decisions.md
   [[old-decision-001]] → Note moved to archive/
   Fix: Update to [[archive/old-decision-001]]

Fix broken links? [all/select/skip]
```

### Note Health

```markdown
HEALTH CHECK

Checking note quality...

Stale notes (>30 days without update): 12
1. notes/decisions/tech-stack.md — 45 days old
   → Consider review: is this still accurate?
2. notes/patterns/repository.md — 38 days old
   → Still relevant?

Empty notes: 3
1. notes/inbox/capture-002.md — empty
   → Delete or process
2. notes/decisions/placeholder.md — placeholder only
   → Remove or complete

Orphan notes: 8
→ Run /reflect --orphans to link

Low-connectivity notes (<2 links): 15
→ Run /reflect to improve connectivity
```

### MOC Health

```markdown
MOC CHECK

hub.md:
✓ 15 entries
✓ Last updated: 2 days ago
✓ All links valid

decisions.md:
✓ 12 entries
⚠ Last updated: 15 days ago
→ Consider refresh: /reflect --mocs
✓ All links valid

patterns.md:
✓ 8 entries
✓ Last updated: 5 days ago
⚠ 2 entries have no summary
→ Add summaries for better navigation

trade-offs.md:
⚠ 3 entries (sparse)
→ Consider merging with decisions.md
✓ All links valid
```

## Modes

### Single Note

```
/verify notes/decisions/data-ownership.md
```

Verify one note.

### All Notes

```
/verify --all
```

Verify entire vault.

```
Running verification on 347 notes...

Schema: 341 passed, 6 issues
Links: 344 passed, 3 broken
Health: 331 passed, 16 issues
MOCs: 4 passed, 1 stale

VERIFICATION COMPLETE
341/347 notes fully compliant
6 notes need attention

Run /verify --issues for details.
```

### Schema Only

```
/verify --schema
```

Check only schema compliance.

### Links Only

```
/verify --links
```

Check only wiki link integrity.

### Health Only

```
/verify --health
```

Check only note health (staleness, emptiness, connectivity).

## Auto-Fix

```
/verify --fix
```

Attempt automatic fixes:

```markdown
AUTO-FIX RESULTS:

Schema fixes:
✓ Added missing _status to 3 notes
✓ Added default _schema to 2 notes

Link fixes:
✓ Fixed 1 moved note reference
⚠ 1 broken link needs manual fix:
  [[Service Discovery]] — no clear target

Health:
✓ Removed 2 empty notes
⚠ 3 stale notes flagged for review

Auto-fix complete. 8 issues resolved, 2 need manual attention.
```

## Report

```
/verify --report
```

Generate detailed report:

```markdown
# Vault Verification Report
Generated: 2024-01-15 14:30

## Summary
- Total notes: 347
- Compliant: 341 (98%)
- Issues: 6 (2%)

## Issues by Type
| Type | Count | Severity |
|------|-------|----------|
| Schema missing | 2 | Medium |
| Schema incomplete | 4 | Low |
| Broken links | 3 | High |
| Stale notes | 12 | Low |
| Empty notes | 3 | Medium |
| Orphan notes | 8 | Medium |

## Priority Fixes
1. [HIGH] Fix broken links (3)
2. [MEDIUM] Process empty notes (3)
3. [MEDIUM] Link orphan notes (8)
4. [LOW] Review stale notes (12)

## Trends
- Compliance rate: 98% (↑ from 95% last week)
- Average links per note: 2.7 (↑ from 2.4)
- Schema adoption: 99% (↑ from 97%)
```

## When to Use

- After running `/reweave`
- Before ending a work session
- Weekly as part of regular maintenance
- When something feels wrong
- Before `/rethink`

## Workflow

```
Capture → Record → Reduce → Reflect → Reweave → [Verify] → Rethink
                                                ↑
                                            YOU ARE HERE
```