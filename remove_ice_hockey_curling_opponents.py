"""
Remove non-Denmark opponents from Ice Hockey and Curling events in JSON.
"""

import json
from pathlib import Path

base_path = Path(__file__).parent

# Load the JSON
with open(base_path / 'data' / 'daily_underdog_schedule_2026.json', 'r', encoding='utf-8') as f:
    schedule = json.load(f)

# Events to clean (keep only Denmark)
events_to_clean = [
    "Ice Hockey - Men's Group Stage",
    "Curling - Women's Round 1",
    "Curling - Women's Round 2",
    "Curling - Women's Round 3",
    "Curling - Women's Round 5",
    "Curling - Women's Round 6",
    "Curling - Women's Round 7",
    "Curling - Women's Round 9",
    "Curling - Women's Round 10",
    "Curling - Women's Round 11"
]

# Process each date
for date, events in schedule.items():
    for event_name in events_to_clean:
        if event_name in events:
            # Keep only Denmark entries
            denmark_entries = [
                entry for entry in events[event_name]
                if entry['nation'] == 'Denmark'
            ]
            events[event_name] = denmark_entries
            print(f"✓ {date} - {event_name}: Kept {len(denmark_entries)} Denmark entry(ies)")

# Save the cleaned JSON
with open(base_path / 'data' / 'daily_underdog_schedule_2026.json', 'w', encoding='utf-8') as f:
    json.dump(schedule, f, ensure_ascii=False, indent=2)

print("\n✓ JSON file updated - removed all non-Denmark opponents from Ice Hockey and Curling")
