---
description: "Управление рисками и позициями в трейдинге"
version: "1.0.0"
tags: ["risk", "fundamentals", "core"]
related: ["position-sizing", "risk-reward-ratio", "stop-loss-strategies"]
---

# Risk Management

## Overview

Risk management is the most critical skill in trading. Without it, even the best strategies will eventually blow up. Think of it as survival — you can't make money if you're out of the game.

## Core Principles

### 1% Rule (Per Trade)

Never risk more than 1-2% of your account on a single trade. This ensures that even a string of losses won't cripple your capital.

### The Kelly Criterion

Optimal position sizing formula: `f* = (bp - q) / b`

Where:
- `f*` = fraction of bankroll to wager
- `b` = odds received
- `p` = probability of winning
- `q` = probability of losing (1 - p)

**Warning:** Most traders use half-Kelly to account for estimation errors.

### Expectancy

`Expectancy = (Win% × Avg Win) - (Loss% × Avg Loss)`

Positive expectancy = long-term profitability. Negative expectancy = gambling.

See [[position-sizing]] for practical sizing calculations.

## Common Mistakes

1. **Overtrading** — Too many positions dilutes focus and increases [[risk-reward-ratio]] pressure
2. **Revenge trading** — Trying to recover losses quickly leads to bigger losses, see [[emotional-control]]
3. **No hard stop** — Markets can move faster than you can think

## Integration

Risk management connects to everything:

- [[market-psychology]] — Fear prevents proper risk-taking, greed causes over-risking
- [[technical-analysis]] — Entry/exit signals define risk parameters
- [[position-sizing]] — Risk percentage → position size calculation

## Quick Reference

| Account Size | Max Risk (1%) | Position Size (Example) |
|--------------|--------------|------------------------|
| $10,000      | $100         | Depends on [[risk-reward-ratio]] |
| $50,000      | $500         | Adjust based on volatility |
| $100,000     | $1,000       | Scale proportionally |

## When to Reassess

- After 5 consecutive losses → Reduce position size
- After reaching new equity high → Re-evaluate risk tolerance
- Market regime change → Adjust risk parameters

See [[portfolio-diversification]] for portfolio-level risk management.
