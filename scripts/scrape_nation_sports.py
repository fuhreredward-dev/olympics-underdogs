"""
Scrape competitor data by sport for each nation from their 2026 Winter Olympics Wikipedia pages.
"""

import json
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from typing import Dict, List


class NationCompetitorsScraper:
    """Scrapes competitor data by sport for each participating nation."""
    
    # IOC code to country name mapping for Wikipedia URLs
    IOC_TO_COUNTRY = {
        'USA': 'United_States', 'CAN': 'Canada', 'ITA': 'Italy', 'GER': 'Germany',
        'SUI': 'Switzerland', 'FRA': 'France', 'AUT': 'Austria', 'CZE': 'Czech_Republic',
        'SWE': 'Sweden', 'FIN': 'Finland', 'JPN': 'Japan', 'CHN': 'China',
        'LAT': 'Latvia', 'NOR': 'Norway', 'POL': 'Poland', 'GBR': 'Great_Britain',
        'SVK': 'Slovakia', 'KOR': 'South_Korea', 'DEN': 'Denmark', 'NED': 'Netherlands',
        'SLO': 'Slovenia', 'BEL': 'Belgium', 'KAZ': 'Kazakhstan', 'ROM': 'Romania',
        'EST': 'Estonia', 'AUS': 'Australia', 'BUL': 'Bulgaria', 'UKR': 'Ukraine',
        'LTU': 'Lithuania', 'HUN': 'Hungary', 'ESP': 'Spain', 'BRA': 'Brazil',
        'GEO': 'Georgia', 'CRO': 'Croatia', 'TPE': 'Chinese_Taipei', 'AND': 'Andorra',
        'ARG': 'Argentina', 'ARM': 'Armenia', 'TUR': 'Turkey', 'GRE': 'Greece',
        'ISR': 'Israel', 'MEX': 'Mexico', 'BIH': 'Bosnia_and_Herzegovina', 'ISL': 'Iceland',
        'IRI': 'Iran', 'IRL': 'Ireland', 'LIE': 'Liechtenstein', 'MKD': 'North_Macedonia',
        'POR': 'Portugal', 'SRB': 'Serbia', 'UZB': 'Uzbekistan', 'CHI': 'Chile',
        'HKG': 'Hong_Kong', 'LIB': 'Lebanon', 'MGL': 'Mongolia', 'RSA': 'South_Africa',
        'THA': 'Thailand', 'ALB': 'Albania', 'AZE': 'Azerbaijan', 'CYP': 'Cyprus',
        'IND': 'India', 'KOS': 'Kosovo', 'KGZ': 'Kyrgyzstan', 'LUX': 'Luxembourg',
        'MDA': 'Moldova', 'MNE': 'Montenegro', 'MAR': 'Morocco', 'NZL': 'New_Zealand',
        'PHI': 'Philippines', 'KSA': 'Saudi_Arabia', 'TTO': 'Trinidad_and_Tobago',
        'UAE': 'United_Arab_Emirates', 'COL': 'Colombia', 'ECU': 'Ecuador',
        'JAM': 'Jamaica', 'KEN': 'Kenya', 'MAS': 'Malaysia', 'MLT': 'Malta',
        'MON': 'Monaco', 'NGR': 'Nigeria', 'PAK': 'Pakistan', 'SMR': 'San_Marino',
        'SGP': 'Singapore', 'URU': 'Uruguay', 'VEN': 'Venezuela'
    }
    
    # Sport name normalization
    SPORT_ALIASES = {
        'alpine skiing': 'Alpine Skiing',
        'biathlon': 'Biathlon',
        'bobsleigh': 'Bobsleigh',
        'bobsled': 'Bobsleigh',
        'cross-country skiing': 'Cross-Country Skiing',
        'curling': 'Curling',
        'figure skating': 'Figure Skating',
        'freestyle skiing': 'Freestyle Skiing',
        'ice hockey': 'Ice Hockey',
        'luge': 'Luge',
        'nordic combined': 'Nordic Combined',
        'short track speed skating': 'Short Track Speed Skating',
        'short track': 'Short Track Speed Skating',
        'skeleton': 'Skeleton',
        'ski jumping': 'Ski Jumping',
        'ski mountaineering': 'Ski Mountaineering',
        'snowboard': 'Snowboard',
        'snowboarding': 'Snowboard',
        'speed skating': 'Speed Skating',
    }
    
    def __init__(self):
        """Initialize scraper."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_all_nations(self, nation_codes: List[str]) -> Dict[str, Dict]:
        """
        Scrape competitor data for all nations.
        
        Args:
            nation_codes: List of IOC codes to scrape
            
        Returns:
            Dict mapping IOC code to their sport participation data
        """
        results = {}
        total = len(nation_codes)
        
        print(f"Scraping competitor data for {total} nations...")
        print("=" * 70)
        
        for i, ioc_code in enumerate(nation_codes, 1):
            print(f"\n[{i}/{total}] {ioc_code}...", end=" ")
            
            try:
                sports_data = self.scrape_nation(ioc_code, debug=False)
                if sports_data:
                    results[ioc_code] = sports_data
                    print(f"✓ {len(sports_data)} sports")
                else:
                    print("✗ No data found")
                    
                # Be polite to Wikipedia
                time.sleep(0.5)
                
            except Exception as e:
                print(f"✗ Error: {e}")
                continue
        
        print("\n" + "=" * 70)
        print(f"✓ Successfully scraped {len(results)}/{total} nations")
        
        return results
    
    def scrape_nation(self, ioc_code: str, debug: bool = False) -> Dict[str, Dict]:
        """
        Scrape competitor data for a single nation.
        
        Args:
            ioc_code: IOC code (e.g., 'USA', 'CAN')
            debug: If True, print debugging information
            
        Returns:
            Dict mapping sport name to competitor counts
        """
        # Get country name for URL
        country_name = self.IOC_TO_COUNTRY.get(ioc_code)
        if not country_name:
            if debug:
                print(f"\n  ✗ No country name mapping for {ioc_code}")
            return {}
        
        # Build Wikipedia URL
        url = f"https://en.wikipedia.org/wiki/{country_name}_at_the_2026_Winter_Olympics"
        
        try:
            # Fetch and clean the HTML with BeautifulSoup first
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Parse with BeautifulSoup and extract just the tables
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all tables
            html_tables = soup.find_all('table', class_='wikitable')
            
            if debug:
                print(f"\n  Found {len(html_tables)} wikitables")
            
            # Try each table
            for i, html_table in enumerate(html_tables):
                try:
                    # Convert to pandas DataFrame
                    df = pd.read_html(str(html_table))[0]
                    
                    cols_str = str(df.columns).lower()
                    
                    if debug:
                        print(f"  Table {i}: {df.columns.tolist()}")
                    
                    # Look for table with sport and men/women columns
                    if ('sport' in cols_str or 'discipline' in cols_str) and ('men' in cols_str or 'women' in cols_str):
                        if debug:
                            print(f"  → Attempting to parse table {i}")
                        result = self._parse_competitors_table(df)
                        if result:
                            return result
                except Exception as e:
                    if debug:
                        print(f"  ✗ Error parsing table {i}: {e}")
                    continue
            
            if debug:
                print(f"  ✗ No matching competitor table found")
            return {}
            
        except Exception as e:
            if debug:
                print(f"\n  ✗ Exception: {e}")
            return {}
    
    def _parse_competitors_table(self, df: pd.DataFrame) -> Dict[str, Dict]:
        """
        Parse the competitors table.
        
        Returns:
            Dict mapping sport name to {men: int, women: int, total: int}
        """
        sports_data = {}
        
        try:
            # Find sport, men, women columns
            sport_col = None
            men_col = None
            women_col = None
            
            for col in df.columns:
                col_str = str(col).lower()
                if 'sport' in col_str or 'discipline' in col_str:
                    if sport_col is None:
                        sport_col = col
                if 'men' in col_str and 'women' not in col_str:
                    men_col = col
                if 'women' in col_str:
                    women_col = col
            
            if sport_col is None:
                return {}
            
            # Process each row
            for idx, row in df.iterrows():
                try:
                    sport = str(row[sport_col]).strip()
                    
                    # Skip invalid rows
                    if not sport or sport.lower() in ['sport', 'discipline', 'total', 'nan']:
                        continue
                    
                    # Normalize sport name
                    sport_normalized = self._normalize_sport_name(sport)
                    if not sport_normalized:
                        continue
                    
                    # Get counts
                    men = 0
                    women = 0
                    
                    if men_col is not None:
                        men = self._safe_int(row[men_col])
                    
                    if women_col is not None:
                        women = self._safe_int(row[women_col])
                    
                    total = men + women
                    
                    if total > 0:
                        sports_data[sport_normalized] = {
                            'men': men,
                            'women': women,
                            'total': total
                        }
                        
                except Exception as e:
                    # Skip rows that cause errors
                    continue
                    
        except Exception as e:
            return {}
        
        return sports_data
    
    def _normalize_sport_name(self, sport: str) -> str:
        """Normalize sport name to match our standard naming."""
        sport_lower = sport.lower().strip()
        
        # Remove any bracketed text
        if '[' in sport_lower:
            sport_lower = sport_lower.split('[')[0].strip()
        
        # Check aliases
        for alias, normalized in self.SPORT_ALIASES.items():
            if alias in sport_lower:
                return normalized
        
        return None
    
    def _safe_int(self, value) -> int:
        """Safely convert value to int."""
        try:
            if pd.notna(value):
                s = str(value).strip()
                
                # Handle malformed data like '4data-sort-value=""'
                # Extract just the leading digits
                import re
                match = re.match(r'^(\d+)', s)
                if match:
                    return int(match.group(1))
                
                # Try normal conversion
                s = s.replace(',', '')
                if s and s not in ['—', '-', '']:
                    return int(float(s))
        except:
            pass
        return 0
    
    def save_to_json(self, data: Dict, filepath: str):
        """Save data to JSON file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved to {filepath}")


