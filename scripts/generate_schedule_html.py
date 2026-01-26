"""
Generate interactive schedule HTML page for underdog competitions.
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def generate_interactive_schedule():
    """Generate interactive daily schedule HTML page."""
    
    base_path = Path(__file__).parent.parent
    
    # Load data
    with open(base_path / 'data' / 'daily_underdog_schedule_2026.json', 'r', encoding='utf-8') as f:
        daily_schedule = json.load(f)
    
    with open(base_path / 'data' / 'nation_schedules_2026.json', 'r', encoding='utf-8') as f:
        nation_schedules = json.load(f)
    
    # Load event_nations to derive a complete sports list
    try:
        with open(base_path / 'data' / 'event_nations_2026.json', 'r', encoding='utf-8') as f:
            event_nations = json.load(f)
        event_sports = set()
        for event_name in event_nations.keys():
            sport = event_name.split(' - ')[0]
            event_sports.add(sport)
    except FileNotFoundError:
        event_nations = {}
        event_sports = set()
    
    # Also load participating nations for cross-page consistency
    try:
        with open(base_path / 'data' / 'participating_nations_2026.json', 'r', encoding='utf-8') as f:
            participating_nations = json.load(f)
    except FileNotFoundError:
        participating_nations = []
    
    print("Generating interactive schedule page...")
    
    # Group events by date
    dates = sorted(daily_schedule.keys())
    
    # Build HTML
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Olympic Underdog Schedule 2026 | Milano-Cortina</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            padding: 40px 20px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .nav-links {
            text-align: center;
            margin: 20px 0;
        }
        
        .nav-links a {
            display: inline-block;
            padding: 12px 24px;
            margin: 0 10px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .nav-links a:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .filters {
            background: rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }
        
        .filter-group {
            flex: 1;
            min-width: 200px;
        }
        
        .filter-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        
        .filter-group input,
        .filter-group select {
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            border: none;
            background: rgba(255, 255, 255, 0.9);
            font-size: 14px;
        }
        
        .day-section {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        
        .day-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.3);
        }
        
        .day-title {
            font-size: 2em;
            font-weight: bold;
        }
        
        .day-stats {
            text-align: right;
            opacity: 0.9;
        }
        
        .event-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #4ade80;
        }
        
        .event-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .event-title {
            font-size: 1.3em;
            font-weight: bold;
            color: #4ade80;
        }
        
        .event-time {
            background: rgba(0, 0, 0, 0.3);
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
        
        .nations-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
        }
        
        .nation-pill {
            background: rgba(255, 255, 255, 0.15);
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s;
        }
        
        .nation-pill:hover {
            background: rgba(255, 255, 255, 0.25);
            transform: scale(1.05);
        }
        
        .nation-pill.unconfirmed {
            opacity: 0.6;
            border: 1px dashed rgba(255, 255, 255, 0.3);
        }
        
        .athlete-count {
            background: rgba(0, 0, 0, 0.3);
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.85em;
            margin-left: 5px;
        }
        
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .summary-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .summary-number {
            font-size: 2.5em;
            font-weight: bold;
            color: #4ade80;
        }
        
        .summary-label {
            opacity: 0.8;
            margin-top: 5px;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2em;
            }
            
            .day-title {
                font-size: 1.5em;
            }
            
            .nations-grid {
                grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏆 Olympic Underdog Schedule</h1>
        <p>Milano-Cortina 2026 Winter Olympics | Complete Competition Calendar</p>
    </div>
    
    <div class="nav-links">
        <a href="index.html">← Back to Main Page</a>
        <a href="#summary">📊 Summary</a>
    </div>
    
    <div class="filters">
        <div class="filter-group">
            <label for="dateFilter">📅 Filter by Date:</label>
            <select id="dateFilter" onchange="filterEvents()">
                <option value="all">All Dates</option>
"""
    
    # Add date options
    for date in dates:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        date_str = date_obj.strftime('%a %b %d, %Y')
        html += f'                <option value="{date}">{date_str}</option>\n'
    
    html += """            </select>
        </div>
        <div class="filter-group">
            <label for="sportFilter">🎿 Filter by Sport:</label>
            <select id="sportFilter" onchange="filterEvents()">
                <option value="all">All Sports</option>
"""
    
    # Get unique sports (prefer the comprehensive set from event_nations)
    sports = set(event_sports)
    if not sports:
        for events in daily_schedule.values():
            for event_name in events.keys():
                sport = event_name.split(' - ')[0]
                sports.add(sport)
    
    for sport in sorted(sports):
        html += f'                <option value="{sport}">{sport}</option>\n'
    
    html += """            </select>
        </div>
        <div class="filter-group">
            <label for="nationSearch">🔍 Search Nation:</label>
            <input type="text" id="nationSearch" placeholder="Type nation name..." oninput="filterEvents()">
        </div>
    </div>
    
    <div id="summary" class="summary-grid">
        <div class="summary-card">
            <div class="summary-number">""" + str(len(participating_nations)) + """</div>
            <div class="summary-label">Participating Nations</div>
        </div>
        <div class="summary-card">
            <div class="summary-number">""" + str(len([n for n in nation_schedules.values() if n.get('total_competition_days', 0) > 0])) + """</div>
            <div class="summary-label">Nations with Schedules</div>
        </div>
        <div class="summary-card">
            <div class="summary-number">""" + str(len(dates)) + """</div>
            <div class="summary-label">Competition Days</div>
        </div>
        <div class="summary-card">
            <div class="summary-number">""" + str(len(sports)) + """</div>
            <div class="summary-label">Total Sports</div>
        </div>
        <div class="summary-card">
            <div class="summary-number">""" + str(sum(len(events) for events in daily_schedule.values())) + """</div>
            <div class="summary-label">Total Events</div>
        </div>
        <div class="summary-card">
            <div class="summary-number">""" + str(sum(len(nations) for events in daily_schedule.values() for nations in events.values())) + """</div>
            <div class="summary-label">Nation Participations</div>
        </div>
    </div>
    
    <div id="schedule">
"""
    
    # Generate day sections
    for date in dates:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        day_name = date_obj.strftime('%A')
        date_str = date_obj.strftime('%B %d, %Y')
        
        events = daily_schedule[date]
        total_nations = sum(len(nations) for nations in events.values())
        
        html += f"""        <div class="day-section" data-date="{date}">
            <div class="day-header">
                <div class="day-title">{day_name}, {date_str}</div>
                <div class="day-stats">
                    {len(events)} events • {total_nations} nation participations
                </div>
            </div>
"""
        
        # Sort events by time
        sorted_events = sorted(events.items(), key=lambda x: x[1][0]['time_est'] if x[1] else '00:00')
        
        for event_name, nations in sorted_events:
            sport = event_name.split(' - ')[0]
            event_display = event_name.split(' - ')[1] if ' - ' in event_name else event_name
            time_est = nations[0]['time_est'] if nations else ''
            
            html += f"""            <div class="event-card" data-sport="{sport}">
                <div class="event-header">
                    <div class="event-title">{sport} - {event_display}</div>
                    <div class="event-time">⏰ {time_est} EST</div>
                </div>
                <div class="nations-grid">
"""
            
            # Sort nations alphabetically
            for nation_info in sorted(nations, key=lambda x: x['nation']):
                nation = nation_info['nation']
                athletes = nation_info['athletes']
                status = nation_info['status']
                status_class = 'unconfirmed' if status == 'unconfirmed' else ''
                status_icon = '?' if status == 'unconfirmed' else '✓'
                
                html += f"""                    <div class="nation-pill {status_class}" data-nation="{nation}">
                        <span>{status_icon} {nation}</span>
                        <span class="athlete-count">{athletes}</span>
                    </div>
"""
            
            html += """                </div>
            </div>
"""
        
        html += """        </div>
"""
    
    html += """    </div>
    
    <script>
        function filterEvents() {
            const dateFilter = document.getElementById('dateFilter').value;
            const sportFilter = document.getElementById('sportFilter').value;
            const nationSearch = document.getElementById('nationSearch').value.toLowerCase();
            
            const daySections = document.querySelectorAll('.day-section');
            
            daySections.forEach(section => {
                const sectionDate = section.dataset.date;
                let showSection = dateFilter === 'all' || dateFilter === sectionDate;
                
                if (showSection) {
                    const eventCards = section.querySelectorAll('.event-card');
                    let visibleEvents = 0;
                    
                    eventCards.forEach(card => {
                        const cardSport = card.dataset.sport;
                        const nations = card.querySelectorAll('.nation-pill');
                        
                        let showCard = sportFilter === 'all' || sportFilter === cardSport;
                        
                        if (showCard && nationSearch) {
                            let hasMatchingNation = false;
                            nations.forEach(nation => {
                                const nationName = nation.dataset.nation.toLowerCase();
                                if (nationName.includes(nationSearch)) {
                                    hasMatchingNation = true;
                                    nation.style.display = 'flex';
                                } else {
                                    nation.style.display = 'none';
                                }
                            });
                            showCard = hasMatchingNation;
                        } else {
                            nations.forEach(nation => {
                                nation.style.display = 'flex';
                            });
                        }
                        
                        card.style.display = showCard ? 'block' : 'none';
                        if (showCard) visibleEvents++;
                    });
                    
                    section.style.display = visibleEvents > 0 ? 'block' : 'none';
                } else {
                    section.style.display = 'none';
                }
            });
        }
        
        // Add smooth scroll
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    </script>
</body>
</html>
"""
    
    # Save HTML file
    output_file = base_path / 'schedule.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"[OK] Generated interactive schedule: {output_file}")
    print(f"     {len(dates)} days, {sum(len(events) for events in daily_schedule.values())} events")

if __name__ == '__main__':
    generate_interactive_schedule()
