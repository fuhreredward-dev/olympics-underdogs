"""
Clean up Alpine Skiing events and add Guinea-Bissau tier.
"""

import json
from pathlib import Path

base_path = Path(__file__).parent

# Load the JSON schedule
with open(base_path / 'data' / 'daily_underdog_schedule_2026.json', 'r', encoding='utf-8') as f:
    schedule = json.load(f)

# Alpine Skiing events that need cleaning
alpine_events = [
    "Alpine Skiing - Men's Downhill",
    "Alpine Skiing - Women's Downhill",
    "Alpine Skiing - Men's Team Combined",
    "Alpine Skiing - Women's Team Combined",
    "Alpine Skiing - Men's Super-G",
    "Alpine Skiing - Women's Super-G",
    "Alpine Skiing - Men's Giant Slalom",
    "Alpine Skiing - Women's Giant Slalom",
    "Alpine Skiing - Men's Slalom",
    "Alpine Skiing - Women's Slalom"
]

# Nations to remove from Alpine Skiing
remove_nations = ["Japan", "Spain"]

# Remove Japan and Spain from Alpine Skiing events
removed_count = 0
for date, events in schedule.items():
    for event_name in alpine_events:
        if event_name in events:
            original_count = len(events[event_name])
            # Keep only non-Japan, non-Spain entries
            events[event_name] = [
                entry for entry in events[event_name]
                if entry['nation'] not in remove_nations
            ]
            removed = original_count - len(events[event_name])
            if removed > 0:
                print(f"✓ {date} - {event_name}: Removed {removed} entries")
                removed_count += removed

print(f"\n✓ Total entries removed: {removed_count}")

# Save the cleaned schedule
with open(base_path / 'data' / 'daily_underdog_schedule_2026.json', 'w', encoding='utf-8') as f:
    json.dump(schedule, f, ensure_ascii=False, indent=2)

# Load nation tiers and add Guinea-Bissau
with open(base_path / 'data' / 'nation_tiers_2026.json', 'r', encoding='utf-8') as f:
    nation_tiers = json.load(f)

if "Guinea-Bissau" not in nation_tiers:
    nation_tiers["Guinea-Bissau"] = 5
    print("\n✓ Added Guinea-Bissau to nation_tiers with tier 5")
    
    # Save the updated nation_tiers
    with open(base_path / 'data' / 'nation_tiers_2026.json', 'w', encoding='utf-8') as f:
        json.dump(nation_tiers, f, ensure_ascii=False, indent=2)
else:
    print(f"\n✓ Guinea-Bissau already in nation_tiers with tier {nation_tiers['Guinea-Bissau']}")

print("\n✓ All updates completed!")
