"""
Underdog checker - determines if a nation meets underdog criteria.
"""

from typing import Dict, List, Tuple
from src.data_loader import DataLoader


class UnderdogChecker:
    """Checks if nations meet underdog criteria."""
    
    def __init__(self, data_loader: DataLoader, config: Dict):
        self.data_loader = data_loader
        self.config = config
        self.criteria_config = config['criteria']
    
    def check_never_medaled(self, ioc_code: str) -> bool:
        """Check if nation has never won any Olympic medal."""
        medals = self.data_loader.get_nation_medals(ioc_code)
        return medals['total'] == 0
    
    def check_never_won_gold(self, ioc_code: str) -> bool:
        """Check if nation has never won Olympic gold medal."""
        medals = self.data_loader.get_nation_medals(ioc_code)
        return medals['gold'] == 0
    
    def check_small_population(self, ioc_code: str) -> bool:
        """Check if nation has population under threshold."""
        population = self.data_loader.get_nation_population(ioc_code)
        threshold = self.criteria_config['population_threshold']
        return 0 < population < threshold
    
    def is_underdog(self, ioc_code: str) -> Tuple[bool, List[str]]:
        """
        Check if nation meets any underdog criteria.
        
        Returns:
            Tuple of (is_underdog: bool, criteria_met: List[str])
        """
        criteria_met = []
        
        # Check each enabled criterion
        if self.criteria_config.get('never_medaled', False):
            if self.check_never_medaled(ioc_code):
                criteria_met.append("Never won any Olympic medal")
        
        if self.criteria_config.get('never_won_gold', False):
            if self.check_never_won_gold(ioc_code):
                # Only add if not already flagged for never medaling
                if "Never won any Olympic medal" not in criteria_met:
                    criteria_met.append("Never won Olympic gold")
        
        if self.criteria_config.get('population_threshold'):
            if self.check_small_population(ioc_code):
                criteria_met.append(f"Population < {self.criteria_config['population_threshold'] / 1_000_000}M")
        
        return (len(criteria_met) > 0, criteria_met)
    
    def get_underdog_nations(self, nations: List[str]) -> Dict[str, List[str]]:
        """
        Filter nations to only underdogs with their criteria.
        
        Returns:
            Dict mapping IOC code to list of criteria met
        """
        underdogs = {}
        
        for nation in nations:
            is_underdog, criteria = self.is_underdog(nation)
            if is_underdog:
                underdogs[nation] = criteria
        
        return underdogs
    
    def get_nation_details(self, ioc_code: str) -> Dict:
        """Get detailed information about a nation."""
        medals = self.data_loader.get_nation_medals(ioc_code)
        population = self.data_loader.get_nation_population(ioc_code)
        is_underdog, criteria = self.is_underdog(ioc_code)
        
        return {
            'ioc_code': ioc_code,
            'medals': medals,
            'population': population,
            'is_underdog': is_underdog,
            'criteria_met': criteria
        }
