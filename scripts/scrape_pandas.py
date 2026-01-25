"""
Alternative scraper using pandas for easier table parsing.
Scrapes both Winter and All-Time Olympic medal data from Wikipedia.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, Tuple


class PandasOlympicScraper:
    """Scrapes Olympic data using pandas.read_html()."""
    
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
    
    def scrape_medals(self) -> Tuple[Dict[str, Dict], Dict[str, Dict]]:
        """
        Scrape both Winter and All-Time Olympic medals from Wikipedia.
        
        Returns:
            Tuple of (winter_medals, all_time_medals)
        """
        print("Scraping Olympic medals from Wikipedia...")
        print("Target: List of NOCs with medals (sortable & unranked)")
        
        url = "https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table"
        
        try:
            # Read all tables from the page with headers to avoid 403
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            tables = pd.read_html(url, storage_options=headers)
            
            print(f"\nFound {len(tables)} tables on page")
            
            # Look for the table with both Summer and Winter columns
            for i, table in enumerate(tables):
                cols_str = str(table.columns).lower()
                
                # This table has multi-level columns with Summer, Winter, and Combined
                if 'summer' in cols_str and 'winter' in cols_str and 'combined' in cols_str:
                    print(f"\n✓ Found combined medal table (Table {i})")
                    print(f"Shape: {table.shape}")
                    
                    # Parse both winter and all-time from this table
                    winter_medals, all_time_medals = self._parse_combined_table(table)
                    return winter_medals, all_time_medals
            
            print("Could not find combined medal table")
            return {}, {}
        
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return {}, {}
    
    def _parse_combined_table(self, df: pd.DataFrame) -> Tuple[Dict[str, Dict], Dict[str, Dict]]:
        """
        Parse the combined table with Summer and Winter columns.
        
        Returns:
            Tuple of (winter_medals, all_time_medals)
        """
        winter_medals = {}
        all_time_medals = {}
        
        print("\nParsing combined Summer/Winter table...")
        
        # The table has multi-level columns
        if not isinstance(df.columns, pd.MultiIndex):
            print("Warning: Expected multi-level columns")
            return {}, {}
        
        print(f"Column levels: {df.columns.nlevels}")
        print(f"Sample columns: {df.columns[:5].tolist()}")
        
        # Find the team/nation column
        team_col = None
        for col in df.columns:
            col_str = str(col).lower()
            if 'team' in col_str or ('ioc' in col_str and len(str(col)) < 50):
                team_col = col
                break
        
        if team_col is None:
            team_col = df.columns[0]
        
        print(f"Using team column: {team_col}")
        
        # Get column indices for different categories
        # For multi-level columns, we need to find where Summer, Winter, Combined start
        summer_cols = []
        winter_cols = []
        combined_cols = []
        
        for i, col in enumerate(df.columns):
            level0 = str(col[0]).lower() if df.columns.nlevels > 0 else str(col).lower()
            if 'summer' in level0:
                summer_cols.append(i)
            elif 'winter' in level0:
                winter_cols.append(i)
            elif 'combined' in level0:
                combined_cols.append(i)
        
        print(f"Summer columns: {len(summer_cols)}, Winter: {len(winter_cols)}, Combined: {len(combined_cols)}")
        
        # Debug: Show which columns we're using
        if len(combined_cols) >= 5:
            print(f"Combined columns being used: {[df.columns[i] for i in combined_cols[:5]]}")
        if len(winter_cols) >= 5:
            print(f"Winter columns being used: {[df.columns[i] for i in winter_cols[:5]]}")
        
        # Process each row
        for idx, row in df.iterrows():
            try:
                # Get nation name
                nation = str(row[team_col])
                
                # Skip header rows
                if pd.isna(nation) or 'team' in nation.lower() or nation.strip() == '':
                    continue
                
                # Extract IOC code
                ioc_code = self._extract_ioc_code(nation)
                if not ioc_code:
                    continue
                
                # Get winter medals (typically columns 6-10: No, Gold, Silver, Bronze, Total)
                if len(winter_cols) >= 5:
                    winter_gold = self._safe_int(row.iloc[winter_cols[1]])  # Skip "No." column
                    winter_silver = self._safe_int(row.iloc[winter_cols[2]])
                    winter_bronze = self._safe_int(row.iloc[winter_cols[3]])
                    winter_total = self._safe_int(row.iloc[winter_cols[4]])
                    
                    if winter_total and winter_total > 0:
                        winter_medals[ioc_code] = {
                            'gold': winter_gold or 0,
                            'silver': winter_silver or 0,
                            'bronze': winter_bronze or 0,
                            'total': winter_total
                        }
                
                # Get all-time medals (combined total)
                if len(combined_cols) >= 5:
                    all_gold = self._safe_int(row.iloc[combined_cols[1]])
                    all_silver = self._safe_int(row.iloc[combined_cols[2]])
                    all_bronze = self._safe_int(row.iloc[combined_cols[3]])
                    all_total = self._safe_int(row.iloc[combined_cols[4]])
                    
                    # Debug specific nations
                    if ioc_code in ['HUN', 'EST', 'USA']:
                        print(f"  DEBUG {ioc_code}: Gold={all_gold}, Silver={all_silver}, Bronze={all_bronze}, Total={all_total}")
                    
                    if all_total and all_total > 0:
                        all_time_medals[ioc_code] = {
                            'gold': all_gold or 0,
                            'silver': all_silver or 0,
                            'bronze': all_bronze or 0,
                            'total': all_total
                        }
            
            except Exception as e:
                continue
        
        print(f"\n✓ Parsed {len(winter_medals)} nations with Winter medals")
        print(f"✓ Parsed {len(all_time_medals)} nations with All-Time medals")
        
        return winter_medals, all_time_medals
    
    def _extract_ioc_code(self, nation: str) -> str:
        """Extract IOC code from nation string."""
        # Clean nation name
        nation_clean = nation.split('[')[0].strip()
        
        # Method 1: From parentheses like "United States (USA)"
        if '(' in nation and ')' in nation:
            code = nation.split('(')[1].split(')')[0].strip()
            if len(code) == 3 and code.isupper():
                return code
        
        # Method 2: From manual mapping
        return self.NATION_TO_IOC.get(nation_clean)
    
    def _safe_int(self, value) -> int:
        """Safely convert value to int, return None if not possible."""
        try:
            if pd.notna(value):
                s = str(value).strip().replace(',', '')
                if s and s not in ['—', '-', '']:
                    return int(float(s))
        except:
            pass
        return None
    
    def save_to_json(self, data: Dict, filepath: str):
        """Save data to JSON file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved to {filepath}")


