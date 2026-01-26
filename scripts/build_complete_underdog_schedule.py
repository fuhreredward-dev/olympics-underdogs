#!/usr/bin/env python3
"""
Build complete underdog schedule for all 16 sports using criteria-based classification.
"""

import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

# All 92 participating nations and their sports
NATIONS_SPORTS = {
    "Albania": ["Alpine skiing"],
    "Andorra": ["Alpine skiing", "Cross-country skiing"],
    "Argentina": ["Alpine skiing", "Cross-country skiing", "Snowboarding"],
    "Armenia": ["Alpine skiing", "Biathlon", "Cross-country skiing"],
    "Australia": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Figure skating", "Freestyle skiing", "Luge", "Short-track speed skating", "Skeleton", "Ski jumping", "Snowboarding", "Speed skating", "Ski mountaineering"],
    "Austria": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Curling", "Figure skating", "Freestyle skiing", "Ice hockey", "Luge", "Nordic combined", "Short-track speed skating", "Skeleton", "Ski jumping", "Snowboarding", "Speed skating"],
    "Azerbaijan": ["Alpine skiing", "Cross-country skiing"],
    "Belgium": ["Alpine skiing", "Biathlon", "Bobsleigh", "Figure skating", "Freestyle skiing", "Short-track speed skating", "Speed skating", "Luge", "Nordic combined"],
    "Benin": ["Alpine skiing"],
    "Bolivia": ["Alpine skiing"],
    "Bosnia and Herzegovina": ["Alpine skiing", "Cross-country skiing"],
    "Brazil": ["Alpine skiing", "Bobsleigh", "Cross-country skiing", "Freestyle skiing", "Snowboarding"],
    "Bulgaria": ["Alpine skiing", "Biathlon", "Cross-country skiing", "Figure skating", "Freestyle skiing", "Short-track speed skating", "Ski jumping", "Speed skating"],
    "Canada": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Curling", "Figure skating", "Freestyle skiing", "Ice hockey", "Luge", "Nordic combined", "Short-track speed skating", "Skeleton", "Ski jumping", "Snowboarding"],
    "Chile": ["Alpine skiing", "Cross-country skiing", "Freestyle skiing"],
    "China": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Curling", "Figure skating", "Freestyle skiing", "Ice hockey", "Luge", "Nordic combined", "Short-track speed skating", "Skeleton", "Ski jumping", "Snowboarding"],
    "Colombia": ["Alpine skiing", "Cross-country skiing"],
    "Croatia": ["Alpine skiing", "Biathlon", "Figure skating", "Freestyle skiing", "Ski jumping"],
    "Cyprus": ["Alpine skiing"],
    "Czech Republic": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Figure skating", "Freestyle skiing", "Luge", "Short-track speed skating", "Skeleton", "Ski jumping", "Snowboarding", "Speed skating", "Nordic combined"],
    "Denmark": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Figure skating", "Freestyle skiing", "Short-track speed skating", "Skeleton", "Speed skating"],
    "Ecuador": ["Alpine skiing"],
    "Eritrea": ["Alpine skiing"],
    "Estonia": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Figure skating", "Luge", "Short-track speed skating", "Skeleton", "Ski jumping", "Speed skating"],
    "Finland": ["Alpine skiing", "Biathlon", "Cross-country skiing", "Figure skating", "Freestyle skiing", "Luge", "Nordic combined", "Short-track speed skating", "Ski jumping"],
    "France": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Curling", "Figure skating", "Freestyle skiing", "Ice hockey", "Luge", "Nordic combined", "Short-track speed skating", "Skeleton", "Ski jumping", "Snowboarding"],
    "Germany": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Curling", "Figure skating", "Freestyle skiing", "Ice hockey", "Luge", "Nordic combined", "Short-track speed skating", "Skeleton", "Ski jumping", "Snowboarding", "Speed skating"],
    "Greece": ["Alpine skiing", "Cross-country skiing"],
    "Great Britain": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Curling", "Figure skating", "Freestyle skiing", "Short-track speed skating", "Skeleton", "Snowboarding", "Speed skating"],
    "Guinea-Bissau": ["Alpine skiing"],
    "Haiti": ["Alpine skiing", "Cross-country skiing"],
    "Hong Kong": ["Alpine skiing", "Short-track speed skating"],
    "Hungary": ["Alpine skiing", "Cross-country skiing", "Figure skating", "Short-track speed skating", "Speed skating"],
    "Iceland": ["Alpine skiing", "Cross-country skiing"],
    "India": ["Alpine skiing", "Cross-country skiing"],
    "Ireland": ["Alpine skiing", "Cross-country skiing", "Freestyle skiing"],
    "Israel": ["Alpine skiing", "Bobsleigh", "Cross-country skiing", "Figure skating", "Skeleton"],
    "Italy": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Curling", "Figure skating", "Freestyle skiing", "Ice hockey", "Luge", "Nordic combined", "Short-track speed skating", "Skeleton", "Ski jumping", "Ski mountaineering", "Snowboarding", "Speed skating"],
    "Jamaica": ["Alpine skiing", "Bobsleigh"],
    "Japan": ["Alpine skiing", "Cross-country skiing", "Curling", "Figure skating", "Freestyle skiing", "Ice hockey", "Luge", "Nordic combined", "Short-track speed skating", "Skeleton", "Ski jumping", "Snowboarding", "Speed skating"],
    "Kazakhstan": ["Alpine skiing", "Biathlon", "Cross-country skiing", "Figure skating", "Freestyle skiing", "Nordic combined", "Short-track speed skating", "Ski jumping", "Speed skating"],
    "Kenya": ["Alpine skiing"],
    "Kosovo": ["Alpine skiing"],
    "Kyrgyzstan": ["Alpine skiing", "Cross-country skiing"],
    "Latvia": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Figure skating", "Ice hockey", "Luge", "Short-track speed skating", "Skeleton"],
    "Lebanon": ["Alpine skiing", "Cross-country skiing"],
    "Liechtenstein": ["Alpine skiing", "Bobsleigh", "Cross-country skiing"],
    "Lithuania": ["Alpine skiing", "Biathlon", "Cross-country skiing", "Figure skating"],
    "Luxembourg": ["Alpine skiing"],
    "Madagascar": ["Alpine skiing"],
    "Malaysia": ["Alpine skiing"],
    "Malta": ["Cross-country skiing"],
    "Mexico": ["Alpine skiing", "Cross-country skiing", "Figure skating"],
    "Moldova": ["Biathlon", "Cross-country skiing"],
    "Monaco": ["Alpine skiing"],
    "Mongolia": ["Alpine skiing", "Cross-country skiing"],
    "Montenegro": ["Alpine skiing", "Cross-country skiing"],
    "Morocco": ["Alpine skiing", "Cross-country skiing"],
    "Netherlands": ["Bobsleigh", "Figure skating", "Short-track speed skating", "Skeleton", "Snowboarding", "Speed skating"],
    "New Zealand": ["Alpine skiing", "Freestyle skiing", "Snowboarding"],
    "Nigeria": ["Cross-country skiing"],
    "North Macedonia": ["Alpine skiing", "Cross-country skiing"],
    "Norway": ["Alpine skiing", "Biathlon", "Cross-country skiing", "Curling", "Freestyle skiing", "Nordic combined", "Ski jumping", "Ski mountaineering", "Snowboarding", "Speed skating"],
    "Pakistan": ["Alpine skiing"],
    "Philippines": ["Alpine skiing"],
    "Poland": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Figure skating", "Luge", "Nordic combined", "Short-track speed skating", "Ski jumping", "Ski mountaineering", "Snowboarding", "Speed skating"],
    "Portugal": ["Alpine skiing", "Cross-country skiing"],
    "Puerto Rico": ["Alpine skiing"],
    "Romania": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Figure skating", "Freestyle skiing", "Luge", "Short-track speed skating"],
    "San Marino": ["Alpine skiing"],
    "Saudi Arabia": ["Alpine skiing"],
    "Serbia": ["Alpine skiing", "Figure skating"],
    "Singapore": ["Figure skating"],
    "Slovakia": ["Alpine skiing", "Biathlon", "Cross-country skiing", "Figure skating", "Freestyle skiing", "Luge", "Nordic combined", "Skeleton", "Ski jumping"],
    "Slovenia": ["Alpine skiing", "Biathlon", "Cross-country skiing", "Freestyle skiing", "Luge", "Nordic combined", "Ski jumping", "Speed skating"],
    "South Africa": ["Alpine skiing", "Cross-country skiing", "Freestyle skiing"],
    "South Korea": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Curling", "Figure skating", "Freestyle skiing", "Ice hockey", "Luge", "Short-track speed skating", "Skeleton", "Ski jumping", "Snowboarding", "Speed skating"],
    "Spain": ["Alpine skiing", "Biathlon", "Cross-country skiing", "Figure skating", "Freestyle skiing", "Luge"],
    "Sweden": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Curling", "Figure skating", "Freestyle skiing", "Ice hockey", "Luge", "Nordic combined", "Short-track speed skating", "Skeleton", "Ski jump", "Snowboarding", "Speed skating"],
    "Switzerland": ["Alpine skiing", "Biathlon", "Bobsleigh", "Cross-country skiing", "Curling", "Figure skating", "Freestyle skiing", "Ice hockey", "Luge", "Nordic combined", "Short-track speed skating", "Skeleton", "Ski jumping", "Ski mountaineering", "Snowboarding", "Speed skating"],
    "Thailand": ["Alpine skiing", "Cross-country skiing"],
    "Trinidad and Tobago": ["Alpine skiing", "Bobsleigh"],
    "Turkey": ["Alpine skiing", "Cross-country skiing", "Freestyle skiing", "Ski jumping"],
    "Ukraine": ["Alpine skiing", "Biathlon", "Cross-country skiing", "Figure skating", "Freestyle skiing", "Luge", "Short-track speed skating"],
    "United Arab Emirates": ["Alpine skiing"],
    "Uruguay": ["Alpine skiing", "Cross-country skiing"],
    "Uzbekistan": ["Alpine skiing", "Biathlon", "Cross-country skiing", "Figure skating", "Freestyle skiing"],
    "Venezuela": ["Alpine skiing"],
}

