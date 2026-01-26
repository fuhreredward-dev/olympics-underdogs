"""
Generate comprehensive HTML overview page for 2026 Winter Olympics underdogs.
"""

import json
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime


class OlympicsHTMLGenerator:
    """Generates HTML overview page."""
    
    # Full nation names by IOC code
    NATION_NAMES = {
        'ALB': 'Albania', 'AND': 'Andorra', 'ARG': 'Argentina', 'ARM': 'Armenia',
        'AUS': 'Australia', 'AUT': 'Austria', 'AZE': 'Azerbaijan', 'BEL': 'Belgium',
        'BEN': 'Benin', 'BIH': 'Bosnia and Herzegovina', 'BOL': 'Bolivia', 'BRA': 'Brazil',
        'BUL': 'Bulgaria', 'CAN': 'Canada', 'CHI': 'Chile', 'CHN': 'China',
        'COL': 'Colombia', 'CRO': 'Croatia', 'CYP': 'Cyprus', 'CZE': 'Czech Republic',
        'DEN': 'Denmark', 'ECU': 'Ecuador', 'ERI': 'Eritrea', 'ESP': 'Spain',
        'EST': 'Estonia', 'FIN': 'Finland', 'FRA': 'France', 'GBR': 'Great Britain',
        'GEO': 'Georgia', 'GER': 'Germany', 'GRE': 'Greece', 'HAI': 'Haiti',
        'HKG': 'Hong Kong', 'HUN': 'Hungary', 'IND': 'India', 'IRI': 'Iran',
        'IRL': 'Ireland', 'ISL': 'Iceland', 'ISR': 'Israel', 'ITA': 'Italy',
        'JAM': 'Jamaica', 'JPN': 'Japan', 'KAZ': 'Kazakhstan', 'KEN': 'Kenya',
        'KGZ': 'Kyrgyzstan', 'KOR': 'South Korea', 'KOS': 'Kosovo', 'KSA': 'Saudi Arabia',
        'LAT': 'Latvia', 'LIB': 'Lebanon', 'LIE': 'Liechtenstein', 'LTU': 'Lithuania',
        'LUX': 'Luxembourg', 'MAD': 'Madagascar', 'MAR': 'Morocco', 'MAS': 'Malaysia',
        'MDA': 'Moldova', 'MEX': 'Mexico', 'MGL': 'Mongolia', 'MKD': 'North Macedonia',
        'MLT': 'Malta', 'MNE': 'Montenegro', 'MON': 'Monaco', 'NED': 'Netherlands',
        'NGR': 'Nigeria', 'NOR': 'Norway', 'NZL': 'New Zealand', 'PAK': 'Pakistan',
        'PHI': 'Philippines', 'POL': 'Poland', 'POR': 'Portugal', 'PUR': 'Puerto Rico',
        'ROM': 'Romania', 'RSA': 'South Africa', 'SRB': 'Serbia', 'SGP': 'Singapore',
        'SKK': 'Slovakia', 'SLO': 'Slovenia', 'SMR': 'San Marino', 'SUI': 'Switzerland',
        'SVK': 'Slovakia', 'SWE': 'Sweden', 'THA': 'Thailand', 'TPE': 'Chinese Taipei',
        'TTO': 'Trinidad and Tobago', 'TUR': 'Turkey', 'UAE': 'United Arab Emirates',
        'UKR': 'Ukraine', 'URU': 'Uruguay', 'USA': 'United States', 'UZB': 'Uzbekistan',
        'VEN': 'Venezuela', 'GBS': 'Guinea-Bissau'
    }
    
    # Nations below the equator (Southern Hemisphere)
    SOUTHERN_HEMISPHERE = {
        'AUS', 'NZL', 'RSA', 'BRA', 'CHI', 'ARG', 'URU', 'ECU', 'MAD'
    }
    
    def __init__(self):
        """Load all data files."""
        self.participating_nations = self._load_json('data/participating_nations_2026.json')
        self.athlete_counts = self._load_json('data/athlete_counts_2026.json')
        self.nation_sports = self._load_json('data/nation_sports_participation_2026.json')
        self.nation_schedules = self._load_json('data/nation_schedules_2026.json')
        self.schedule = self._load_json('data/schedule/2026_olympics_schedule.json')
        self.winter_medals = self._load_json('data/medals/winter_medals.json')
        self.all_time_medals = self._load_json('data/medals/all_time_medals.json')
        self.population = self._load_json('data/population/population.json')
    
    def _load_json(self, filepath: str):
        """Load JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} if 'json' in filepath else []
    
    def generate_html(self) -> str:
        """Generate complete HTML page."""
        
        # Calculate stats
        nation_data = self._calculate_nation_data()
        sport_stats = self._calculate_sport_stats(nation_data)
        underdog_stats = self._calculate_underdog_stats()
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026 Winter Olympics - Underdog Nations Overview</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f0f23;
            color: #e0e0e0;
            line-height: 1.6;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: #1a1a2e;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.8);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #0f4c75 0%, #1b1b2f 100%);
            color: white;
            padding: 40px;
            text-align: center;
            border-bottom: 3px solid #00d4ff;
        }}
        
        h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            color: #00d4ff;
        }}
        
        .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
            color: #a8dadc;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        h2 {{
            color: #00d4ff;
            font-size: 2em;
            margin-bottom: 20px;
            border-bottom: 3px solid #00d4ff;
            padding-bottom: 10px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
            border: 2px solid #00d4ff;
        }}
        
        .stat-number {{
            font-size: 3em;
            font-weight: bold;
            margin: 10px 0;
            color: #00d4ff;
        }}
        
        .stat-label {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .accordion {{
            background: #16213e;
            border-radius: 10px;
            margin-bottom: 10px;
            border: 1px solid #2a2a40;
        }}
        
        .accordion-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            cursor: pointer;
            background: #16213e;
            border-radius: 10px;
            transition: background 0.3s;
        }}
        
        .accordion-header:hover {{
            background: #1e2d50;
        }}
        
        .accordion-title {{
            font-weight: bold;
            color: #00d4ff;
            font-size: 1.1em;
        }}
        
        .accordion-count {{
            background: #00d4ff;
            color: #0f0f23;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }}
        
        .accordion-content {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
            background: #1a1a2e;
        }}
        
        .accordion-content.active {{
            max-height: 1000px;
            padding: 20px;
        }}
        
        .nations-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .nation-pill {{
            background: #0f3460;
            padding: 8px 15px;
            border-radius: 20px;
            border: 1px solid #00d4ff;
            color: #e0e0e0;
            font-size: 0.95em;
        }}
        
        .day-tabs {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 30px;
        }}
        
        .day-tab {{
            padding: 12px 20px;
            background: #16213e;
            border: 2px solid #2a2a40;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            color: #a8dadc;
        }}
        
        .day-tab:hover {{
            border-color: #00d4ff;
            transform: translateY(-2px);
        }}
        
        .day-tab.active {{
            background: #00d4ff;
            color: #0f0f23;
            border-color: #00d4ff;
        }}
        
        .day-content {{
            display: none;
            background: #16213e;
            padding: 30px;
            border-radius: 15px;
            border: 2px solid #00d4ff;
        }}
        
        .day-content.active {{
            display: block;
            animation: fadeIn 0.3s;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        .sport-section {{
            margin-bottom: 25px;
            background: #1a1a2e;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #00d4ff;
        }}
        
        .sport-title {{
            font-size: 1.3em;
            color: #00d4ff;
            margin-bottom: 15px;
            font-weight: bold;
        }}
        
        .underdog-nations {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .underdog-chip {{
            background: #f39c12;
            color: #0f0f23;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.95em;
        }}
        
        .nations-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .nation-card {{
            background: #16213e;
            border-radius: 10px;
            padding: 20px;
            border: 2px solid #2a2a40;
            transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s;
        }}
        
        .nation-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,212,255,0.3);
            border-color: #00d4ff;
        }}
        
        .nation-card.underdog {{
            border-color: #f39c12;
            background: #1e2530;
        }}
        
        .nation-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
        }}
        
        .nation-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #00d4ff;
        }}
        
        .underdog-badge {{
            background: #f39c12;
            color: #0f0f23;
            padding: 3px 8px;
            border-radius: 5px;
            font-size: 0.7em;
            margin-left: auto;
            font-weight: bold;
        }}
        
        .tier-badge {{
            padding: 5px 12px;
            border-radius: 8px;
            font-size: 0.85em;
            font-weight: bold;
            margin-left: 10px;
        }}
        
        .tier-5 {{
            background: #e74c3c;
            color: white;
            border: 2px solid #c0392b;
        }}
        
        .tier-4 {{
            background: #e67e22;
            color: white;
            border: 2px solid #d35400;
        }}
        
        .tier-3 {{
            background: #f39c12;
            color: #0f0f23;
            border: 2px solid #d68910;
        }}
        
        .tier-2 {{
            background: #f1c40f;
            color: #0f0f23;
            border: 2px solid #d4ac0d;
        }}
        
        .tier-1 {{
            background: #3498db;
            color: white;
            border: 2px solid #2980b9;
        }}
        
        .tier-section {{
            margin-bottom: 40px;
            background: #16213e;
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid;
        }}
        
        .tier-section.tier-5 {{
            border-left-color: #e74c3c;
        }}
        
        .tier-section.tier-4 {{
            border-left-color: #e67e22;
        }}
        
        .tier-section.tier-3 {{
            border-left-color: #f39c12;
        }}
        
        .tier-section.tier-2 {{
            border-left-color: #f1c40f;
        }}
        
        .tier-section.tier-1 {{
            border-left-color: #3498db;
        }}
        
        .tier-header {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }}
        
        .tier-title {{
            font-size: 1.8em;
            font-weight: bold;
            color: #00d4ff;
        }}
        
        .tier-description {{
            color: #a8dadc;
            margin-bottom: 20px;
            font-style: italic;
        }}
        
        .nation-stats {{
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }}
        
        .mini-stat {{
            background: #1a1a2e;
            padding: 8px 12px;
            border-radius: 5px;
            font-size: 0.9em;
            color: #a8dadc;
            border: 1px solid #2a2a40;
        }}
        
        .sports-list {{
            margin-top: 10px;
        }}
        
        .sport-tag {{
            display: inline-block;
            background: #0f3460;
            color: #00d4ff;
            padding: 5px 10px;
            border-radius: 5px;
            margin: 3px;
            font-size: 0.85em;
            border: 1px solid #00d4ff;
        }}
        
        .competing-days {{
            margin-top: 10px;
            font-size: 0.9em;
            color: #a8dadc;
        }}
        
        .criteria-text {{
            color: white;
            font-size: 0.9em;
        }}
        
        .sport-rankings {{
            background: #16213e;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #2a2a40;
        }}
        
        .sport-row {{
            padding: 12px;
            margin: 5px 0;
            background: #1a1a2e;
            border-radius: 5px;
            transition: transform 0.2s, border-left 0.2s;
            border-left: 3px solid transparent;
        }}
        
        .sport-row:hover {{
            transform: translateX(5px);
            border-left-color: #00d4ff;
        }}
        
        .sport-row[open] {{
            border-left-color: #00d4ff;
        }}

        .sport-row summary {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            list-style: none;
        }}

        .sport-row summary::-webkit-details-marker {{
            display: none;
        }}

        .sport-name {{
            font-weight: bold;
            color: #e0e0e0;
        }}
        
        .sport-count {{
            background: #00d4ff;
            color: #0f0f23;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }}

        .sport-nations {{
            margin-top: 12px;
            padding-top: 10px;
            border-top: 1px solid #2a2a40;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .sport-nation {{
            background: #0f3460;
            color: #00d4ff;
            padding: 6px 10px;
            border-radius: 16px;
            border: 1px solid #00d4ff;
            font-size: 0.9em;
        }}
        
        footer {{
            background: #0f0f23;
            color: #a8dadc;
            text-align: center;
            padding: 20px;
            margin-top: 40px;
            border-top: 2px solid #00d4ff;
        }}
        
        /* Mobile Responsive Styles */
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            
            .container {{
                border-radius: 10px;
            }}
            
            header {{
                padding: 20px 15px;
            }}
            
            h1 {{
                font-size: 1.8em;
                margin-bottom: 8px;
            }}
            
            .subtitle {{
                font-size: 0.9em;
            }}
            
            .content {{
                padding: 20px 15px;
            }}
            
            h2 {{
                font-size: 1.5em;
                margin-bottom: 15px;
            }}
            
            h3 {{
                font-size: 1.2em;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr;
                gap: 15px;
            }}
            
            .stat-card {{
                padding: 20px 15px;
            }}
            
            .stat-number {{
                font-size: 2.2em;
            }}
            
            .stat-label {{
                font-size: 1em;
            }}
            
            .day-tabs {{
                overflow-x: auto;
                flex-wrap: nowrap;
                -webkit-overflow-scrolling: touch;
                scrollbar-width: thin;
                scrollbar-color: #00d4ff #16213e;
            }}
            
            .day-tabs::-webkit-scrollbar {{
                height: 6px;
            }}
            
            .day-tabs::-webkit-scrollbar-track {{
                background: #16213e;
                border-radius: 3px;
            }}
            
            .day-tabs::-webkit-scrollbar-thumb {{
                background: #00d4ff;
                border-radius: 3px;
            }}
            
            .day-tab {{
                padding: 10px 15px;
                font-size: 0.9em;
                white-space: nowrap;
                flex-shrink: 0;
            }}
            
            .day-content {{
                padding: 20px 15px;
            }}
            
            .sport-section {{
                padding: 15px;
                margin-bottom: 20px;
            }}
            
            .sport-title {{
                font-size: 1.1em;
            }}
            
            .nations-grid {{
                grid-template-columns: 1fr;
                gap: 15px;
            }}
            
            .nation-card {{
                padding: 15px;
            }}
            
            .nation-name {{
                font-size: 1.1em;
            }}
            
            .nation-stats {{
                gap: 10px;
            }}
            
            .mini-stat {{
                font-size: 0.85em;
                padding: 6px 10px;
            }}
            
            .sport-tag {{
                font-size: 0.8em;
                padding: 4px 8px;
            }}
            
            .tier-badge {{
                font-size: 0.75em;
                padding: 4px 10px;
            }}
            
            .tier-title {{
                font-size: 1.4em;
            }}
            
            .tier-description {{
                font-size: 0.9em;
            }}
            
            .accordion-header {{
                padding: 12px 15px;
            }}
            
            .accordion-title {{
                font-size: 1em;
            }}
            
            .accordion-count {{
                font-size: 0.9em;
                padding: 4px 12px;
            }}
            
            .nations-list {{
                gap: 8px;
            }}
            
            .nation-pill {{
                font-size: 0.85em;
                padding: 6px 12px;
            }}
            
            .underdog-chip {{
                font-size: 0.85em;
                padding: 6px 12px;
            }}
            
            .sport-row {{
                padding: 10px;
                font-size: 0.9em;
            }}
            
            .criteria-text {{
                font-size: 0.85em;
            }}
            
            footer {{
                padding: 15px;
                font-size: 0.9em;
            }}
        }}
        
        @media (max-width: 480px) {{
            h1 {{
                font-size: 1.5em;
            }}
            
            .subtitle {{
                font-size: 0.85em;
            }}
            
            .stat-number {{
                font-size: 1.8em;
            }}
            
            .tier-title {{
                font-size: 1.2em;
            }}
            
            .day-tab {{
                padding: 8px 12px;
                font-size: 0.85em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏂 2026 Winter Olympics</h1>
            <div class="subtitle">Underdog Nations & Competition Overview</div>
            <div class="subtitle">Milan-Cortina d'Ampezzo | February 6-22, 2026</div>
            <div style="margin-top: 20px;">
                <a href="schedule.html" style="display: inline-block; padding: 12px 30px; background: #00d4ff; color: #0f0f23; text-decoration: none; border-radius: 8px; font-weight: bold; transition: transform 0.2s;">📅 View Full Schedule</a>
            </div>
        </header>
        
        <div class="content">
            {self._generate_overview_section(nation_data, sport_stats, underdog_stats)}
            {self._generate_underdog_criteria_section(underdog_stats, nation_data)}
            {self._generate_day_by_day_section(nation_data)}
            {self._generate_sports_rankings_section(sport_stats)}
            {self._generate_nations_section(nation_data)}
            {self._generate_all_nations_section(nation_data)}
        </div>
        
        <footer>
            <p>Data compiled from Wikipedia and official Olympic sources</p>
            <p>Generated {datetime.now().strftime('%B %d, %Y')}</p>
        </footer>
    </div>
    
    <script>
        // Accordion functionality
        document.querySelectorAll('.accordion-header').forEach(header => {{
            header.addEventListener('click', () => {{
                const content = header.nextElementSibling;
                content.classList.toggle('active');
            }});
        }});
        
        // Day tab functionality
        document.querySelectorAll('.day-tab').forEach(tab => {{
            tab.addEventListener('click', () => {{
                const targetDay = tab.dataset.day;
                
                // Remove active class from all tabs and contents
                document.querySelectorAll('.day-tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.day-content').forEach(c => c.classList.remove('active'));
                
                // Add active class to clicked tab and corresponding content
                tab.classList.add('active');
                document.getElementById('day-' + targetDay).classList.add('active');
            }});
        }});
        
        // Activate first day tab by default
        if (document.querySelector('.day-tab')) {{
            document.querySelector('.day-tab').click();
        }}
    </script>
</body>
</html>
"""
        return html
    
    def _calculate_nation_data(self) -> Dict:
        """Calculate comprehensive data for each nation."""
        nation_data = {}
        
        for nation in self.participating_nations:
            # Get sports they compete in
            sports = list(self.nation_sports.get(nation, {}).keys())
            
            # Calculate which days they compete
            competing_days = self._get_competing_days(nation, sports)
            
            # Check underdog status
            underdog_criteria = []
            
            # Criterion 1: < 5 athletes
            athlete_count = self.athlete_counts.get(nation, 0)
            if 1 <= athlete_count < 5:
                underdog_criteria.append("< 5 athletes")
            
            # Criterion 2-3: Olympic medals
            all_time = self.all_time_medals.get(nation, {})
            if all_time.get('gold', 0) == 0:
                underdog_criteria.append("No Olympic gold")
            if all_time.get('total', 0) == 0:
                underdog_criteria.append("No Olympic medals")
            
            # Criterion 4: Population
            pop = self.population.get(nation, float('inf'))
            if pop < 1_000_000:
                underdog_criteria.append(f"Pop: {pop:,}")
            
            # Criterion 5-6: Winter medals
            winter = self.winter_medals.get(nation, {})
            if winter.get('gold', 0) == 0:
                underdog_criteria.append("No Winter gold")
            if winter.get('total', 0) == 0:
                underdog_criteria.append("No Winter medals")
            
            # Criterion 7: Southern Hemisphere
            if nation in self.SOUTHERN_HEMISPHERE:
                underdog_criteria.append("Southern Hemisphere")
            
            # Calculate underdog tier (1-5, where 5 is ultimate underdog)
            criteria_count = len(underdog_criteria)
            if criteria_count >= 6:
                tier = 5  # Ultimate underdog (6-7 criteria)
            elif criteria_count >= 4:
                tier = 4  # Major underdogs (4-5 criteria)
            elif criteria_count == 3:
                tier = 3  # Strong underdogs (3 criteria)
            elif criteria_count == 2:
                tier = 2
            elif criteria_count == 1:
                tier = 1
            else:
                tier = 0  # Not an underdog
            
            nation_data[nation] = {
                'ioc_code': nation,
                'name': self.NATION_NAMES.get(nation, nation),
                'sports': sports,
                'athlete_count': athlete_count,
                'competing_days': sorted(competing_days),
                'is_underdog': len(underdog_criteria) > 0,
                'underdog_criteria': underdog_criteria,
                'underdog_tier': tier,
                'criteria_count': criteria_count,
                'winter_medals': winter.get('total', 0),
                'all_time_medals': all_time.get('total', 0),
                'population': pop if pop != float('inf') else None
            }
        
        return nation_data
    
    def _get_competing_days(self, nation: str, sports: List[str]) -> Set[str]:
        """Get all days when a nation competes."""
        days = set()
        
        # Try to get from nation_schedules first (more reliable)
        # nation_schedules uses full names, so convert IOC code to full name
        nation_name = self.NATION_NAMES.get(nation, nation)
        nation_schedule = self.nation_schedules.get(nation_name, {})
        if 'competition_dates' in nation_schedule:
            return set(nation_schedule['competition_dates'])
        
        # Fallback to schedule data
        for date, day_data in self.schedule.items():
            for sport_entry in day_data['sports']:
                if sport_entry['sport'] in sports:
                    days.add(date)
        
        return days
    
    def _calculate_sport_stats(self, nation_data) -> Dict:
        """Calculate statistics for each sport (underdog nations only)."""
        sport_nations = {}
        
        for nation, sports_data in self.nation_sports.items():
            # Only include underdog nations
            if nation_data.get(nation, {}).get('is_underdog', False):
                for sport in sports_data.keys():
                    if sport not in sport_nations:
                        sport_nations[sport] = []
                    sport_nations[sport].append(nation)
        
        # Sort by number of nations
        sorted_sports = sorted(sport_nations.items(), key=lambda x: len(x[1]), reverse=True)
        
        return {sport: nations for sport, nations in sorted_sports}
    
    def _calculate_underdog_stats(self) -> Dict:
        """Calculate underdog statistics."""
        stats = {
            'total_underdogs': 0,
            'by_criteria': {
                'small_athletes': 0,
                'no_olympic_gold': 0,
                'no_olympic_medals': 0,
                'small_population': 0,
                'no_winter_gold': 0,
                'no_winter_medals': 0,
                'southern_hemisphere': 0
            },
            'ultimate_underdogs': []  # Nations meeting all criteria
        }
        
        for nation in self.participating_nations:
            criteria_count = 0
            
            athlete_count = self.athlete_counts.get(nation, 0)
            if 1 <= athlete_count < 5:
                stats['by_criteria']['small_athletes'] += 1
                criteria_count += 1
            
            all_time = self.all_time_medals.get(nation, {})
            if all_time.get('gold', 0) == 0:
                stats['by_criteria']['no_olympic_gold'] += 1
                criteria_count += 1
            if all_time.get('total', 0) == 0:
                stats['by_criteria']['no_olympic_medals'] += 1
                criteria_count += 1
            
            pop = self.population.get(nation, float('inf'))
            if pop < 1_000_000:
                stats['by_criteria']['small_population'] += 1
                criteria_count += 1
            
            winter = self.winter_medals.get(nation, {})
            if winter.get('gold', 0) == 0:
                stats['by_criteria']['no_winter_gold'] += 1
                criteria_count += 1
            if winter.get('total', 0) == 0:
                stats['by_criteria']['no_winter_medals'] += 1
                criteria_count += 1
            
            if nation in self.SOUTHERN_HEMISPHERE:
                stats['by_criteria']['southern_hemisphere'] += 1
                criteria_count += 1
            
            if criteria_count > 0:
                stats['total_underdogs'] += 1
            
            if criteria_count >= 6:
                stats['ultimate_underdogs'].append(nation)
        
        return stats
    
    def _generate_overview_section(self, nation_data, sport_stats, underdog_stats) -> str:
        """Generate overview statistics section."""
        total_nations = len(self.participating_nations)
        total_underdogs = underdog_stats['total_underdogs']
        most_popular_sport = list(sport_stats.keys())[0] if sport_stats else "N/A"
        least_popular_sport = list(sport_stats.keys())[-1] if sport_stats else "N/A"
        
        # Calculate tier breakdown
        tier_counts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        for nation, data in nation_data.items():
            tier = data.get('underdog_tier', 0)
            if tier > 0:
                tier_counts[tier] += 1
        
        return f"""
            <section class="section">
                <h2>📊 Overview Statistics</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-label">Participating Nations</div>
                        <div class="stat-number">{total_nations}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Underdog Nations</div>
                        <div class="stat-number">{total_underdogs}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Total Sports</div>
                        <div class="stat-number">{len(sport_stats)}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Ultimate Underdogs (Tier 5)</div>
                        <div class="stat-number">{len(underdog_stats['ultimate_underdogs'])}</div>
                        <div style="font-size: 0.9em; margin-top: 10px;">
                            {', '.join([self.NATION_NAMES.get(n, n) for n in underdog_stats['ultimate_underdogs']])}
                        </div>
                    </div>
                </div>
                
                <h3 style="color: #00d4ff; margin-top: 30px; margin-bottom: 15px;">🎯 Underdog Tier Breakdown</h3>
                <div class="stats-grid">
                    <div class="stat-card" style="background: linear-gradient(135deg, #c0392b 0%, #e74c3c 100%);">
                        <div class="stat-label">Tier 5 (6-7 criteria)</div>
                        <div class="stat-number">{tier_counts[5]}</div>
                        <div style="font-size: 0.85em; margin-top: 5px;">Ultimate Underdogs</div>
                    </div>
                    <div class="stat-card" style="background: linear-gradient(135deg, #d35400 0%, #e67e22 100%);">
                        <div class="stat-label">Tier 4 (4-5 criteria)</div>
                        <div class="stat-number">{tier_counts[4]}</div>
                        <div style="font-size: 0.85em; margin-top: 5px;">Major Underdogs</div>
                    </div>
                    <div class="stat-card" style="background: linear-gradient(135deg, #d68910 0%, #f39c12 100%);">
                        <div class="stat-label">Tier 3 (3 criteria)</div>
                        <div class="stat-number">{tier_counts[3]}</div>
                        <div style="font-size: 0.85em; margin-top: 5px;">Strong Underdogs</div>
                    </div>
                    <div class="stat-card" style="background: linear-gradient(135deg, #d4ac0d 0%, #f1c40f 100%); color: #0f0f23;">
                        <div class="stat-label" style="color: #0f0f23;">Tier 2 (2 criteria)</div>
                        <div class="stat-number" style="color: #0f0f23;">{tier_counts[2]}</div>
                        <div style="font-size: 0.85em; margin-top: 5px;">Moderate Underdogs</div>
                    </div>
                    <div class="stat-card" style="background: linear-gradient(135deg, #2980b9 0%, #3498db 100%);">
                        <div class="stat-label">Tier 1 (1 criterion)</div>
                        <div class="stat-number">{tier_counts[1]}</div>
                        <div style="font-size: 0.85em; margin-top: 5px;">Mild Underdogs</div>
                    </div>
                </div>
            </section>
        """
    
    def _generate_underdog_criteria_section(self, underdog_stats, nation_data) -> str:
        """Generate underdog criteria breakdown with interactive accordions."""
        criteria = underdog_stats['by_criteria']
        
        # Map criteria to nation lists
        criteria_nations = {
            'small_athletes': [],
            'no_olympic_gold': [],
            'no_olympic_medals': [],
            'small_population': [],
            'no_winter_gold': [],
            'no_winter_medals': [],
            'southern_hemisphere': []
        }
        
        for ioc, nation_info in nation_data.items():
            athletes = nation_info.get('athlete_count', 0)
            
            if athletes < 5:
                criteria_nations['small_athletes'].append(ioc)
            
            all_time = self.all_time_medals.get(ioc, {})
            if all_time.get('gold', 0) == 0:
                criteria_nations['no_olympic_gold'].append(ioc)
            if all_time.get('total', 0) == 0:
                criteria_nations['no_olympic_medals'].append(ioc)
            
            pop = self.population.get(ioc, float('inf'))
            if pop < 1_000_000:
                criteria_nations['small_population'].append(ioc)
            
            winter = self.winter_medals.get(ioc, {})
            if winter.get('gold', 0) == 0:
                criteria_nations['no_winter_gold'].append(ioc)
            if winter.get('total', 0) == 0:
                criteria_nations['no_winter_medals'].append(ioc)
            
            if ioc in self.SOUTHERN_HEMISPHERE:
                criteria_nations['southern_hemisphere'].append(ioc)
        
        criteria_info = [
            ('small_athletes', '< 5 Athletes'),
            ('no_olympic_gold', 'No Olympic Gold Medals'),
            ('no_olympic_medals', 'No Olympic Medals'),
            ('small_population', 'Population Under 1M'),
            ('no_winter_gold', 'No Winter Olympic Gold'),
            ('no_winter_medals', 'No Winter Olympic Medals'),
            ('southern_hemisphere', 'Southern Hemisphere (Below Equator)')
        ]
        
        html = '<section class="section">\n'
        html += '<h2>🎯 Underdog Criteria Breakdown</h2>\n'
        
        for key, label in criteria_info:
            nations = sorted(criteria_nations[key])
            count = len(nations)
            
            html += f'''
            <div class="accordion">
                <div class="accordion-header">
                    <div class="accordion-title">{label}</div>
                    <div class="accordion-count">{count} nations</div>
                </div>
                <div class="accordion-content">
                    <div class="nations-list">
            '''
            
            for ioc_code in nations:
                name = nation_data[ioc_code]['name'] if ioc_code in nation_data else self.NATION_NAMES.get(ioc_code, ioc_code)
                
                html += f'<div class="nation-pill">{name}</div>\n'
            
            html += '''
                    </div>
                </div>
            </div>
            '''
        
        html += '</section>\n'
        return html
    
    def _generate_sports_rankings_section(self, sport_stats) -> str:
        """Generate sports popularity rankings (underdog nations only)."""
        html = """
            <section class="section">
                <h2>🏅 Sports by Number of Underdog Nations</h2>
                <div class="sport-rankings">
        """
        
        for sport, nations in sport_stats.items():
            nation_names = sorted([self.NATION_NAMES.get(n, n) for n in nations])
            html += """
                    <details class="sport-row">
                        <summary>
                            <span class="sport-name">{sport}</span>
                            <span class="sport-count">{count} underdog nations</span>
                        </summary>
                        <div class="sport-nations">
            """.format(sport=sport, count=len(nations))
            
            if nation_names:
                for name in nation_names:
                    html += f"<span class=\"sport-nation\">{name}</span>"
            else:
                html += "<span class=\"sport-nation\">No underdog nations</span>"
            
            html += """
                        </div>
                    </details>
            """
        
        html += """
                </div>
            </section>
        """
        
        return html
    
    def _generate_nations_section(self, nation_data) -> str:
        """Generate nations grouped by tier."""
        html = '<section class="section">\n'
        html += '<h2>🏅 Nations by Underdog Tier</h2>\n'
        
        tier_info = {
            5: ('Tier 5: Ultimate Underdogs', 'Meet 6-7 criteria - the most compelling underdog stories', 'tier-5'),
            4: ('Tier 4: Major Underdogs', 'Meet 4-5 criteria - exceptional underdog potential', 'tier-4'),
            3: ('Tier 3: Strong Underdogs', 'Meet 3 criteria - significant underdog narratives', 'tier-3'),
            2: ('Tier 2: Moderate Underdogs', 'Meet 2 criteria - notable underdog elements', 'tier-2'),
            1: ('Tier 1: Mild Underdogs', 'Meet 1 criterion - emerging underdog stories', 'tier-1')
        }
        
        # Group nations by tier
        nations_by_tier = {5: [], 4: [], 3: [], 2: [], 1: []}
        for nation, data in nation_data.items():
            tier = data.get('underdog_tier', 0)
            if tier > 0:
                nations_by_tier[tier].append((nation, data))
        
        # Generate sections for each tier (5 to 1)
        for tier in [5, 4, 3, 2, 1]:
            if not nations_by_tier[tier]:
                continue
                
            title, description, tier_class = tier_info[tier]
            nations = sorted(nations_by_tier[tier], key=lambda x: (-x[1]['criteria_count'], x[1]['name']))
            
            html += f'<div class="tier-section {tier_class}">\n'
            html += '<div class="tier-header">\n'
            html += f'<div class="tier-title">{title}</div>\n'
            html += f'<span class="tier-badge {tier_class}">TIER {tier}</span>\n'
            html += '</div>\n'
            html += f'<div class="tier-description">{description} ({len(nations)} nations)</div>\n'
            html += '<div class="nations-grid">\n'
            
            for nation, data in nations:
                nation_name = self.NATION_NAMES.get(nation, nation)
                
                sports_html = ''.join([f'<span class="sport-tag">{sport}</span>' for sport in data['sports']])
                
                competing_days_str = f"{len(data['competing_days'])} days"
                if data['competing_days']:
                    first_day = datetime.strptime(data['competing_days'][0], '%Y-%m-%d').strftime('%b %d')
                    last_day = datetime.strptime(data['competing_days'][-1], '%Y-%m-%d').strftime('%b %d')
                    competing_days_str += f" ({first_day} - {last_day})"
                
                criteria_html = ''
                if data['underdog_criteria']:
                    criteria_html = '<br><span class="criteria-text">🎯 ' + ', '.join(data['underdog_criteria']) + '</span>'
                
                html += f"""
                    <div class="nation-card underdog">
                        <div class="nation-header">
                            <span class="nation-name">{nation_name}</span>
                            <span class="tier-badge {tier_class}">T{tier}</span>
                        </div>
                        <div class="nation-stats">
                            <div class="mini-stat">👥 {data['athlete_count']} athletes</div>
                            <div class="mini-stat">🏆 {data['winter_medals']} Winter medals</div>
                            <div class="mini-stat">🥇 {data['all_time_medals']} All-time medals</div>
                        </div>
                        <div class="competing-days">📅 Competing: {competing_days_str}</div>
                        <div class="sports-list">
                            {sports_html}
                        </div>
                        {criteria_html}
                    </div>
                """
            
            html += '</div>\n'
            html += '</div>\n'
        
        html += '</section>\n'
        return html
    
    def _generate_all_nations_section(self, nation_data) -> str:
        """Generate all nations including non-underdogs."""
        # Get non-underdog nations
        non_underdogs = [(nation, data) for nation, data in nation_data.items() if not data['is_underdog']]
        
        if not non_underdogs:
            return ""
        
        html = '<section class="section">\n'
        html += '<h2>🌍 Other Participating Nations</h2>\n'
        html += '<div class="nations-grid">\n'
        
        for nation, data in sorted(non_underdogs, key=lambda x: -x[1]['athlete_count']):
            nation_name = self.NATION_NAMES.get(nation, nation)
            
            sports_html = ''.join([f'<span class="sport-tag">{sport}</span>' for sport in data['sports']])
            
            competing_days_str = f"{len(data['competing_days'])} days"
            if data['competing_days']:
                first_day = datetime.strptime(data['competing_days'][0], '%Y-%m-%d').strftime('%b %d')
                last_day = datetime.strptime(data['competing_days'][-1], '%Y-%m-%d').strftime('%b %d')
                competing_days_str += f" ({first_day} - {last_day})"
            
            html += f"""
                <div class="nation-card">
                    <div class="nation-header">
                        <span class="nation-name">{nation_name}</span>
                    </div>
                    <div class="nation-stats">
                        <div class="mini-stat">👥 {data['athlete_count']} athletes</div>
                        <div class="mini-stat">🏆 {data['winter_medals']} Winter medals</div>
                        <div class="mini-stat">🥇 {data['all_time_medals']} All-time medals</div>
                    </div>
                    <div class="competing-days">📅 Competing: {competing_days_str}</div>
                    <div class="sports-list">
                        {sports_html}
                    </div>
                </div>
            """
        
        html += '</div>\n'
        html += '</section>\n'
        return html
    
    def _generate_calendar_section(self) -> str:
        """Generate day-by-day calendar."""
        html = """
            <section class="section">
                <h2>📅 Competition Calendar</h2>
                <div class="calendar">
        """
        
        for date in sorted(self.schedule.keys()):
            day_data = self.schedule[date]
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date_str = date_obj.strftime('%A, %B %d, %Y')
            
            sports_html = ''.join([
                f'<span class="sport-tag">{sport["sport"]}</span>'
                for sport in day_data['sports']
            ])
            
            html += f"""
                    <div class="day-card">
                        <div class="date-header">{date_str}</div>
                        <div class="day-sports">
                            {sports_html}
                        </div>
                    </div>
            """
        
        html += """
                </div>
            </section>
        """
        
        return html
    
    def _generate_day_by_day_section(self, nation_data) -> str:
        """Generate interactive day-by-day view with underdog nations."""
        
        # Build map of date -> underdog nations competing
        day_underdogs = {}
        for date in sorted(self.schedule.keys()):
            day_underdogs[date] = []
            
            # Get sports for this day
            day_sports = set()
            for sport_info in self.schedule[date]['sports']:
                sport_name = sport_info['sport']
                day_sports.add(sport_name)
            
            # Find underdog nations competing in these sports
            for nation_info in nation_data.values():
                if nation_info['is_underdog']:
                    ioc = nation_info['ioc_code']
                    # Check if this nation competes in any sport on this day
                    nation_sports = set(self.nation_sports.get(ioc, {}).keys())
                    if nation_sports.intersection(day_sports):
                        day_underdogs[date].append(nation_info)
        
        html = '<section class="section">\n'
        html += '<h2>📅 Daily Competition Schedule & Underdog Nations</h2>\n'
        html += '<div class="day-tabs">\n'
        
        # Generate tabs for each day
        for date in sorted(self.schedule.keys()):
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            tab_label = date_obj.strftime('%b %d')
            html += f'<div class="day-tab" data-day="{date}">{tab_label}</div>\n'
        
        html += '</div>\n'
        
        # Generate content for each day
        for date in sorted(self.schedule.keys()):
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date_header = date_obj.strftime('%A, %B %d, %Y')
            
            day_data = self.schedule[date]
            underdogs = day_underdogs[date]
            
            html += f'<div class="day-content" id="day-{date}">\n'
            html += f'<h3 style="color: #00d4ff; margin-bottom: 20px;">{date_header}</h3>\n'
            
            # Group sports by type
            regular_events = []
            medal_events = []
            
            for sport_info in day_data['sports']:
                sport_name = sport_info['sport']
                sport_type = sport_info.get('type', 'regular_event')
                
                if sport_type == 'medal_event':
                    medal_events.append(sport_name)
                else:
                    regular_events.append(sport_name)
            
            # Display events
            if medal_events:
                html += '<div class="sport-section">\n'
                html += '<div class="sport-title">🥇 Medal Events</div>\n'
                html += '<div class="day-sports">\n'
                for sport in medal_events:
                    html += f'<span class="sport-tag">{sport}</span>\n'
                html += '</div>\n</div>\n'
            
            if regular_events:
                html += '<div class="sport-section">\n'
                html += '<div class="sport-title">🏂 Competition Events</div>\n'
                html += '<div class="day-sports">\n'
                for sport in regular_events:
                    html += f'<span class="sport-tag">{sport}</span>\n'
                html += '</div>\n</div>\n'
            
            # Display underdog nations
            if underdogs:
                html += '<div class="sport-section">\n'
                html += f'<div class="sport-title">⭐ Underdog Nations Competing ({len(underdogs)})</div>\n'
                html += '<div class="underdog-nations">\n'
                
                for nation_info in sorted(underdogs, key=lambda x: x['name']):
                    name = nation_info['name']
                    html += f'<div class="underdog-chip">{name}</div>\n'
                
                html += '</div>\n</div>\n'
            else:
                html += '<p style="color: #a8dadc; font-style: italic;">No underdog nations competing on this day.</p>\n'
            
            html += '</div>\n'
        
        html += '</section>\n'
        return html
    
    def save(self, filepath: str):
        """Generate and save HTML file."""
        html = self.generate_html()
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✓ HTML page generated: {filepath}")


def main():
    """Main function."""
    print("=" * 70)
    print("Generating 2026 Winter Olympics Overview HTML")
    print("=" * 70)
    print()
    
    generator = OlympicsHTMLGenerator()
    output_file = 'olympics_overview.html'
    generator.save(output_file)
    
    print()
    print("=" * 70)
    print(f"✓ Complete! Open {output_file} in your browser.")
    print("=" * 70)


if __name__ == '__main__':
    main()
