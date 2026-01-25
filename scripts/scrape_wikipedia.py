"""
Data scraper for Olympic medals and population from Wikipedia.
"""

import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
from typing import Dict, Optional


class WikipediaOlympicScraper:
    """Scrapes Olympic medal data from Wikipedia."""
    
    # Wikipedia URLs
    ALL_TIME_MEDALS_URL = "https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table"
    WINTER_MEDALS_URL = "https://en.wikipedia.org/wiki/All-time_Winter_Olympic_Games_medal_table"
    POPULATION_URL = "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_all_time_medals(self) -> Dict[str, Dict]:
        """
        Scrape all-time Olympic medal counts (Summer + Winter combined).
        
        Returns:
            Dict mapping IOC codes to medal counts
        """
        print("Scraping all-time Olympic medals from Wikipedia...")
        
        try:
            response = self.session.get(self.ALL_TIME_MEDALS_URL)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the medal table (usually the first wikitable)
            table = soup.find('table', {'class': 'wikitable'})
            if not table:
                print("Could not find medal table on page")
                return {}
            
            medals_data = {}
            
            # Parse table rows
            rows = table.find_all('tr')[1:]  # Skip header row
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 5:
                    continue
                
                # Extract data
                try:
                    # Nation name and IOC code
                    nation_cell = cells[0]
                    nation_link = nation_cell.find('a')
                    if not nation_link:
                        continue
                    
                    nation_name = nation_link.get_text(strip=True)
                    
                    # Try to get IOC code from the second cell or extract from name
                    ioc_code = None
                    if len(cells) > 1:
                        code_cell = cells[1]
                        code_text = code_cell.get_text(strip=True)
                        if len(code_text) == 3 and code_text.isupper():
                            ioc_code = code_text
                    
                    # If IOC code not found, try to extract from common patterns
                    if not ioc_code:
                        # Some tables have IOC code in parentheses
                        if '(' in nation_name and ')' in nation_name:
                            ioc_code = nation_name.split('(')[1].split(')')[0].strip()
                        else:
                            # Skip this row if we can't determine IOC code
                            continue
                    
                    # Medal counts - try different column positions
                    # Usually: Nation, IOC, Gold, Silver, Bronze, Total
                    try:
                        gold = int(cells[2].get_text(strip=True).replace(',', ''))
                        silver = int(cells[3].get_text(strip=True).replace(',', ''))
                        bronze = int(cells[4].get_text(strip=True).replace(',', ''))
                        total = gold + silver + bronze
                        
                        medals_data[ioc_code] = {
                            'gold': gold,
                            'silver': silver,
                            'bronze': bronze,
                            'total': total
                        }
                        
                        print(f"  ✓ {ioc_code}: {total} medals")
                    
                    except (ValueError, IndexError) as e:
                        print(f"  ✗ Could not parse medals for {nation_name}: {e}")
                        continue
                
                except Exception as e:
                    print(f"  ✗ Error parsing row: {e}")
                    continue
            
            print(f"\n✓ Scraped {len(medals_data)} nations")
            return medals_data
        
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return {}
    
    def scrape_winter_medals(self) -> Dict[str, Dict]:
        """
        Scrape Winter Olympics medal counts specifically.
        
        Returns:
            Dict mapping IOC codes to medal counts
        """
        print("Scraping Winter Olympic medals from Wikipedia...")
        
        try:
            response = self.session.get(self.WINTER_MEDALS_URL)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the medal table
            table = soup.find('table', {'class': 'wikitable'})
            if not table:
                print("Could not find medal table on page")
                return {}
            
            medals_data = {}
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 5:
                    continue
                
                try:
                    # Similar parsing logic as all-time
                    nation_cell = cells[0]
                    nation_link = nation_cell.find('a')
                    if not nation_link:
                        continue
                    
                    nation_name = nation_link.get_text(strip=True)
                    
                    # Get IOC code
                    ioc_code = None
                    if len(cells) > 1:
                        code_text = cells[1].get_text(strip=True)
                        if len(code_text) == 3 and code_text.isupper():
                            ioc_code = code_text
                    
                    if not ioc_code:
                        if '(' in nation_name and ')' in nation_name:
                            ioc_code = nation_name.split('(')[1].split(')')[0].strip()
                        else:
                            continue
                    
                    gold = int(cells[2].get_text(strip=True).replace(',', ''))
                    silver = int(cells[3].get_text(strip=True).replace(',', ''))
                    bronze = int(cells[4].get_text(strip=True).replace(',', ''))
                    total = gold + silver + bronze
                    
                    medals_data[ioc_code] = {
                        'gold': gold,
                        'silver': silver,
                        'bronze': bronze,
                        'total': total
                    }
                    
                    print(f"  ✓ {ioc_code}: {total} medals")
                
                except Exception as e:
                    continue
            
            print(f"\n✓ Scraped {len(medals_data)} nations")
            return medals_data
        
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return {}
    
    def scrape_population(self) -> Dict[str, int]:
        """
        Scrape population data from Wikipedia.
        
        Returns:
            Dict mapping IOC codes to population
        """
        print("Scraping population data from Wikipedia...")
        
        try:
            response = self.session.get(self.POPULATION_URL)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the population table
            table = soup.find('table', {'class': 'wikitable'})
            if not table:
                print("Could not find population table")
                return {}
            
            population_data = {}
            
            # This is a simplified version - you'll need to map country names to IOC codes
            # Wikipedia doesn't always use IOC codes in population tables
            
            print("Note: Population scraping requires manual IOC code mapping")
            print("Consider using a dedicated population API or dataset instead")
            
            return population_data
        
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return {}
    
    def save_to_json(self, data: Dict, filepath: str):
        """Save data to JSON file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved data to {filepath}")


def main():
    """Main scraper function."""
    print("=" * 60)
    print("Olympic Data Scraper - Wikipedia")
    print("=" * 60)
    print()
    
    scraper = WikipediaOlympicScraper()
    
    # Menu
    print("What would you like to scrape?")
    print("1. All-time Olympic medals (Summer + Winter)")
    print("2. Winter Olympics medals only")
    print("3. Both")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice in ['1', '3']:
        print("\n" + "=" * 60)
        medals = scraper.scrape_all_time_medals()
        if medals:
            scraper.save_to_json(
                medals, 
                'data/medals/historical_medals.json'
            )
    
    if choice in ['2', '3']:
        print("\n" + "=" * 60)
        winter_medals = scraper.scrape_winter_medals()
        if winter_medals:
            scraper.save_to_json(
                winter_medals,
                'data/medals/winter_medals.json'
            )
    
    print("\n" + "=" * 60)
    print("✓ Scraping complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
