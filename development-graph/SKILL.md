---
name: development-graph
description: Use this skill for software development best practices, clean code principles, testing strategies, debugging techniques, and architecture patterns. Access to structured knowledge with wiki-links for engineering decisions.
tags: ["development", "clean-code", "testing", "debugging", "architecture", "refactoring"]
related: ["trading-graph"]
---

# Development Graph Skill

This skill provides access to the **development-graph** — a structured knowledge graph for software development with 10 interconnected skills covering clean code, testing, debugging, refactoring, and more.

## When to use

Use this skill when user asks about:
- Clean code principles and practices
- Testing strategies and quality assurance
- Debugging techniques and troubleshooting
- Code review and collaboration
- Architecture patterns and design principles
- Refactoring strategies and patterns
- Version control and Git workflows

## Graph structure

The development graph files are now located at:
```
skills/development-graph/
├── INDEX.md                    # Entry point
├── clean-code.md              # Clean code principles
├── testing.md                # Testing strategies
├── debugging.md              # Debugging techniques
├── code-review.md            # Code review practices
├── documentation.md          # Documentation standards
├── refactoring.md            # Refactoring patterns
├── architecture.md          # Architecture principles
├── version-control.md         # Git workflows
└── ...
```

## How to use

### 1. Start with INDEX

```bash
"Read skills/development-graph/INDEX.md"
```

The INDEX.md provides:
- Core practices overview
- Navigation to all 10 skills
- YAML frontmatter for quick scanning

### 2. Scan frontmatter

Before reading a skill file, check its frontmatter:
```yaml
---
description: "Brief description"
tags: ["tag1", "tag2"]
related: ["skill-1", "skill-2"]
---
```

This allows progressive disclosure:
- Skip skills not relevant to query
- Follow [[wiki-links]] to related concepts
- Provide targeted knowledge, not entire files

### 3. Follow wiki-links

When navigating to graph:
- Start with [[clean-code]] for code quality
- Follow [[testing]] for testing strategies
- Use [[architecture]] for design decisions

## Available skills

### Core principles
- [[clean-code]] — Principles of clean, maintainable code
- [[testing]] — Testing strategies and quality assurance
- [[debugging]] — Debugging techniques and troubleshooting

### Collaborative practices
- [[code-review]] — Code review practices and feedback
- [[documentation]] — Documentation standards and practices

### Advanced practices
- [[refactoring]] — Refactoring patterns and strategies
- [[architecture]] — Architectural principles and patterns
- [[version-control]] — Git workflows and version control best practices

## Agent behavior

When answering development questions:

1. **Read INDEX.md** first for overview
2. **Scan frontmatter** of relevant skills
3. **Follow [[wiki-links]]** based on query relevance
4. **Provide progressive knowledge** — index → descriptions → targeted sections
5. **Maintain context** — keep track of related concepts

## Best practices

- **Start broad**, then drill down: INDEX → core principles → specific practices
- **Use wiki-links** for navigation — don't read everything linearly
- **Cross-reference concepts**: testing connects to debugging, clean-code connects to all practices
- **Progressive disclosure**: Show overview first, details only when needed

## Reference

- **Graph location:** `skills/development-graph/INDEX.md`
- **Main docs:** `skills/README.md`
- **Agent guide:** `skills/AGENT-GUIDE.md`
- **Creation guide:** `skills/skill-graph-creation/SKILL.md`

## Summary

The development graph provides structured knowledge for engineering decisions. Access via `skills/development-graph/INDEX.md` and navigate using wiki-links.

This skill is a **wrapper** that provides access to development knowledge graph files.
