#!/usr/bin/env python3
"""Remove orphaned day-content CSS and JavaScript references"""

# Read the file
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Process lines to remove those with .day-content references
output_lines = []
skip_block = False

for i, line in enumerate(lines):
    # Check if this line has day-content CSS
    if '.day-content {' in line or '.day-content.active {' in line:
        # Skip this line and the next closing brace
        skip_block = True
        continue
    
    # Check if we're in a CSS block to skip
    if skip_block:
        if '}' in line:
            skip_block = False
        continue
    
    # Check if this line has .day-content JavaScript 
    if ".day-content" in line and "querySelectorAll" in line:
        continue
    
    # Also skip day-tab references since there's no schedule section anymore
    if ".day-tab" in line and ("querySelectorAll" in line or "{" in line):
        if "forEach" in line or "{" in line:
            skip_block = True
        continue
    
    output_lines.append(line)

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"Removed orphaned CSS/JS references")
print(f"Original: {len(lines)} lines")
print(f"New: {len(output_lines)} lines")

# Verify
remaining = sum(1 for line in output_lines if 'day-content' in line or 'day-tab' in line)
print(f"Remaining references: {remaining}")
