---
description: "Расчет размера позиции и управление капиталом"
version: "1.0.0"
tags: ["position-sizing", "capital-management", "core"]
related: ["risk-management", "risk-reward-ratio", "portfolio-diversification"]
---

# Position Sizing

## Overview

Position sizing determines how much of your capital to allocate to a single trade. It's the bridge between [[risk-management]] principles and actual trade execution. Get this wrong, and nothing else matters.

## Core Formula

### Fixed Fractional Method

`Position Size = (Account Value × Risk %) / (Entry - Stop Loss)`

**Example:**
- Account: $10,000
- Risk: 1% = $100
- Entry: $50
- Stop Loss: $48 (2-point difference)

`Position Size = $100 / $2 = 50 shares`

**Total Position Value = 50 × $50 = $2,500 (25% of account)**

### Volatility-Adjusted Sizing

For highly volatile assets, reduce position size:

`Position Size = Base Size × (1 - Volatility Adjustment)`

Where Volatility Adjustment is based on ATR (Average True Range) or historical volatility.

## Key Components

### 1. Risk Per Trade

Standard: 1-2% of account
- New traders: 0.5-1% (preservation focused)
- Experienced: 1-2% (growth focused)
- Pros: 2-3% in their edge zone

See [[risk-management]] for 1% rule details.

### 2. Stop Loss Distance

Wider stops = smaller positions
- Too tight → Stopped out on noise
- Too wide = Too much risk
- Balance with ATR and [[technical-analysis]]

### 3. [[Risk-Reward-Ratio]]

Higher R:R allows smaller positions for same profit potential
- 2:1 ratio = can risk 1% to make 2%
- 3:1 ratio = even better economics

## Position Sizing Strategies

### Equal Dollar Amount

Allocate equal dollar amount to each position:
- Pros: Simple, clear risk
- Cons: Doesn't account for volatility differences

### Equal Risk Amount

Risk equal dollar amount on each trade:
- Pros: Consistent risk per trade
- Cons: Requires good stop loss placement

### Volatility-Parity

Size positions inversely to volatility:
- Pros: Smooths portfolio volatility
- Cons: More complex calculation

## Portfolio-Level Considerations

### Concentration Risk

Never allocate more than 20-25% to a single sector or asset class. See [[portfolio-diversification]].

### Correlation Risk

Two highly correlated positions = one bigger position
- Example: Two tech stocks = double sector exposure
- Solution: Diversify across sectors or hedge

### Timeframe Alignment

Position size should match:
- Day trading: Smaller, more frequent trades
- Swing trading: Moderate positions
- Long-term investing: Larger, fewer trades

## Common Mistakes

1. **Ignoring volatility** — Same dollar amount in calm vs volatile assets
2. **No stop loss** — Position size becomes undefined risk → See [[stop-loss-strategies]]
3. **Overleveraging** — Using margin to size beyond cash capacity
4. **Averaging down** — Adding to losers = increasing risk, not reducing

## Quick Reference Table

| Account | Risk (1%) | Stop ($/share) | Max Shares |
|---------|----------|----------------|------------|
| $10,000 | $100     | $1.00          | 100        |
| $10,000 | $100     | $2.00          | 50         |
| $10,000 | $100     | $5.00          | 20         |

## When to Adjust

- **After winning streak** → Consider slightly increasing (but keep 1% rule)
- **After losing streak** → Reduce to 0.5% until confidence returns
- **Market regime change** → Adjust for new volatility levels

## Integration

Position sizing connects to everything:
- [[risk-management]] — Provides the risk percentage
- [[risk-reward-ratio]] — Determines efficiency of position
- [[market-psychology]] — Emotions affect sizing discipline
- [[technical-analysis]] — Entry/exit defines stop loss distance
