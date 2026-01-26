"""
Event Underdog Mapper - Maps specific underdog nations to specific events and dates.

This module creates clean mappings: Event → Date → Underdog Nations Actually Competing
Used by watchlist generator to show only events where underdogs are present.
"""

import json
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime


class EventUnderdogMapper:
    """Maps underdog nations to specific events and competition dates."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.schedule_data = {}
        self.underdog_nations = set()
        self.event_mappings = {}
        
    def load_schedule(self, schedule_file: str = "schedules/ioc_schedule_authoritative.json"):
        """Load the authoritative IOC schedule."""
        schedule_path = self.data_dir / schedule_file
        with open(schedule_path, 'r', encoding='utf-8') as f:
            self.schedule_data = json.load(f)
        print(f"✓ Loaded schedule from {schedule_file}")
        
    def load_underdog_nations(self):
        """Load the list of underdog nations from participating nations."""
        # Load participating nations
        nations_path = self.data_dir / "participating_nations_2026.json"
        with open(nations_path, 'r', encoding='utf-8') as f:
            nations = json.load(f)
        
        # Load medal and population data
        medals_path = self.data_dir / "medals" / "all_time_medals.json"
        with open(medals_path, 'r', encoding='utf-8') as f:
            all_time_medals = json.load(f)
            
        winter_medals_path = self.data_dir / "medals" / "winter_medals.json"
        with open(winter_medals_path, 'r', encoding='utf-8') as f:
            winter_medals = json.load(f)
            
        population_path = self.data_dir / "population" / "population.json"
        with open(population_path, 'r', encoding='utf-8') as f:
            population = json.load(f)
        
        # Identify underdogs based on criteria
        southern_hemisphere = {"AUS", "ARG", "BRA", "CHI", "NZL", "RSA", "URU", "ECU"}
        
        for nation in nations:
            criteria_met = []
            
            # Check criteria
            if nation not in all_time_medals or all_time_medals[nation].get('gold', 0) == 0:
                criteria_met.append("no_olympic_gold")
            
            if nation not in all_time_medals or all_time_medals[nation].get('total', 0) == 0:
                criteria_met.append("no_olympic_medals")
            
            pop = population.get(nation, float('inf'))
            if 0 < pop < 1_000_000:
                criteria_met.append("population_under_1m")
            
            if nation not in winter_medals or winter_medals[nation].get('gold', 0) == 0:
                criteria_met.append("no_winter_gold")
            
            if nation not in winter_medals or winter_medals[nation].get('total', 0) == 0:
                criteria_met.append("no_winter_medals")
            
            if nation in southern_hemisphere:
                criteria_met.append("southern_hemisphere")
            
            if len(criteria_met) > 0:
                self.underdog_nations.add(nation)
        
        print(f"✓ Loaded {len(self.underdog_nations)} underdog nations")
        
    def add_event_mapping(self, discipline: str, event: str, date: str, 
                         underdog_nations: List[str], stage: str = None):
        """
        Add a mapping of underdog nations to a specific event instance.
        
        Args:
            discipline: e.g., "Skeleton"
            event: e.g., "Men's Skeleton"
            date: ISO format date "2026-02-12"
            underdog_nations: List of IOC codes for underdogs competing
            stage: Optional stage identifier (e.g., "prelim", "final", "Heat 1")
        """
        # Create event key
        event_key = f"{discipline}|{event}|{date}"
        if stage:
            event_key += f"|{stage}"
        
        # Filter to only include nations that are actually underdogs
        valid_underdogs = [n for n in underdog_nations if n in self.underdog_nations]
        
        if valid_underdogs:
            self.event_mappings[event_key] = {
                "discipline": discipline,
                "event": event,
                "date": date,
                "stage": stage,
                "underdog_nations": sorted(valid_underdogs),
                "underdog_count": len(valid_underdogs)
            }
            
    def get_events_for_date(self, date: str) -> List[Dict]:
        """Get all events with underdogs on a specific date."""
        events = []
        for key, mapping in self.event_mappings.items():
            if mapping["date"] == date:
                events.append(mapping)
        return sorted(events, key=lambda x: x["discipline"])
    
    def get_events_for_nation(self, ioc_code: str) -> List[Dict]:
        """Get all events where a specific nation is competing."""
        events = []
        for key, mapping in self.event_mappings.items():
            if ioc_code in mapping["underdog_nations"]:
                events.append(mapping)
        return sorted(events, key=lambda x: x["date"])
    
    def get_discipline_summary(self) -> Dict[str, Dict]:
        """Get summary of underdog participation by discipline."""
        summary = {}
        for key, mapping in self.event_mappings.items():
            discipline = mapping["discipline"]
            if discipline not in summary:
                summary[discipline] = {
                    "events": [],
                    "dates": set(),
                    "underdogs": set(),
                    "event_count": 0
                }
            
            summary[discipline]["events"].append(mapping["event"])
            summary[discipline]["dates"].add(mapping["date"])
            summary[discipline]["underdogs"].update(mapping["underdog_nations"])
            summary[discipline]["event_count"] += 1
        
        # Convert sets to sorted lists for JSON serialization
        for discipline in summary:
            summary[discipline]["dates"] = sorted(list(summary[discipline]["dates"]))
            summary[discipline]["underdogs"] = sorted(list(summary[discipline]["underdogs"]))
        
        return summary
    
    def save_mappings(self, output_file: str = "event_underdog_mappings.json"):
        """Save all mappings to a JSON file."""
        output_path = self.data_dir / output_file
        
        output = {
            "metadata": {
                "total_events_with_underdogs": len(self.event_mappings),
                "total_underdog_nations": len(self.underdog_nations),
                "underdog_nations": sorted(list(self.underdog_nations)),
                "generated": datetime.now().isoformat()
            },
            "event_mappings": self.event_mappings,
            "discipline_summary": self.get_discipline_summary()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved mappings to {output_path}")
        return output_path
    
    def load_mappings(self, input_file: str = "event_underdog_mappings.json"):
        """Load previously saved mappings."""
        input_path = self.data_dir / input_file
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.event_mappings = data["event_mappings"]
        self.underdog_nations = set(data["metadata"]["underdog_nations"])
        
        print(f"✓ Loaded {len(self.event_mappings)} event mappings")
        return data


def main():
    """Example usage."""
    mapper = EventUndergMapper()
    mapper.load_underdog_nations()
    mapper.load_schedule()
    
    # Example: Add Skeleton events with underdogs
    # (You would manually populate these based on qualification data)
    mapper.add_event_mapping(
        discipline="Skeleton",
        event="Men's Skeleton",
        date="2026-02-12",
        underdog_nations=["DEN", "ISR"],
        stage="Heat 1"
    )
    
    mapper.add_event_mapping(
        discipline="Skeleton",
        event="Women's Skeleton",
        date="2026-02-13",
        underdog_nations=["BRA", "DEN", "RSA"],
        stage="Heat 1"
    )
    
    # Save mappings
    mapper.save_mappings()
    
    # Get summary
    summary = mapper.get_discipline_summary()
    print("\nDiscipline Summary:")
    for discipline, info in summary.items():
        print(f"\n{discipline}:")
        print(f"  Events: {info['event_count']}")
        print(f"  Dates: {', '.join(info['dates'])}")
        print(f"  Underdogs ({len(info['underdogs'])}): {', '.join(info['underdogs'])}")


if __name__ == "__main__":
    main()
