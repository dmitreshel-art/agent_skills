#!/usr/bin/env python3
"""
Remove template wiki-links from skill graph files

This script removes template/dummy wiki-links like [[skill]], [[skill-name]], etc.
while preserving real cross-graph links like [[clean-code]], [[refactoring]], etc.
"""

import re
import os

# Template links to remove (these are dummies, not real references)
TEMPLATE_LINKS = [
    '[[skill]]',
    '[[skill-name]]',
    '[[skill-1]]',
    '[[skill-2]]',
    '[[skill-3]]',
    '[[skill-4]]',
    '[[skill-5]]',
    '[[writing-moc]]',
    '[[structure-moc]]',
    '[[{link}]]',
    '[[{target}]]',
    '[[non-existent]]',
    '[[wiki-links]]',  # Should be [[linking-strategies]]
]

def clean_template_links(directory):
    """Remove template wiki-links from all markdown files"""
    files_cleaned = 0
    links_removed = 0
    
    for file in os.listdir(directory):
        if not file.endswith('.md'):
            continue
        
        file_path = os.path.join(directory, file)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_length = len(content)
        
        # Remove each template link
        for template in TEMPLATE_LINKS:
            count = content.count(template)
            if count > 0:
                content = content.replace(template, '')
                links_removed += count
    
        # Also clean up variations with whitespace
        content = re.sub(r'\[\s*\{link\}\s*\]', '', content)
        content = re.sub(r'\[\s*\{target\}\s*\]', '', content)
        
        if len(content) != original_length:
            # Only write if changes were made
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            files_cleaned += 1
    
    print(f"✅ Cleaned {files_cleaned} files")
    print(f"✅ Removed {links_removed} template links")
    return files_cleaned > 0

def find_existing_skills(directory):
    """Find all existing skill files for validation"""
    return set(f.replace('.md', '') for f in os.listdir(directory) if f.endswith('.md'))

def validate_after_cleanup(directory):
    """Run validation after cleanup to ensure all links are valid"""
    import subprocess
    
    print("\n🔍 Running validation after cleanup...")
    
    link_validator = os.path.join(os.path.dirname(directory), 'validation-scripts', 'link-validator.py')
    
    result = subprocess.run(
        ['python3', link_validator, directory],
        capture_output=True,
        text=True
    )
    
    if 'All' in result.stdout:
        print("✅ Validation passed - no broken links!")
        return True
    else:
        print("⚠️  Validation still has issues")
        return False

if __name__ == '__main__':
    import sys
    
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    if not os.path.isdir(directory):
        print(f"❌ Error: {directory} is not a directory")
        sys.exit(1)
    
    print(f"🧹 Cleaning template links from: {directory}")
    print("=" * 50)
    
    changed = clean_template_links(directory)
    
    print("=" * 50)
    
    if changed:
        validate_after_cleanup(directory)
    else:
        print("✓ No changes needed")
