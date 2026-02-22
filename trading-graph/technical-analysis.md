---
description: "Технический анализ и паттерны в трейдинге"
version: "1.0.0"
tags: ["analysis", "technical", "patterns"]
related: ["risk-management", "risk-reward-ratio", "stop-loss-strategies"]
---

# Technical Analysis

## Overview

Technical analysis studies price action to identify trading opportunities. It provides the framework for your entries, exits, and [[stop-loss-strategies]]. Combined with proper [[risk-management]], technical analysis gives you an edge in the markets.

## Core Principles

### 1. Price Discounts Everything

All known information is reflected in price:
- News, earnings, economic data
- Market psychology
- Supply and demand

### 2. Price Moves in Trends

Trends persist until proven otherwise:
- Uptrend: Higher highs, higher lows
- Downtrend: Lower highs, lower lows
- Range: Price stuck between levels

### 3. History Repeats

Patterns repeat because human psychology repeats:
- Support and resistance
- Chart patterns
- Market cycles

## Key Concepts

### Support and Resistance

**Support:** Price level where buyers emerge
**Resistance:** Price level where sellers emerge

```python
Support levels become resistance when broken
Resistance levels become support when broken
```

See [[breakout-trading]] for trading these levels.

### Trends

**Uptrend:**
- Series of higher highs and higher lows
- Buy pullbacks to support
- Ride trend until broken

**Downtrend:**
- Series of lower highs and lower lows
- Sell rallies to resistance
- Ride trend until broken

**Range:**
- Price stuck between support and resistance
- Buy low, sell high
- Fade breakouts

### Volume

Price + Volume = True picture:
- **Up on high volume:** Strong, valid move
- **Up on low volume:** Weak, suspect move
- **Down on high volume:** Strong selling pressure
- **Down on low volume:** Weak selling

## Chart Patterns

### Reversal Patterns

**Head and Shoulders:**
- Top formation in uptrend
- Signal potential reversal
- Target below neckline

**Double Top/Bottom:**
- Two tests of same level
- Failed breakout attempt
- Reversal signal

**Wedges:**
- Converging trendlines
- Usually reverses against wedge direction
- Look for breakout opposite wedge

### Continuation Patterns

**Flags and Pennants:**
- Brief pause in trend
- High-volume breakout
- Continues original trend

**Triangles:**
- Converging trendlines
- Compression before big move
- Breakout direction hard to predict

### Candlestick Patterns

**Doji:** Indecision, potential reversal
**Hammer:** Bullish reversal at support
**Shooting Star:** Bearish reversal at resistance
**Engulfing:** Strong reversal signal

## Indicators

### Trend Indicators

**Moving Averages:**
- SMA: Simple moving average
- EMA: Exponential moving average (weights recent more)
- Golden cross: 50-day above 200-day (bullish)
- Death cross: 50-day below 200-day (bearish)

**MACD:**
- Trend + momentum indicator
- MACD line above signal = bullish
- MACD line below signal = bearish
- Divergence signals reversals

### Momentum Indicators

**RSI (Relative Strength Index):**
- 0-100 range
- Overbought above 70
- Oversold below 30
- Divergence signals reversal

**Stochastic:**
- 0-100 range
- Overbought above 80
- Oversold below 20
- Crosses signal entries/exits

### Volatility Indicators

**ATR (Average True Range):**
- Measures volatility
- Higher ATR = more volatility
- Used for [[stop-loss-strategies]]

**Bollinger Bands:**
- Volatility-based channels
- Price outside bands = extreme
- Bands contract before expansion

## Trading Setups

### Pullback to Moving Average

**Setup:**
- Price in uptrend
- Pulls back to 20/50 EMA
- Hold or bounces off EMA
- Volume supports bounce

**Entry:** At or near EMA
**Stop:** Below swing low
**Target:** Previous high or measured move

### Support Bounce

**Setup:**
- Price at known support
- Multiple tests respected
- Hold on support
- Volume drying up on sell-offs

**Entry:** At support
**Stop:** Below support
**Target:** Resistance level

### Breakout

**Setup:**
- Price consolidating
- Volume builds
- Breaks above/below consolidation
- Holds breakout

**Entry:** On breakout
**Stop:** Opposite side of consolidation
**Target:** Measured move

## Common Mistakes

### 1. Overcomplicating

Using too many indicators:
- 10+ indicators on chart
- Contradictory signals
- Analysis paralysis

**Solution:** Focus on 2-3 indicators that work for you.

### 2. Ignoring Price Action

Focusing only on indicators:
- "RSI is overbought, must sell!"
- But price keeps going up
- Missing big moves

**Solution:** Price action > Indicators.

### 3. No Context

Trading patterns in wrong market:
- Trying to trend trade in range
- Trying to fade breakout in trend
- Not reading market state

**Solution:** Check market conditions first.

## Timeframe Alignment

**Rule:** Trade in direction of higher timeframe

**Example:**
- Daily: Uptrend
- 4-hour: Pullback
- 1-hour: Entry signal

Only buy 1-hour pullback in uptrending market.

See [[breakout-trading]] for multi-timeframe strategies.

## Quick Reference

| Pattern | Bias | Typical R:R |
|---------|------|-------------|
| Pullback to MA | Trend direction | 2:1 to 2.5:1 |
| Support bounce | Reversal to upside | 2:1 to 3:1 |
| Breakout | Continuation | 2:1 to 3:1 |
| Mean reversion | Counter-trend | 1:1 to 1.5:1 |

## Integration

Technical analysis connects to:
- [[risk-management]] — Entry/exit define risk parameters
- [[risk-reward-ratio]] — Setup quality determines R:R
- [[stop-loss-strategies]] — Technical levels guide placement
- [[position-sizing]] — Volatility affects sizing
- [[market-psychology]] — Patterns reflect collective psychology

## Next Steps

See specific strategy skills:
- [[breakout-trading]] — Trading breakouts
- [[momentum-trading]] — Trading momentum
- [[mean-reversion]] — Trading reversals
- [[portfolio-diversification]] — Managing multiple positions

## Wisdom

> "The trend is your friend until the end when it bends."

Respect the trend.
Wait for your setup.
Follow your plan.

Technical analysis gives you the framework.
Discipline gives you the results.
