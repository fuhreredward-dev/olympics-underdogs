# Data Templates & Expansion Guide

## Schedule Data Template

To add more events to the schedule, use this JSON structure in `data/schedule/schedule.json`:

```json
{
  "YYYY-MM-DD": [
    {
      "sport": "Sport Name",
      "discipline": "Discipline Name (can be same as sport)",
      "event": "Specific Event Name",
      "session": "Session Type",
      "time": "HH:MM",
      "nations": ["IOC1", "IOC2", "IOC3"]
    }
  ]
}
```

### Session Types
Based on the schedule image provided:
- `"Training"` - Training sessions (○)
- `"Regular Event"` - Regular competition (●)
- `"Medal Event"` - Medal events (⊗)

### Sports from 2026 Winter Olympics
Use these sport names for consistency:
- Alpine Skiing
- Biathlon
- Bobsleigh
- Cross-Country Skiing
- Curling
- Figure Skating
- Freestyle Skiing
- Ice Hockey
- Luge
- Nordic Combined
- Short Track Speed Skating
- Skeleton
- Ski Jumping
- Ski Mountaineering
- Snowboard
- Speed Skating

### Example: Converting from Schedule Image

From your attached schedule, you can see the pattern. For example, looking at February 07:
- Alpine Skiing has both Training (○) and Medal Events (⊗)
- Cross-Country Skiing has Medal Events (⊗)
- Biathlon has events scheduled

To add these, create entries like:
```json
{
  "2026-02-07": [
    {
      "sport": "Alpine Skiing",
      "discipline": "Downhill",
      "event": "Men's Downhill",
      "session": "Medal Event",
      "time": "11:00",
      "nations": ["AUT", "SUI", "NOR", "ITA", "FRA", "USA", "GER"]
    },
    {
      "sport": "Cross-Country Skiing",
      "discipline": "Cross-Country",
      "event": "Men's 15km Classic",
      "session": "Medal Event",
      "time": "15:00",
      "nations": ["NOR", "RUS", "FIN", "SWE", "FRA", "GER", "ITA"]
    }
  ]
}
```

## Finding Competing Nations

If the official schedule doesn't list nations, you have options:

### Option 1: Use Discipline-Level Data
```json
{
  "sport": "Ice Hockey",
  "discipline": "Ice Hockey",
  "event": "Qualification Round",
  "session": "Regular Event",
  "time": "12:00",
  "nations": []  // Empty if not known
}
```

### Option 2: Reference Federation Entry Lists
Check these sources:
- **FIS (International Ski Federation)**: fis-ski.com - for skiing, snowboard
- **IBU (Biathlon)**: biathlonworld.com
- **ISU (Skating)**: isu.org - for figure skating, speed skating, short track
- **IBSF (Bobsleigh & Skeleton)**: ibsf.org
- **FIL (Luge)**: fil-luge.org
- **WCF (Curling)**: worldcurling.org
- **IIHF (Ice Hockey)**: iihf.com

### Option 3: Historical Participation
Use past Winter Olympics to predict likely participants:
- Nations with strong winter sports programs
- Nations that have qualified in previous Olympics
- Nations with athletes ranked in world standings

## Medal Data

Historical Olympic medal data (combined Summer + Winter Olympics) by nation.

Template:
```json
{
  "IOC": {"gold": 0, "silver": 0, "bronze": 0, "total": 0}
}
```

Sources for official data:
- **Olympic.org**: olympics.com/en/olympic-games/olympic-results
- **Wikipedia**: en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table

## Population Data

Current population estimates by nation.

Template:
```json
{
  "IOC": 1000000
}
```

Sources:
- **World Bank**: data.worldbank.org
- **UN Data**: data.un.org
- **Wikipedia**: en.wikipedia.org/wiki/List_of_countries_by_population

## IOC Country Codes

Standard 3-letter codes used by International Olympic Committee. The file `src/utils.py` contains a mapping function `get_ioc_code_name_map()` with many codes.

Common codes:
- USA - United States
- CAN - Canada
- GER - Germany (DEU in some contexts)
- GBR - Great Britain
- NED - Netherlands
- SUI - Switzerland
- etc.

Full list: olympic.org/ioc

## Tips for Expanding Data

1. **Start with Medal Events**: Focus on medal rounds first, as these are most important
2. **Priority Sports**: Focus on sports with more underdog nations (Biathlon, Cross-Country, Ski Jumping)
3. **Check Small Nations**: Pay special attention to entry lists for nations like:
   - Liechtenstein
   - Andorra
   - Monaco
   - San Marino
   - Luxembourg
   - Iceland
   - Jamaica (bobsled!)
   
4. **Validation**: After adding data, test with:
   ```bash
   python main.py --date YYYY-MM-DD
   ```

5. **Complete Schedule**: To generate complete watchlists, work through the schedule image systematically, adding at least the medal events for each sport

## Automated Data Collection (Future Enhancement)

Consider building scrapers for:
- Official Olympics API (if available)
- FIS start lists
- IBU competition calendars
- ISU entry lists

This would require additional dependencies:
```
beautifulsoup4
selenium  # if JavaScript rendering needed
```
