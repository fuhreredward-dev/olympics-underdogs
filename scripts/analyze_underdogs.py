"""
Analyze 2026 Winter Olympics participating nations against underdog criteria.
"""

import json
from pathlib import Path
from typing import List, Dict, Set


class UnderdogAnalyzer:
    """Analyzes participating nations against underdog criteria."""
    
    def __init__(self):
        """Load all necessary data."""
        self.participating_nations = self._load_json('data/participating_nations_2026.json')
        self.athlete_counts = self._load_json('data/athlete_counts_2026.json')
        self.winter_medals = self._load_json('data/medals/winter_medals.json')
        self.all_time_medals = self._load_json('data/medals/all_time_medals.json')
        self.population = self._load_json('data/population/population.json')
    
    def _load_json(self, filepath: str):
        """Load JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {filepath} not found")
            return {} if 'json' in filepath else []
    
    def analyze_criteria(self):
        """Analyze all participating nations against each criterion."""
        print("=" * 70)
        print("UNDERDOG CRITERIA ANALYSIS - 2026 Winter Olympics")
        print("=" * 70)
        print(f"\nTotal participating nations: {len(self.participating_nations)}")
        print()
        
        # Track nations meeting each criterion
        criteria_nations = {
            1: set(),  # < 5 athletes
            2: set(),  # No Olympic gold
            3: set(),  # No Olympic medals
            4: set(),  # Population < 1M
            5: set(),  # No Winter gold
            6: set(),  # No Winter medals
        }
        
        # Analyze each participating nation
        for nation in self.participating_nations:
            # Criterion 1: Less than 5 athletes (but at least 1)
            athlete_count = self.athlete_counts.get(nation, 0)
            if 1 <= athlete_count < 5:
                criteria_nations[1].add(nation)
            
            # Criterion 2: No Olympic gold medals
            all_time = self.all_time_medals.get(nation, {})
            if all_time.get('gold', 0) == 0:
                criteria_nations[2].add(nation)
            
            # Criterion 3: No Olympic medals
            if all_time.get('total', 0) == 0:
                criteria_nations[3].add(nation)
            
            # Criterion 4: Population under 1M
            pop = self.population.get(nation, float('inf'))
            if pop < 1_000_000:
                criteria_nations[4].add(nation)
            
            # Criterion 5: No Winter Olympic gold medals
            winter = self.winter_medals.get(nation, {})
            if winter.get('gold', 0) == 0:
                criteria_nations[5].add(nation)
            
            # Criterion 6: No Winter Olympic medals
            if winter.get('total', 0) == 0:
                criteria_nations[6].add(nation)
        
        # Print results for each criterion
        print("CRITERION ANALYSIS:")
        print("-" * 70)
        
        print(f"\n1. Has less than 5 athletes (but at least 1): {len(criteria_nations[1])} nations")
        if criteria_nations[1]:
            nations_sorted = sorted(criteria_nations[1])
            for nation in nations_sorted:
                count = self.athlete_counts.get(nation, 0)
                print(f"   {nation}: {count} athlete{'s' if count != 1 else ''}")
        
        print(f"\n2. Has no Olympic gold medals: {len(criteria_nations[2])} nations")
        if criteria_nations[2]:
            print(f"   {', '.join(sorted(criteria_nations[2]))}")
        
        print(f"\n3. Has no Olympic medals: {len(criteria_nations[3])} nations")
        if criteria_nations[3]:
            print(f"   {', '.join(sorted(criteria_nations[3]))}")
        
        print(f"\n4. Has population under 1M people: {len(criteria_nations[4])} nations")
        if criteria_nations[4]:
            for nation in sorted(criteria_nations[4]):
                pop = self.population.get(nation, 0)
                print(f"   {nation}: {pop:,}")
        
        print(f"\n5. Has no Winter Olympic gold medals: {len(criteria_nations[5])} nations")
        if criteria_nations[5]:
            print(f"   {', '.join(sorted(criteria_nations[5]))}")
        
        print(f"\n6. Has no Winter Olympic medals: {len(criteria_nations[6])} nations")
        if criteria_nations[6]:
            print(f"   {', '.join(sorted(criteria_nations[6]))}")
        
        # Find nations meeting ALL criteria
        print("\n" + "=" * 70)
        print("BONUS: Nations meeting ALL 6 criteria")
        print("=" * 70)
        
        all_criteria = criteria_nations[1]
        for i in range(2, 7):
            all_criteria = all_criteria.intersection(criteria_nations[i])
        
        if all_criteria:
            print(f"\n✓ {len(all_criteria)} nation(s) meet ALL 6 criteria:")
            for nation in sorted(all_criteria):
                print(f"\n  {nation}:")
                print(f"    Athletes: {self.athlete_counts.get(nation, 0)}")
                print(f"    Olympic gold: {self.all_time_medals.get(nation, {}).get('gold', 0)}")
                print(f"    Olympic medals: {self.all_time_medals.get(nation, {}).get('total', 0)}")
                print(f"    Population: {self.population.get(nation, 0):,}")
                print(f"    Winter gold: {self.winter_medals.get(nation, {}).get('gold', 0)}")
                print(f"    Winter medals: {self.winter_medals.get(nation, {}).get('total', 0)}")
        else:
            print("\n✗ No nations meet all 6 criteria")
            
            # Find closest matches
            print("\nClosest matches (nations meeting 5 out of 6 criteria):")
            for nation in self.participating_nations:
                criteria_met = 0
                criteria_list = []
                
                athlete_count = self.athlete_counts.get(nation, 0)
                if 1 <= athlete_count < 5:
                    criteria_met += 1
                    criteria_list.append(f"<5 athletes ({athlete_count})")
                
                all_time = self.all_time_medals.get(nation, {})
                if all_time.get('gold', 0) == 0:
                    criteria_met += 1
                    criteria_list.append("No Olympic gold")
                
                if all_time.get('total', 0) == 0:
                    criteria_met += 1
                    criteria_list.append("No Olympic medals")
                
                pop = self.population.get(nation, float('inf'))
                if pop < 1_000_000:
                    criteria_met += 1
                    criteria_list.append(f"Pop <1M ({pop:,})")
                
                winter = self.winter_medals.get(nation, {})
                if winter.get('gold', 0) == 0:
                    criteria_met += 1
                    criteria_list.append("No Winter gold")
                
                if winter.get('total', 0) == 0:
                    criteria_met += 1
                    criteria_list.append("No Winter medals")
                
                if criteria_met >= 5:
                    print(f"\n  {nation} ({criteria_met}/6):")
                    for c in criteria_list:
                        print(f"    ✓ {c}")
        
        print("\n" + "=" * 70)


def main():
    """Main function."""
    analyzer = UnderdogAnalyzer()
    analyzer.analyze_criteria()


if __name__ == '__main__':
    main()
