---
description: "Отношение риск/прибыль и его влияние на торговлю"
version: "1.0.0"
tags: ["risk", "fundamentals", "core"]
related: ["risk-management", "position-sizing", "stop-loss-strategies"]
---

# Risk-Reward Ratio

## Overview

Risk-reward ratio (R:R) measures how much you're risking to make how much profit. It's the fundamental economics of every trade. Get this wrong, and even good [[position-sizing]] won't save you.

## The Formula

```
Risk-Reward Ratio = Potential Profit / Potential Risk
```

**Example:**
- Entry: $100
- Stop Loss: $95 (Risk: $5)
- Target: $110 (Profit: $10)

`R:R = $10 / $5 = 2:1`

For every $1 risked, you make $2 if correct.

## Why It Matters

### The Math of Win Rate

**Scenario A: 2:1 R:R, 40% Win Rate**

10 trades × $100 risk each = $1,000 total risk

Wins: 4 × $200 profit = $800
Losses: 6 × $100 loss = $600

**Net: +$200**

### Scenario B: 0.5:1 R:R, 60% Win Rate**

10 trades × $100 risk each = $1,000 total risk

Wins: 6 × $50 profit = $300
Losses: 4 × $100 loss = $400

**Net: -$100**

**Lesson:** High R:R beats high win rate (within reason).

## Optimal R:R Targets

| Strategy | Typical R:R | Win Rate Range | Notes |
|----------|-------------|----------------|-------|
| Day trading | 1.5:1 to 2:1 | 40-50% | Short-term moves |
| Swing trading | 2:1 to 3:1 | 40-45% | Medium-term holds |
| Trend following | 3:1 to 5:1 | 30-40% | Ride big moves |
| Mean reversion | 1:1 to 1.5:1 | 55-65% | Smaller, frequent wins |

## Common Mistakes

### 1. Ignoring Win Rate Context

2:1 R:R sounds great, but if your win rate is 20%, you'll lose:
- 10 trades × $100 risk
- 2 wins × $200 = $400
- 8 losses × $100 = $800
- **Net: -$400**

**Rule:** Never assume high R:R compensates for terrible win rate.

### 2. Unrealistic Targets

Setting targets the market rarely hits:
- "I'll take 5:1 on this!"
- Market moves 1.5:1 then reverses

Result: Missed profits, or worse, losses when reverses happen.

### 3. Variable R:R Without Tracking

Taking 1:1 trades, then 3:1 trades, mixing them:
- How do you know what's working?
- Can't improve systematically

**Solution:** Track each setup type separately.

## Position Sizing with R:R

### Fixed Dollar Risk

Regardless of R:R, risk the same dollar amount:
```python
# Always risk $100 per trade
if R:R == 2:1:
    # Make $200 if correct
elif R:R == 0.5:1:
    # Make $50 if correct (don't take this!)
```

### Risk-Adjusted Expectancy

`Expectancy = (Win% × R:R) - Loss%`

For profitable trading:
- 40% win rate, 2:1 R:R = 0.4×2 - 0.6 = 0.2 ✓
- 60% win rate, 0.5:1 R:R = 0.6×0.5 - 0.4 = -0.1 ✗

## When to Adjust R:R

### Lower R:R (1:1 to 1.5:1) When:
- High win rate strategy (mean reversion)
- Very liquid market with tight spreads
- Scalping or very short-term trades

### Higher R:R (2:1 to 3:1) When:
- Trend following strategies
- Lower win rate strategies
- Volatile markets with bigger moves

### Avoid (< 1:1):
- Rarely makes sense mathematically
- Unless you have extremely high win rate (75%+)
- Usually indicates poor [[risk-management]]

## Quick Reference

| R:R | Min Win Rate | Example |
|-----|--------------|---------|
| 0.5:1 | 67% | High frequency scalping |
| 1:1 | 50% | Balanced approach |
| 1.5:1 | 40% | Day trading |
| 2:1 | 33% | Swing trading |
| 3:1 | 25% | Trend following |

## Integration

Risk-reward ratio connects to:
- [[risk-management]] — Defines your risk per trade
- [[position-sizing]] — Determines position efficiency
- [[stop-loss-strategies]] — Stop placement affects R:R
- [[technical-analysis]] — Entry/exit define R:R parameters

## Common Setups and Their R:R

### Breakout Trading
- Enter on breakout
- Stop below breakout level
- Target at measured move
- **Typical R:R:** 2:1 to 3:1

### Pullback to Support
- Enter on bounce
- Stop below support
- Target at resistance
- **Typical R:R:** 2:1 to 2.5:1

### Mean Reversion
- Enter at extremes
- Stop beyond extreme
- Target at mean
- **Typical R:R:** 1:1 to 1.5:1

## Tracking Your R:R

Keep a log:
```
Date | Setup | Entry | Stop | Target | R:R | Win/Loss
```

After 50+ trades, you'll know:
- What R:R works for your style
- Which setups have best R:R
- When to pass on low R:R trades

## Final Wisdom

> "Amateurs think about how much money they can make. Professionals think about how much money they can lose."

R:R is how you implement that thinking.

Always know your ratio before entering.

And respect it.

## Integration

See also:
- [[risk-management]] for overall risk framework
- [[position-sizing]] for how R:R affects position size
- [[stop-loss-strategies]] for stop placement optimization
- [[market-psychology]] for emotional aspects of holding for R:R
