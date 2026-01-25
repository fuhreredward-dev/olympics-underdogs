"""
Master data scraper - fetches all data at once.
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from scrape_pandas import PandasOlympicScraper
from scrape_population import PopulationScraper


def main():
    """Scrape all data sources."""
    print("=" * 70)
    print(" " * 20 + "MASTER DATA SCRAPER")
    print("=" * 70)
    print("\nThis will fetch:")
    print("  1. Olympic medal counts from Wikipedia")
    print("  2. Population data from REST Countries API")
    print("\n" + "=" * 70)
    
    # Confirm
    response = input("\nProceed? (y/n): ").strip().lower()
    if response != 'y':
        print("Cancelled.")
        return
    
    print("\n" + "=" * 70)
    print("STEP 1: Scraping Olympic Medal Data")
    print("=" * 70)
    
    try:
        medal_scraper = PandasOlympicScraper()
        medals = medal_scraper.scrape_all_time_medals()
        
        if medals:
            medal_scraper.save_to_json(medals, 'data/medals/historical_medals.json')
            print(f"✓ Scraped {len(medals)} nations' medal data")
        else:
            print("✗ No medal data scraped")
    except Exception as e:
        print(f"✗ Error scraping medals: {e}")
    
    print("\n" + "=" * 70)
    print("STEP 2: Scraping Population Data")
    print("=" * 70)
    
    try:
        pop_scraper = PopulationScraper()
        population = pop_scraper.scrape_population()
        
        if population:
            pop_scraper.save_to_json(population, 'data/population/population.json')
            print(f"✓ Scraped population for {len(population)} nations")
        else:
            print("✗ No population data scraped")
    except Exception as e:
        print(f"✗ Error scraping population: {e}")
    
    print("\n" + "=" * 70)
    print("COMPLETE!")
    print("=" * 70)
    print("\nData saved to:")
    print("  • data/medals/historical_medals.json")
    print("  • data/population/population.json")
    print("\nNext steps:")
    print("  1. Review the data files")
    print("  2. Run: python main.py --date 2026-02-08")
    print("  3. Generate watchlists with real data!")
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
