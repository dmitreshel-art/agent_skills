---
name: roborock
description: Control Roborock robot vacuums via local API. Use when user needs to start/stop cleaning, check status, change fan speed, or perform specific cleaning tasks on a Roborock robot vacuum.
---

# Roborock Robot Vacuum Control

Control Roborock robot vacuums through local API (Mi Home integration). Supports start/stop cleaning, fan speed control, zone cleaning, and status monitoring.

## Prerequisites

### Requirements

```bash
pip install mirobo
```

### Get Robot Credentials

**To use this skill, you need:**

1. **Robot IP Address** - Find in your router's DHCP table or Mi Home app
2. **Robot Token** - Get from Mi Home app:

**Getting the token:**

1. Install Mi Home app on Android
2. Add your Roborock device
3. Use Token Extractor app or method:
   - Android: Use token extractor app
   - Alternative: Extract from Mi Home app data

**Token extractors (search web):**
- "Mi Home token extractor Android"
- "Xiaomi cloud token extractor"

## Commands

### Basic Commands

**Start cleaning:**
```bash
python3 scripts/roborock_cli.py <host> <token> start
```

**Stop cleaning:**
```bash
python3 scripts/roborock_cli.py <host> <token> stop
```

**Pause cleaning:**
```bash
python3 scripts/roborock_cli.py <host> <token> pause
```

**Resume cleaning:**
```bash
python3 scripts/roborock_cli.py <host> <token> resume
```

**Get status:**
```bash
python3 scripts/roborock_cli.py <host> <token> status
```

**Find robot (make beep):**
```bash
python3 scripts/roborock_cli.py <host> <token> find_me
```

### Advanced Commands

**Set fan speed:**
```bash
python3 scripts/roborock_cli.py <host> <token> fan_speed quiet|balanced|turbo|max
```

**Clean zone:**
```bash
python3 scripts/roborock_cli.py <host> <token> clean_zone x1,y1,x2,y2
```

**Clean spot:**
```bash
python3 scripts/roborock_cli.py <host> <token> clean_spot x,y
```

## Fan Speed Levels

- `quiet` - Lowest noise, 38% power
- `balanced` - Standard cleaning, 60% power
- `turbo` - High power, 77% power
- `max` - Maximum power, 90% power

## Status Information

The `status` command returns:
- `state` - Current state (cleaning, paused, charging, etc.)
- `battery` - Battery percentage (0-100)
- `error` - Error code if any
- `cleaning_area` - Area cleaned (m²)
- `cleaning_time` - Cleaning duration (minutes)

## Usage Examples

**Example 1: Start cleaning**
```bash
python3 scripts/roborock_cli.py 192.168.1.100 abc123def456 start
```

**Example 2: Set fan speed to quiet mode**
```bash
python3 scripts/roborock_cli.py 192.168.1.100 abc123def456 fan_speed quiet
```

**Example 3: Check battery and status**
```bash
python3 scripts/roborock_cli.py 192.168.1.100 abc123def456 status
```

## Troubleshooting

**Connection refused:**
- Check robot IP address
- Ensure device is on same network
- Verify token is correct

**Token invalid:**
- Extract token again from Mi Home app
- Token format should be alphanumeric string

**Module not found (mirobo):**
```bash
pip install mirobo
```
