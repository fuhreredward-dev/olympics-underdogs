"""
Data loader for Olympic schedule, medals, and population data.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class DataLoader:
    """Handles loading and parsing of all data sources."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.schedule_data = None
        self.medals_data = None
        self.population_data = None
    
    def load_schedule(self, schedule_path: Optional[str] = None) -> Dict:
        """
        Load Olympic schedule data.
        
        Expected format:
        {
            "2026-02-06": [
                {
                    "sport": "Curling",
                    "discipline": "Curling",
                    "event": "Mixed Doubles",
                    "session": "Training",
                    "time": "09:00",
                    "nations": ["CAN", "USA", "SWE", "NOR"]
                },
                ...
            ],
            ...
        }
        """
        path = schedule_path or self.config['data_paths']['schedule']
        
        if not Path(path).exists():
            print(f"Warning: Schedule file not found at {path}. Using empty schedule.")
            return {}
        
        with open(path, 'r') as f:
            self.schedule_data = json.load(f)
        
        return self.schedule_data
    
    def load_medals(self, medals_path: Optional[str] = None) -> Dict:
        """
        Load historical Olympic medal data.
        
        Expected format:
        {
            "USA": {"gold": 105, "silver": 112, "bronze": 88, "total": 305},
            "NOR": {"gold": 148, "silver": 133, "bronze": 122, "total": 403},
            "LIE": {"gold": 0, "silver": 2, "bronze": 2, "total": 4},
            "MON": {"gold": 0, "silver": 0, "bronze": 0, "total": 0},
            ...
        }
        """
        path = medals_path or self.config['data_paths']['medals']
        
        if not Path(path).exists():
            print(f"Warning: Medals file not found at {path}. Using empty medals data.")
            return {}
        
        with open(path, 'r') as f:
            self.medals_data = json.load(f)
        
        return self.medals_data
    
    def load_population(self, population_path: Optional[str] = None) -> Dict:
        """
        Load population data by nation.
        
        Expected format:
        {
            "USA": 331900000,
            "NOR": 5425000,
            "LIE": 39000,
            "AND": 77000,
            ...
        }
        """
        path = population_path or self.config['data_paths']['population']
        
        if not Path(path).exists():
            print(f"Warning: Population file not found at {path}. Using empty population data.")
            return {}
        
        with open(path, 'r') as f:
            self.population_data = json.load(f)
        
        return self.population_data
    
    def load_all(self):
        """Load all data sources."""
        self.load_schedule()
        self.load_medals()
        self.load_population()
    
    def get_events_for_date(self, date: str) -> List[Dict]:
        """Get all events for a specific date."""
        if self.schedule_data is None:
            self.load_schedule()
        
        return self.schedule_data.get(date, [])
    
    def get_competing_nations_for_date(self, date: str) -> set:
        """Get all nations competing on a specific date."""
        events = self.get_events_for_date(date)
        nations = set()
        
        for event in events:
            if 'nations' in event:
                nations.update(event['nations'])
        
        return nations
    
    def get_nation_medals(self, ioc_code: str) -> Dict:
        """Get medal count for a nation."""
        if self.medals_data is None:
            self.load_medals()
        
        return self.medals_data.get(ioc_code, {
            "gold": 0,
            "silver": 0,
            "bronze": 0,
            "total": 0
        })
    
    def get_nation_population(self, ioc_code: str) -> int:
        """Get population for a nation."""
        if self.population_data is None:
            self.load_population()
        
        return self.population_data.get(ioc_code, 0)
