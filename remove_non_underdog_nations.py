"""
Remove all non-underdog nations from schedule JSON.
"""

import json
from pathlib import Path

base_path = Path(__file__).parent

# Load nation tiers to identify underdog nations
with open(base_path / 'data' / 'nation_tiers_2026.json', 'r', encoding='utf-8') as f:
    nation_tiers = json.load(f)

# Get list of underdog nations (those with tier >= 1)
underdog_nations = {nation for nation, tier in nation_tiers.items() if tier >= 1}

print(f"Found {len(underdog_nations)} underdog nations")
print(f"Underdog nations: {sorted(underdog_nations)}\n")

# Load the schedule
with open(base_path / 'data' / 'daily_underdog_schedule_2026.json', 'r', encoding='utf-8') as f:
    schedule = json.load(f)

# Remove non-underdog nations from all events
removed_count = 0
for date, events in schedule.items():
    for event_name, nations in events.items():
        original_count = len(nations)
        # Keep only underdog nations
        events[event_name] = [
            entry for entry in nations
            if entry['nation'] in underdog_nations
        ]
        removed = original_count - len(events[event_name])
        if removed > 0:
            print(f"✓ {date} - {event_name}: Removed {removed} non-underdog entries")
            removed_count += removed

print(f"\n✓ Total non-underdog entries removed: {removed_count}")

# Save the cleaned schedule
with open(base_path / 'data' / 'daily_underdog_schedule_2026.json', 'w', encoding='utf-8') as f:
    json.dump(schedule, f, ensure_ascii=False, indent=2)

print("✓ Schedule JSON updated!")
