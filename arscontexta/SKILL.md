---
name: arscontexta
description: Generate a personalized knowledge system through conversation. Run /arscontexta:setup to create your "second brain" - folder structure, context files, processing pipeline, hooks, and note templates derived from how you think and work. No templates, no configuration. Just conversation. Based on Tools for Thought research with 249 backing claims.
---

# Ars Contexta

A second brain for your agent, derived through conversation.

## Overview

Most AI tools start every session blank. Ars Contexta changes that by generating a persistent thinking system tailored to how you actually work.

Unlike templated approaches, this skill **derives** your knowledge system from first principles. Through a 20-minute conversation, it discovers your domain, thinking patterns, and needs — then generates:

- **Vault structure** — folders, context files, MOCs (Maps of Content)
- **Processing pipeline** — skills to capture, reduce, reflect, reweave, verify
- **Hooks** — automation for quality enforcement and git commits
- **Templates** — note templates with schema blocks
- **User manual** — domain-native documentation

## Quick Start

```
/arscontexta:setup
```

Answer 2-4 questions (~20 minutes). The engine generates your complete system.

Then restart OpenClaw to activate hooks.

## Commands

### Setup & Management

| Command | Description |
|---------|-------------|
| `/arscontexta:setup` | Conversational onboarding — generates your full system |
| `/arscontexta:help` | Contextual guidance and command discovery |
| `/arscontexta:health` | Run diagnostic checks on your vault |
| `/arscontexta:architect` | Research-backed evolution guidance |
| `/arscontexta:reseed` | Re-derive from first principles when drift accumulates |
| `/arscontexta:add-domain` | Add a new knowledge domain to existing system |

### Processing Pipeline (Generated)

These commands are **generated during setup** based on your domain:

| Command | Phase | Description |
|---------|-------|-------------|
| `/reduce` | Reduce | Extract insights with domain-native categories |
| `/reflect` | Reflect | Find connections, update MOCs |
| `/reweave` | Reweave | Update older notes with new context |
| `/verify` | Verify | Combined quality check |
| `/remember` | Record | Mine session learnings |

## The Setup Flow

`/arscontexta:setup` runs a 6-phase process:

| Phase | What Happens |
|-------|--------------|
| Detection | Detects environment and capabilities |
| Understanding | 2-4 conversation turns about your domain |
| Derivation | Maps signals to 8 configuration dimensions |
| Proposal | Shows what will be generated and why |
| Generation | Produces all files |
| Validation | Checks primitives, runs smoke test |

## Three-Space Architecture

Every generated system separates content into three spaces:

| Space | Purpose | Growth |
|-------|---------|--------|
| `self/` | Agent persistent mind — identity, methodology, goals | Slow (tens of files) |
| `notes/` | Knowledge graph — the reason the system exists | Steady (10-50/week) |
| `ops/` | Operational coordination — queue state, sessions | Fluctuating |

Names adapt to your domain (`notes/` might become `reflections/`, `claims/`, or `decisions/`).

## Configuration Dimensions

The derivation engine maps your conversation to 8 dimensions:

1. **Atomicity** — Note granularity (atomic vs. comprehensive)
2. **Connectivity** — Link density and patterns
3. **Structure** — Hierarchy level (flat to deep)
4. **Temporal** — Time-based organization relevance
5. **Processing** — Pipeline complexity needed
6. **Automation** — Hook intensity
7. **Navigation** — MOC depth and style
8. **Domain** — Vocabulary and concept mapping

## Research Foundation

See [references/methodology.md](references/methodology.md) for the 249 research claims backing all configuration decisions.

Key research synthesized:
- Zettelkasten — Cornell Note-Taking — Evergreen Notes — PARA — GTD
- Memory Palaces — Cognitive Science (extended mind, spreading activation)
- Network Theory (small-world topology, betweenness centrality)
- Agent Architecture (context windows, session boundaries, multi-agent patterns)

Query directly: "Why does my system use atomic notes?" → Load methodology.md

## Files Generated

```
<vault>/
├── self/
│   ├── identity.md        # Who I am, how I think
│   ├── methodology.md     # My processing approach
│   └── goals.md           # What I'm working toward
├── notes/
│   ├── inbox/             # Zero-friction capture
│   ├── MOCs/              # Maps of Content (navigation hubs)
│   └── templates/         # Note templates with schemas
├── ops/
│   ├── queue/             # Processing queue state
│   └── sessions/          # Session state persistence
├── CLAUDE.md              # Generated context file (or AGENTS.md)
└── hooks.json             # Hook configuration
```

## Philosophy

**Derivation, not templating.** Every choice traces to specific research claims. The engine reasons from principles about what your domain needs and why.

The name connects to a tradition. **Ars Combinatoria, Ars Memoria, Ars Contexta**: the art of context.

Llull's rotating wheels generated truth through combination. Bruno's memory wheels created millions of image combinations. They were external thinking systems — tools to think with rather than just store in. The missing piece: they required a human mind to do the traversing. Now LLMs can traverse. The wheels can spin again.

## When to Use This Skill

- First session: Run `/arscontexta:setup` to generate your system
- Adding domains: Run `/arscontexta:add-domain` to extend
- Feeling drift: Run `/arscontexta:reseed` to realign with first principles
- Architecture questions: Run `/arscontexta:architect` for guidance
- Health check: Run `/arscontexta:health` to diagnose issues

## References

For detailed methodology, research claims, and implementation patterns:

- [references/methodology.md](references/methodology.md) — Research foundation (249 claims)
- [references/kernel.md](references/kernel.md) — 15 kernel primitives every system needs
- [references/presets.md](references/presets.md) — Pre-validated configurations