def main():
    """Main function."""
    print("=" * 70)
    print("Nation Competitors by Sport Scraper")
    print("=" * 70)
    print()
    
    # Load participating nations
    with open('data/participating_nations_2026.json', 'r') as f:
        nations = json.load(f)
    
    print(f"Loaded {len(nations)} participating nations")
    
    scraper = NationCompetitorsScraper()
    
    # Scrape all nations
    results = scraper.scrape_all_nations(nations)
    
    if results:
        print("\n" + "=" * 70)
        print("SAMPLE DATA")
        print("=" * 70)
        
        # Show sample for first few nations
        for i, (ioc, sports) in enumerate(list(results.items())[:3]):
            print(f"\n{ioc}:")
            for sport, counts in sports.items():
                print(f"  {sport}: {counts['men']}M + {counts['women']}W = {counts['total']}")
        
        # Save results
        print("\n" + "=" * 70)
        print("SAVING DATA")
        print("=" * 70)
        
        output_file = 'data/nation_sports_participation_2026.json'
        scraper.save_to_json(results, output_file)
        
        # Statistics
        total_sports = sum(len(sports) for sports in results.values())
        avg_sports = total_sports / len(results) if results else 0
        print(f"\nTotal sport participations: {total_sports}")
        print(f"Average sports per nation: {avg_sports:.1f}")
        
    else:
        print("\n✗ No data scraped")


if __name__ == '__main__':
    main()
