"""
Verify cross-page data consistency for Overview and Schedule.
- Participating nations count
- Nations with schedules count
- Total sports count (from daily schedule)
- Ensure name mapping covers schedule names
- Check sports/athletes presence for participating nations
"""
import json
from pathlib import Path

BASE = Path(__file__).parent.parent

# Load files
participating = json.loads((BASE / 'data' / 'participating_nations_2026.json').read_text(encoding='utf-8'))
nation_schedules = json.loads((BASE / 'data' / 'nation_schedules_2026.json').read_text(encoding='utf-8'))
daily_schedule = json.loads((BASE / 'data' / 'daily_underdog_schedule_2026.json').read_text(encoding='utf-8'))
try:
    event_nations = json.loads((BASE / 'data' / 'event_nations_2026.json').read_text(encoding='utf-8'))
except FileNotFoundError:
    event_nations = {}
athletes = json.loads((BASE / 'data' / 'athlete_counts_2026.json').read_text(encoding='utf-8'))
nation_sports = json.loads((BASE / 'data' / 'nation_sports_participation_2026.json').read_text(encoding='utf-8'))
gen = (BASE / 'scripts' / 'generate_html_overview.py').read_text(encoding='utf-8')

# Build mapping IOC->Full Name
import re
NATION_NAMES = {}
for m in re.finditer(r"'([A-Z]{3})'\s*:\s*'([^']+)'", gen):
    NATION_NAMES[m.group(1)] = m.group(2)

# Compute stats
participating_count = len(participating)
schedule_nations_count = sum(1 for v in nation_schedules.values() if v.get('total_competition_days', 0) > 0)
# Prefer comprehensive sports set from event_nations
sports_set = set()
if event_nations:
    for event_name in event_nations.keys():
        sport = event_name.split(' - ')[0]
        sports_set.add(sport)
else:
    for events in daily_schedule.values():
        for event_name in events.keys():
            sport = event_name.split(' - ')[0]
            sports_set.add(sport)

sports_count = len(sports_set)

print('=== CONSISTENCY SUMMARY ===')
print(f'Participating Nations: {participating_count}')
print(f'Nations with Schedules: {schedule_nations_count}')
print(f'Total Sports: {sports_count}')

# Check mapping coverage for schedule full names
schedule_names = set(nation_schedules.keys())
full_name_map = {v: k for k, v in NATION_NAMES.items()}
missing_name_mappings = sorted(name for name in schedule_names if name not in full_name_map)
if missing_name_mappings:
    print('Missing name mappings:', ', '.join(missing_name_mappings))
else:
    print('All schedule names covered by NATION_NAMES mapping.')

# Validate each participating IOC code has athletes and sports entries
missing_athletes = [code for code in participating if code not in athletes]
missing_sports = [code for code in participating if code not in nation_sports]
print('Missing athletes for:', ', '.join(missing_athletes) if missing_athletes else 'None')
print('Missing sports for:', ', '.join(missing_sports) if missing_sports else 'None')

# Exit non-zero if mismatches
import sys
errors = 0
if missing_name_mappings:
    errors += 1
if missing_athletes or missing_sports:
    errors += 1
sys.exit(errors)
