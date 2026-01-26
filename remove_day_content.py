#!/usr/bin/env python3
"""Remove all remaining day-content divs from index.html"""
import re

# Read the file
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and remove lines containing day-content divs and everything until matching close
output_lines = []
skip_until_close = 0

for i, line in enumerate(lines):
    # Skip lines if we're in a day-content section
    if skip_until_close > 0:
        skip_until_close -= line.count('</div>')
        continue
    
    # Check if this line starts a day-content div
    if 'class="day-content" id="day-' in line:
        # Count opening and closing divs in this line
        skip_until_close = line.count('<div') - line.count('</div>') - 1
        # Also skip lines until we find 2 closing </div> tags (for outer structure)
        skip_until_close = 3  # We need to skip this line + all nested + 2 closing divs
        continue
    
    output_lines.append(line)

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f'Successfully removed all remaining day-content fragments')

