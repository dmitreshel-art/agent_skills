---
name: arscontexta:setup
description: Start the conversational onboarding process to generate your personalized knowledge system. Asks 2-4 questions about your domain, then derives and generates your complete vault structure.
---

# Setup — Conversational Onboarding

Generate your complete knowledge system through conversation.

## Usage

```
/arscontexta:setup
```

Advanced (skip conversation, configure directly):
```
/arscontexta:setup --advanced
```

## The 6-Phase Process

### Phase 1: Detection

Detect the environment:

1. Check for existing vault structure
2. Identify OpenClaw configuration
3. Detect Agent Memory System availability
4. Assess current hooks configuration

**Output**: Environment report

```
Environment detected:
- OpenClaw: ✓
- Agent Memory System: ✓
- Existing vault: ✗ (fresh start)
- Hooks active: ✗
```

### Phase 2: Understanding

Conduct 2-4 conversation turns to understand:

1. **Domain**: What field do you work in? What knowledge are you managing?
2. **Goals**: What do you want from this system? What problems are you solving?
3. **Patterns**: How do you currently capture and process information?
4. **Preferences**: Automation level? Structure preference? Vocabulary?

**Example conversation**:

```
AI: What domain or field are you building this knowledge system for?

You: I'm a software architect. I research and document system designs,
patterns, and trade-offs. I want to capture decisions and their reasoning.

AI: Got it — software architecture with focus on decisions and trade-offs.
How do you currently capture architecture decisions?

You: Mostly in scattered docs, Confluence pages, sometimes just emails.
The problem is I can never find the "why" later.

AI: Classic traceability problem. Do you prefer structured forms (like ADRs)
or more narrative notes?

You: ADRs feel too rigid. I want structure but more flexible.
```

### Phase 3: Derivation

Map conversation signals to 8 dimensions:

| Dimension | Signals |
|-----------|---------|
| Atomicity | How granular are your concepts? Do you combine or separate ideas? |
| Connectivity | How much cross-reference do you need? Network thinking? |
| Structure | Hierarchical domain or flat exploration? |
| Temporal | Does time matter? Versioning? History? |
| Processing | How much processing pipeline do you need? Heavy or light? |
| Automation | Want enforcement? Gentleness? Speed? |
| Navigation | How do you find things? Search? Browse? Follow links? |
| Domain | What vocabulary fits? What concepts are central? |

**Output**: Configuration report with confidence scores

```
Derived Configuration:
- Atomicity: High (you separate concerns clearly)
- Connectivity: High (architectural relationships matter)
- Structure: Medium (some hierarchy, not rigid)
- Temporal: Medium (decisions evolve)
- Processing: Medium (capture → decide → connect)
- Automation: High (quality enforcement)
- Navigation: Both (search + browse + link-following)
- Domain: software-architecture

Confidence: 0.87
Preset similarity: None (unique derivation)
```

### Phase 4: Proposal

Show what will be generated:

```
Your System Proposal:

Space Structure:
├── self/
│   ├── identity.md      # Architect identity, principles
│   ├── methodology.md   # Decision documentation approach
│   └── goals.md         # Architecture goals
├── decisions/           # Architecture Decision Records (flexible)
│   ├── inbox/           # Raw captures
│   ├── active/          # Active decisions
│   └── superseded/      # Replaced decisions
├── patterns/            # Design patterns catalog
├── trade-offs/          # Trade-off analyses
├── MOCs/
│   ├── decisions.md     # Decision index
│   ├── patterns.md      # Pattern index
│   └── systems.md       # System overview
└── ops/
    └── queue/

Pipeline Phases:
1. Record → Capture to inbox/
2. Reduce → Extract decision, patterns, trade-offs
3. Reflect → Find related decisions, update MOCs
4. Reweave → Back-link new context to old decisions
5. Verify → Check schema, completeness, links
6. Rethink → Challenge assumptions periodically

Hooks:
- Session start: Load identity, show pending decisions
- Write validation: Check decision schema
- Auto-commit: Git commit after writes
- Session stop: Capture session learnings

Domain Vocabulary:
- "decision" instead of generic "note"
- ADR-style but flexible
- "context", "decision", "consequences" fields

Proceed with generation? [y/n]
```

### Phase 5: Generation

Create all files:

1. **Create directory structure**
2. **Generate context files** (identity.md, methodology.md, goals.md)
3. **Create MOCs** with initial structure
4. **Write templates** with domain-specific schemas
5. **Generate CLAUDE.md/AGENTS.md** integration
6. **Create hooks.json** with hook definitions
7. **Write user manual** (domain-specific documentation)

### Phase 6: Validation

Run validation checks:

```
Validation Results:
✓ Directory structure complete
✓ Context files generated
✓ MOCs created (3)
✓ Templates created (4)
✓ AGENTS.md updated
✓ hooks.json valid
✓ User manual generated

15/15 kernel primitives verified.

System ready. Restart OpenClaw to activate hooks.

Next steps:
1. Restart OpenClaw
2. Run /arscontexta:help for available commands
3. Start capturing to inbox/
```

## Advanced Mode

Skip conversation, configure dimensions directly:

```
/arscontexta:setup --advanced

Configure dimensions:
1. Atomicity [low/medium/high]: high
2. Connectivity [low/medium/high]: high
3. Structure [flat/medium/deep]: medium
4. Temporal [low/medium/high]: medium
5. Processing [light/medium/heavy]: medium
6. Automation [none/light/medium/heavy]: heavy
7. Navigation [search/browse/links/all]: all
8. Domain name: software-architecture

Generating...
```

## Re-running Setup

If you run setup again:

- Detects existing structure
- Offers options: extend, re-derive, or backup-and-recreate
- Preserves existing notes
- Updates structure and hooks

## Output Files

The setup generates:

```
<vault>/
├── self/
│   ├── identity.md
│   ├── methodology.md
│   └── goals.md
├── [domain-space]/        # Named based on domain
│   ├── inbox/
│   └── ...
├── MOCs/
│   └── ...
├── ops/
│   └── queue/
├── templates/
│   └── [domain-templates]
├── AGENTS.md             # Updated with vault reference
├── hooks.json            # Hook configuration
└── MANUAL.md             # Domain-specific user manual
```

## What to Do After Setup

1. **Restart OpenClaw** — activates hooks
2. **Read MANUAL.md** — your domain-specific guide
3. **Explore MOCs** — see the navigation structure
4. **Start capturing** — add to inbox/
5. **Run pipeline** — try `/reduce` on an inbox item