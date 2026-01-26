"""
Update index.html daily schedule to only show dates with actual underdog competitions.
Uses line-by-line parsing to safely replace only the day-tabs section.
"""

import json
from pathlib import Path
from datetime import datetime

base_path = Path(__file__).parent

# Load the schedule to get actual active dates
with open(base_path / 'data' / 'daily_underdog_schedule_2026.json', 'r', encoding='utf-8') as f:
    schedule = json.load(f)

# Get all dates that have underdog nations
active_dates = sorted(schedule.keys())

print(f"Found {len(active_dates)} days with underdog competition")
print(f"First day: {active_dates[0]}, Last day: {active_dates[-1]}\n")

# Read the index.html
index_path = base_path / 'index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the day-tabs section
# Strategy: Find the opening <div class="day-tabs"> and replace everything until its closing </div>

import_start = content.find('<div class="day-tabs">')
if import_start == -1:
    print("ERROR: Could not find day-tabs opening")
    exit(1)

# Find the matching closing </div> for day-tabs
# Count divs to find the matching close
div_count = 1
search_start = import_start + len('<div class="day-tabs">')
search_pos = search_start

while div_count > 0 and search_pos < len(content):
    next_open = content.find('<div', search_pos)
    next_close = content.find('</div>', search_pos)
    
    if next_close == -1:
        print("ERROR: Could not find matching closing </div>")
        exit(1)
    
    if next_open != -1 and next_open < next_close:
        div_count += 1
        search_pos = next_open + 1
    else:
        div_count -= 1
        search_pos = next_close + 6
        if div_count == 0:
            import_end = next_close + 6
            break

# Build the replacement HTML
tabs_html = '<div class="day-tabs">\n'
for date in active_dates:
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    date_str = date_obj.strftime('%b %d')
    tabs_html += f'<div class="day-tab" data-day="{date}">{date_str}</div>\n'
tabs_html += '</div>'

# Replace the old section with new
new_content = content[:import_start] + tabs_html + content[import_end:]

# Write back
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✓ Updated day-tabs section with only active dates")
print(f"✓ Shows {len(active_dates)} active competition days from {active_dates[0]} to {active_dates[-1]}")
