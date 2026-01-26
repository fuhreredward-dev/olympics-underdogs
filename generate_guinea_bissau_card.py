"""
Analyze Guinea-Bissau schedule data for index.html entry.
"""

import json
from pathlib import Path
from datetime import datetime

base_path = Path(__file__).parent

# Load the schedule
with open(base_path / 'data' / 'daily_underdog_schedule_2026.json', 'r', encoding='utf-8') as f:
    schedule = json.load(f)

# Find all Guinea-Bissau entries
gb_dates = set()
total_athletes = 0
sports = set()

for date, events in schedule.items():
    for event_name, nations in events.items():
        for nation_entry in nations:
            if nation_entry['nation'] == 'Guinea-Bissau':
                gb_dates.add(date)
                total_athletes += nation_entry.get('athletes', 0)
                sport = event_name.split(' - ')[0]
                sports.add(sport)

# Sort dates
sorted_dates = sorted(gb_dates)
if sorted_dates:
    start_date = datetime.strptime(sorted_dates[0], '%Y-%m-%d')
    end_date = datetime.strptime(sorted_dates[-1], '%Y-%m-%d')
    
    print(f"Guinea-Bissau Competing Info:")
    print(f"  Dates: {start_date.strftime('%b %d')} - {end_date.strftime('%b %d')}")
    print(f"  Days: {len(gb_dates)}")
    print(f"  Total Athletes: {total_athletes}")
    print(f"  Sports: {', '.join(sorted(sports))}")
    
    # Create the HTML entry
    html = f'''                    <div class="nation-card underdog">
                        <div class="nation-header">
                            <span class="nation-name">Guinea-Bissau</span>
                            <span class="tier-badge tier-5">T5</span>
                        </div>
                        <div class="nation-stats">
                            <div class="mini-stat">👥 {total_athletes} athletes</div>
                            <div class="mini-stat">🏆 0 Winter medals</div>
                            <div class="mini-stat">🥇 0 All-time medals</div>
                        </div>
                        <div class="competing-days">📅 Competing: {len(gb_dates)} days ({start_date.strftime('%b %d')} - {end_date.strftime('%b %d')})</div>
                        <div class="sports-list">
                            <span class="sport-tag">{sports.pop()}</span>
                        </div>
                        <br><span class="criteria-text">🎯 < 5 athletes, No Olympic gold, No Olympic medals, No Winter gold, No Winter medals, Western Africa</span>
                    </div>'''
    
    print("\n" + html)
