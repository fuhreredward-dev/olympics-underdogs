"""
Parse the Olympic Underdog List.txt to create comprehensive event-to-nation mappings.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

# Known sports from the Olympics
OLYMPIC_SPORTS = {
    'Skeleton', 'Ski Jumping', 'Ski Mountaineering', 'Snowboarding', 'Speed Skating',
    'Bobsleigh', 'Curling', 'Figure Skating', 'Freestyle Skiing', 'Ice Hockey',
    'Luge', 'Short Track Speed Skating', 'Biathlon', 'Cross-Country Skiing',
    'Alpine Skiing'
}

# Map standalone event headers to their parent sport
EVENT_TO_SPORT_MAP = {
    "Men's Giant Slalom": "Alpine Skiing",
    "Women's Giant Slalom": "Alpine Skiing",
    "Men's Slalom": "Alpine Skiing",
    "Women's Slalom": "Alpine Skiing",
    "Men's Super-G": "Alpine Skiing",
    "Women's Super-G": "Alpine Skiing",
    "Men's Downhill": "Alpine Skiing",
    "Women's Downhill": "Alpine Skiing",
    "Men's Team Combined": "Alpine Skiing",
    "Women's Team Combined": "Alpine Skiing",
}

def normalize_text(text):
    """Normalize text by fixing encoding issues."""
    # Fix various apostrophe/quote encodings
    # These are the actual Unicode characters in the file
    text = text.replace('\u2019', "'")  # RIGHT SINGLE QUOTATION MARK
    text = text.replace('\u2018', "'")  # LEFT SINGLE QUOTATION MARK
    text = text.replace('\u201c', '"')  # LEFT DOUBLE QUOTATION MARK
    text = text.replace('\u201d', '"')  # RIGHT DOUBLE QUOTATION MARK
    return text.strip()

def parse_underdog_list(file_path):
    """Parse the underdog list text file and create mappings."""
    
    with open(file_path, 'r', encoding='utf-8-sig') as f:  # utf-8-sig strips BOM
        lines = [normalize_text(line.rstrip()) for line in f]
    
    print(f"Read {len(lines)} lines from file")
    
    # Mappings we'll create
    nation_to_events = defaultdict(lambda: {
        'sports': set(),
        'events': [],
        'total_events': 0,
        'probable_events': 0,
        'unconfirmed_events': 0
    })
    
    event_to_nations = {}
    sport_to_events = defaultdict(list)
    
    current_sport = None
    current_event = None
    
    for i, line in enumerate(lines):
        # Skip empty lines
        if not line.strip():
            continue
        
        stripped = line.strip()
        
        # Detect sport headers - these are known sports
        if line.endswith(':') and '(' not in line:
            # Check if this is a standalone event that maps to a sport
            potential_event = stripped.rstrip(':')
            if potential_event in EVENT_TO_SPORT_MAP:
                current_sport = EVENT_TO_SPORT_MAP[potential_event]
                current_event = potential_event
                sport_to_events[current_sport].append(current_event)
                event_to_nations[f"{current_sport} - {current_event}"] = []
                print(f"Found Alpine event: {current_event}")
                continue
            # Check if this matches a known sport
            elif any(sport_name in potential_event for sport_name in OLYMPIC_SPORTS):
                current_sport = potential_event
                current_event = None
                print(f"Found sport: {current_sport}")
                continue
            # Otherwise it's an event within the current sport
            elif current_sport:
                current_event = stripped.rstrip(':')
                sport_to_events[current_sport].append(current_event)
                event_to_nations[f"{current_sport} - {current_event}"] = []
                if len(event_to_nations) <= 10:
                    print(f"  Found event: {current_event}")
                continue
        
        # Parse nation entries (format: "Nation (count)" or "Nation (count)*")
        match = re.match(r'^(.+?)\s*\((\d+)\)(\*?)$', stripped)
        if match and current_sport and current_event:
            nation = match.group(1).strip()
            count = int(match.group(2))
            is_unconfirmed = match.group(3) == '*'
            
            # Add to event mapping
            event_key = f"{current_sport} - {current_event}"
            event_to_nations[event_key].append({
                'nation': nation,
                'athletes': count,
                'status': 'unconfirmed' if is_unconfirmed else 'probable'
            })
            
            # Add to nation mapping
            nation_data = nation_to_events[nation]
            nation_data['sports'].add(current_sport)
            nation_data['events'].append({
                'sport': current_sport,
                'event': current_event,
                'athletes': count,
                'status': 'unconfirmed' if is_unconfirmed else 'probable'
            })
            nation_data['total_events'] += 1
            if is_unconfirmed:
                nation_data['unconfirmed_events'] += 1
            else:
                nation_data['probable_events'] += 1
    
    # Convert sets to lists for JSON serialization
    for nation, data in nation_to_events.items():
        data['sports'] = sorted(list(data['sports']))
    
    return dict(nation_to_events), event_to_nations, dict(sport_to_events)

def main():
    # File paths
    base_path = Path(__file__).parent.parent
    input_file = base_path / 'data' / 'Olympic Underdog List.txt'
    
    # Parse the file
    print("Parsing underdog participation list...")
    nation_to_events, event_to_nations, sport_to_events = parse_underdog_list(input_file)
    
    # Save nation-to-events mapping
    output_file = base_path / 'data' / 'nation_events_2026.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(nation_to_events, f, indent=2, ensure_ascii=False)
    print(f"[OK] Saved nation-to-events mapping: {output_file}")
    
    # Save event-to-nations mapping
    output_file = base_path / 'data' / 'event_nations_2026.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(event_to_nations, f, indent=2, ensure_ascii=False)
    print(f"[OK] Saved event-to-nations mapping: {output_file}")
    
    # Save sport-to-events mapping
    output_file = base_path / 'data' / 'sport_events_2026.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sport_to_events, f, indent=2, ensure_ascii=False)
    print(f"[OK] Saved sport-to-events mapping: {output_file}")
    
    # Print summary statistics
    print(f"\n[Summary]")
    print(f"   Nations with events: {len(nation_to_events)}")
    print(f"   Total events: {len(event_to_nations)}")
    print(f"   Sports: {len(sport_to_events)}")
    
    # Show sample nation data
    print(f"\n[Sample nation data]")
    for nation in list(nation_to_events.keys())[:3]:
        data = nation_to_events[nation]
        print(f"   {nation}: {len(data['sports'])} sports, {data['total_events']} events ({data['probable_events']} probable, {data['unconfirmed_events']} unconfirmed)")

if __name__ == '__main__':
    main()
