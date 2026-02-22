#!/usr/bin/env python3
"""
Find skills not referenced by anyone

This script detects orphaned skill files that are not referenced
by any other skills in the graph (except INDEX.md which is the entry point).
"""

import re
import os
import sys

def find_orphans(directory):
    """Find skills not referenced by anyone"""
    files = set(f.replace('.md', '') for f in os.listdir(directory) if f.endswith('.md'))
    references = {f: set() for f in files}
    
    for file in os.listdir(directory):
        if not file.endswith('.md'):
            continue
        
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all wiki-links
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        
        source = file.replace('.md', '')
        
        # Track references (only to existing skills)
        for link in links:
            if link in files:
                references[link].add(source)
    
    # Find orphaned files (not referenced by anyone, except INDEX)
    orphans = sorted([f for f in files if len(references[f]) == 0 and f != 'INDEX'])
    
    if orphans:
        print(f"❌ Orphaned Skills ({len(orphans)}):")
        for orphan in orphans:
            ref_count = len(references.get(orphan, []))
            print(f"  - {orphan}.md (ссылаются {ref_count} файлов(а))")
        return False
    else:
        print(f"✅ No orphaned skills")
        
        # Show reference statistics
        print(f"\n📊 Связи:")
        for file in sorted(files):
            if file == 'INDEX':
                refs = list(references.get('INDEX', []))
                print(f"  INDEX → {', '.join(refs[:5])}...")
            else:
                ref_count = len(references.get(file, []))
                if ref_count > 0:
                    print(f"  {file} → ссылаются {ref_count} файлов(а)")
        
        return True

if __name__ == '__main__':
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    success = find_orphans(directory)
    sys.exit(0 if success else 1)
