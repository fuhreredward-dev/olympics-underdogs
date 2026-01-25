"""
Parse the TV schedule CSV and extract preliminary round dates for each discipline/event.
"""

import csv
import json
import re
from datetime import datetime
from collections import defaultdict
from pathlib import Path

def parse_schedule_csv(csv_path):
    """
    Parse the two-column TV schedule CSV and extract all events with dates/times.
    Returns a dict mapping discipline -> events with preliminary round info.
    """
    
    events_by_discipline = defaultdict(lambda: defaultdict(list))
    current_date = None
    
    # Read CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into lines and clean
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    # Parse line by line
    for i, line in enumerate(lines):
        # Check for date pattern (e.g., "Wednesday, February 4" or "Friday, February 6")
        date_match = re.search(r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+(January|February)\s+(\d{1,2})', line)
        if date_match:
            month_str = date_match.group(2)
            day_str = date_match.group(3)
            month = 1 if month_str == "January" else 2
            day = int(day_str)
            current_date = f"2026-{month:02d}-{day:02d}"
            continue
        
        # Check for time pattern (e.g., "1:30 PM" or "4:05 AM")
        time_match = re.search(r'(\d{1,2}):(\d{2})\s*(AM|PM)', line)
        if time_match and current_date:
            hour = int(time_match.group(1))
            minute = time_match.group(2)
            period = time_match.group(3)
            
            # Convert to 24-hour format
            if period == 'PM' and hour != 12:
                hour += 12
            elif period == 'AM' and hour == 12:
                hour = 0
            
            time_str = f"{hour:02d}:{minute}"
            
            # Look ahead for event details (discipline, event name, round type)
            event_details = extract_event_info(line, i, lines)
            
            if event_details:
                discipline, event_name, round_type = event_details
                
                # Store event
                events_by_discipline[discipline][event_name].append({
                    'date': current_date,
                    'time': time_str,
                    'round': round_type
                })
    
    return events_by_discipline

def extract_event_info(line, line_idx, all_lines):
    """
    Extract discipline, event name, and round type from schedule line.
    Returns (discipline, event_name, round_type) or None.
    """
    
    # Map of discipline keywords to standard names
    discipline_map = {
        'ALPINE': 'Alpine Skiing',
        'BIATHLON': 'Biathlon',
        'BOBSLEIGH': 'Bobsleigh',
        'CROSS-COUNTRY': 'Cross-Country Skiing',
        'CURLING': 'Curling',
        'FIGURE SKATING': 'Figure Skating',
        'FREESTYLE': 'Freestyle Skiing',
        'ICE HOCKEY': 'Ice Hockey',
        'LUGE': 'Luge',
        'NORDIC COMBINED': 'Nordic Combined',
        'SHORT TRACK': 'Short-Track Speed Skating',
        'SKELETON': 'Skeleton',
        'SKI JUMPING': 'Ski Jumping',
        'SKI MOUNTAINEERING': 'Ski Mountaineering',
        'SNOWBOARD': 'Snowboarding',
        'SPEED SKATING': 'Speed Skating'
    }
    
    # Round type keywords
    round_keywords = {
        'QUALIFICATION': 'Qualification',
        'QUALIF': 'Qualification',
        'PRELIMINARY': 'Preliminary',
        'PRELIM': 'Preliminary',
        'GROUP': 'Group Stage',
        'HEAT': 'Heat',
        'HEATS': 'Heat',
        'RUN': 'Run',
        'SHORT PROGRAM': 'Short Program',
        'FREE SKATE': 'Free Skate',
        'RHYTHM DANCE': 'Rhythm Dance',
        'FREE DANCE': 'Free Dance',
        'SHORT': 'Short Program',
        'FREE': 'Free Skate',
        'PAIRS': 'Pairs'
    }
    
    # Extract content between parentheses/quotes
    content = line.upper()
    
    # Find discipline
    discipline = None
    for key, std_name in discipline_map.items():
        if key in content:
            discipline = std_name
            break
    
    if not discipline:
        return None
    
    # Extract event name (usually before round type)
    event_name = None
    
    # Try to get more detail from context
    if '(' in line:
        # Event info is often in parentheses or after discipline
        parts = line.split('\n')
        for part in parts:
            if discipline.upper() in part.upper():
                # Get the text after the discipline name
                idx = part.upper().find(discipline.upper())
                detail = part[idx + len(discipline):].strip()
                if detail:
                    event_name = detail[:100]  # Take first 100 chars
    
    if not event_name:
        # Fallback: extract text between discipline and round type
        event_name = f"{discipline} Event"
    
    # Find round type
    round_type = 'Unknown'
    for key, std_round in round_keywords.items():
        if key in content:
            round_type = std_round
            break
    
    # Clean up event name
    event_name = event_name.replace('(', '').replace(')', '').strip()
    
    return (discipline, event_name, round_type)

def format_schedule_by_discipline(events_data):
    """
    Format the parsed events into a cleaner structure organized by discipline.
    """
    output = {}
    
    for discipline in sorted(events_data.keys()):
        events = events_data[discipline]
        output[discipline] = {
            'medal_events': len(events),
            'events': []
        }
        
        for event_name in sorted(events.keys()):
            sessions = events[event_name]
            
            # Group by preliminary rounds (first occurrence per date)
            prelim_rounds = []
            seen_dates = set()
            
            for session in sessions:
                # Only include first occurrence per date (preliminary/qualification)
                if session['date'] not in seen_dates:
                    prelim_rounds.append({
                        'date': session['date'],
                        'time': session['time'],
                        'round': session['round']
                    })
                    seen_dates.add(session['date'])
            
            output[discipline]['events'].append({
                'event_name': event_name,
                'preliminary_rounds': prelim_rounds,
                'total_preliminary_days': len(prelim_rounds)
            })
    
    return output

def main():
    csv_file = Path(__file__).parent.parent / 'data' / 'schedule' / 'Winter Olympics 2026 TV Schedule (EST) - Two Columns (Print Narrow Margins).csv'
    
    print(f"Parsing schedule from: {csv_file}")
    
    # Parse CSV
    raw_events = parse_schedule_csv(str(csv_file))
    
    # Format for output
    formatted = format_schedule_by_discipline(raw_events)
    
    # Save to JSON
    output_file = Path(__file__).parent.parent / 'data' / 'schedules' / 'disciplines_preliminary_schedule.json'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(formatted, f, indent=2)
    
    print(f"\n✓ Extracted schedule saved to: {output_file}")
    
    # Print summary
    print(f"\nSchedule Summary:")
    print(f"─" * 60)
    for discipline in sorted(formatted.keys()):
        data = formatted[discipline]
        event_count = len(data['events'])
        print(f"  {discipline:<30} {event_count:>2} events")
    
    return formatted

if __name__ == '__main__':
    main()