# Load existing data files to get medal/population criteria
def load_json(filepath: str) -> Dict:
    """Load JSON file safely."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def check_underdog_criteria(nation: str, athlete_count: int, all_medals: Dict, winter_medals: Dict, population: int) -> Tuple[bool, List[str]]:
    """Check how many underdog criteria a nation meets."""
    criteria_met = []
    
    # Criterion 1: < 5 athletes (but at least 1)
    if 1 <= athlete_count < 5:
        criteria_met.append("< 5 Athletes")
    
    # Criterion 2: No Olympic gold medals
    if all_medals.get('gold', 0) == 0:
        criteria_met.append("No Olympic Gold")
    
    # Criterion 3: No Olympic medals
    if all_medals.get('total', 0) == 0:
        criteria_met.append("No Olympic Medals")
    
    # Criterion 4: Population under 1M
    if 0 < population < 1_000_000:
        criteria_met.append("Population < 1M")
    
    # Criterion 5: No Winter Olympic gold
    if winter_medals.get('gold', 0) == 0:
        criteria_met.append("No Winter Gold")
    
    # Criterion 6: No Winter Olympic medals
    if winter_medals.get('total', 0) == 0:
        criteria_met.append("No Winter Medals")
    
    # Criterion 7: Southern Hemisphere
    southern_hemisphere = {
        "Argentina", "Australia", "Bolivia", "Brazil", "Chile", 
        "New Zealand", "Paraguay", "South Africa", "Uruguay"
    }
    if nation in southern_hemisphere:
        criteria_met.append("Southern Hemisphere")
    
    is_underdog = len(criteria_met) > 0
    return is_underdog, criteria_met

def main():
    """Build complete underdog schedule."""
    data_dir = Path("data")
    
    # Load supporting data
    athlete_counts = load_json(data_dir / "athlete_counts_2026.json")
    all_time_medals = load_json(data_dir / "medals" / "all_time_medals.json")
    winter_medals = load_json(data_dir / "medals" / "winter_medals.json")
    population = load_json(data_dir / "population" / "population.json")
    
    # Map nation names to IOC codes
    name_to_ioc = {
        "Albania": "ALB", "Andorra": "AND", "Argentina": "ARG", "Armenia": "ARM",
        "Australia": "AUS", "Austria": "AUT", "Azerbaijan": "AZE", "Belgium": "BEL",
        "Benin": "BEN", "Bolivia": "BOL", "Bosnia and Herzegovina": "BIH", "Brazil": "BRA",
        "Bulgaria": "BUL", "Canada": "CAN", "Chile": "CHI", "China": "CHN",
        "Colombia": "COL", "Croatia": "CRO", "Cyprus": "CYP",
        "Czech Republic": "CZE", "Denmark": "DEN", "Ecuador": "ECU", "Eritrea": "ERI", "Estonia": "EST",
        "Finland": "FIN", "France": "FRA", "Germany": "GER", "Greece": "GRE",
        "Great Britain": "GBR", "Guinea-Bissau": "GBS", "Haiti": "HAI", "Hong Kong": "HKG", "Hungary": "HUN",
        "Iceland": "ISL", "India": "IND", "Ireland": "IRL", "Israel": "ISR",
        "Italy": "ITA", "Jamaica": "JAM", "Japan": "JPN", "Kazakhstan": "KAZ",
        "Kenya": "KEN", "Kosovo": "KOS", "Kyrgyzstan": "KGZ", "Latvia": "LAT",
        "Lebanon": "LBN", "Liechtenstein": "LIE", "Lithuania": "LTU", "Luxembourg": "LUX",
        "Madagascar": "MAD", "Malaysia": "MAS", "Malta": "MLT", "Mexico": "MEX", "Moldova": "MDA",
        "Monaco": "MON", "Mongolia": "MGL", "Montenegro": "MNE", "Morocco": "MAR",
        "Netherlands": "NED", "New Zealand": "NZL", "Nigeria": "NGR", "North Macedonia": "MKD",
        "Norway": "NOR", "Pakistan": "PAK", "Philippines": "PHI", "Poland": "POL",
        "Portugal": "POR", "Puerto Rico": "PUR", "Romania": "ROU", "San Marino": "SMR",
        "Saudi Arabia": "KSA", "Serbia": "SRB", "Singapore": "SGP", "Slovakia": "SVK",
        "Slovenia": "SLO", "South Africa": "RSA", "South Korea": "KOR", "Spain": "ESP",
        "Sweden": "SWE", "Switzerland": "SUI", "Thailand": "THA",
        "Trinidad and Tobago": "TTO", "Turkey": "TUR", "Ukraine": "UKR",
        "United Arab Emirates": "UAE", "Uruguay": "URU", "Uzbekistan": "UZB", "Venezuela": "VEN"
    }
    
    underdog_by_sport = {}
    nation_underdog_status = {}
    
    # Analyze each nation
    print("=" * 80)
    print("ANALYZING ALL 92 NATIONS FOR UNDERDOG STATUS")
    print("=" * 80)
    
    for nation in sorted(NATIONS_SPORTS.keys()):
        if not NATIONS_SPORTS[nation]:  # Skip nations with no data
            continue
        
        ioc_code = name_to_ioc.get(nation, nation[:3].upper())
        athlete_count = athlete_counts.get(ioc_code, 0)
        all_med = all_time_medals.get(ioc_code, {})
        winter_med = winter_medals.get(ioc_code, {})
        pop = population.get(ioc_code, 0)
        
        is_underdog, criteria = check_underdog_criteria(nation, athlete_count, all_med, winter_med, pop)
        nation_underdog_status[nation] = {
            "is_underdog": is_underdog,
            "criteria_met": criteria,
            "criteria_count": len(criteria),
            "sports": NATIONS_SPORTS[nation]
        }
        
        if is_underdog:
            print(f"\n✓ {nation}")
            print(f"  Criteria ({len(criteria)}):", ", ".join(criteria))
            print(f"  Sports ({len(NATIONS_SPORTS[nation])}):", ", ".join(NATIONS_SPORTS[nation]))
    
    # Build underdog list by sport
    print("\n" + "=" * 80)
    print("UNDERDOGS BY SPORT")
    print("=" * 80)
    
    all_sports = set()
    for sports in NATIONS_SPORTS.values():
        all_sports.update(sports)
    
    for sport in sorted(all_sports):
        underdogs = []
        for nation in sorted(NATIONS_SPORTS.keys()):
            if sport in NATIONS_SPORTS[nation]:
                if nation in nation_underdog_status and nation_underdog_status[nation]["is_underdog"]:
                    underdogs.append(nation)
        
        underdog_by_sport[sport] = underdogs
        print(f"\n{sport}: {len(underdogs)} underdog nations")
        if underdogs:
            print(f"  {', '.join(underdogs)}")
    
    # Save results
    output = {
        "underdog_by_sport": underdog_by_sport,
        "nation_underdog_status": nation_underdog_status,
        "total_nations": len(NATIONS_SPORTS),
        "total_underdogs": sum(1 for s in nation_underdog_status.values() if s["is_underdog"]),
        "total_sports": len(all_sports)
    }
    
    output_path = data_dir / "underdog_schedule_2026.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n" + "=" * 80)
    print(f"✓ Saved to: {output_path}")
    print(f"  Total Nations: {output['total_nations']}")
    print(f"  Total Underdogs: {output['total_underdogs']}")
    print(f"  Total Sports: {output['total_sports']}")
    print("=" * 80)

if __name__ == "__main__":
    main()
