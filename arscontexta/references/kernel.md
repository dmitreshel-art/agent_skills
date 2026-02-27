# Kernel — 15 Primitives

Every Ars Contexta system includes these 15 kernel primitives. They are non-negotiable — derived from first principles and backed by research claims.

## Space Primitives

### 1. Three-Space Architecture

Three distinct spaces with different growth rates and purposes:

```
self/      → Agent mind (slow growth, tens of files)
notes/     → Knowledge graph (steady growth, 10-50/week)
ops/       → Operations (fluctuating, transient)
```

**Cognitive grounding**: COG-001 (extended mind), AGT-002 (session boundaries)

### 2. Inbox Folder

Zero-friction capture location. All new notes start here.

```
notes/inbox/
```

**Cognitive grounding**: COR-001 (record), PAR-005 (action-orientation)

### 3. MOC Hierarchy

Three-level map structure for navigation:

```
MOCs/
├── Hub MOC      (high-level navigation)
├── Domain MOCs  (domain-specific)
└── Topic MOCs   (topic clusters)
```

**Cognitive grounding**: MOC-001 through MOC-005, COG-004

## Note Primitives

### 4. Atomic Notes

One idea per note. Enables recombination and connection.

**Cognitive grounding**: ZET-001, EVE-003

### 5. Description Field

Every note starts with a one-sentence description. Provides progressive disclosure — scan without reading full note.

**Cognitive grounding**: COG-005 (working memory), EVE-002 (concept-oriented)

### 6. Wiki Links

Notes connect via `[[wiki-link]]` syntax. Creates traversable knowledge graph.

**Cognitive grounding**: ZET-002, COG-002 (spreading activation)

### 7. Schema Blocks

Notes include `_schema` blocks defining expected structure. Single source of truth for note format.

```markdown
---
_schema: claim
_claim_type: empirical
_source: doi:10.xxxx
_status: verified
---
```

**Cognitive grounding**: EVE-005 (context-specific)

### 8. Templates

Note templates with embedded schemas. Jumpstart creation with consistency.

**Cognitive grounding**: COR-001 (record), EVE-004 (iterative refinement)

## Processing Primitives

### 9. Pipeline Phases

Six-phase processing pipeline:

```
Record → Reduce → Reflect → Reweave → Verify → Rethink
```

Extended from Cornell's 5 Rs with meta-cognitive layer.

**Cognitive grounding**: COR-001 through COR-005, AGT-003

### 10. Fresh Context Per Phase

Each pipeline phase runs in fresh context via subagent spawning.

**Cognitive grounding**: AGT-001, AGT-003

### 11. Queue-Based Orchestration

Processing queue tracks task state across phases. Enables pause/resume and parallel work.

```
ops/queue/
├── pending/
├── in-progress/
├── blocked/
└── complete/
```

**Cognitive grounding**: AGT-002, PAR-001 (projects)

## Automation Primitives

### 12. Session Orientation Hook

Runs on session start. Injects workspace tree, loads identity, surfaces maintenance signals.

**Cognitive grounding**: AGT-002 (session boundaries), COG-004 (context-switching)

### 13. Write Validation Hook

Runs on every note write. Validates schema compliance, suggests links, enforces structure.

**Cognitive grounding**: EVE-004 (iterative refinement), COR-005 (review)

### 14. Auto-Commit Hook

Async git commits on write. Maintains version history without blocking.

**Cognitive grounding**: AGT-005 (tool-augmented memory)

### 15. Session Capture Hook

Runs on session stop. Persists state, captures learnings, updates MOCs.

**Cognitive grounding**: COR-004 (reflect), AGT-002

## Primitive Interdependence

Primitives reinforce each other:

```
Atomic Notes + Wiki Links → Traversable knowledge graph
Description Field + MOCs → Progressive disclosure navigation
Pipeline + Fresh Context → Maintained quality at scale
Hooks + Schema → Automated quality enforcement
```

No primitive stands alone. Together they form a coherent cognitive architecture.

## Customization Within Constraints

While primitives are fixed, implementation varies by domain:

| Primitive | Fixed | Variable |
|-----------|-------|----------|
| Three-Space | Yes | Space names, subfolders |
| Atomic Notes | Yes | Schema fields |
| MOC Hierarchy | Yes | MOC topics, depth |
| Pipeline Phases | Yes | Phase commands, categories |
| Hooks | Yes | Hook intensity |

The derivation engine determines the variable aspects based on your domain and preferences.

---

*Each kernel primitive maps to specific research claims in methodology.md.*