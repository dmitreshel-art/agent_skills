---
name: arscontexta:architect
description: Research-backed evolution guidance. Analyzes your vault usage patterns and recommends architectural changes based on Tools for Thought research.
---

# Architect — Evolution Guidance

Get research-backed recommendations for evolving your knowledge system.

## Usage

```
/arscontexta:architect
/arscontexta:architect --analyze
/arscontexta:architect --recommend
```

## What It Does

Architect analyzes your vault and provides guidance on:

1. **Structure evolution** — Should your hierarchy deepen or flatten?
2. **Processing tuning** — Is your pipeline too heavy or light?
3. **Navigation gaps** — Are MOCs serving their purpose?
4. **Automation calibration** — Are hooks helping or hindering?

## Analysis Report

```
═══════════════════════════════════════════
ARCHITECT ANALYSIS
═══════════════════════════════════════════

VAULT STATISTICS:
- Notes: 347
- Links: 892 (2.6 links/note average)
- MOCs: 5
- Orphans: 12 (3.5%)
- Avg note age: 23 days
- Inactivity: 5 days since last note

DIMENSION ANALYSIS:

Atomicity: HIGH
✓ Most notes are atomic
⚠ Some notes exceed ideal length (see below)
Recommendation: Split long notes with /reduce

Connectivity: MEDIUM
✓ Link density acceptable
⚠ 12 orphans detected
Recommendation: Link orphans in next /reflect session

Structure: MEDIUM
✓ Hierarchy appropriate for current size
⚠ Some MOCs are sparse (see below)
Recommendation: Consolidate sparse MOCs or add content

Temporal: LOW
⚠ Few notes track version/state
Recommendation: Add _updated fields to tracked decisions

Processing: FIT FOR PURPOSE
✓ Pipeline depth matches domain needs
✓ Queue processing consistent

Automation: MEDIUM
✓ Hooks active
⚠ Some manual patterns detected
Recommendation: Consider automation for repeated tasks

Navigation: DEVELOPING
✓ Hub MOC well-populated
⚠ Topic MOCs need expansion
Recommendation: Run /reflect to identify MOC candidates

USAGE PATTERNS:

High-frequency paths:
- decisions/ → MOCs/decisions.md (47 traversals)
- patterns/ → trade-offs/ (32 traversals)
- inbox/ → decisions/ (processing path)

Underutilized:
- trade-offs/ (3 notes, low connectivity)
- ops/sessions/ (not accessed in 14 days)

DRIFT INDICATORS:

⚠ 5 notes with outdated schemas
⚠ 3 broken wiki links
⚠ MOCs/topics/architecture.md last updated 12 days ago

RECOMMENDATIONS:

1. IMMEDIATE (5 min):
   - Fix 3 broken links: /arscontexta:health --fix
   - Process inbox items: /reduce

2. SHORT-TERM (this week):
   - Run /reflect to update MOCs
   - Link 12 orphans
   - Update 5 outdated schema notes

3. ARCHITECTURAL (this month):
   - Consider merging sparse MOCs
   - Add version tracking to decisions
   - Expand trade-offs/ or deprecate

4. EVOLUTION (quarterly):
   - Review dimension calibration
   - Consider /arscontexta:reseed if drift persists
```

## Research-Backed Recommendations

Each recommendation links to research:

```
RECOMMENDATION: Split long notes with /reduce

Research grounding:
- COG-005: Working memory limit (4±1 chunks)
- EVE-001: Evergreen notes written for future self
- ZET-001: Atomic notes enable recombination

When notes exceed ~500 words, they become:
- Harder to link (what does this note connect to?)
- Harder to find (what's in this note?)
- Harder to maintain (which part changed?)

Action: Run /reduce on long notes to extract atomic concepts.
```

## Dimension Recalibration

If usage patterns suggest wrong calibration:

```
DIMENSION RECALIBRATION SUGGESTED:

Structure: MEDIUM → HIGH

Your vault has grown beyond 300 notes. Deeper hierarchy
may improve navigation.

Research grounding:
- NET-001: Small-world topology
- MOC-001: Hub structure reduces search time

Actions:
1. Create sub-MOCs for high-activity domains
2. Add topic-level MOCs under domain MOCs
3. Run /reflect to identify natural clusters

Proceed with recalibration? [y/n/skip]
```

## Periodic Review

Architect should be run:

- **Weekly**: Quick health check
- **Monthly**: Full analysis
- **Quarterly**: Architectural review

Or when you notice:
- Difficulty finding notes
- Processing feels slow
- MOCs feel outdated
- Not using the system

## Commands

```
/arscontexta:architect
```
Full analysis with recommendations.

```
/arscontexta:architect --analyze
```
Analysis only, no recommendations.

```
/architect:architect --recommend
```
Recommendations only (uses cached analysis).

```
/arscontexta:architect --dimension [name]
```
Deep dive on specific dimension:

- `--dimension atomicity`
- `--dimension connectivity`
- `--dimension structure`
- `--dimension temporal`
- `--dimension processing`
- `--dimension automation`
- `--dimension navigation`
- `--dimension domain`

## Example Output

```
/arscontexta:architect --dimension connectivity

CONNECTIVITY ANALYSIS

Current state: MEDIUM (2.6 links/note)

Optimal range: 2-4 links/note
Your position: ✓ Within range

Distribution:
- 0 links: 12 notes (orphans)
- 1 link: 34 notes
- 2 links: 89 notes
- 3 links: 156 notes
- 4 links: 48 notes
- 5+ links: 8 notes (hub candidates)

Research context:
- COG-002: Spreading activation (linked concepts prime each other)
- ZET-002: Connection over categorization
- EVE-003: Dense linking

Recommendations:
1. The 12 orphans need links — run /reflect to find homes
2. The 8 high-link notes are hub candidates — consider MOC membership
3. Current link density is healthy — maintain current practices

No recalibration needed.
```