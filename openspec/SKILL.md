# OpenSpec - Spec-Driven Development (SDD) Skill

## Overview

OpenSpec is a lightweight spec framework for AI coding assistants that helps you agree on what to build before any code is written. This skill implements the SDD (Spec-Driven Development) methodology within OpenClaw.

**Core Philosophy:**
- Fluid, not rigid — no phase gates, work on what makes sense
- Iterative, not waterfall — learn as you build, refine as you go
- Easy, not complex — lightweight setup, minimal ceremony
- Brownfield-first — works with existing codebases, not just greenfield

## When to Use This Skill

Use this skill when the user wants to:
- Start a new feature development with proper planning
- Implement changes with clear specifications
- Work with the OpenSpec SDD methodology
- Create structured proposals, specs, designs, and tasks
- Archive completed changes and maintain spec history

## Core Concepts

### Two Key Directories

**`openspec/specs/`** — Source of truth for current system behavior
- Organized by domain (e.g., `auth/`, `payments/`, `ui/`)
- Contains requirements and scenarios in behavior-first format
- Describes observable behavior, not implementation details

**`openspec/changes/`** — Proposed modifications
- Each change gets its own folder with all related artifacts
- Contains delta specs (ADDED/MODIFIED/REMOVED requirements)
- When archived, deltas merge into main specs
- Then moves to `changes/archive/` for audit trail

### Artifact Types

Each change folder contains four artifacts:

1. **`proposal.md`** — The "why" and "what"
   - Intent, scope (in/out), and approach
   - High-level decision making before diving into details

2. **`specs/`** (delta specs) — What's changing
   - ADDED: New requirements
   - MODIFIED: Changed requirements with previous version noted
   - REMOVED: Deprecated requirements
   - Uses Given/When/Then scenario format

3. **`design.md`** — The "how"
   - Technical approach and architecture decisions
   - Data flow diagrams
   - File changes
   - Technology choices and rationale

4. **`tasks.md`** — Implementation checklist
   - Concrete steps with checkboxes
   - Hierarchical numbering (1.1, 1.2, etc.)
   - Grouped by related work

### Spec Format

Specs use structured requirements with scenarios:

```markdown
# Auth Specification

## Purpose
Authentication and session management for the application.

## Requirements

### Requirement: User Authentication
The system SHALL issue a JWT token upon successful login.

#### Scenario: Valid credentials
- GIVEN a user with valid credentials
- WHEN the user submits login form
- THEN a JWT token is returned
- AND the user is redirected to dashboard
```

**Key elements:**
- `## Purpose` — High-level description
- `### Requirement:` — Specific behavior (RFC 2119: SHALL/MUST/SHOULD/MAY)
- `#### Scenario:` — Concrete examples in Given/When/Then format

## Workflow Commands

### `/opsx:new [change-name] [--schema <schema-name>]`
Start a new change. Creates the change folder structure.

**What it does:**
- Creates `openspec/changes/<change-name>/` directory
- Creates `.openspec.yaml` metadata file
- Shows first artifact ready for creation

**Example:**
```
User: /opsx:new add-dark-mode
AI: Created openspec/changes/add-dark-mode/
     Schema: spec-driven
     Ready to create: proposal
```

### `/opsx:continue [change-name]`
Create the next artifact in the dependency chain (one at a time).

**What it does:**
- Queries dependency graph
- Shows which artifacts are ready vs blocked
- Creates the first ready artifact
- Reads dependency files for context

**Example:**
```
User: /opsx:continue
AI: Change: add-dark-mode
     Artifact status:
     ✓ proposal    (done)
     ◆ specs       (ready)
     ◆ design      (ready)
     ○ tasks       (blocked - needs: specs)
     Creating specs...
     ✓ Created openspec/changes/add-dark-mode/specs/ui/spec.md
     Now available: tasks
```

### `/opsx:ff [change-name]`
Fast-forward: create all planning artifacts at once.

**What it does:**
- Creates all artifacts in dependency order
- Tracks progress via todo list
- Stops when all apply-required artifacts are complete

**Example:**
```
User: /opsx:ff add-dark-mode
AI: Fast-forwarding add-dark-mode...
     ✓ Creating proposal.md
     ✓ Creating specs/ui/spec.md
     ✓ Creating design.md
     ✓ Creating tasks.md
     All planning artifacts complete!
     Ready for implementation.
```

### `/opsx:apply [change-name]`
Implement tasks from the change.

