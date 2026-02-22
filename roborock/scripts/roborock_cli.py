#!/usr/bin/env python3
"""
Roborock Robot Vacuum Controller
Command-line interface for controlling Roborock robot vacuums.

Requirements:
    pip install mirobo

Usage:
    python3 roborock_cli.py <host> <token> <command> [args]
"""

import sys
import json
import argparse
from mirobo import Roborock

def main():
    parser = argparse.ArgumentParser(description='Control Roborock robot vacuum')
    parser.add_argument('host', help='Robot IP address or hostname')
    parser.add_argument('token', help='Robot token from Mi Home')
    parser.add_argument('command', choices=[
        'start', 'stop', 'pause', 'resume', 'status', 
        'find_me', 'fan_speed', 'clean_zone', 'clean_spot'
    ], help='Command to execute')
    parser.add_argument('args', nargs='*', help='Additional arguments for command')
    
    args = parser.parse_args()
    
    try:
        robot = Roborock(args.host, args.token)
        
        commands = {
            'start': cmd_start,
            'stop': cmd_stop,
            'pause': cmd_pause,
            'resume': cmd_resume,
            'status': cmd_status,
            'find_me': cmd_find_me,
            'fan_speed': cmd_fan_speed,
            'clean_zone': cmd_clean_zone,
            'clean_spot': cmd_clean_spot,
        }
        
        if args.command in commands:
            result = commands[args.command](robot, args.args)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def cmd_start(robot, args):
    """Start cleaning"""
    result = robot.start()
    return {"command": "start", "status": "success", "result": result}

def cmd_stop(robot, args):
    """Stop cleaning"""
    result = robot.stop()
    return {"command": "stop", "status": "success", "result": result}

def cmd_pause(robot, args):
    """Pause cleaning"""
    result = robot.pause()
    return {"command": "pause", "status": "success", "result": result}

def cmd_resume(robot, args):
    """Resume cleaning"""
    result = robot.resume()
    return {"command": "resume", "status": "success", "result": result}

def cmd_status(robot, args):
    """Get robot status"""
    status = robot.status()
    # Extract useful information
    return {
        "command": "status",
        "status": "success",
        "data": {
            "state": status.state,
            "battery": status.battery,
            "error": status.error,
            "cleaning_area": status.clean_area,
            "cleaning_time": status.clean_time
        }
    }

def cmd_find_me(robot, args):
    """Locate robot (make it beep)"""
    result = robot.find_me()
    return {"command": "find_me", "status": "success", "result": result}

def cmd_fan_speed(robot, args):
    """Set fan speed (quiet, balanced, turbo, max)"""
    if not args:
        return {"command": "fan_speed", "status": "error", "message": "Speed level required"}
    
    speed = args[0].lower()
    speed_map = {
        'quiet': 38,
        'balanced': 60,
        'turbo': 77,
        'max': 90
    }
    
    if speed not in speed_map:
        valid = ', '.join(speed_map.keys())
        return {
            "command": "fan_speed", 
            "status": "error", 
            "message": f"Invalid speed. Use: {valid}"
        }
    
    result = robot.set_fan_speed(speed_map[speed])
    return {"command": "fan_speed", "status": "success", "speed": speed, "result": result}

def cmd_clean_zone(robot, args):
    """Clean specific zone (requires zone coordinates)"""
    if len(args) < 4:
        return {
            "command": "clean_zone",
            "status": "error",
            "message": "Zone coordinates required: x1,y1,x2,y2"
        }
    
    # Parse coordinates
    coords = [int(x) for x in ','.join(args[:4]).split(',')]
    result = robot.zoned_clean([coords])
    return {"command": "clean_zone", "status": "success", "zone": coords, "result": result}

def cmd_clean_spot(robot, args):
    """Clean specific spot"""
    if len(args) < 2:
        return {
            "command": "clean_spot",
            "status": "error",
            "message": "Spot coordinates required: x,y"
        }
    
    coords = [int(args[0]), int(args[1])]
    result = robot.spot_clean(coords)
    return {"command": "clean_spot", "status": "success", "spot": coords, "result": result}

if __name__ == '__main__':
    main()