def main():
    """Main function."""
    print("=" * 70)
    print("Olympic Medal Scraper - Winter & All-Time")
    print("=" * 70)
    print()
    
    scraper = PandasOlympicScraper()
    
    # Scrape both datasets
    winter_medals, all_time_medals = scraper.scrape_medals()
    
    if winter_medals or all_time_medals:
        print("\n" + "=" * 70)
        print("SAVING DATA")
        print("=" * 70)
        
        # Save Winter medals
        if winter_medals:
            winter_file = 'data/medals/winter_medals.json'
            scraper.save_to_json(winter_medals, winter_file)
            print(f"  {len(winter_medals)} nations with Winter medals")
        
        # Save All-Time medals
        if all_time_medals:
            all_time_file = 'data/medals/all_time_medals.json'
            scraper.save_to_json(all_time_medals, all_time_file)
            print(f"  {len(all_time_medals)} nations with All-Time medals")
        
        # Test cases
        print("\n" + "=" * 70)
        print("VERIFICATION - Testing against known values")
        print("=" * 70)
        
        test_cases = [
            ('USA', 114, 330, 1219, 3095),
            ('HUN', 2, 10, 189, 543),
            ('EST', 4, 8, 25, 44)
        ]
        
        all_passed = True
        for ioc, exp_w_gold, exp_w_total, exp_all_gold, exp_all_total in test_cases:
            print(f"\nTesting {ioc}:")
            
            # Check winter
            if ioc in winter_medals:
                w_gold = winter_medals[ioc]['gold']
                w_total = winter_medals[ioc]['total']
                winter_ok = (w_gold == exp_w_gold and w_total == exp_w_total)
                status = "✓" if winter_ok else "✗"
                print(f"  {status} Winter: {w_gold} gold, {w_total} total (expected {exp_w_gold}/{exp_w_total})")
                all_passed = all_passed and winter_ok
            else:
                print(f"  ✗ Winter: Not found (expected {exp_w_gold}/{exp_w_total})")
                all_passed = False
            
            # Check all-time
            if ioc in all_time_medals:
                all_gold = all_time_medals[ioc]['gold']
                all_total = all_time_medals[ioc]['total']
                all_ok = (all_gold == exp_all_gold and all_total == exp_all_total)
                status = "✓" if all_ok else "✗"
                print(f"  {status} All-Time: {all_gold} gold, {all_total} total (expected {exp_all_gold}/{exp_all_total})")
                all_passed = all_passed and all_ok
            else:
                print(f"  ✗ All-Time: Not found (expected {exp_all_gold}/{exp_all_total})")
                all_passed = False
        
        print("\n" + "=" * 70)
        if all_passed:
            print("✓✓✓ ALL TESTS PASSED! Data is accurate. ✓✓✓")
        else:
            print("⚠ SOME TESTS FAILED - Review the data")
        print("=" * 70)
        
    else:
        print("\n✗ No data scraped")


if __name__ == '__main__':
    main()
