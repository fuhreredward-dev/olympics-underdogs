import json
import os

# Define underdog criteria
UNDERDOG_CRITERIA = {
    "minimal_team": {"label": "< 5 Athletes", "key": "minimal_team"},
    "no_olympic_gold": {"label": "No Olympic Gold Medals", "key": "no_olympic_gold"},
    "no_olympic_medals": {"label": "No Olympic Medals", "key": "no_olympic_medals"},
    "small_population": {"label": "Population Under 1M", "key": "small_population"},
    "no_winter_gold": {"label": "No Winter Olympic Gold", "key": "no_winter_gold"},
    "no_winter_medals": {"label": "No Winter Olympic Medals", "key": "no_winter_medals"},
    "southern_hemisphere": {"label": "Southern Hemisphere", "key": "southern_hemisphere"},
}

# Southern Hemisphere nations
SOUTHERN_HEMISPHERE = {
    "AUS", "ARG", "BRA", "CHI", "NZL", "RSA", "URU", "ECU",  # main ones
    "FIJ", "MAS", "SIN", "THA", "PNG", "VUT"  # others
}

# Load data files
base_path = r"c:\Users\emf48\OneDrive\Documents\Olympic Underdogs and GOATs\data"

with open(os.path.join(base_path, "nation_sports_participation_2026_complete.json")) as f:
    sports_data = json.load(f)

with open(os.path.join(base_path, "population", "population.json")) as f:
    population_data = json.load(f)

with open(os.path.join(base_path, "medals", "all_time_medals.json")) as f:
    all_time_medals = json.load(f)

with open(os.path.join(base_path, "medals", "winter_medals.json")) as f:
    winter_medals = json.load(f)


def get_total_athletes(nation_data):
    """Calculate total athletes for a nation"""
    total = 0
    for sport, athletes in nation_data.get("sports", {}).items():
        total += athletes.get("total", 0)
    return total


def is_underdog(nation_code, nation_data):
    """Check if a nation meets any underdog criteria"""
    criteria_met = []

    # 1. Minimal team (< 5 athletes)
    total_athletes = get_total_athletes(nation_data)
    if total_athletes < 5:
        criteria_met.append("minimal_team")

    # 2. No Olympic Gold Medals
    if nation_code not in all_time_medals or all_time_medals[nation_code].get("gold", 0) == 0:
        criteria_met.append("no_olympic_gold")

    # 3. No Olympic Medals
    if nation_code not in all_time_medals or all_time_medals[nation_code].get("total", 0) == 0:
        criteria_met.append("no_olympic_medals")

    # 4. Population Under 1M
    population = population_data.get(nation_code, float('inf'))
    if population < 1_000_000:
        criteria_met.append("small_population")

    # 5. No Winter Olympic Gold
    if nation_code not in winter_medals or winter_medals[nation_code].get("gold", 0) == 0:
        criteria_met.append("no_winter_gold")

    # 6. No Winter Olympic Medals
    if nation_code not in winter_medals or winter_medals[nation_code].get("total", 0) == 0:
        criteria_met.append("no_winter_medals")

    # 7. Southern Hemisphere
    if nation_code in SOUTHERN_HEMISPHERE:
        criteria_met.append("southern_hemisphere")

    return criteria_met


# Identify all underdogs
underdog_nations = {}
for nation_code, nation_data in sports_data["nations"].items():
    criteria = is_underdog(nation_code, nation_data)
    if criteria:
        underdog_nations[nation_code] = {
            "name": nation_data.get("name", nation_code),
            "total_athletes": get_total_athletes(nation_data),
            "criteria_met": criteria,
            "population": population_data.get(nation_code, "N/A"),
        }

print(f"Total Underdog Nations: {len(underdog_nations)}")
print("\nUnderdog Nations Found:")
for code, info in sorted(underdog_nations.items()):
    print(f"  {code}: {info['name']} ({info['total_athletes']} athletes, meets {len(info['criteria_met'])} criteria)")

# Build sport-specific underdog lists
sports_list = [
    "Alpine Skiing",
    "Biathlon",
    "Bobsleigh",
    "Cross-Country Skiing",
    "Curling",
    "Figure Skating",
    "Freestyle Skiing",
    "Ice Hockey",
    "Luge",
    "Nordic Combined",
    "Short-Track Speed Skating",
    "Skeleton",
    "Ski Jumping",
    "Ski Mountaineering",
    "Snowboarding",
    "Speed Skating",
]

sport_underdog_data = {}

for sport in sports_list:
    underdog_competitors = []
    all_competitors = []
    
    for nation_code, nation_data in sports_data["nations"].items():
        sports_dict = nation_data.get("sports", {})
        
        # Handle both "Snowboard" and "Snowboarding" naming
        sport_key = sport
        if sport == "Snowboarding" and "Snowboard" in sports_dict:
            sport_key = "Snowboard"
        
        if sport_key in sports_dict:
            all_competitors.append(nation_data.get("name", nation_code))
            
            # Check if this nation is an underdog
            if nation_code in underdog_nations:
                underdog_competitors.append(nation_data.get("name", nation_code))
    
    sport_underdog_data[sport] = {
        "underdog_nations": sorted(underdog_competitors),
        "count": len(underdog_competitors),
        "all_competing_nations": sorted(all_competitors),
        "total_competitors": len(all_competitors),
    }

# Output results
output = {
    "metadata": {
        "total_nations": 92,
        "total_underdog_nations": len(underdog_nations),
        "competition": "2026 Winter Olympics",
        "date_generated": "January 25, 2026",
    },
    "underdog_nations": underdog_nations,
    "sport_underdog_analysis": sport_underdog_data,
}

# Save to file
output_path = os.path.join(base_path, "..", "sport_underdogs_2026.json")
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"\n✓ Results saved to: {output_path}")

# Print sport summary
print("\n" + "="*80)
print("SPORT UNDERDOG SUMMARY")
print("="*80)
for sport, data in sport_underdog_data.items():
    print(f"\n{sport}:")
    print(f"  Total Competitors: {data['total_competitors']}")
    print(f"  Underdog Competitors: {data['count']}")
    if data["underdog_nations"]:
        print(f"  Underdogs: {', '.join(data['underdog_nations'])}")
    else:
        print(f"  Underdogs: None")
