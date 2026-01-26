"""
Update nation cards in index.html with actual sports and events from parsed data.
"""

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict

# IOC code mapping
IOC_CODE_MAP = {
    'Albania': 'ALB', 'Andorra': 'AND', 'Argentina': 'ARG', 'Armenia': 'ARM',
    'Australia': 'AUS', 'Azerbaijan': 'AZE', 'Benin': 'BEN', 'Bolivia': 'BOL',
    'Bosnia and Herzegovina': 'BIH', 'Brazil': 'BRA', 'Bulgaria': 'BG',
    'Chile': 'CHI', 'Chinese Taipei': 'TPE', 'Colombia': 'COL', 'Cyprus': 'CYP',
    'Denmark': 'DEN', 'Ecuador': 'ECU', 'Eritrea': 'ERI', 'Estonia': 'EST',
    'Georgia': 'GEO', 'Guinea-Bissau': 'GBS', 'Haiti': 'HAI', 'Hong Kong': 'HKG',
    'Hungary': 'HUN', 'Iceland': 'ISL', 'India': 'IND', 'Iran': 'IRI',
    'Ireland': 'IRL', 'Israel': 'ISR', 'Jamaica': 'JAM', 'Japan': 'JPN',
    'Kazakhstan': 'KAZ', 'Kenya': 'KEN', 'Kosovo': 'KOS', 'Kyrgyzstan': 'KGZ',
    'Latvia': 'LAT', 'Lebanon': 'LBN', 'Liechtenstein': 'LIE', 'Lithuania': 'LTU',
    'Luxembourg': 'LUX', 'Madagascar': 'MAD', 'Malaysia': 'MAS', 'Malta': 'MLT',
    'Mexico': 'MEX', 'Moldova': 'MDA', 'Monaco': 'MON', 'Mongolia': 'MGL',
    'Montenegro': 'MNE', 'Morocco': 'MAR', 'New Zealand': 'NZL', 'Nigeria': 'NGR',
    'North Macedonia': 'MKD', 'Pakistan': 'PAK', 'Philippines': 'PHI',
    'Poland': 'POL', 'Portugal': 'POR', 'Puerto Rico': 'PUR', 'Romania': 'ROU',
    'San Marino': 'SMR', 'Saudi Arabia': 'KSA', 'Serbia': 'SRB', 'Singapore': 'SGP',
    'South Africa': 'RSA', 'South Korea': 'KOR', 'Spain': 'ESP', 'Thailand': 'THA',
    'Trinidad and Tobago': 'TTO', 'Turkey': 'TUR', 'Ukraine': 'UKR',
    'United Arab Emirates': 'UAE', 'United States': 'USA', 'Uruguay': 'URU',
    'Uzbekistan': 'UZB', 'Venezuela': 'VEN'
}

def get_nation_ioc_code(nation_name):
    """Get IOC code for a nation."""
    return IOC_CODE_MAP.get(nation_name, nation_name[:3].upper())

def format_sports_list(sports):
    """Format list of sports for display."""
    if len(sports) == 1:
        return sports[0]
    elif len(sports) == 2:
        return f"{sports[0]} and {sports[1]}"
    else:
        return f"{', '.join(sports[:-1])}, and {sports[-1]}"

def update_nation_cards():
    """Update nation cards with actual sports data."""
    
    base_path = Path(__file__).parent.parent
    
    # Load data files
    with open(base_path / 'data' / 'nation_events_2026.json', 'r', encoding='utf-8') as f:
        nation_events = json.load(f)
    
    with open(base_path / 'data' / 'participating_nations_2026.json', 'r', encoding='utf-8') as f:
        participating_nations = json.load(f)
    
    with open(base_path / 'data' / 'athlete_counts_2026.json', 'r', encoding='utf-8') as f:
        athlete_counts = json.load(f)
    
    print(f"Loaded data for {len(nation_events)} nations with event schedules")
    
    # Create a mapping of IOC codes to nation data
    ioc_to_nation = {}
    for nation_name, data in nation_events.items():
        ioc_code = get_nation_ioc_code(nation_name)
        ioc_to_nation[ioc_code] = {
            'name': nation_name,
            'data': data
        }
    
    # Read HTML file
    html_file = base_path / 'index.html'
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find all nation cards and update their sports
    # Pattern: <div class="nation-card underdog"> with <span class="nation-name">NAME</span>
    card_pattern = r'(<div class="nation-card underdog">.*?<span class="nation-name">([^<]+)</span>.*?</div>\s*<!-- End [^>]+ card -->|<div class="nation-card underdog">.*?<span class="nation-name">([^<]+)</span>.*?(?=<div class="nation-card|</section>))'
    
    updates_made = 0
    
    def update_card(match):
        nonlocal updates_made
        full_card = match.group(0)
        # Nation name can be in either group 2 or 3 depending on pattern match
        nation_name = match.group(2) or match.group(3) if match.lastindex >= 3 else match.group(2)
        
        if not nation_name:
            return full_card
        
        nation_name = nation_name.strip()
        
        # Check if we have event data for this nation
        if nation_name not in nation_events:
            return full_card  # No updates needed
        
        nation_data = nation_events[nation_name]
        sports = nation_data['sports']
        total_events = nation_data['total_events']
        probable_events = nation_data['probable_events']
        
        # Update the sports tags - replace <span class="sport-tag">TBD</span>
        if '<span class="sport-tag">TBD</span>' in full_card:
            # Create sport tags for each sport
            sport_tags = ''.join([f'<span class="sport-tag">{sport}</span>\n                            ' for sport in sports])
            # Remove trailing whitespace from last tag
            sport_tags = sport_tags.rstrip()
            
            # Replace the TBD tag
            full_card = full_card.replace(
                '<span class="sport-tag">TBD</span>',
                sport_tags
            )
            updates_made += 1
            print(f"Updated {nation_name}: {len(sports)} sports, {total_events} events")
        
        return full_card
    
    # Update all cards - simpler pattern
    # Match from nation-card to either next nation-card or end of section
    simple_pattern = r'<div class="nation-card underdog">.*?<span class="nation-name">([^<]+)</span>.*?(?=<div class="nation-card|</section>|<!-- End)'
    
    def simple_update(match):
        nonlocal updates_made
        full_card = match.group(0)
        nation_name = match.group(1).strip()
        
        # Check if we have event data for this nation
        if nation_name not in nation_events:
            return full_card  # No updates needed
        
        nation_data = nation_events[nation_name]
        sports = nation_data['sports']
        total_events = nation_data['total_events']
        
        # Update the sports tags - replace <span class="sport-tag">TBD</span>
        if '<span class="sport-tag">TBD</span>' in full_card:
            # Create sport tags for each sport
            sport_tags = ''.join([f'<span class="sport-tag">{sport}</span>\n                            ' for sport in sports])
            sport_tags = sport_tags.rstrip()
            
            # Replace the TBD tag
            full_card = full_card.replace(
                '<span class="sport-tag">TBD</span>',
                sport_tags
            )
            updates_made += 1
            print(f"Updated {nation_name}: {len(sports)} sports, {total_events} events")
        
        return full_card
    
    # Update all cards
    updated_html = re.sub(simple_pattern, simple_update, html_content, flags=re.DOTALL)
    
    # Write updated HTML
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    
    print(f"\n[OK] Updated {updates_made} nation cards in index.html")
    
    return updates_made

if __name__ == '__main__':
    update_nation_cards()
