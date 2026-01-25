"""
Population data scraper using REST Countries API.
More reliable than Wikipedia for population data.
"""

import json
import requests
from pathlib import Path
from typing import Dict


class PopulationScraper:
    """Scrapes population data from REST Countries API."""
    
    API_URL = "https://restcountries.com/v3.1/all?fields=name,population"
    
    # Mapping from country names to IOC codes
    # This is necessary because REST Countries uses different codes
    IOC_CODE_MAP = {
        'United States': 'USA',
        'United States of America': 'USA',
        'Canada': 'CAN',
        'Germany': 'GER',
        'France': 'FRA',
        'Italy': 'ITA',
        'Norway': 'NOR',
        'Sweden': 'SWE',
        'Finland': 'FIN',
        'Austria': 'AUT',
        'Switzerland': 'SUI',
        'Japan': 'JPN',
        'China': 'CHN',
        'South Korea': 'KOR',
        'Korea (Republic of)': 'KOR',
        'United Kingdom': 'GBR',
        'Netherlands': 'NED',
        'Russia': 'RUS',
        'Russian Federation': 'RUS',
        'Czechia': 'CZE',
        'Czech Republic': 'CZE',
        'Poland': 'POL',
        'Slovakia': 'SVK',
        'Slovenia': 'SLO',
        'Croatia': 'CRO',
        'Belarus': 'BLR',
        'Ukraine': 'UKR',
        'Kazakhstan': 'KAZ',
        'Australia': 'AUS',
        'New Zealand': 'NZL',
        'Spain': 'ESP',
        'Belgium': 'BEL',
        'Latvia': 'LAT',
        'Estonia': 'EST',
        'Lithuania': 'LTU',
        'Bulgaria': 'BUL',
        'Romania': 'ROM',
        'Hungary': 'HUN',
        'Liechtenstein': 'LIE',
        'Andorra': 'AND',
        'Monaco': 'MON',
        'San Marino': 'SMR',
        'Iceland': 'ISL',
        'Luxembourg': 'LUX',
        'Malta': 'MLT',
        'Cyprus': 'CYP',
        'Georgia': 'GEO',
        'Armenia': 'ARM',
        'Moldova': 'MDA',
        'Bosnia and Herzegovina': 'BIH',
        'North Macedonia': 'MKD',
        'Albania': 'ALB',
        'Montenegro': 'MNE',
        'Serbia': 'SRB',
        'Kosovo': 'KOS',
        'Jamaica': 'JAM',
        'Mexico': 'MEX',
        'Brazil': 'BRA',
        'Argentina': 'ARG',
        'Chile': 'CHI',
        'India': 'IND',
        'Pakistan': 'PAK',
        'Thailand': 'THA',
        'Malaysia': 'MAS',
        'Singapore': 'SGP',
        'Hong Kong': 'HKG',
        'Taiwan': 'TPE',
        'Philippines': 'PHI',
        'Iran': 'IRI',
        'Iran (Islamic Republic of)': 'IRI',
        'Israel': 'ISR',
        'Turkey': 'TUR',
        'Türkiye': 'TUR',
        'Egypt': 'EGY',
        'Morocco': 'MAR',
        'South Africa': 'RSA',
        'Kenya': 'KEN',
        'Nigeria': 'NGR',
        'Ghana': 'GHA',
        'Tunisia': 'TUN',
        'Algeria': 'ALG',
    }
    
    def scrape_population(self) -> Dict[str, int]:
        """
        Scrape population data from REST Countries API.
        
        Returns:
            Dict mapping IOC codes to population
        """
        print("Fetching population data from REST Countries API...")
        
        try:
            response = requests.get(self.API_URL)
            response.raise_for_status()
            countries = response.json()
            
            population_data = {}
            
            for country in countries:
                try:
                    # Get country name and population
                    name = country.get('name', {}).get('common', '')
                    population = country.get('population', 0)
                    
                    # Try to map to IOC code
                    ioc_code = self.IOC_CODE_MAP.get(name)
                    
                    if ioc_code and population > 0:
                        population_data[ioc_code] = population
                        print(f"  ✓ {ioc_code} ({name}): {population:,}")
                
                except Exception as e:
                    continue
            
            print(f"\n✓ Scraped population for {len(population_data)} nations")
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
    """Main function."""
    print("=" * 60)
    print("Population Data Scraper")
    print("=" * 60)
    print()
    
    scraper = PopulationScraper()
    
    population = scraper.scrape_population()
    
    if population:
        scraper.save_to_json(
            population,
            'data/population/population.json'
        )
        
        print("\nSample data:")
        for ioc_code, pop in list(population.items())[:5]:
            print(f"  {ioc_code}: {pop:,}")


if __name__ == '__main__':
    main()
