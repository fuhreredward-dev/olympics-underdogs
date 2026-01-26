"""
Update nation cards with actual competition dates and create interactive schedule.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def format_date_range(first_date, last_date):
    """Format date range for display."""
    first = datetime.strptime(first_date, '%Y-%m-%d')
    last = datetime.strptime(last_date, '%Y-%m-%d')
    
    if first == last:
        return first.strftime('%b %d')
    elif first.month == last.month:
        return f"{first.strftime('%b %d')}-{last.day}"
    else:
        return f"{first.strftime('%b %d')} - {last.strftime('%b %d')}"

def update_nation_cards_with_dates():
    """Update nation cards with actual competition dates."""
    
    base_path = Path(__file__).parent.parent
    
    # Load data
    with open(base_path / 'data' / 'nation_schedules_2026.json', 'r', encoding='utf-8') as f:
        nation_schedules = json.load(f)
    
    # Read HTML
    html_file = base_path / 'index.html'
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("Updating nation cards with competition dates...")
    print("=" * 70)
    
    updates_made = 0
    
    # Pattern to match nation cards
    def update_card(match):
        nonlocal updates_made
        full_card = match.group(0)
        nation_name = match.group(1).strip()
        
        # Check if we have schedule data
        if nation_name not in nation_schedules:
            return full_card
        
        schedule = nation_schedules[nation_name]
        if schedule['total_competition_days'] == 0:
            return full_card
        
        # Format date string
        date_str = format_date_range(schedule['first_competition'], schedule['last_competition'])
        num_days = schedule['total_competition_days']
        
        # Update the competing days line
        # Replace <div class="competing-days">📅 TBD</div>
        if '📅 TBD</div>' in full_card:
            new_date_line = f'📅 Competing: {num_days} days ({date_str})</div>'
            full_card = full_card.replace('📅 TBD</div>', new_date_line)
            updates_made += 1
            print(f"Updated {nation_name}: {num_days} days ({date_str})")
        
        return full_card
    
    # Simple pattern to match nation cards
    pattern = r'<div class="nation-card underdog">.*?<span class="nation-name">([^<]+)</span>.*?(?=<div class="nation-card|</section>|<!-- End)'
    
    # Update all cards
    updated_html = re.sub(pattern, update_card, html_content, flags=re.DOTALL)
    
    # Write updated HTML
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    
    print(f"\n[OK] Updated {updates_made} nation cards in index.html")
    
    return updates_made

if __name__ == '__main__':
    update_nation_cards_with_dates()
