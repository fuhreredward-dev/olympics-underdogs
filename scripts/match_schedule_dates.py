"""
Match underdog events to IOC schedule dates and create comprehensive schedule mappings.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def normalize_event_name(event_name):
    """Normalize event names for matching."""
    # Remove run numbers, heat numbers, finals, etc for matching
    event_name = re.sub(r'\s+(Run|Heat)\s+\d+', '', event_name)
    event_name = re.sub(r'\s+Final.*', '', event_name)
    event_name = re.sub(r'\s+/\s+Final.*', '', event_name)
    event_name = event_name.strip()
    return event_name

def match_event_to_schedule(sport, event, schedule_data, nation=None):
    """Match an event from our underdog list to the IOC schedule."""
    # Map our sport names to IOC discipline names
    sport_mapping = {
        'Alpine Skiing': 'Alpine',
        'Biathlon': 'Biathlon',
        'Bobsleigh': 'Bobsleigh',
        'Cross-Country Skiing': 'Cross-Country Skiing',
        'Curling': 'Curling',
        'Figure Skating': 'Figure Skating',
        'Freestyle Skiing': 'Freestyle Skiing',
        'Ice Hockey': 'Ice Hockey',
        'Luge': 'Luge',
        'Short Track Speed Skating': 'Short Track',
        'Skeleton': 'Skeleton',
        'Ski Jumping': 'Ski Jumping',
        'Ski Mountaineering': 'Ski Mountaineering',
        'Snowboarding': 'Snowboard',
        'Speed Skating': 'Speed Skating'
    }
    
    ioc_discipline = sport_mapping.get(sport)
    if not ioc_discipline:
        return None
    
    discipline_data = schedule_data['disciplines'].get(ioc_discipline)
    if not discipline_data:
        return None
    
    # Special handling for Curling and Ice Hockey - only use RR Session 1 for Denmark
    if sport in ['Curling', 'Ice Hockey'] and nation == 'Denmark':
        matches = []
        for sched_event in discipline_data.get('medal_events', []):
            if 'RR Session 1' in sched_event['event']:
                # Match gender
                if ("Women's" in event and "Women's" in sched_event['event']) or \
                   ("Men's" in event and "Men's" in sched_event['event']):
                    matches.append(sched_event)
        return matches if matches else None
    
    # Special handling for Cross-Country - complex event name mapping
    if sport == 'Cross-Country Skiing':
        cc_mapping = {
            "Men's 15km classical": "Men's 10km Interval Start Free",
            "Women's 10km classical": "Women's 10km Interval Start Free",
            "Men's skiathlon": "Men's 10km + 10km Skiathlon",
            "Women's skiathlon": "Women's 10km + 10km Skiathlon",
            "Men's 50km mass start": "Men's 50km Mass Start Classic",
            "Women's 30km mass start": "Women's 50km Mass Start Classic"
        }
        
        mapped_event = cc_mapping.get(event, event)
        for sched_event in discipline_data.get('medal_events', []):
            if mapped_event in sched_event['event']:
                return [sched_event]
    
    # Normalize our event name for matching
    normalized_event = normalize_event_name(event)
    
    # Try to find matching schedule entries
    matches = []
    for sched_event in discipline_data.get('medal_events', []):
        sched_event_name = normalize_event_name(sched_event['event'])
        
        # Direct match
        if normalized_event == sched_event_name:
            matches.append(sched_event)
        # Partial match (event name contains or is contained)
        elif normalized_event in sched_event_name or sched_event_name in normalized_event:
            matches.append(sched_event)
    
    return matches

def create_nation_schedule_mapping():
    """Create comprehensive mapping of nations to their competition dates."""
    
    base_path = Path(__file__).parent.parent
    
    # Load data files
    with open(base_path / 'data' / 'nation_events_2026.json', 'r', encoding='utf-8') as f:
        nation_events = json.load(f)
    
    with open(base_path / 'data' / 'schedules' / 'ioc_schedule_complete.json', 'r', encoding='utf-8') as f:
        ioc_schedule = json.load(f)
    
    # Create mappings
    nation_schedules = {}
    daily_underdog_schedule = defaultdict(lambda: defaultdict(list))
    event_date_mapping = {}
    
    print("Matching events to schedule dates...")
    print("=" * 70)
    
    for nation, data in nation_events.items():
        nation_schedule = {
            'sports': data['sports'],
            'competition_dates': set(),
            'events_by_date': defaultdict(list),
            'first_competition': None,
            'last_competition': None
        }
        
        for event_info in data['events']:
            sport = event_info['sport']
            event = event_info['event']
            athletes = event_info['athletes']
            status = event_info['status']
            
            # Match to IOC schedule
            schedule_matches = match_event_to_schedule(sport, event, ioc_schedule, nation)
            
            if schedule_matches:
                # Use first match (typically the first heat/run)
                first_match = schedule_matches[0]
                date = first_match['date']
                time_est = first_match['time_est']
                
                # Store in nation schedule
                nation_schedule['competition_dates'].add(date)
                nation_schedule['events_by_date'][date].append({
                    'sport': sport,
                    'event': event,
                    'time_est': time_est,
                    'athletes': athletes,
                    'status': status
                })
                
                # Store in daily schedule
                daily_underdog_schedule[date][f"{sport} - {event}"].append({
                    'nation': nation,
                    'athletes': athletes,
                    'status': status,
                    'time_est': time_est
                })
                
                # Store event to date mapping
                event_key = f"{sport} - {event}"
                if event_key not in event_date_mapping:
                    event_date_mapping[event_key] = {
                        'date': date,
                        'time_est': time_est,
                        'all_dates': [date]
                    }
                elif date not in event_date_mapping[event_key]['all_dates']:
                    event_date_mapping[event_key]['all_dates'].append(date)
        
        # Calculate first and last competition dates
        if nation_schedule['competition_dates']:
            sorted_dates = sorted(nation_schedule['competition_dates'])
            nation_schedule['first_competition'] = sorted_dates[0]
            nation_schedule['last_competition'] = sorted_dates[-1]
            nation_schedule['total_competition_days'] = len(sorted_dates)
            
            # Convert set to sorted list for JSON
            nation_schedule['competition_dates'] = sorted_dates
            
            # Convert defaultdict to regular dict
            nation_schedule['events_by_date'] = dict(nation_schedule['events_by_date'])
            
            print(f"[OK] {nation}: {len(sorted_dates)} days, {sorted_dates[0]} to {sorted_dates[-1]}")
        else:
            nation_schedule['competition_dates'] = []
            nation_schedule['events_by_date'] = {}
            nation_schedule['total_competition_days'] = 0
            print(f"[SKIP] {nation}: No schedule matches found")
        
        nation_schedules[nation] = nation_schedule
    
    # Convert daily schedule to regular dict
    daily_schedule_dict = {}
    for date in sorted(daily_underdog_schedule.keys()):
        daily_schedule_dict[date] = dict(daily_underdog_schedule[date])
    
    # Save all mappings
    print("\n" + "=" * 70)
    print("Saving schedule mappings...")
    
    # Save nation schedules
    output_file = base_path / 'data' / 'nation_schedules_2026.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(nation_schedules, f, indent=2, ensure_ascii=False)
    print(f"[SAVED] Nation schedules: {output_file}")
    
    # Save daily schedule
    output_file = base_path / 'data' / 'daily_underdog_schedule_2026.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(daily_schedule_dict, f, indent=2, ensure_ascii=False)
    print(f"[SAVED] Daily schedule: {output_file}")
    
    # Save event date mapping
    output_file = base_path / 'data' / 'event_dates_2026.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(event_date_mapping, f, indent=2, ensure_ascii=False)
    print(f"[SAVED] Event dates: {output_file}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Nations with schedule data: {len([n for n in nation_schedules.values() if n['total_competition_days'] > 0])}")
    print(f"Total competition days with underdogs: {len(daily_schedule_dict)}")
    print(f"Events with date mappings: {len(event_date_mapping)}")
    
    # Show busiest days
    print("\nBusiest days for underdogs:")
    day_counts = [(date, sum(len(nations) for nations in events.values())) 
                  for date, events in daily_schedule_dict.items()]
    day_counts.sort(key=lambda x: x[1], reverse=True)
    for date, count in day_counts[:5]:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        print(f"  {date_obj.strftime('%a %b %d')}: {count} underdog participations")

if __name__ == '__main__':
    create_nation_schedule_mapping()
