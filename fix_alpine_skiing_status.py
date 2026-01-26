"""
Fix Alpine Skiing entries to have 'maybe' status instead of 'probable'.
Alpine skiing entries are uncertain and should be categorized as maybe.
"""

import json
from pathlib import Path

base_path = Path(__file__).parent

# Load the schedule
schedule_path = base_path / 'data' / 'daily_underdog_schedule_2026.json'
with open(schedule_path, 'r', encoding='utf-8') as f:
    schedule = json.load(f)

# Track changes
changes_made = 0

# Update all Alpine Skiing entries
for date, events in schedule.items():
    for event_name, participants in events.items():
        if event_name.startswith('Alpine Skiing'):
            for participant in participants:
                if participant.get('status') == 'probable':
                    participant['status'] = 'maybe'
                    changes_made += 1

# Write back
with open(schedule_path, 'w', encoding='utf-8') as f:
    json.dump(schedule, f, indent=2)

print(f"✓ Updated {changes_made} Alpine Skiing entries from 'probable' to 'maybe'")
