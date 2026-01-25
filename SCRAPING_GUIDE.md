# Web Scraping Guide

## Overview

I've created three scraping scripts to fetch real data from Wikipedia and other sources:

1. **scrape_pandas.py** - Easiest method using pandas (RECOMMENDED)
2. **scrape_wikipedia.py** - More control with BeautifulSoup
3. **scrape_population.py** - Population data from REST Countries API

## Quick Start

### 1. Install Additional Dependencies

```bash
pip install beautifulsoup4 lxml html5lib
```

All dependencies are in [requirements.txt](requirements.txt).

### 2. Run the Pandas Scraper (Easiest)

```bash
python scripts/scrape_pandas.py
```

This will:
- Fetch all-time Olympic medal data from Wikipedia
- Parse the medal table automatically
- Save to `data/medals/historical_medals.json`
- Show you sample data

### 3. Run the Population Scraper

```bash
python scripts/scrape_population.py
```

This will:
- Fetch current population data from REST Countries API
- Map country names to IOC codes
- Save to `data/population/population.json`

## Detailed Usage

### Option 1: Pandas Scraper (Recommended)

**Pros:**
- Simplest to use
- Automatically parses HTML tables
- Most reliable for structured data

**Usage:**
```bash
cd "c:\Users\emf48\OneDrive\Documents\Olympic Underdogs and GOATs"
python scripts/scrape_pandas.py
```

**What it does:**
```python
# Fetches from:
https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table

# Parses table with columns: Nation, Gold, Silver, Bronze, Total
# Extracts IOC codes from nation names (e.g., "United States (USA)")
# Outputs JSON with structure:
{
  "USA": {"gold": 113, "silver": 122, "bronze": 95, "total": 330},
  "NOR": {"gold": 148, "silver": 133, "bronze": 122, "total": 403}
}
```

### Option 2: BeautifulSoup Scraper (More Control)

**Pros:**
- More control over parsing
- Can handle complex HTML structures
- Supports both all-time and Winter-only medals

**Usage:**
```bash
python scripts/scrape_wikipedia.py
```

**Interactive menu:**
```
1. All-time Olympic medals (Summer + Winter)
2. Winter Olympics medals only
3. Both
```

### Option 3: Population Scraper

**Pros:**
- Uses REST Countries API (reliable)
- Current population data
- Already mapped to IOC codes

**Usage:**
```bash
python scripts/scrape_population.py
```

**Data source:**
```
API: https://restcountries.com/v3.1/all
Returns: Current population estimates for all countries
```

## Understanding the Scrapers

### How Pandas Scraper Works

```python
# 1. Fetch Wikipedia page
tables = pd.read_html(url)

# 2. Find table with Gold, Silver, Bronze columns
for table in tables:
    if 'gold' in columns and 'silver' in columns:
        # This is the medal table!
        
# 3. Parse each row
for row in table:
    nation = row['Nation']
    ioc_code = extract_from_parentheses(nation)  # "USA" from "United States (USA)"
    gold = int(row['Gold'])
    # ... etc
```

### Wikipedia Table Structure

The Wikipedia medal tables typically look like:

```
| Rank | Team           | Gold | Silver | Bronze | Total |
|------|----------------|------|--------|--------|-------|
| 1    | Norway (NOR)   | 148  | 133    | 122    | 403   |
| 2    | USA (USA)      | 113  | 122    | 95     | 330   |
```

The scraper extracts the IOC code from the parentheses.

### IOC Code Extraction

```python
# Method 1: From parentheses
"United States (USA)" → "USA"
"Norway (NOR)" → "NOR"

# Method 2: From dedicated column (some tables)
| Nation        | IOC | Gold | Silver | Bronze |
| United States | USA | 113  | 122    | 95     |
```

## Customization

### Add More IOC Code Mappings

If countries aren't being recognized, add to the mapping in [scrape_population.py](scripts/scrape_population.py):

```python
IOC_CODE_MAP = {
    'New Country Name': 'NEW',
    'Alternative Name': 'ALT',
}
```

### Scrape Winter Olympics Only

Modify scraper to use Winter Olympics URL:

```python
url = "https://en.wikipedia.org/wiki/All-time_Winter_Olympic_Games_medal_table"
```

### Save to Different Location

```python
scraper.save_to_json(data, 'custom/path/medals.json')
```

## Troubleshooting

### "No tables found"

