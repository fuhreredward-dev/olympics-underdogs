# Frequently Asked Questions (FAQ)

## General Questions

### What is this project?
This is a daily watchlist generator for the 2026 Winter Olympics that identifies and tracks "underdog" nations competing each day. It helps you discover lesser-known teams and athletes who are competing against the odds.

### What makes a nation an "underdog"?
A nation meets underdog criteria if it has:
- **Never won any Olympic medal** (Summer or Winter), OR
- **Never won an Olympic gold medal**, OR
- **Population under 1 million people**

### Why medals per capita?
The medals per capita leaderboard shows which nations are the most successful relative to their population size. Smaller nations like Liechtenstein (39,000 people) can compete with much larger nations when you account for population size!

## Usage Questions

### How do I run it?
```bash
python main.py --date 2026-02-07
```
Or just `python main.py` to use today's date.

### Can I generate all days at once?
Yes! Run:
```bash
python main.py --all
```

### Where are the watchlists saved?
In `outputs/daily_watchlists/` with filenames like `watchlist_2026-02-07.md`

### Can I change the output format?
Yes, edit `config.yaml` and change the `output.format` setting. Markdown is currently the implemented format, but the structure supports JSON and HTML.

## Data Questions

### Where does the schedule data come from?
The schedule data is based on the official Olympics schedule. You need to populate `data/schedule/schedule.json` with event dates, sports, and competing nations.

### How do I add more schedule data?
See [DATA_GUIDE.md](DATA_GUIDE.md) for detailed instructions. You can:
1. Reference the Olympics schedule image provided
2. Check official federation websites (FIS, IBU, ISU, etc.)
3. Use historical participation patterns

### Where did the medal data come from?
Historical Olympic medal counts (all-time, Summer + Winter combined). Sources:
- Olympic.org official database
- Wikipedia Olympic medal tables

### Can I update the medal counts during the Olympics?
Yes! Edit `data/medals/historical_medals.json` to add new medals as they're won. This will update the medals per capita leaderboard.

### Why are some population numbers estimates?
Population data comes from World Bank, UN, and other official sources, but exact numbers vary. The important thing is relative scale (under 1M vs over 1M).

## Configuration Questions

### How do I change the population threshold?
Edit `config.yaml`:
```yaml
criteria:
  population_threshold: 500000  # Now 500k instead of 1M
```

### Can I disable certain criteria?
Yes, edit `config.yaml`:
```yaml
criteria:
  never_medaled: true
  never_won_gold: false  # Disable this one
  population_threshold: 1000000
```

### How do I show more nations in the medals per capita leaderboard?
Edit `config.yaml`:
```yaml
display:
  max_nations_sidebar: 30  # Show top 30 instead of 20
```

### Can I hide session times?
Yes, edit `config.yaml`:
```yaml
display:
  show_session_times: false
```

## Technical Questions

### What Python version do I need?
Python 3.7 or higher. The code has been tested with Python 3.13.

### What dependencies are required?
- pyyaml
- pandas
- python-dateutil
- requests

Install with: `pip install -r requirements.txt`

### Can I run this on Linux/Mac?
Yes! The code is cross-platform. Just use forward slashes in paths if you edit the config.

### How do I handle IOC code for new nations?
Add them to the mapping in `src/utils.py` in the `get_ioc_code_name_map()` function:
```python
return {
    ...
    "NEW": "New Nation Name",
}
```

## Specific Nations

### Why does Liechtenstein show up so much?
Liechtenstein has:
- Population of only 39,000 people (under 1M threshold)
- Strong winter sports tradition (skiing, bobsleigh)
- 10 Olympic medals total (impressive for their size!)
- They're consistently competitive in Alpine skiing

### Will Jamaica's bobsled team appear?
Yes! Jamaica meets the "never won Olympic gold" criterion (they have 4 bronze medals). They'll show up when competing in bobsled events.

### What about Monaco?
Monaco (39,000 people) has never won any Olympic medal, so they're a true underdog. If they compete in any winter sport, they'll be highlighted.

### Does this track Summer Olympics too?
No, this project is specifically for Winter Olympics 2026. However, the medal data includes all-time Olympic medals (Summer + Winter combined).

## Feature Requests

### Can you add historical context?
You could extend the project to show:
- Best historical finish for each underdog nation
- Athletes to watch from underdog nations
- Previous Olympic performances

### Can you add live results?
This would require:
- Real-time results API
- More frequent updates (not just daily)
- Medal ceremony tracking

### Can you create an HTML dashboard?
Yes! The project structure supports HTML output. You'd need to:
1. Create HTML templates
2. Add rendering logic to `watchlist_generator.py`
3. Set `output.format: html` in config

### Can you add predictions?
You could add:
- World rankings integration
- Betting odds
- Expert predictions
- Previous season results

## Troubleshooting

### I get "No events scheduled for this date"
This means there's no data in `schedule.json` for that date. Add events following the [DATA_GUIDE.md](DATA_GUIDE.md).

### A nation I expect isn't showing up
Check:
1. Is the nation in the schedule data's `nations` array?
2. Does the nation meet any underdog criteria?
3. Is the nation's data in medals.json and population.json?

### The medals per capita seems wrong
Verify:
1. Medal count in `data/medals/historical_medals.json`
2. Population in `data/population/population.json`
3. Calculation: (total medals / population) × 1,000,000

### File path errors on Windows
Make sure to:
- Use full paths with drive letters
- Or use forward slashes: `c:/Users/...`
- Or escape backslashes: `c:\\Users\\...`

## Olympics 2026 Specifics

### When are the 2026 Winter Olympics?
February 6-22, 2026 in Milano-Cortina, Italy (17 days)

### What sports are included?
All 16 Winter Olympic sports:
- Alpine Skiing, Biathlon, Bobsleigh, Cross-Country Skiing
- Curling, Figure Skating, Freestyle Skiing, Ice Hockey
- Luge, Nordic Combined, Short Track, Skeleton
- Ski Jumping, Ski Mountaineering, Snowboard, Speed Skating

### What's new in 2026?
- Ski Mountaineering makes its Olympic debut!
- Watch for underdog nations in this new sport

### How many nations typically compete?
Around 90-95 nations compete in Winter Olympics. Of these, typically 20-30 meet underdog criteria.

## Support

### Where can I report bugs?
Check the code in the `src/` directory and fix directly, or document issues for future updates.

### How can I contribute?
- Add more schedule data
- Update medal counts during the Olympics
- Improve IOC code mappings
- Create HTML templates
- Add new features

### Can I use this for other Olympics?
Yes! Just update:
1. Olympics dates in `config.yaml`
2. Schedule data for the new games
3. Updated medal counts (post-Olympics)

---

**Not finding your question?** Check:
- [README.md](README.md) - Project overview
- [QUICKSTART.md](QUICKSTART.md) - Basic usage
- [DATA_GUIDE.md](DATA_GUIDE.md) - Data formats
- [AUTOMATION.md](AUTOMATION.md) - Scheduling
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Complete summary
