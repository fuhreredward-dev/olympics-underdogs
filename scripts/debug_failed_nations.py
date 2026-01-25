"""
Debug script to test failed nations.
"""

import sys
sys.path.insert(0, 'scripts')
from scrape_nation_sports import NationCompetitorsScraper

# Failed nations
failed_nations = ['GER', 'AUT', 'CZE', 'GBR', 'SLO', 'AUS', 'GEO', 'CRO', 'HKG']

scraper = NationCompetitorsScraper()

print("Testing failed nations with debug output:")
print("=" * 70)

for ioc in failed_nations:
    print(f"\n{ioc}:")
    result = scraper.scrape_nation(ioc, debug=True)
    if result:
        print(f"  ✓ SUCCESS: {len(result)} sports found")
    print()
