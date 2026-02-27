# Presets — Pre-Validated Configurations

Three pre-validated configurations for common use cases. Presets provide starting defaults — the derivation engine adapts from there.

## Research Preset

**For**: Academic work, literature reviews, synthesis

**What you get**:
- Atomic claims with citation tracking
- Methodology MOCs
- Evidence hierarchy schemas
- Source processing pipeline
- Academic vocabulary

### Space Structure

```
self/
├── identity.md        # Research identity, interests
├── methodology.md     # Research approach
└── goals.md           # Research questions, milestones

notes/
├── inbox/             # Raw captures
├── claims/            # Atomic research claims
├── sources/           # Source notes with citations
├── methodology/       # Method notes
├── MOCs/
│   ├── hub.md         # Research overview MOC
│   ├── topics/        # Topic MOCs
│   └── methods/       # Method MOCs
└── templates/

ops/
├── queue/             # Processing queue
└── sessions/          # Session state
```

### Schema Examples

**Claim Note**:
```markdown
---
_schema: claim
_claim_type: empirical | theoretical | methodological
_source: doi:10.xxxx
_status: unverified | partial | verified
_confidence: low | medium | high
---

# [Claim Title]

## Summary
[One-sentence description]

## Evidence
[Supporting evidence]

## Connections
- [[Related Claim 1]]
- [[Related Claim 2]]

## Questions
[Open questions about this claim]
```

**Source Note**:
```markdown
---
_schema: source
_type: paper | book | article | talk
_bib_key: author2024title
_read: y | n | partial
---

# [Source Title]

## Metadata
- Authors: 
- Year: 
- DOI: 

## Key Claims
- → [[Claim extracted]]
- → [[Another claim]]

## Notes
[Reading notes]
```

### Pipeline Focus

Heavy on **Reduce** (extract claims from sources) and **Reflect** (find connections between claims).

### Dimension Values

| Dimension | Value | Reason |
|-----------|-------|--------|
| Atomicity | Maximum | Claims must be atomic |
| Connectivity | High | Citation networks |
| Structure | Deep | Method/topic hierarchies |
| Temporal | Medium | Version tracking |
| Processing | Heavy | Source processing |
| Automation | Medium | Schema validation |
| Navigation | Deep | Multiple MOC levels |
| Domain | Academic | Research vocabulary |

---

## Personal Preset

**For**: Life management, journaling, relationships

**What you get**:
- Reflective note structure
- Goal tracking integration
- Relationship MOCs
- Gentle processing pipeline
- Personal vocabulary

### Space Structure

```
self/
├── identity.md        # Personal identity, values
├── methodology.md     # Reflective practice
└── goals.md           # Life goals, areas

notes/
├── inbox/             # Quick captures
├── reflections/       # Daily/weekly reflections
├── relationships/     # People in your life
├── events/            # Significant events
├── areas/             # Life areas (health, career, etc.)
├── MOCs/
│   ├── hub.md         # Life overview
│   ├── people/        # Relationship MOCs
│   └── areas/         # Area MOCs
└── templates/

ops/
├── queue/             # Light processing queue
└── sessions/          # Session captures
```

### Schema Examples

**Reflection Note**:
```markdown
---
_schema: reflection
_date: 2024-01-15
_mood: 
_energy: low | medium | high
---

# [Date] Reflection

## Highlights
[What went well]

## Challenges
[What was difficult]

## Learnings
[What I learned]

## Intentions
[Tomorrow's focus]
```

**Relationship Note**:
```markdown
---
_schema: relationship
_person: [[Person Name]]
_last_contact: 2024-01-10
---

# [Person Name]

## Context
[How we know each other]

## Interactions
- [[Interaction 1]] - 2024-01-10
- [[Interaction 2]] - 2024-01-05

## Notes
[Private notes about relationship]

## Next
[Next steps, reminders]
```

### Pipeline Focus

Emphasis on **Reflect** (meaning-making) and **Rethink** (challenging assumptions). Light on **Reduce**.

### Dimension Values

| Dimension | Value | Reason |
|-----------|-------|--------|
| Atomicity | Medium | Balance atomic and narrative |
| Connectivity | Medium | Relationship networks |
| Structure | Medium | Life areas provide structure |
| Temporal | High | Time-based reflection |
| Processing | Light | Gentle, not industrial |
| Automation | Light | Minimal enforcement |
| Navigation | Medium | People and areas |
| Domain | Personal | Life vocabulary |

---

## Experimental Preset

**For**: Testing, iteration, rapid prototyping

**What you get**:
- Lightweight structure
- Fast capture
- Minimal ceremony
- Flexibility-first approach

### Space Structure

```
self/
├── identity.md        # Brief identity
└── goals.md           # Current experiments

notes/
├── inbox/             # Everything starts here
├── experiments/       # Active experiments
├── learnings/         # What you learned
├── MOCs/
│   └── hub.md         # Single hub MOC
└── templates/         # Minimal templates

ops/
└── sessions/          # Session captures
```

### Schema Examples

**Experiment Note**:
```markdown
---
_schema: experiment
_status: active | paused | complete
_started: 2024-01-15
---

# [Experiment Name]

## Hypothesis
[What you're testing]

## Method
[How you're testing it]

## Results
[Updated as you go]

## Learnings
[What you learned]
```

### Pipeline Focus

Minimal structure. **Record** and **Reduce** only, optional **Reflect**.

### Dimension Values

| Dimension | Value | Reason |
|-----------|-------|--------|
| Atomicity | Low | Comprehensive notes OK |
| Connectivity | Low | Links optional |
| Structure | Flat | Minimal hierarchy |
| Temporal | Low | Not time-organized |
| Processing | Minimal | Fast capture |
| Automation | None | No enforcement |
| Navigation | Minimal | Single hub |
| Domain | Neutral | Flexible vocabulary |

---

## Choosing a Preset

Use these guidelines:

| If you're... | Choose... |
|--------------|-----------|
| Doing academic research, literature review | Research |
| Managing life, journaling, relationships | Personal |
| Testing ideas, rapid iteration | Experimental |
| Unsure or have unique needs | Run setup, derive from conversation |

Presets are starting points. The derivation engine adapts all dimensions based on what you say during setup.

---

## Custom Derivation

For unique domains, skip presets entirely. The setup conversation will derive:

1. Your domain vocabulary
2. Your thinking patterns
3. Your processing needs
4. Your automation preferences

The engine maps conversation signals to the 8 dimensions, generating a system tailored to you.