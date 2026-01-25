"""
Medals per capita calculator and leaderboard generator.
"""

from typing import Dict, List, Tuple
from src.data_loader import DataLoader
from src.utils import calculate_per_capita, format_population


class MedalsPerCapitaCalculator:
    """Calculate and rank nations by medals per capita."""
    
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
    
    def calculate_for_nation(self, ioc_code: str) -> Dict:
        """
        Calculate medals per capita for a single nation.
        
        Returns dict with total and gold medals per capita.
        """
        medals = self.data_loader.get_nation_medals(ioc_code)
        population = self.data_loader.get_nation_population(ioc_code)
        
        if population == 0:
            return {
                'total_per_capita': 0.0,
                'gold_per_capita': 0.0,
                'medals': medals,
                'population': population
            }
        
        return {
            'total_per_capita': calculate_per_capita(medals['total'], population),
            'gold_per_capita': calculate_per_capita(medals['gold'], population),
            'medals': medals,
            'population': population
        }
    
    def calculate_all(self, nations: List[str]) -> Dict[str, Dict]:
        """Calculate medals per capita for all nations."""
        results = {}
        
        for nation in nations:
            results[nation] = self.calculate_for_nation(nation)
        
        return results
    
    def get_leaderboard(self, 
                        nations: List[str] = None, 
                        top_n: int = 20,
                        sort_by: str = 'total') -> List[Tuple[str, Dict]]:
        """
        Generate leaderboard of nations by medals per capita.
        
        Args:
            nations: List of nations to include. If None, uses all nations with data.
            top_n: Number of top nations to return
            sort_by: 'total' or 'gold' - which medals per capita to sort by
        
        Returns:
            List of tuples (ioc_code, stats_dict) sorted by per capita rate
        """
        # If no nations specified, get all from medals data
        if nations is None:
            if self.data_loader.medals_data is None:
                self.data_loader.load_medals()
            nations = list(self.data_loader.medals_data.keys())
        
        # Calculate for all nations
        results = self.calculate_all(nations)
        
        # Sort by specified metric
        sort_key = 'total_per_capita' if sort_by == 'total' else 'gold_per_capita'
        
        leaderboard = sorted(
            results.items(),
            key=lambda x: x[1][sort_key],
            reverse=True
        )
        
        # Filter out nations with 0 population or 0 medals
        leaderboard = [
            (nation, stats) for nation, stats in leaderboard
            if stats['population'] > 0 and stats['medals']['total'] > 0
        ]
        
        return leaderboard[:top_n]
    
    def format_leaderboard(self, leaderboard: List[Tuple[str, Dict]], 
                          nation_names: Dict[str, str]) -> str:
        """
        Format leaderboard as markdown string.
        
        Args:
            leaderboard: List from get_leaderboard()
            nation_names: Dict mapping IOC codes to full names
        """
        if not leaderboard:
            return "No data available for medals per capita leaderboard."
        
        output = ["## 🏅 Medals Per Capita Leaderboard", ""]
        output.append("| Rank | Nation | Total Medals | Population | Medals/1M |")
        output.append("|------|--------|--------------|------------|-----------|")
        
        for rank, (ioc_code, stats) in enumerate(leaderboard, 1):
            name = nation_names.get(ioc_code, ioc_code)
            total_medals = stats['medals']['total']
            population_str = format_population(stats['population'])
            per_capita = stats['total_per_capita']
            
            output.append(
                f"| {rank} | {name} ({ioc_code}) | {total_medals} | "
                f"{population_str} | {per_capita:.2f} |"
            )
        
        return "\n".join(output)
