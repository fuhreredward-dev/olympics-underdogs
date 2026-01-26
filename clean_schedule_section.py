#!/usr/bin/env python3
"""Remove the entire daily schedule section from index.html"""

# Read the file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start of the schedule section
start_marker = '<section class="section">\n<h2>📅 Daily Competition Schedule & Underdog Nations</h2>'
start_idx = content.find(start_marker)

if start_idx == -1:
    print("Could not find schedule section start")
    exit(1)

# Find the end - look for the first </section> that closes this opening
# Count sections from the start marker position
depth = 1
i = start_idx + len(start_marker)
end_idx = None

while i < len(content) and depth > 0:
    if content[i:i+18] == '<section class="section">':
        depth += 1
        i += 18
    elif content[i:i+10] == '</section>':
        depth -= 1
        if depth == 0:
            end_idx = i + 10
            break
        i += 10
    else:
        i += 1

if end_idx is None:
    print("Could not find matching closing tag for schedule section")
    exit(1)

print(f"Found schedule section from {start_idx} to {end_idx}")
print(f"Removing {end_idx - start_idx} characters (~{(end_idx - start_idx)//50} lines)")

# Remove the section
new_content = content[:start_idx] + content[end_idx:]

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully removed schedule section from index.html")

# Verify
with open('index.html', 'r', encoding='utf-8') as f:
    new_lines = f.readlines()

print(f"New file has {len(new_lines)} lines")

# Check for any orphaned day-content divs
orphaned = sum(1 for line in new_lines if 'day-content' in line)
print(f"Orphaned day-content references: {orphaned}")


