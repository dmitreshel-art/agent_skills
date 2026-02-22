# OpenSpec Skill for OpenClaw

Spec-Driven Development (SDD) methodology skill for OpenClaw AI assistant.

## What is OpenSpec?

OpenSpec is a lightweight spec framework that helps you and your AI coding assistant agree on what to build before any code is written. It adds a spec layer so you align on requirements before implementation begins.

## Core Philosophy

- **Fluid, not rigid** — No phase gates, work on what makes sense
- **Iterative, not waterfall** — Learn as you build, refine as you go
- **Easy, not complex** — Lightweight setup, minimal ceremony
- **Brownfield-first** — Works with existing codebases

## Quick Start

### Initialize OpenSpec in Your Project

```bash
# If you have OpenSpec CLI installed globally
openspec init
```

Or if you don't have the CLI, this skill can help you create the structure manually.

### Start Your First Change

```
You: /opsx:new add-dark-mode

AI: Created openspec/changes/add-dark-mode/
     Schema: spec-driven
     Ready to create: proposal
```

### Create All Planning Artifacts

```
You: /opsx:ff

AI: ✓ Creating proposal.md
     ✓ Creating specs/ui/spec.md
     ✓ Creating design.md
     ✓ Creating tasks.md
     All planning artifacts complete!
```

### Implement

```
You: /opsx:apply

AI: Implementing add-dark-mode...
     ✓ 1.1 Create ThemeContext
     ✓ 1.2 Add CSS custom properties
     ✓ 1.3 Implement localStorage persistence
     All tasks complete!
```

### Archive

```
You: /opsx:archive

AI: ✓ Synced specs to openspec/specs/ui/spec.md
     ✓ Moved to openspec/changes/archive/2025-01-24-add-dark-mode/
```

## Available Commands

| Command | Purpose |
|---------|---------|
| `/opsx:new` | Start a new change |
| `/opsx:continue` | Create next artifact step by step |
| `/opsx:ff` | Fast-forward: create all planning artifacts |
| `/opsx:apply` | Implement tasks |
| `/opsx:verify` | Validate implementation |
| `/opsx:sync` | Merge delta specs (optional) |
| `/opsx:archive` | Archive completed change |
| `/opsx:bulk-archive` | Archive multiple changes |
| `/opsx:explore` | Think through ideas |
| `/opsx:onboard` | Guided tutorial |

## Project Structure

```
openspec/
├── specs/              # Source of truth
│   └── <domain>/
│       └── spec.md
├── changes/            # Proposed changes
│   └── <change-name>/
│       ├── proposal.md
│       ├── design.md
│       ├── tasks.md
│       └── specs/      # Delta specs
│           └── <domain>/
│               └── spec.md
└── changes/archive/    # Completed changes
```

## Learning More

- **Full documentation:** See [SKILL.md](./SKILL.md) for complete reference
- **External docs:** https://github.com/Fission-AI/OpenSpec
- **Philosophy:** Spec-driven development with delta specs

## Why Use This Skill?

✅ **Agreement before building** — Align on specs first
✅ **Stay organized** — Each change has its own folder
✅ **Work fluidly** — Update any artifact anytime
✅ **Clean history** — Archived changes are preserved
✅ **No bureaucracy** — Lightweight setup, minimal ceremony

Use this skill when you want structured, predictable development with clear documentation.
