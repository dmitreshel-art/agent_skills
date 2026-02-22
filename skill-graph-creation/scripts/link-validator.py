#!/usr/bin/env python3
"""
Validate all wiki-links point to existing files

This script checks that all wiki-links in skill files point to
files that actually exist in the skill graph or other graphs.
"""

import re
import os
import sys

def is_skill_file(filename):
    """Check if a file is a skill file (not INDEX/README)"""
    skill_exclusions = ['INDEX', 'README', 'AGENT-GUIDE']
    name = filename.replace('.md', '')
    return name not in skill_exclusions

def get_all_skill_files(base_path):
    """Get all skill files from all graphs in skill-graphs/"""
    all_skills = set()
    
    if not os.path.isdir(base_path):
        return all_skills
    
    # First, check for graph subdirectories
    if os.path.isdir(base_path):
        # Collect files from base path level
        for file in os.listdir(base_path):
            file_path = os.path.join(base_path, file)
            if file_path.endswith('-graph'):
                # This is a graph directory
                for subfile in os.listdir(file_path):
                    if subfile.endswith('.md') and is_skill_file(subfile):
                        all_skills.add(subfile.replace('.md', ''))
            elif file.endswith('.md') and is_skill_file(file):
                # Also collect skill files at base level (if any)
                all_skills.add(file.replace('.md', ''))
    
    return all_skills

def validate_wiki_links(directory):
    """Verify all wiki-links point to existing files"""
    base_path = os.path.dirname(os.path.dirname(directory))
    
    # Get current graph's skill files only
    current_files = set(f.replace('.md', '') for f in os.listdir(directory) 
                     if f.endswith('.md') and is_skill_file(f))
    
    all_skills = get_all_skill_files(base_path)
    
    all_links = []
    broken_links = []
    external_links = []
    
    for file in os.listdir(directory):
        if not file.endswith('.md'):
            continue
        
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all wiki-links
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        
        for link in links:
            all_links.append((file, link))
            
            # Check if linked file exists ANYWHERE (in this or other graphs)
            if link in all_skills:
                # Link exists in some graph - VALID
                if link in current_files:
                    # Link is in this graph - OK
                    pass
                else:
                    # Link is in another graph - cross-graph link, VALID
                    external_links.append((file, link))
            else:
                # Link doesn't exist anywhere - broken
                broken_links.append((file, link))
    
    if broken_links:
        print(f"❌ Broken Wiki-Links ({len(broken_links)}):")
        for source, target in broken_links:
            print(f"  - {source} → [[{target}]] (не найден)")
        return False
    else:
        if external_links:
            print(f"✅ All {len(all_links)} wiki-links valid")
            print(f"✅ {len(external_links)} cross-graph links to other graphs")
        else:
            print(f"✅ All {len(all_links)} wiki-links valid")
        
        # Show some examples
        if all_links:
            print(f"\n📊 Примеры связей:")
            for source, target in all_links[:10]:
                print(f"  {source} → [[{target}]]")
        
        return True

if __name__ == '__main__':
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    success = validate_wiki_links(directory)
    sys.exit(0 if success else 1)
