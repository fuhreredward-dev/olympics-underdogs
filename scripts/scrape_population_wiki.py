"""
Scrape population data for countries from Wikipedia.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict


class PopulationScraper:
    """Scrapes population data from Wikipedia."""
    
    # IOC code mapping
    NATION_TO_IOC = {
        'United States': 'USA', 'Russia': 'RUS', 'Germany': 'GER', 'China': 'CHN',
        'Great Britain': 'GBR', 'United Kingdom': 'GBR', 'France': 'FRA', 'Italy': 'ITA', 
        'Sweden': 'SWE', 'Norway': 'NOR', 'Canada': 'CAN', 'Australia': 'AUS', 
        'Netherlands': 'NED', 'Japan': 'JPN', 'South Korea': 'KOR', 'Hungary': 'HUN', 
        'Finland': 'FIN', 'Spain': 'ESP', 'Poland': 'POL', 'Romania': 'ROM', 
        'Switzerland': 'SUI', 'Austria': 'AUT', 'Belgium': 'BEL', 'Denmark': 'DEN', 
        'Turkey': 'TUR', 'Greece': 'GRE', 'Czech Republic': 'CZE', 'Czechia': 'CZE',
        'Bulgaria': 'BUL', 'Cuba': 'CUB', 'New Zealand': 'NZL', 'Brazil': 'BRA', 
        'Kenya': 'KEN', 'Jamaica': 'JAM', 'Croatia': 'CRO', 'Ukraine': 'UKR', 
        'Argentina': 'ARG', 'South Africa': 'RSA', 'Iran': 'IRI', 'Belarus': 'BLR', 
        'Serbia': 'SRB', 'Estonia': 'EST', 'Slovenia': 'SLO', 'Georgia': 'GEO', 
        'Slovakia': 'SVK', 'Latvia': 'LAT', 'Lithuania': 'LTU', 'Liechtenstein': 'LIE', 
        'Mexico': 'MEX', 'India': 'IND', 'Kazakhstan': 'KAZ', 'Azerbaijan': 'AZE', 
        'Uzbekistan': 'UZB', 'Algeria': 'ALG', 'Ethiopia': 'ETH', 'Egypt': 'EGY', 
        'Mongolia': 'MGL', 'Thailand': 'THA', 'Morocco': 'MAR', 'Tunisia': 'TUN', 
        'Nigeria': 'NGR', 'Trinidad and Tobago': 'TTO', 'Venezuela': 'VEN', 
        'Zimbabwe': 'ZIM', 'Portugal': 'POR', 'Ireland': 'IRL', 'Israel': 'ISR', 
        'Chile': 'CHI', 'Indonesia': 'INA', 'Colombia': 'COL', 'Pakistan': 'PAK', 
        'Dominican Republic': 'DOM', 'North Korea': 'PRK', 'Bahamas': 'BAH', 
        'Cameroon': 'CMR', 'Iceland': 'ISL', 'Luxembourg': 'LUX', 'Uruguay': 'URU', 
        'Peru': 'PER', 'Armenia': 'ARM', 'Philippines': 'PHI', 'Malaysia': 'MAS', 
        'Kyrgyzstan': 'KGZ', 'Taiwan': 'TPE', 'Chinese Taipei': 'TPE', 
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
    
    def scrape_population(self) -> Dict[str, int]:
        """
        Scrape population data from Wikipedia.
        
        Returns:
            Dict mapping IOC codes to population
        """
        print("Scraping population data from Wikipedia...")
        print("Target: Sovereign states and dependencies by population")
        
        url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
        
        try:
            # Read all tables from the page with headers to avoid 403
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            tables = pd.read_html(url, storage_options=headers)
            
            print(f"\nFound {len(tables)} tables on page")
            
            # Look for the main population table
            for i, table in enumerate(tables):
                cols_str = str(table.columns).lower()
                
                # Look for table with country/location and population columns
                if ('country' in cols_str or 'location' in cols_str) and 'population' in cols_str:
                    print(f"\nChecking Table {i}:")
                    print(f"  Columns: {list(table.columns)}")
                    print(f"  Shape: {table.shape}")
                    
                    # Try to parse this table
                    populations = self._parse_population_table(table)
                    if populations and len(populations) > 50:
                        print(f"\n✓ Found population table (Table {i})")
                        return populations
            
            print("\nCould not find population table")
            return {}
        
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def _parse_population_table(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        Parse population table.
        
        Returns:
            Dict mapping IOC codes to population
        """
        populations = {}
        
        # Find the country and population columns
        country_col = None
        pop_col = None
        
        for col in df.columns:
            col_str = str(col).lower()
            if 'country' in col_str or 'location' in col_str or 'state' in col_str:
                if country_col is None:
                    country_col = col
            if 'population' in col_str and pop_col is None:
                pop_col = col
        
        if country_col is None:
            country_col = df.columns[0]
        if pop_col is None:
            pop_col = df.columns[1]
        
        print(f"  Using country column: {country_col}")
        print(f"  Using population column: {pop_col}")
        
        # Process each row
        for idx, row in df.iterrows():
            try:
                # Get country name
                country = str(row[country_col])
                
                # Skip header rows and empty rows
                if pd.isna(country) or country.strip() == '':
                    continue
                
                # Get population
                pop_value = row[pop_col]
                if pd.isna(pop_value):
                    continue
                
                # Parse population (remove commas, convert to int)
                pop_str = str(pop_value).replace(',', '').replace(' ', '')
                try:
                    population = int(float(pop_str))
                except:
                    continue
                
                # Extract IOC code
                ioc_code = self._extract_ioc_code(country)
                if ioc_code:
                    populations[ioc_code] = population
                    
            except Exception as e:
                continue
        
        return populations
    
    def _extract_ioc_code(self, country: str) -> str:
        """Extract IOC code from country string."""
        # Clean country name
        country_clean = country.split('[')[0].strip()
        
        # Remove any leading numbers or symbols
        import re
        country_clean = re.sub(r'^[\d\s\-–—]+', '', country_clean).strip()
        
        # Method 1: From parentheses
        if '(' in country and ')' in country:
            code = country.split('(')[1].split(')')[0].strip()
            if len(code) == 3 and code.isupper():
                return code
        
        # Method 2: From manual mapping
        return self.NATION_TO_IOC.get(country_clean)
    
    def save_to_json(self, data: Dict, filepath: str):
        """Save population data to JSON file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved to {filepath}")


def main():
    """Main function."""
    print("=" * 70)
    print("Population Data Scraper")
    print("=" * 70)
    print()
    
    scraper = PopulationScraper()
    
    # Scrape population data
    populations = scraper.scrape_population()
    
    if populations:
        print("\n" + "=" * 70)
        print("RESULTS")
        print("=" * 70)
        print(f"\n✓ Found population data for {len(populations)} countries")
        
        # Show some examples
        print("\nSample data:")
        for i, (ioc, pop) in enumerate(list(populations.items())[:5]):
            print(f"  {ioc}: {pop:,}")
        
        # Save to file
        print("\n" + "=" * 70)
        print("SAVING DATA")
        print("=" * 70)
        
        output_file = 'data/population/population.json'
        scraper.save_to_json(populations, output_file)
        
    else:
        print("\n✗ No population data found")


if __name__ == '__main__':
    main()
