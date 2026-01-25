"""
Scrape the list of participating NOCs for 2026 Winter Olympics.
"""

import json
import pandas as pd
from pathlib import Path
from typing import List, Dict


class ParticipatingNationsScraper:
    """Scrapes list of participating nations from 2026 Winter Olympics Wikipedia page."""
    
    # IOC code mapping for nations where code isn't in parentheses
    NATION_TO_IOC = {
        'United States': 'USA', 'Russia': 'RUS', 'Germany': 'GER', 'China': 'CHN',
        'Great Britain': 'GBR', 'France': 'FRA', 'Italy': 'ITA', 'Sweden': 'SWE',
        'Norway': 'NOR', 'Canada': 'CAN', 'Australia': 'AUS', 'Netherlands': 'NED',
        'Japan': 'JPN', 'South Korea': 'KOR', 'Hungary': 'HUN', 'Finland': 'FIN',
        'Spain': 'ESP', 'Poland': 'POL', 'Romania': 'ROM', 'Switzerland': 'SUI',
        'Austria': 'AUT', 'Belgium': 'BEL', 'Denmark': 'DEN', 'Turkey': 'TUR',
        'Greece': 'GRE', 'Czech Republic': 'CZE', 'Bulgaria': 'BUL', 'Cuba': 'CUB',
        'New Zealand': 'NZL', 'Brazil': 'BRA', 'Kenya': 'KEN', 'Jamaica': 'JAM',
        'Croatia': 'CRO', 'Ukraine': 'UKR', 'Argentina': 'ARG', 'South Africa': 'RSA',
        'Iran': 'IRI', 'Belarus': 'BLR', 'Serbia': 'SRB', 'Estonia': 'EST',
        'Slovenia': 'SLO', 'Georgia': 'GEO', 'Slovakia': 'SVK', 'Latvia': 'LAT',
        'Lithuania': 'LTU', 'Liechtenstein': 'LIE', 'Mexico': 'MEX', 'India': 'IND',
        'Kazakhstan': 'KAZ', 'Azerbaijan': 'AZE', 'Uzbekistan': 'UZB', 'Algeria': 'ALG',
        'Ethiopia': 'ETH', 'Egypt': 'EGY', 'Mongolia': 'MGL', 'Thailand': 'THA',
        'Morocco': 'MAR', 'Tunisia': 'TUN', 'Nigeria': 'NGR', 'Trinidad and Tobago': 'TTO',
        'Venezuela': 'VEN', 'Zimbabwe': 'ZIM', 'Portugal': 'POR', 'Ireland': 'IRL',
        'Israel': 'ISR', 'Chile': 'CHI', 'Indonesia': 'INA', 'Colombia': 'COL',
        'Pakistan': 'PAK', 'Dominican Republic': 'DOM', 'North Korea': 'PRK',
        'Bahamas': 'BAH', 'Cameroon': 'CMR', 'Iceland': 'ISL', 'Luxembourg': 'LUX',
        'Uruguay': 'URU', 'Peru': 'PER', 'Armenia': 'ARM', 'Philippines': 'PHI',
        'Malaysia': 'MAS', 'Kyrgyzstan': 'KGZ', 'Chinese Taipei': 'TPE',
        'Ecuador': 'ECU', 'Puerto Rico': 'PUR', 'Costa Rica': 'CRC',
        'Mozambique': 'MOZ', 'Singapore': 'SGP', 'Tajikistan': 'TJK',
        'Afghanistan': 'AFG', 'Hong Kong': 'HKG', 'Bahrain': 'BRN',
        'Burundi': 'BDI', 'Cyprus': 'CYP', 'Fiji': 'FIJ', 'Grenada': 'GRN',
        'Guatemala': 'GUA', 'Jordan': 'JOR', 'Kosovo': 'KOS', 'Kuwait': 'KUW',
        'Lebanon': 'LIB', 'Moldova': 'MDA', 'Montenegro': 'MNE', 'Nicaragua': 'NCA',
        'Niger': 'NIG', 'Panama': 'PAN', 'Paraguay': 'PAR', 'Qatar': 'QAT',
        'San Marino': 'SMR', 'Saudi Arabia': 'KSA', 'Sri Lanka': 'SRI',
        'Sudan': 'SUD', 'Suriname': 'SUR', 'Syria': 'SYR', 'Togo': 'TOG',
        'Tonga': 'TGA', 'United Arab Emirates': 'UAE', 'Uganda': 'UGA',
        'Vietnam': 'VIE', 'Virgin Islands': 'ISV', 'Zambia': 'ZAM',
        'Albania': 'ALB', 'Andorra': 'AND', 'Malta': 'MLT', 'Monaco': 'MON',
        'North Macedonia': 'MKD', 'Bosnia and Herzegovina': 'BIH', 'Ghana': 'GHA',
    }
    
    def scrape_participating_nations(self) -> tuple[List[str], Dict[str, int]]:
        """
        Scrape list of participating NOCs for 2026 Winter Olympics.
        
        Returns:
            Tuple of (list of IOC codes, dict mapping IOC code to athlete count)
        """
        print("Scraping participating nations from 2026 Winter Olympics Wikipedia page...")
        print("Target: Participating National Olympic Committees")
        
        url = "https://en.wikipedia.org/wiki/2026_Winter_Olympics"
        
        try:
            # Read all tables from the page with headers to avoid 403
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            tables = pd.read_html(url, storage_options=headers)
            
            print(f"\nFound {len(tables)} tables on page")
            
            # Look for the participating NOCs table
            for i, table in enumerate(tables):
                cols_str = str(table.columns).lower()
                
                # Look for table with NOC/Team/Nation columns
                if 'noc' in cols_str or ('team' in cols_str and 'athletes' in cols_str):
                    print(f"\nChecking Table {i}:")
                    print(f"  Columns: {list(table.columns)}")
                    print(f"  Shape: {table.shape}")
                    
                    # Try to parse this table
                    nations, athlete_counts = self._parse_noc_table(table)
                    if nations and len(nations) > 20:  # Reasonable check - should be 80+ nations
                        print(f"\n✓ Found participating nations table (Table {i})")
                        return nations, athlete_counts
            
            print("\nCould not find participating nations table")
            return [], {}
        
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _parse_noc_table(self, df: pd.DataFrame) -> tuple[List[str], Dict[str, int]]:
        """
        Parse table to extract IOC codes and athlete counts.
        
        Returns:
            Tuple of (list of IOC codes, dict mapping IOC code to athlete count)
        """
        nations = []
        athlete_counts = {}
        
        # Find the nation/NOC/team column
        nation_col = None
        for col in df.columns:
            col_str = str(col).lower()
            if any(keyword in col_str for keyword in ['noc', 'team', 'nation', 'country']):
                nation_col = col
                break
        
        if nation_col is None:
            nation_col = df.columns[0]
        
        # Find athlete count column
        athlete_col = None
        for col in df.columns:
            col_str = str(col).lower()
            if 'athlete' in col_str or 'competitor' in col_str:
                athlete_col = col
                break
        
        print(f"  Using nation column: {nation_col}")
        if athlete_col:
            print(f"  Using athlete column: {athlete_col}")
        
        # Process each row
        for idx, row in df.iterrows():
            try:
                # Get nation name
                nation = str(row[nation_col])
                
                # Skip header rows and empty rows
                if pd.isna(nation) or nation.strip() == '' or 'noc' in nation.lower() or 'team' in nation.lower():
                    continue
                
                # Extract IOC code
                ioc_code = self._extract_ioc_code(nation)
                if ioc_code and ioc_code not in nations:
                    nations.append(ioc_code)
                    
                    # Get athlete count if available
                    if athlete_col is not None:
                        try:
                            athlete_count = int(row[athlete_col])
                            athlete_counts[ioc_code] = athlete_count
                        except:
                            pass
                    
            except Exception as e:
                continue
        
        return nations, athlete_counts
    
    def _extract_ioc_code(self, nation: str) -> str:
        """Extract IOC code from nation string."""
        # Clean nation name
        nation_clean = nation.split('[')[0].strip()
        
        # Method 1: From parentheses like "United States (USA)"
        if '(' in nation and ')' in nation:
            code = nation.split('(')[1].split(')')[0].strip()
            if len(code) == 3 and code.isupper():
                return code
        
        # Method 2: If it's already just a 3-letter code
        if len(nation_clean) == 3 and nation_clean.isupper():
            return nation_clean
        
        # Method 3: From manual mapping
        return self.NATION_TO_IOC.get(nation_clean)
    
    def save_to_json(self, nations: List[str], filepath: str):
        """Save participating nations list to JSON file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(nations, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved to {filepath}")


def main():
    """Main function."""
    print("=" * 70)
    print("2026 Winter Olympics - Participating Nations Scraper")
    print("=" * 70)
    print()
    
    scraper = ParticipatingNationsScraper()
    
    # Scrape participating nations
    nations, athlete_counts = scraper.scrape_participating_nations()
    
    if nations:
        print("\n" + "=" * 70)
        print("RESULTS")
        print("=" * 70)
        print(f"\n✓ Found {len(nations)} participating nations:")
        
        # Print in columns
        for i in range(0, len(nations), 10):
            print("  " + ", ".join(nations[i:i+10]))
        
        # Save to files
        print("\n" + "=" * 70)
        print("SAVING DATA")
        print("=" * 70)
        
        nations_file = 'data/participating_nations_2026.json'
        scraper.save_to_json(nations, nations_file)
        
        if athlete_counts:
            print(f"\n✓ Found athlete counts for {len(athlete_counts)} nations")
            athletes_file = 'data/athlete_counts_2026.json'
            scraper.save_to_json(athlete_counts, athletes_file)
        
    else:
        print("\n✗ No participating nations found")


if __name__ == '__main__':
    main()