**What it does:**
- Reads `tasks.md` and identifies incomplete tasks
- Works through tasks one by one
- Writes code, creates files, runs tests
- Marks tasks complete with checkboxes `[x]`

**Example:**
```
User: /opsx:apply
AI: Implementing add-dark-mode...
     Working on 1.1: Create ThemeContext...
     ✓ 1.1 Complete
     Working on 1.2: Add CSS custom properties...
     ✓ 1.2 Complete
```

### `/opsx:verify [change-name]`
Validate implementation matches artifacts.

**What it does:**
- Checks three dimensions: Completeness, Correctness, Coherence
- Searches codebase for implementation evidence
- Reports issues as CRITICAL, WARNING, or SUGGESTION
- Does not block archive, but surfaces issues

**Example:**
```
User: /opsx:verify
AI: Verifying add-dark-mode...
     COMPLETENESS
     ✓ All 8 tasks in tasks.md are checked
     ✓ All requirements in specs have corresponding code
     CORRECTNESS
     ✓ Implementation matches spec intent
     COHERENCE
     ✓ Design decisions reflected in code
     Ready to archive!
```

### `/opsx:sync [change-name]`
Merge delta specs into main specs (optional; archive prompts if needed).

**What it does:**
- Reads delta specs from change folder
- Parses ADDED/MODIFIED/REMOVED sections
- Merges changes into main `openspec/specs/` directory
- Change remains active (not archived)

### `/opsx:archive [change-name]`
Archive a completed change.

**What it does:**
- Checks artifact and task completion status
- Offers to sync delta specs if not already done
- Moves change to `openspec/changes/archive/YYYY-MM-DD-<name>/`
- Preserves all artifacts for audit trail

**Example:**
```
User: /opsx:archive
AI: Archiving add-dark-mode...
     Delta specs: Not yet synced
     → Sync now? (recommended)
     ✓ Synced specs to openspec/specs/ui/spec.md
     ✓ Moved to openspec/changes/archive/2025-01-24-add-dark-mode/
```

### `/opsx:bulk-archive [change-names...]`
Archive multiple completed changes at once.

**What it does:**
- Lists all completed changes
- Validates each change before archiving
- Detects spec conflicts across changes
- Resolves conflicts by checking actual implementation
- Archives in chronological order

### `/opsx:explore [topic]`
Think through ideas before committing to a change.

**What it does:**
- Opens exploratory conversation with no structure
- Investigates codebase to answer questions
- Compares options and approaches
- Can create visual diagrams
- No artifacts created during exploration

**Example:**
```
User: /opsx:explore
AI: What would you like to explore?
User: How should we handle rate limiting for our API?
AI: Let me investigate your current setup...
     I see three approaches:
     1. Middleware-based (simple, per-endpoint)
     2. Redis-backed (scalable, shared state)
     3. Token bucket per user (fair, complex)
```

### `/opsx:onboard`
Guided onboarding through the complete workflow.

**What it does:**
- Walks through complete workflow cycle with narration
- Scans codebase for real improvement opportunities
- Creates an actual change with real artifacts
- Implements actual work (small, safe changes)
- Archives the completed change
- Explains each step as it happens

## Best Practices

### 1. Keep Changes Focused
One logical unit of work per change. If doing "add feature X and also refactor Y", consider two separate changes.

**Why:** Easier to review, cleaner archive history, can ship independently, simpler rollback.

### 2. Use `/opsx:explore` for Unclear Requirements
Before committing to a change, explore the problem space.

**Example:**
```
User: /opsx:explore how should we handle rate limiting for our API?
AI: Let me investigate... [analyzes options]
```

### 3. Verify Before Archiving
Use `/opsx:verify` to catch mismatches before closing out the change.

### 4. Name Changes Clearly
Good names make `openspec list` useful:
- Good: `add-dark-mode`, `fix-login-redirect`, `implement-2fa`
- Avoid: `feature-1`, `update`, `changes`

### 5. Use Progressive Rigor
Most changes should stay in **Lite spec** mode:
- Short behavior-first requirements
- Clear scope and non-goals
- A few concrete acceptance checks

Use **Full spec** only for:
- Cross-team or cross-repo changes
- API/contract changes, migrations
- Security/privacy concerns
- High-ambiguity changes where rework would be expensive

### 6. When to Update vs Start Fresh

**Update existing change when:**
- Same intent, refined execution
- Scope narrows (MVP first, rest later)
- Learning-driven corrections

