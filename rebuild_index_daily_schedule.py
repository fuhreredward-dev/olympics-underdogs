"""
Rebuild the daily schedule section in index.html with accurate nation counts and events.
Only show nations that actually have events on each specific day.
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

base_path = Path(__file__).parent

# Load the actual schedule data
with open(base_path / 'data' / 'daily_underdog_schedule_2026.json', 'r', encoding='utf-8') as f:
    schedule = json.load(f)

# Load nation tiers for coloring
with open(base_path / 'data' / 'nation_tiers_2026.json', 'r', encoding='utf-8') as f:
    nation_tiers = json.load(f)

# Define tier colors (matching schedule.html)
tier_colors = {
    1: "#adff2f",  # Mild Underdogs
    2: "#98fb98",  # Moderate Underdogs
    3: "#90ee90",  # Strong Underdogs
    4: "#3cb371",  # Major Underdogs
    5: "#228b22"   # Ultimate Underdogs
}

def get_nation_color(nation):
    """Get the background color for a nation based on tier"""
    tier = nation_tiers.get(nation, 0)
    return tier_colors.get(tier, "#ccc")

# Read the index.html
index_path = base_path / 'index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find where the day-content sections start (after the day-tabs closing </div>)
day_tabs_end = content.find('</div>', content.find('<div class="day-tabs">')) + 6

# Find where the daily schedule section ends (before the next major section)
# Look for the closing of the daily-schedule-container
schedule_section_end = content.find('</div>', content.find('</div>', content.find('class="day-content"', day_tabs_end) + 100) + 100)

# Actually, let's find ALL day-content sections and replace them entirely
# Find the first day-content
first_day_content = content.find('<div class="day-content"', day_tabs_end)

# Find the last closing tag before the next major section
# Search for something distinctive that comes after all day-content sections
# Let's look for the footer or next section
next_section_marker = content.find('<footer', first_day_content)
if next_section_marker == -1:
    next_section_marker = content.find('</body>', first_day_content)

# Find the last day-content closing before that marker
last_day_content_end = content.rfind('</div>', first_day_content, next_section_marker)

# Build the new day-content sections
day_contents = []

for date in sorted(schedule.keys()):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    date_display = date_obj.strftime('%A, %B %d, %Y')
    
    # Get all events and nations for this day
    day_data = schedule[date]
    
    # Categorize sports by type (medal vs competition)
    # For simplicity, treat all as competition events
    sports = set()
    nations_by_status = {
        'confirmed': [],
        'probable': [],
        'maybe': []
    }
    
    for event_name, participants in day_data.items():
        # Extract sport from event name (e.g., "Biathlon - Men's 15km Mass Start" -> "Biathlon")
        sport = event_name.split(' - ')[0].strip()
        sports.add(sport)
        
        for participant in participants:
            nation = participant['nation']
            status = participant.get('status', 'unconfirmed')
            # Group unconfirmed with maybe
            if status == 'unconfirmed':
                status = 'maybe'
            # Keep duplicates to show nations competing in multiple events
            nations_by_status[status].append(nation)
    
    # Sort collections
    sports = sorted(sports)
    # Remove duplicates and sort nations within each status group
    for status in nations_by_status:
        nations_by_status[status] = sorted(set(nations_by_status[status]))
    
    # Build HTML for this day
    day_html = f'<div class="day-content" id="day-{date}">\n'
    day_html += f'<h3 style="color: #00d4ff; margin-bottom: 20px;">{date_display}</h3>\n'
    
    # Competition events section
    if sports:
        day_html += '<div class="sport-section">\n'
        day_html += '<div class="sport-title">🏂 Competition Events</div>\n'
        day_html += '<div class="day-sports">\n'
        for sport in sports:
            day_html += f'<span class="sport-tag">{sport}</span>\n'
        day_html += '</div>\n'
        day_html += '</div>\n'
    
    # Underdog nations section - split by status
    total_nations = sum(len(nations) for nations in nations_by_status.values())
    
    if total_nations > 0:
        # Confirmed entries
        if nations_by_status['confirmed']:
            day_html += '<div class="sport-section">\n'
            day_html += f'<div class="sport-title">✅ Confirmed Entries ({len(nations_by_status["confirmed"])})</div>\n'
            day_html += '<div class="underdog-nations">\n'
            for nation in nations_by_status['confirmed']:
                color = get_nation_color(nation)
                day_html += f'<div class="underdog-chip" style="background-color: {color}; border-color: {color};">{nation}</div>\n'
            day_html += '</div>\n'
            day_html += '</div>\n'
        
        # Probable entries
        if nations_by_status['probable']:
            day_html += '<div class="sport-section">\n'
            day_html += f'<div class="sport-title">⭐ Probable Entries ({len(nations_by_status["probable"])})</div>\n'
            day_html += '<div class="underdog-nations">\n'
            for nation in nations_by_status['probable']:
                color = get_nation_color(nation)
                day_html += f'<div class="underdog-chip" style="background-color: {color}; border-color: {color};">{nation}</div>\n'
            day_html += '</div>\n'
            day_html += '</div>\n'
        
        # Maybe entries (includes unconfirmed)
        if nations_by_status['maybe']:
            day_html += '<div class="sport-section">\n'
            day_html += f'<div class="sport-title">❓ Maybe Entries ({len(nations_by_status["maybe"])})</div>\n'
            day_html += '<div class="underdog-nations">\n'
            for nation in nations_by_status['maybe']:
                color = get_nation_color(nation)
                day_html += f'<div class="underdog-chip" style="background-color: {color}; border-color: {color};">{nation}</div>\n'
            day_html += '</div>\n'
            day_html += '</div>\n'
    
    day_html += '</div>\n'
    day_contents.append(day_html)

# Join all day contents
new_day_contents = '\n'.join(day_contents)

# Replace in the content
new_content = content[:first_day_content] + new_day_contents + content[last_day_content_end + 6:]

# Write back
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✓ Rebuilt daily schedule sections in index.html")
print(f"✓ Generated {len(day_contents)} day-content sections")
print(f"✓ Date range: {min(schedule.keys())} to {max(schedule.keys())}")

# Show a sample
print("\nSample: Feb 20, 2026")
feb_20_data = schedule.get('2026-02-20', {})
print(f"  Events: {list(feb_20_data.keys())}")
feb_20_nations = set()
for event, participants in feb_20_data.items():
    for p in participants:
        feb_20_nations.add(p['nation'])
print(f"  Nations competing: {len(feb_20_nations)} - {sorted(feb_20_nations)}")
