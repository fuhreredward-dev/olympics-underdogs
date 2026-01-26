"""
Daily watchlist generator for Olympic underdogs.
Uses event underdog mappings to show only events where underdogs are actually competing.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
from src.data_loader import DataLoader
from src.underdog_checker import UnderdogChecker
from src.medals_per_capita import MedalsPerCapitaCalculator
from src.utils import format_date_display, get_ioc_code_name_map

try:
    from src.event_underdog_mapper import EventUnderdogMapper
except ImportError:
    EventUnderdogMapper = None


class WatchlistGenerator:
    """Generates daily watchlists of underdog nations competing."""
    
    def __init__(self, data_loader: DataLoader, underdog_checker: UnderdogChecker,
                 medals_calculator: MedalsPerCapitaCalculator, config: Dict,
                 event_mapper: Optional['EventUnderdogMapper'] = None):
        self.data_loader = data_loader
        self.underdog_checker = underdog_checker
        self.medals_calculator = medals_calculator
        self.config = config
        self.nation_names = get_ioc_code_name_map()
        self.event_mapper = event_mapper
    
    def generate_for_date(self, date: str) -> str:
        """
        Generate watchlist for a specific date.
        
        Args:
            date: Date string in format YYYY-MM-DD
        
        Returns:
            Formatted watchlist as string
        """
        # If using event mapper, use the refined mappings
        if self.event_mapper:
            return self._generate_mapped_watchlist(date)
        
        # Otherwise use legacy method
        # Get events for this date
        events = self.data_loader.get_events_for_date(date)
        
        if not events:
            return self._format_empty_watchlist(date)
        
        # Get all competing nations
        competing_nations = self.data_loader.get_competing_nations_for_date(date)
        
        # Filter to underdogs
        underdogs = self.underdog_checker.get_underdog_nations(list(competing_nations))
        
        if not underdogs:
            return self._format_no_underdogs_watchlist(date, len(competing_nations))
        
        # Build watchlist
        return self._format_watchlist(date, events, underdogs)
    
    def _generate_mapped_watchlist(self, date: str) -> str:
        """Generate watchlist using event underdog mappings (refined version)."""
        # Get events with underdog mappings for this date
        mapped_events = self.event_mapper.get_events_for_date(date)
        
        if not mapped_events:
            return self._format_empty_watchlist(date)
        
        # Extract unique underdogs competing
        all_underdogs = set()
        for event in mapped_events:
            all_underdogs.update(event['underdog_nations'])
        
        # Get criteria for each underdog
        underdogs = {}
        for nation in all_underdogs:
            is_underdog, criteria = self.underdog_checker.is_underdog(nation)
            if is_underdog:
                underdogs[nation] = criteria
        
        # Format watchlist
        return self._format_mapped_watchlist(date, mapped_events, underdogs)
    
    def _format_empty_watchlist(self, date: str) -> str:
        """Format watchlist when no events scheduled."""
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        output = [
            f"# Olympic Underdogs Watchlist - {format_date_display(date_obj)}",
            "",
            "No events scheduled for this date.",
            ""
        ]
        return "\n".join(output)
    
    def _format_no_underdogs_watchlist(self, date: str, total_nations: int) -> str:
        """Format watchlist when no underdogs competing."""
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        output = [
            f"# Olympic Underdogs Watchlist - {format_date_display(date_obj)}",
            "",
            f"No underdog nations competing today ({total_nations} nations total).",
            ""
        ]
        
        # Still include medals per capita sidebar
        if self.config['output'].get('include_sidebar', True):
            output.append("")
            output.append(self._generate_sidebar())
        
        return "\n".join(output)
    
    def _format_mapped_watchlist(self, date: str, mapped_events: List[Dict], 
                                 underdogs: Dict[str, List[str]]) -> str:
        """Format watchlist using refined event mappings."""
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        output = [
            f"# Olympic Underdogs Watchlist - {format_date_display(date_obj)}",
            "",
            f"**{len(underdogs)} underdog nation(s) competing in {len(mapped_events)} event(s) today!**",
            ""
        ]
        
        # Group by discipline
        disciplines = {}
        for event in mapped_events:
            disc = event['discipline']
            if disc not in disciplines:
                disciplines[disc] = []
            disciplines[disc].append(event)
        
        # Format each discipline
        for discipline in sorted(disciplines.keys()):
            output.append(f"## {discipline}")
            output.append("")
            
            disc_events = disciplines[discipline]
            
            # Get all underdogs in this discipline
            disc_underdogs = set()
            for event in disc_events:
                disc_underdogs.update(event['underdog_nations'])
            
            # Show each underdog
            for nation in sorted(disc_underdogs):
                name = self.nation_names.get(nation, nation)
                output.append(f"### {name} ({nation})")
                
                # Show criteria
                if nation in underdogs:
                    for criterion in underdogs[nation]:
                        output.append(f"- _{criterion}_")
                
                # Show events for this nation
                nation_events = [e for e in disc_events if nation in e['underdog_nations']]
                
                if nation_events:
                    output.append("")
                    output.append("**Events:**")
                    for event in nation_events:
                        event_str = f"{event['event']}"
                        if event.get('stage'):
                            event_str += f" ({event['stage']})"
                        output.append(f"- {event_str}")
                
                output.append("")
        
        # Add sidebar
        if self.config['output'].get('include_sidebar', True):
            output.append("---")
            output.append("")
            output.append(self._generate_sidebar())
        
        return "\n".join(output)
    
    def _format_watchlist(self, date: str, events: List[Dict], 
                         underdogs: Dict[str, List[str]]) -> str:
        """Format full watchlist with underdogs."""
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        output = [
            f"# Olympic Underdogs Watchlist - {format_date_display(date_obj)}",
            "",
            f"**{len(underdogs)} underdog nation(s) competing today!**",
            ""
        ]
        
        # Group events by sport if configured
        if self.config['display'].get('group_by_sport', True):
            output.extend(self._format_by_sport(events, underdogs))
        else:
            output.extend(self._format_chronologically(events, underdogs))
        
        # Add medals per capita sidebar
        if self.config['output'].get('include_sidebar', True):
            output.append("")
            output.append("---")
            output.append("")
            output.append(self._generate_sidebar())
        
        return "\n".join(output)
    
    def _format_by_sport(self, events: List[Dict], underdogs: Dict[str, List[str]]) -> List[str]:
        """Format underdog entries grouped by sport."""
        output = []
        
        # Group events by sport
        sports_events = {}
        for event in events:
            sport = event.get('sport', 'Unknown')
            if sport not in sports_events:
                sports_events[sport] = []
            sports_events[sport].append(event)
        
        # Process each sport
        for sport, sport_events in sorted(sports_events.items()):
            # Find underdogs in this sport
            sport_underdogs = set()
            for event in sport_events:
                # Use underdog_nations field if available (for sports with specific competitor lists)
                # Otherwise fall back to general nations field
                competing_nations = event.get('underdog_nations', event.get('nations', []))
                for nation in competing_nations:
                    if nation in underdogs:
                        sport_underdogs.add(nation)
            
            if not sport_underdogs:
                continue
            
            output.append(f"## {sport}")
            output.append("")
            
            for nation in sorted(sport_underdogs):
                name = self.nation_names.get(nation, nation)
                output.append(f"### {name} ({nation})")
                
                # Show criteria
                for criterion in underdogs[nation]:
                    output.append(f"- _{criterion}_")
                
                # Show events for this nation in this sport
                nation_events = []
                for e in sport_events:
                    # Check if nation is in underdog_nations (preferred) or nations field
                    competing_nations = e.get('underdog_nations', e.get('nations', []))
                    if nation in competing_nations:
                        nation_events.append(e)
                
                if nation_events:
                    output.append("")
                    output.append("**Events:**")
                    for event in nation_events:
                        event_str = self._format_event_line(event)
                        output.append(f"- {event_str}")
                
                output.append("")
        
        return output
    
    def _format_chronologically(self, events: List[Dict], 
                               underdogs: Dict[str, List[str]]) -> List[str]:
        """Format underdog entries chronologically."""
        output = []
        
        for nation in sorted(underdogs.keys()):
            name = self.nation_names.get(nation, nation)
            output.append(f"## {name} ({nation})")
            
            # Show criteria
            for criterion in underdogs[nation]:
                output.append(f"- _{criterion}_")
            
            # Show events for this nation
            nation_events = []
            for e in events:
                # Check if nation is in underdog_nations (preferred) or nations field
                competing_nations = e.get('underdog_nations', e.get('nations', []))
                if nation in competing_nations:
                    nation_events.append(e)
            
            if nation_events:
                output.append("")
                output.append("**Events:**")
                for event in nation_events:
                    event_str = self._format_event_line(event)
                    output.append(f"- {event_str}")
            
            output.append("")
        
        return output
    
    def _format_event_line(self, event: Dict) -> str:
        """Format a single event line."""
        parts = []
        
        # Add discipline/event
        if event.get('event'):
            parts.append(event['event'])
        elif event.get('discipline'):
            parts.append(event['discipline'])
        
        # Add session type
        if event.get('session'):
            parts.append(f"({event['session']})")
        
        # Add time if available and configured
        if self.config['display'].get('show_session_times', True):
            if event.get('time'):
                parts.append(f"@ {event['time']}")
        
        return " ".join(parts) if parts else "Event details not available"
    
    def _generate_sidebar(self) -> str:
        """Generate medals per capita leaderboard sidebar."""
        max_nations = self.config['display'].get('max_nations_sidebar', 20)
        leaderboard = self.medals_calculator.get_leaderboard(top_n=max_nations)
        return self.medals_calculator.format_leaderboard(leaderboard, self.nation_names)
    
    def save_watchlist(self, date: str, content: str):
        """Save watchlist to file."""
        output_dir = Path(self.config['output']['directory'])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"watchlist_{date}.md"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Watchlist saved to: {filepath}")
    
    def generate_all_dates(self) -> List[str]:
        """Generate watchlists for all dates in the Olympics."""
        start_date = datetime.strptime(self.config['olympics']['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(self.config['olympics']['end_date'], "%Y-%m-%d")
        
        current_date = start_date
        generated_files = []
        
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            content = self.generate_for_date(date_str)
            self.save_watchlist(date_str, content)
            generated_files.append(date_str)
            current_date += timedelta(days=1)
        
        return generated_files