**Start new change when:**
- Intent fundamentally changed
- Scope exploded to different work entirely
- Original change can be marked "done" standalone

## Delta Spec Format

```markdown
# Delta for Auth

## ADDED Requirements

### Requirement: Two-Factor Authentication
The system MUST support TOTP-based two-factor authentication.

#### Scenario: 2FA enrollment
- GIVEN a user without 2FA enabled
- WHEN the user enables 2FA in settings
- THEN a QR code is displayed for authenticator app setup

## MODIFIED Requirements

### Requirement: Session Expiration
The system MUST expire sessions after 15 minutes of inactivity.
(Previously: 30 minutes)

## REMOVED Requirements

### Requirement: Remember Me
(Deprecated in favor of 2FA)
```

**What happens on archive:**
- ADDED → Appended to main spec
- MODIFIED → Replaces existing requirement
- REMOVED → Deleted from main spec

## Common Workflows

### Quick Feature
When you know what to build and just need to execute:
```
/opsx:new ──► /opsx:ff ──► /opsx:apply ──► /opsx:verify ──► /opsx:archive
```

### Exploratory
When requirements are unclear:
```
/opsx:explore ──► /opsx:new ──► /opsx:continue ──► ... ──► /opsx:apply
```

### Parallel Changes
Work on multiple changes simultaneously. Switch context with `/opsx:apply <change-name>`.

## Artifact Dependencies

```
                    proposal
                   (root node)
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
      specs                       design
   (requires:                  (requires:
    proposal)                   proposal)
         │                           │
         └─────────────┬─────────────┘
                       │
                       ▼
                    tasks
                (requires:
                specs, design)
```

**Dependencies are enablers, not gates.** They show what's possible, not what you must create next.

## When to Use `/opsx:ff` vs `/opsx:continue`

| Situation | Use |
|-----------|-----|
| Clear requirements, ready to build | `/opsx:ff` |
| Exploring, want to review each step | `/opsx:continue` |
| Time pressure, need to move fast | `/opsx:ff` |
| Complex change, want control | `/opsx:continue` |

**Rule of thumb:** If you can describe full scope upfront, use `/opsx:ff`. If figuring it out as you go, use `/opsx:continue`.

## Implementation Notes

### Spec vs Design vs Tasks

- **Specs** describe observable behavior (inputs, outputs, errors)
- **Design** describes technical approach (how it works internally)
- **Tasks** are concrete steps to implement the design

**Quick test:** If implementation can change without changing externally visible behavior, it doesn't belong in the spec.

### What Goes Where

**In specs:**
- Observable behavior users or downstream systems rely on
- Inputs, outputs, and error conditions
- External constraints (security, privacy, reliability)
- Scenarios that can be tested

**Avoid in specs:**
- Internal class/function names
- Library or framework choices
- Step-by-step implementation details
- Detailed execution plans (those belong in `design.md` or `tasks.md`)

## Integration with OpenClaw

This skill integrates with OpenClaw's file operations and workspace management:

1. **File structure** — Uses standard OpenClaw workspace directory structure
2. **Markdown files** — Creates and edits `.md` files using write/read/edit tools
3. **Validation** — Checks spec structure and task completion
4. **Context management** — Reads existing artifacts for context

## Troubleshooting

### "Change not found"
- Specify change name explicitly: `/opsx:apply add-dark-mode`
- Check that change folder exists
- Verify you're in the right project directory

### "No artifacts ready"
- All artifacts are either complete or blocked
- Check if required artifacts exist
- Create missing dependency artifacts first

### Artifacts not generating properly
- Add project context in `openspec/config.yaml`
- Provide more detail in your change description
- Use `/opsx:continue` instead of `/opsx:ff` for more control

## External Resources

- **OpenSpec GitHub:** https://github.com/Fission-AI/OpenSpec
- **Documentation:** https://github.com/Fission-AI/OpenSpec/tree/main/docs
- **Philosophy:** https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md
- **Commands reference:** https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md
- **Workflows:** https://github.com/Fission-AI/OpenSpec/blob/main/docs/workflows.md

## Summary

OpenSpec brings predictability to AI-assisted development without the ceremony. It's designed for:
- **Agreement before building** — Human and AI align on specs first
- **Organization** — Each change gets its own folder with all artifacts
- **Fluid work** — Update any artifact anytime, no rigid phase gates
- **Your tools** — Works with any AI coding assistant via slash commands

Use this skill whenever you want structured, spec-driven development with clear documentation and audit trails.
