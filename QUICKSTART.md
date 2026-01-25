# Quick Start Guide

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify data files exist:**
   - `data/schedule/schedule.json` - Olympic schedule with competing nations
   - `data/medals/historical_medals.json` - Historical medal counts
   - `data/population/population.json` - Population by nation

## Usage

### Generate today's watchlist:
```bash
python main.py
```

### Generate watchlist for specific date:
```bash
python main.py --date 2026-02-07
```

### Generate all watchlists for entire Olympics:
```bash
python main.py --all
```

## Example Output

The watchlist will be saved to `outputs/daily_watchlists/watchlist_YYYY-MM-DD.md` and will look like:

```markdown
# Olympic Underdogs Watchlist - February 07, 2026

**2 underdog nation(s) competing today!**

## Alpine Skiing

### Liechtenstein (LIE)
- _Never won Olympic gold_
- _Population < 1.0M_

**Events:**
- Women's Downhill Training (Training) @ 11:00

## Biathlon

### Liechtenstein (LIE)
- _Never won Olympic gold_
- _Population < 1.0M_

**Events:**
- Men's 10km Sprint (Medal Event) @ 14:30

---

## 🏅 Medals Per Capita Leaderboard

| Rank | Nation | Total Medals | Population | Medals/1M |
|------|--------|--------------|------------|-----------|
| 1 | Liechtenstein (LIE) | 10 | 39.00K | 256.41 |
| 2 | Norway (NOR) | 403 | 5.42M | 74.29 |
...
```

## Customization

Edit `config.yaml` to customize:
- Underdog criteria (thresholds, which criteria to enable)
- Data file paths
- Output format and display options
- Number of nations in medals per capita leaderboard

## Adding More Data

### Schedule Data
Add more dates and events to `data/schedule/schedule.json`:
```json
{
  "2026-02-13": [
    {
      "sport": "Ice Hockey",
      "discipline": "Ice Hockey",
      "event": "Men's Preliminary Round",
      "session": "Regular Event",
      "time": "12:00",
      "nations": ["CAN", "USA", "FIN", "SWE"]
    }
  ]
}
```

### Medal Data
Update `data/medals/historical_medals.json` with complete historical data:
```json
{
  "NEW": {"gold": 0, "silver": 0, "bronze": 0, "total": 0}
}
```

### Population Data
Update `data/population/population.json`:
```json
{
  "NEW": 500000
}
```

## Project Structure

```
├── main.py                    # Main entry point
├── config.yaml                # Configuration
├── requirements.txt           # Dependencies
├── data/
│   ├── schedule/              # Olympic schedule
│   ├── medals/                # Historical medals
│   └── population/            # Population data
├── src/
│   ├── data_loader.py         # Data loading
│   ├── underdog_checker.py    # Underdog detection
│   ├── medals_per_capita.py   # Per capita calculations
│   ├── watchlist_generator.py # Watchlist generation
│   └── utils.py               # Utilities
└── outputs/
    └── daily_watchlists/      # Generated watchlists
```

## Tips

1. **Update nation names**: Edit `get_ioc_code_name_map()` in `src/utils.py` to add more nations
2. **Change criteria**: Modify thresholds in `config.yaml`
3. **Different formats**: Set output format to "json" or "html" in config (markdown is default)
4. **Schedule automation**: Use cron/Task Scheduler to run daily:
   ```bash
   python main.py --date $(date +%Y-%m-%d)
   ```
