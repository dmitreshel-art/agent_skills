#!/usr/bin/env python3
"""
Validate YAML frontmatter in skill files

This script checks that all skill files have valid YAML frontmatter
with required fields: description, version, tags, related.
"""

import yaml
import os
import sys

def validate_frontmatter(directory):
    """Verify all skills have required YAML fields"""
    required_fields = ['description', 'version', 'tags', 'related']
    issues = []
    files_checked = 0
    
    for file in os.listdir(directory):
        if not file.endswith('.md'):
            continue
        
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for YAML delimiters
        if not content.startswith('---'):
            issues.append(f"{file}: No YAML frontmatter")
            continue
        
        # Find YAML end
        yaml_end = content.find('---', 3)
        if yaml_end == -1:
            issues.append(f"{file}: Incomplete YAML frontmatter")
            continue
        
        # Parse YAML
        yaml_content = content[3:yaml_end]
        
        try:
            data = yaml.safe_load(yaml_content)
            files_checked += 1
            
            # Check required fields
            missing = [field for field in required_fields if field not in data]
            
            if missing:
                issues.append(f"{file}: Missing fields: {missing}")
            
            # Check field formats
            if 'tags' in data:
                if not isinstance(data['tags'], list):
                    issues.append(f"{file}: Tags must be a list")
            
            if 'related' in data:
                if not isinstance(data['related'], list):
                    issues.append(f"{file}: Related must be a list")
                    
        except yaml.YAMLError as e:
            issues.append(f"{file}: Invalid YAML - {e}")
        except Exception as e:
            issues.append(f"{file}: Error - {e}")
    
    if issues:
        print(f"❌ YAML Frontmatter Issues:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"✅ All {files_checked} files have valid YAML frontmatter")
        return True

if __name__ == '__main__':
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    success = validate_frontmatter(directory)
    sys.exit(0 if success else 1)
