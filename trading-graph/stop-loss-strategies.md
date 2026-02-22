---
description: "Стратегии размещения и управления стоп-лоссами"
version: "1.0.0"
tags: ["risk", "execution", "core"]
related: ["risk-management", "risk-reward-ratio", "position-sizing"]
---

# Stop Loss Strategies

## Overview

Stop loss is your insurance policy. It defines the maximum loss you're willing to accept on a trade. Without it, no [[risk-management]] system works. Position size is undefined, and risk is unlimited.

## Types of Stop Losses

### 1. Percentage Stop

Stop at fixed percentage from entry:
- Entry: $100
- Stop: $95 (5% stop)

**Pros:** Simple, easy to calculate [[position-sizing]]
**Cons:** Ignores market structure and volatility

### 2. Volatility Stop (ATR-Based)

Stop based on Average True Range:
- Calculate 14-period ATR
- Set stop at Entry ± (2×ATR)

**Pros:** Accounts for market volatility
**Cons:** More complex calculation

### 3. Technical Stop

Stop at key technical levels:
- Below support for longs
- Above resistance for shorts
- Below recent swing low

**Pros:** Respects market structure
**Cons:** Can be too wide or too tight

### 4. Time-Based Stop

Exit if trade doesn't work within X bars:
- "If not profitable in 10 bars, exit"

**Pros:** Prevents capital tying in dead trades
**Cons:** May exit before move develops

## Placement Strategies

### Support/Resistance Stops

Place stops just beyond key levels:

```
$50 ━━━━━━━━━ Resistance
$48 ━━━━━━━━━ Entry
$46 ━━━━━━━━━ Support
$45 ━━━━━━━━━ Stop (just below support)
```

### Swing High/Low Stops

For longs: Below most recent swing low
For shorts: Above most recent swing high

**Pros:** Respects market structure
**Cons:** Can be wide in volatile markets

### ATR Multiple Stops

`Stop = Entry ± (N × ATR)`

Where N is your multiple:
- Conservative: 2×ATR
- Moderate: 1.5×ATR
- Aggressive: 1×ATR

See [[technical-analysis]] for ATR calculation.

## Common Mistakes

### 1. Too Tight Stops

Stops that get hit by normal volatility:
- Market wiggles, hits stop, then moves in your direction
- Repeated small losses add up

**Solution:** Use ATR-based or technical stops, not arbitrary percentages.

### 2. No Hard Stop

" mental stops only" — you'll move it when price approaches:
- "It's just a little further, I can handle it"
- "It will bounce back from here"
- [[emotional-control]] fails, loss grows

**Rule:** Always use hard, automatic stops.

### 3. Moving Stops in Wrong Direction

For longs, moving stop **down** as price approaches:
- Turns small loss into big loss
- No [[risk-management]]可言

**Rule:** Only move stops in direction of trade (trail stop).

## Trailing Stops

Moving stop to protect profits as trade develops:

### Fixed Trailing Stop

Maintain fixed distance from price:
- Long: Stop at Price - $5
- Short: Stop at Price + $5

**Pros:** Simple, locks in profit
**Cons:** Can exit too early in volatile moves

### Percentage Trailing Stop

Maintain fixed percentage:
- Long: Stop at Price × 0.95 (5% trail)
- Short: Stop at Price × 1.05

**Pros:** Scales with price
**Cons:** Same as fixed trail issues

### Swing Trailing Stop

Move stop to recent swing lows (longs):
```python
As price makes new highs:
    Update stop to most recent swing low
```

**Pros:** Respects market structure
**Cons:** Can give back more profit

## Stop Loss vs [[Risk-Reward-Ratio]]

Your stop loss determines your R:R:

```
Entry: $100
Stop: $95 (Risk: $5)
Target: $110 (Profit: $10)
R:R = $10 / $5 = 2:1 ✓
```

```
Entry: $100
Stop: $98 (Risk: $2)
Target: $110 (Profit: $10)
R:R = $10 / $2 = 5:1 ✓✓
```

**Lesson:** Tighter stops = Better R:R (if not too tight).

## When to Use Each Type

| Market Condition | Recommended Stop Type |
|------------------|----------------------|
| Trending, low volatility | Trailing stop on swing lows |
| Ranging, choppy | Volatility stop (ATR) |
| Breakout trades | Technical stop below breakout level |
| News events | Wider stops to account for volatility |

## Stop Loss Management

### Never Move Stop Against Trade

For longs, never lower stop:
- Original: $95
- Current price: $92
- "I'll move stop to $88" ❌

This turns potential -$3 loss into guaranteed -$12 loss.

### Trail Stop With Profit

Once profitable, protect gains:
```
Entry: $100
Stop: $95

Price moves to $110
Trail stop to $105 (protecting $5 profit)

Price reverses, exits at $105
Net: +$5 instead of -$5
```

## Quick Reference

| Setup | Stop Type | R:R Target |
|-------|----------|------------|
| Breakout | Below breakout level | 2:1 to 3:1 |
| Pullback | Below support | 2:1 to 2.5:1 |
| Trend following | Trailing on swings | 3:1 to 5:1 |
| Mean reversion | Beyond extreme | 1:1 to 1.5:1 |

## Common Questions

### Q: Can I use no stop loss?

**A:** Only if you're:
- Holding for very long term
- Willing to accept 50%+ drawdowns
- Not using leverage

Otherwise, **always use stops**.

### Q: Should I widen my stop loss?

**A:** Only if:
- Volatility has increased (check ATR)
- Your setup analysis supports it
- You're adjusting [[position-sizing]] accordingly

Never widen to avoid taking a loss.

### Q: Can I use mental stops?

**A:** Only for experienced traders with:
- Perfect [[emotional-control]]
- Ability to execute instantly
- Proven track record

For everyone else: **automatic stops**.

## Integration

Stop loss strategies connect to:
- [[risk-management]] — Defining your risk
- [[risk-reward-ratio]] — Determining your economics
- [[position-sizing]] — Affecting position calculation
- [[market-psychology]] — Managing exit emotions
- [[technical-analysis]] — Finding optimal placement

## Final Rules

1. **Always have a stop** — No exceptions
2. **Never move it against you** — Only trail in profit
3. **Use automatic stops** — Not mental stops
4. **Respect volatility** — ATR-based when needed
5. **Know your R:R** — Before entering trade

Your stop loss is your last line of defense.

Use it wisely.