**Problem:** Wikipedia page structure changed

**Solutions:**
1. Print all tables to inspect: `print(f"Found {len(tables)} tables")`
2. Inspect the Wikipedia page HTML manually
3. Adjust table detection logic

### "IOC code not found"

**Problem:** Wikipedia table doesn't include IOC codes

**Solutions:**
1. Check table structure on Wikipedia
2. Add manual mapping: `MANUAL_MAP = {'Norway': 'NOR'}`
3. Use alternative data source

### "Connection error"

**Problem:** Network issue or Wikipedia blocking

**Solutions:**
1. Check internet connection
2. Add user agent: `headers = {'User-Agent': 'Mozilla/5.0 ...'}`
3. Add delay between requests: `time.sleep(1)`

### "Parsing error"

**Problem:** Unexpected table format

**Solutions:**
1. Print table structure: `print(table.head())`
2. Check column names: `print(table.columns.tolist())`
3. Adjust parsing logic for that specific table

## Best Practices

### 1. Check Data After Scraping

```bash
# View the scraped file
cat data/medals/historical_medals.json

# Or in Python
python -c "import json; print(json.load(open('data/medals/historical_medals.json')))"
```

### 2. Backup Existing Data

```bash
# Before scraping
cp data/medals/historical_medals.json data/medals/historical_medals.backup.json
```

### 3. Validate Scraped Data

```python
# Check for expected nations
expected = ['USA', 'NOR', 'GER', 'CAN']
medals = json.load(open('data/medals/historical_medals.json'))

for nation in expected:
    if nation not in medals:
        print(f"Warning: {nation} not found!")
```

### 4. Be Respectful to Servers

- Don't scrape too frequently
- Add delays between requests
- Cache data locally
- Use official APIs when available

## Alternative Data Sources

### Official Olympic Data

**Olympic.org API** (if available):
- Most authoritative source
- May require API key
- Check: https://olympics.com/en/olympic-games/olympic-results

### Sports Statistics Websites

- **Sports Reference**: https://www.sports-reference.com/olympics/
- **Olympic Database**: http://www.olympedia.org/

### Government Statistics

For population:
- **World Bank**: https://data.worldbank.org/
- **UN Data**: http://data.un.org/

## Advanced: Scheduling Automatic Updates

### Daily Update Script

Create `scripts/update_data.py`:

```python
from scrape_pandas import PandasOlympicScraper
from scrape_population import PopulationScraper

# Update medals
medal_scraper = PandasOlympicScraper()
medals = medal_scraper.scrape_all_time_medals()
medal_scraper.save_to_json(medals, 'data/medals/historical_medals.json')

# Update population
pop_scraper = PopulationScraper()
population = pop_scraper.scrape_population()
pop_scraper.save_to_json(population, 'data/population/population.json')

print("✓ Data updated!")
```

### Schedule with Task Scheduler

Run weekly to keep data current:
```bash
# Every Sunday at 2 AM
schtasks /create /tn "Update Olympic Data" /tr "python scripts/update_data.py" /sc weekly /d SUN /st 02:00
```

## Example: Complete Data Refresh

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Backup existing data
mkdir -p backups
cp data/medals/historical_medals.json backups/medals_$(date +%Y%m%d).json
cp data/population/population.json backups/population_$(date +%Y%m%d).json

# 3. Scrape new medal data
python scripts/scrape_pandas.py

# 4. Scrape new population data
python scripts/scrape_population.py

# 5. Verify data
python -c "import json; m = json.load(open('data/medals/historical_medals.json')); print(f'Medals: {len(m)} nations')"
python -c "import json; p = json.load(open('data/population/population.json')); print(f'Population: {len(p)} nations')"

# 6. Test the application
python main.py --date 2026-02-08
```

## Next Steps

After scraping real data:

1. **Verify accuracy** - Spot check some medal counts
2. **Update IOC mappings** - Add missing nations to `src/utils.py`
3. **Test watchlists** - Generate watchlists with real data
4. **Document sources** - Note data source and scrape date
5. **Set up updates** - Schedule periodic refreshes

## Resources

- **Wikipedia Olympic Medal Tables**: https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table
- **REST Countries API**: https://restcountries.com/
- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **BeautifulSoup Documentation**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

---

**Ready to scrape?** Start with the pandas scraper - it's the easiest!

```bash
python scripts/scrape_pandas.py
```
