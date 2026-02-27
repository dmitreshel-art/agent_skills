---
name: arscontexta:help
description: Contextual guidance and command discovery. Shows available commands, explains concepts, and provides help based on your current vault state.
---

# Help — Contextual Guidance

Get help with Ars Contexta commands and concepts.

## Usage

```
/arscontexta:help
/arscontexta:help [topic]
/arscontexta:help [command]
```

## Quick Reference

### Setup & Management

| Command | What It Does |
|---------|--------------|
| `/arscontexta:setup` | Generate your knowledge system (first run) |
| `/arscontexta:health` | Check vault health |
| `/arscontexta:architect` | Get architecture guidance |
| `/arscontexta:reseed` | Re-derive from first principles |
| `/arscontexta:add-domain` | Add a new knowledge domain |

### Processing Pipeline

| Command | Phase | What It Does |
|---------|-------|--------------|
| `/record` | 1 | Zero-friction capture to inbox |
| `/reduce` | 2 | Extract insights, categorize |
| `/reflect` | 3 | Find connections, update MOCs |
| `/reweave` | 4 | Back-link new context to old notes |
| `/verify` | 5 | Quality check (schema + links + health) |
| `/rethink` | 6 | Challenge assumptions periodically |

### Navigation

| Command | What It Does |
|---------|--------------|
| `/find` | Search vault content |
| `/moc` | Browse MOCs |
| `/next` | What should I work on? |
| `/recent` | Recent changes |
| `/random` | Serendipitous discovery |

## Topic Help

### Concepts

```
/arscontexta:help atomic-notes
```

Explains atomic note philosophy and how to write them.

```
/arscontexta:help mocs
```

Explains Maps of Content and navigation strategy.

```
/arscontexta:help pipeline
```

Explains the 6-phase processing pipeline.

```
/arscontexta:help hooks
```

Explains automation hooks and what they do.

```
/arscontexta:help three-spaces
```

Explains self/notes/ops architecture.

### Workflows

```
/arscontexta:help getting-started
```

Step-by-step guide for new users.

```
/arscontexta:help daily-workflow
```

Recommended daily workflow with the system.

```
/arscontexta:help processing-inbox
```

How to process inbox items through the pipeline.

## Contextual Help

Help adapts to your vault state:

**Fresh vault (no notes)**:
```
Welcome to your new vault! Here's how to start:

1. Capture something → /record "First note about..."
2. Process it → /reduce notes/inbox/first-note.md
3. Find connections → /reflect notes/decisions/first-note.md
4. Build habits → /arscontexta:help daily-workflow
```

**Stale vault (no recent activity)**:
```
Your vault has been quiet. Consider:

- Process pending inbox items: /reduce
- Update MOCs: /reflect
- Review old notes: /reweave
- Challenge assumptions: /rethink
```

**Healthy vault**:
```
Your vault is healthy!

Recent activity: 12 notes this week
Queue status: 3 pending
MOCs: All up to date

Try: /random for serendipitous discovery
```

## Query Research

```
/arscontexta:help why:[concept]
```

Query the research foundation:

```
/arscontexta:help why:atomic-notes

Atomic notes derive from:

1. ZET-001: One idea per note enables recombination
   - Source: Luhmann's Zettelkasten
   - When ideas are atomic, they can be linked in new combinations

2. EVE-003: Dense linking connects ideas
   - Source: Andy Matuschak
   - Every note should connect to several others

3. COG-002: Spreading activation
   - Source: Collins & Loftus 1975
   - Linked concepts prime each other in memory

Together: Atomic notes + dense links = generative knowledge system
```

Other research queries:
- `/arscontexta:help why:mocs`
- `/arscontexta:help why:pipeline`
- `/arscontexta:help why:fresh-context`
- `/arscontexta:help why:three-spaces`

## Troubleshooting

```
/arscontexta:help troubleshoot:[issue]
```

Common issues:
- `troubleshoot:broken-links` — Fix broken wiki links
- `troubleshoot:orphans` — Handle notes with no incoming links
- `troubleshoot:stale-mocs` — Update outdated MOCs
- `troubleshoot:queue-stuck` — Unstick processing queue
- `troubleshoot:hooks-not-working` — Debug hook configuration