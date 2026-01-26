#!/usr/bin/env python3
"""Remove non-Denmark opponents from Ice Hockey and Curling events in schedule.html"""

import re

with open('schedule.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Use regex to find and fix Ice Hockey and Curling event cards
# Pattern: find event-card with data-sport="Ice Hockey" or data-sport="Curling"
# Then remove all nation-pill divs except the Denmark one

def remove_non_denmark_opponents(content):
    # Find all Ice Hockey and Curling event cards
    # Pattern: <div class="event-card" data-sport="Ice Hockey"> ... </div>
    pattern = r'(<div class="event-card" data-sport="(?:Ice Hockey|Curling)">.*?</div>\s*</div>)'
    
    def clean_event(match):
        event_html = match.group(1)
        
        # Find the nations-grid section
        grid_pattern = r'(<div class="nations-grid">)(.*?)(</div>\s*</div>\s*</div>)'
        
        def clean_grid(grid_match):
            start = grid_match.group(1)
            nations = grid_match.group(2)
            end = grid_match.group(3)
            
            # Extract only Denmark nation pills
            # Pattern: <div class="nation-pill ... data-nation="Denmark"> ... </div>
            denmark_pattern = r'<div class="nation-pill[^>]*data-nation="Denmark"[^>]*>.*?</div>'
            denmark_matches = re.findall(denmark_pattern, nations, re.DOTALL)
            
            if denmark_matches:
                cleaned_nations = '\n'.join(denmark_matches)
                return start + '\n' + cleaned_nations + '\n' + end
            else:
                return grid_match.group(0)
        
        return re.sub(grid_pattern, clean_grid, event_html, flags=re.DOTALL)
    
    return re.sub(pattern, clean_event, content, flags=re.DOTALL)

# Apply the cleaning
cleaned_content = remove_non_denmark_opponents(content)

# Write back to file
with open('schedule.html', 'w', encoding='utf-8') as f:
    f.write(cleaned_content)

print("✓ Removed non-Denmark opponents from Ice Hockey and Curling events!")
