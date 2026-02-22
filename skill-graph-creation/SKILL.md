---
name: skill-graph-creation
description: Use this skill when user asks about creating skill graphs, knowledge graphs, or structured domain knowledge. This skill teaches how to create, organize, and maintain skill graphs using wiki-links and YAML frontmatter.
tags: ["knowledge-management", "documentation", "meta-skill"]
related: []
---

# Skill Graph Creation

This skill teaches agents how to create, organize, and maintain **skill graphs** — a system for structured knowledge where each file is one skill, connected by wiki-links.

## When to use

Use this skill when user asks about:
- Creating skill graphs or knowledge graphs
- Structuring domain knowledge (trading, development, medicine, etc.)
- Wiki-links and YAML frontmatter
- Organizing related skills as a graph
- Progressive disclosure in documentation

## How skill graphs work

Unlike single-file documentation, skill graphs provide:
- **Network of files** — each skill is one file
- **Wiki-links** — [[like-this]] create connections
- **YAML frontmatter** — metadata for quick understanding
- **Progressive disclosure** — INDEX → descriptions → links → content

## Workflow for creating new graphs

### 1. Read the creation guide

Point agent to the meta-skill:

For example graphs:
- Trading: "Read skills/trading-graph/INDEX.md"
- Development: "Read skills/development-graph/INDEX.md"
- ZVEC: "Read skills/zvec/INDEX.md"

These provide:
- [[graph-structure]] — File/folder organization
- [[content-writing]] — Writing quality skills
- [[linking-strategies]] — Creating connections
- [[naming-conventions]] — Naming rules
- [[validation]] — Quality checks

### 2. Choose a domain

Pick a topic you understand well:
- Trading, development, medicine, marketing
- Narrow: 5-8 skills
- Broad: 8-15 skills
- Complex: 15+ skills

### 3. Create structure

Follow [[graph-structure]]:

```bash
mkdir -p skills/your-graph-name
cat > skills/your-graph-name/INDEX.md << 'EOF'
---
description: "Entry point for your graph"
tags: ["domain"]
---

# Your Graph Name

## Core concepts
- [[skill-1]] — Description
- [[skill-2]] — Description
EOF
```

### 4. Add skills with frontmatter

Each skill file needs:

```markdown
---
description: "Brief description"
tags: ["tag1", "tag2"]
related: ["skill-1", "skill-2"]
---

# Skill Name

Content here. See [[skill-1]] for related concepts.
```

### 5. Connect with wiki-links

Use `[[skill-name]]` format:
- In text: "See [[risk-management]] for details"
- In lists: "- [[skill-name]]"
- In tables: "[[skill-name]]"

### 6. Validate

Check:
- [ ] All YAML frontmatter is valid
- [ ] Wiki-links work correctly
- [ ] No orphan files
- [ ] Agent can navigate to graph

## Available example graphs

### Trading
```bash
"Read skills/trading-graph/INDEX.md"
```

Skills:
- [[risk-management]]
- [[market-psychology]]
- [[position-sizing]]
- And 12 more...

### Development
```bash
"Read skills/development-graph/INDEX.md"
```

Skills:
- [[clean-code]]
- [[testing]]
- [[debugging]]
- And 6 more...

### ZVEC
```bash
"Read skills/zvec/INDEX.md"
```

Skills:
- [[zvec-basics]]
- [[installation]]
- [[dense-vectors]]
- And 9 more...

## Agent behavior

When working with skill graphs:

1. **Start with INDEX.md** — entry point
2. **Scan frontmatter** — understand available skills quickly
3. **Follow relevant links** — don't read everything
4. **Provide targeted knowledge** — not entire files
5. **Maintain progressive disclosure** — index → descriptions → content

## Best practices

### One skill = one idea

Good:
- `risk-management.md` — all about risk
- `emotional-control.md` — emotion techniques

Bad:
- `trading-everything.md` — everything at once

### Meaningful links

Good:
```markdown
Before entering a trade, check [[risk-management]] rules.
```

Bad:
```markdown
See also: [[risk-management]]
```

### Use YAML frontmatter

Always include:
- `description` — brief description
- `tags` — for search/discovery
- `related` — connections to other skills

## Summary

Skill graphs provide structured, navigable knowledge. This skill teaches how to create them.

For creating new graphs: read the relevant graph's INDEX.md
For using existing graphs: read the relevant graph's INDEX.md

This is a **meta-skill** for teaching how to create knowledge graphs.
