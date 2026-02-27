---
name: arscontexta:health
description: Run diagnostic checks on your vault. Verifies directory structure, MOCs, hooks, schemas, and kernel primitives. Reports issues and suggests fixes.
---

# Health — Vault Diagnostics

Check the health of your knowledge system.

## Usage

```
/arscontexta:health
```

## What It Checks

### 1. Directory Structure

Verifies three-space architecture:

```
✓ self/ exists
✓ self/identity.md exists
✓ self/methodology.md exists
✓ self/goals.md exists
✓ [notes-space]/ exists
✓ [notes-space]/inbox/ exists
✓ MOCs/ exists
✓ ops/ exists
✓ ops/queue/ exists
```

### 2. MOC Integrity

Checks Maps of Content:

```
MOC Status:
✓ hub.md — 12 links, last updated 2 days ago
✓ topics/ — 3 MOCs
⚠ domain.md — empty (no links yet)
```

### 3. Hooks Status

Verifies hook configuration:

```
Hooks:
✓ Session orientation — configured
✓ Write validation — configured
✓ Auto-commit — configured
✓ Session capture — configured
```

### 4. Schema Compliance

Checks notes against their declared schemas:

```
Schema Check (notes/):
✓ 45 notes compliant
⚠ 3 notes missing required fields:
  - notes/decisions/001.md: missing "decision" field
  - notes/decisions/002.md: missing "status" field
  - notes/patterns/observer.md: missing "_schema" declaration
```

### 5. Link Health

Checks for broken wiki links:

```
Link Health:
✓ 156 internal links
⚠ 2 broken links:
  - notes/decisions/005.md links to [[non-existent-note]]
  - MOCs/hub.md links to [[old-decision]] (moved to superseded/)
```

### 6. Orphan Detection

Finds notes with no incoming links:

```
Orphans (no incoming links):
⚠ 8 orphan notes:
  - notes/inbox/capture-2024-01-10.md
  - notes/inbox/capture-2024-01-12.md
  - notes/patterns/factory-variant.md
  ... (5 more)
  
Suggestion: Process inbox items or link orphans to MOCs
```

### 7. Kernel Primitives

Verifies all 15 kernel primitives:

```
Kernel Primitives:
✓ 1. Three-Space Architecture
✓ 2. Inbox Folder
✓ 3. MOC Hierarchy
✓ 4. Atomic Notes
✓ 5. Description Field
✓ 6. Wiki Links
✓ 7. Schema Blocks
✓ 8. Templates
✓ 9. Pipeline Phases
✓ 10. Fresh Context Per Phase
✓ 11. Queue-Based Orchestration
✓ 12. Session Orientation Hook
✓ 13. Write Validation Hook
✓ 14. Auto-Commit Hook
✓ 15. Session Capture Hook
```

### 8. Processing Queue

Shows queue status:

```
Queue Status:
├── pending: 12 items
├── in-progress: 2 items
├── blocked: 0 items
└── complete: 45 items (this week)

Oldest pending: 5 days (notes/inbox/capture-2024-01-05.md)
```

## Health Report Format

```
═══════════════════════════════════════════
ARS CONTEXTA HEALTH REPORT
Generated: 2024-01-15 14:30
═══════════════════════════════════════════

OVERALL: ⚠ NEEDS ATTENTION

✓ Structure: Healthy (all directories present)
✓ MOCs: Healthy (3 MOCs, 1 empty)
✓ Hooks: Healthy (all 4 configured)
⚠ Schema: 3 notes non-compliant
⚠ Links: 2 broken links
⚠ Orphans: 8 notes with no incoming links
✓ Primitives: All 15 present
⚠ Queue: 12 pending, oldest 5 days

RECOMMENDED ACTIONS:
1. Fix broken links in decisions/005.md and MOCs/hub.md
2. Process 8 inbox items
3. Add schema declarations to 3 non-compliant notes
4. Link orphans to appropriate MOCs

Run /arscontexta:fix to attempt automatic fixes.
```

## Fix Mode

```
/arscontexta:health --fix
```

Attempts automatic fixes:

- Creates missing directories
- Fixes broken links where target is obvious
- Adds default schemas to schemaless notes
- Updates MOC timestamps

## Verbose Mode

```
/arscontexta:health --verbose
```

Shows detailed check output for each category.

## Exit Codes

For scripting:

| Code | Meaning |
|------|---------|
| 0 | All checks passed |
| 1 | Warnings but functional |
| 2 | Critical issues |
| 3 | Not initialized |