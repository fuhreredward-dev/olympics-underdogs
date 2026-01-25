#!/usr/bin/env python3
"""
Scrape official IOC schedule pages and generate normalized schedule JSON.
Converts local (CET) times to EST and includes network data.
"""

import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import requests
from bs4 import BeautifulSoup
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Discipline codes and IOC URLs
DISCIPLINES = {
    'alp': 'Alpine Skiing',
    'bth': 'Biathlon',
    'bob': 'Bobsleigh',
    'ccs': 'Cross-Country Skiing',
    'fsk': 'Figure Skating',
    'frs': 'Freestyle Skiing',
    'iho': 'Ice Hockey',
    'lug': 'Luge',
    'ncb': 'Nordic Combined',
    'stk': 'Short Track Speed Skating',
    'skn': 'Skeleton',
    'sjp': 'Ski Jumping',
    'smt': 'Ski Mountaineering',
    'sbd': 'Snowboard',
    'ssk': 'Speed Skating',
}

BASE_URL = 'https://www.olympics.com/en/milano-cortina-2026/schedule'

def get_ioc_schedule_page(discipline_code: str) -> Optional[str]:
    """Fetch IOC schedule page HTML for a discipline."""
    url = f"{BASE_URL}/{discipline_code}"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text
        # Save first fetch for debugging
        if discipline_code == 'skn':
            with open('debug_skeleton.html', 'w') as f:
                f.write(html[:5000])
        return html
    except Exception as e:
        print(f"Error fetching {discipline_code}: {e}")
        return None

def parse_ioc_schedule(html: str, discipline: str) -> List[Dict[str, Any]]:
    """
    Parse IOC schedule HTML and extract events.
    Returns list of events with date, time (local), round, stage, venue.
    """
    events = []
    
    # Parse raw text to find dates, times, and events
    lines = html.split('\n')
    current_date = None
    current_venue = None
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for date patterns like "## 04February" or "04February"
        date_match = re.search(r'(\d{1,2})\s*([A-Za-z]+)', line)
        if date_match and len(line) < 50 and any(c in line for c in ['#', 'February', 'January']):
            day_str = date_match.group(1).zfill(2)
            month_str = date_match.group(2)[:3].lower()
            month_map = {
                'feb': '02', 'jan': '01', 'mar': '03', 'apr': '04',
                'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
            }
            month_num = month_map.get(month_str, '02')
            current_date = f"2026-{month_num}-{day_str}"
        
        # Look for venue lines (Centre, Arena, Park, Stadium)
        if any(v in line for v in ['Centre', 'Arena', 'Park', 'Stadium']):
            if len(line) < 200:
                current_venue = line
        
        # Look for time + event pattern: "HH:MM" followed by event name
        time_match = re.match(r'(\d{1,2}):(\d{2})\s+(.+)', line)
        if time_match and current_date:
            hour = time_match.group(1).zfill(2)
            minute = time_match.group(2)
            event_desc = time_match.group(3).strip()
            
            # Check if this line or next few lines contain stage indicators
            stage = 'prelim'
            if 'final' in event_desc.lower() or 'medal' in event_desc.lower():
                stage = 'final'
            elif 'playoff' in event_desc.lower() or 'semi' in event_desc.lower():
                stage = 'playoff'
            
            # Clean up event description (remove HTML artifacts)
            event_name = re.sub(r'\[.*?\]', '', event_desc).strip()
            event_name = re.sub(r'Image:.*?(?=\s|$)', '', event_name).strip()
            
            if event_name:
                event = {
                    'date': current_date,
                    'time_local_cet': f"{hour}:{minute}",
                    'round': event_name[:80],  # Truncate long names
                    'stage': stage,
                    'venue': current_venue or 'TBD',
                    'network': ['TBD'],
                    'is_replay': False
                }
                events.append(event)
        
        i += 1
    
    return events

def convert_cet_to_est(date_str: str, time_cet: str) -> tuple:
    """Convert CET time to EST (CET - 6 hours)."""
    try:
        dt_cet = datetime.strptime(f"{date_str} {time_cet}", "%Y-%m-%d %H:%M")
        dt_est = dt_cet - timedelta(hours=6)
        return dt_est.strftime("%Y-%m-%d"), dt_est.strftime("%H:%M")
    except:
        return date_str, time_cet

def build_normalized_schedule() -> List[Dict[str, Any]]:
    """Build normalized schedule from IOC pages."""
    all_disciplines = []
    
    for code, name in DISCIPLINES.items():
        print(f"Fetching {name} ({code})...")
        html = get_ioc_schedule_page(code)
        
        if not html:
            print(f"  Skipped (fetch error)")
            continue
        
        events = parse_ioc_schedule(html, name)
        
        # Group events by event type
        event_groups = {}
        for event in events:
            # Simple grouping by round name (e.g., "Men's Downhill")
            key = event['round']
            if key not in event_groups:
                event_groups[key] = []
            event_groups[key].append(event)
        
        # Build discipline entry
        discipline_entry = {
            'discipline': name,
            'code': code,
            'events': []
        }
        
        # Convert times to EST and create event entries
        for event_name, instances in event_groups.items():
            event_entry = {
                'event': event_name,
                'instances': []
            }
            
            for instance in instances:
                date_est, time_est = convert_cet_to_est(instance['date'], instance['time_local_cet'])
                event_entry['instances'].append({
                    'date': date_est,
                    'time_est': time_est,
                    'time_local_cet': instance['time_local_cet'],
                    'round': instance['round'],
                    'stage': instance['stage'],
                    'venue': instance['venue'],
                    'network': instance['network'],
                    'is_replay': instance['is_replay']
                })
            
            discipline_entry['events'].append(event_entry)
        
        all_disciplines.append(discipline_entry)
        print(f"  Found {len(events)} events")
    
    return all_disciplines

def main():
    print("IOC Schedule Scraper - 2026 Winter Olympics")
    print("=" * 60)
    
    # Build schedule
    schedule = build_normalized_schedule()
    
    # Output JSON
    output_path = 'data/schedules/ioc_schedule_full.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(schedule, f, indent=2)
    
    print(f"\nSchedule saved to {output_path}")
    print(f"Total disciplines: {len(schedule)}")
    
    # Summary
    total_events = sum(len(d['events']) for d in schedule)
    print(f"Total events: {total_events}")

if __name__ == '__main__':
    main()
