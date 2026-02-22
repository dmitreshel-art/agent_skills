---
name: trading-graph
description: Use this skill for trading knowledge, market psychology, risk management, position sizing, and technical analysis. Access to structured knowledge with wiki-links for trading decisions.
tags: ["trading", "finance", "risk-management", "psychology", "technical-analysis"]
related: ["development-graph"]
---

# Trading Graph Skill

This skill provides access to the **trading-graph** — a structured knowledge graph for trading with 15 interconnected skills covering risk management, market psychology, technical analysis, and more.

## When to use

Use this skill when user asks about:
- Trading strategies and tactics
- Risk management and position sizing
- Market psychology and emotional control
- Technical analysis patterns
- Trading routines and discipline
- Stop-loss strategies and profit targets

## Graph structure

The trading graph files are now located at:
```
skills/trading-graph/
├── INDEX.md                    # Entry point
├── risk-management.md          # Risk management principles
├── market-psychology.md       # Psychology of trading
├── position-sizing.md           # Position and risk sizing
├── emotional-control.md        # Emotional discipline
├── technical-analysis.md        # Technical analysis
├── momentum-trading.md         # Momentum strategies
├── mean-reversion.md          # Mean reversion
├── breakout-trading.md         # Breakout trading
└── ... (7 more skills)
```

## How to use

### 1. Start with INDEX

```bash
"Read skills/trading-graph/INDEX.md"
```

The INDEX.md provides:
- Core concepts overview
- Navigation to all 15 skills
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
- Start with `[[risk-management]]` for risk questions
- Follow `[[market-psychology]]` for psychological aspects
- Use `[[technical-analysis]]` for analysis techniques

## Available skills

### Core concepts
- [[risk-management]] — Risk management principles and position sizing
- [[market-psychology]] — Psychology of markets and emotions
- [[position-sizing]] — How to size positions based on risk
- [[technical-analysis]] — Chart patterns and indicators

### Trading strategies
- [[momentum-trading]] — Trading with trend momentum
- [[mean-reversion]] — Trading reversals to mean
- [[breakout-trading]] — Trading breakouts from ranges

### Risk & psychology
- [[emotional-control]] — Managing emotions during trading
- [[fear-and-greed]] — Understanding fear and greed in markets
- [[risk-reward-ratio]] — Profit/loss ratio optimization

### Execution
- [[stop-loss-strategies]] — Stop-loss placement techniques
- [[portfolio-diversification]] — Diversification principles
- [[trading-routine]] — Daily trading workflow and habits

### Philosophy
- [[forced-engagement-produces-weak-connections]] — Quality over quantity in learning

## Agent behavior

When answering trading questions:

1. **Read INDEX.md** first for overview
2. **Scan frontmatter** of relevant skills
3. **Follow [[wiki-links]]** based on query relevance
4. **Provide progressive knowledge** — index → descriptions → targeted sections
5. **Maintain context** — keep track of related concepts

## Best practices

- **Start broad**, then drill down: INDEX → core concepts → specific strategies
- **Use wiki-links** for navigation — don't read everything linearly
- **Cross-reference concepts**: risk management connects to position sizing, psychology connects to all strategies
- **Progressive disclosure**: Show overview first, details only when needed

## Reference

- **Graph location:** `skills/trading-graph/INDEX.md`
- **Main docs:** `skills/README.md`
- **Agent guide:** `skills/AGENT-GUIDE.md`
- **Creation guide:** `skills/skill-graph-creation/SKILL.md`

## Summary

The trading graph provides structured knowledge for trading decisions. Access via `skills/trading-graph/INDEX.md` and navigate using wiki-links.

This skill is a **wrapper** that provides access to trading knowledge graph files.
