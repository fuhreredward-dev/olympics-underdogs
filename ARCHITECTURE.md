# System Architecture

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │   schedule.json  │  │ historical_      │  │ population.  │  │
│  │                  │  │ medals.json      │  │ json         │  │
│  │ • Dates          │  │ • Gold medals    │  │ • IOC code   │  │
│  │ • Sports         │  │ • Silver medals  │  │ • Population │  │
│  │ • Events         │  │ • Bronze medals  │  │              │  │
│  │ • Nations        │  │ • Total medals   │  │              │  │
│  │ • Times          │  │                  │  │              │  │
│  └────────┬─────────┘  └────────┬─────────┘  └───────┬──────┘  │
│           │                     │                     │          │
└───────────┼─────────────────────┼─────────────────────┼──────────┘
            │                     │                     │
            ▼                     ▼                     ▼
    ┌───────────────────────────────────────────────────────┐
    │              DATA LOADER (data_loader.py)             │
    │ • Loads and parses all JSON files                     │
    │ • Provides data access methods                        │
    │ • Caches data in memory                               │
    └──────────────┬────────────────────────────────────────┘
                   │
                   │ Provides data to ↓
                   │
        ┌──────────┴──────────┬──────────────────────┐
        ▼                     ▼                       ▼
┌───────────────┐  ┌──────────────────┐  ┌────────────────────┐
│ UNDERDOG      │  │ MEDALS PER       │  │ WATCHLIST          │
│ CHECKER       │  │ CAPITA           │  │ GENERATOR          │
│               │  │ CALCULATOR       │  │                    │
│ Checks if     │  │                  │  │ Combines all       │
│ nation meets: │  │ • Calculates per │  │ components to      │
│               │  │   capita metrics │  │ generate:          │
│ • Never       │  │ • Ranks nations  │  │                    │
│   medaled     │  │ • Formats        │  │ • Daily watchlist  │
│ • Never gold  │  │   leaderboard    │  │ • Underdog list    │
│ • Pop < 1M    │  │                  │  │ • Sidebar          │
│               │  │                  │  │ • Formatted output │
└───────────────┘  └──────────────────┘  └──────────┬─────────┘
                                                      │
                                                      │ Generates ↓
                                                      │
                                          ┌───────────▼──────────┐
                                          │  MARKDOWN OUTPUT     │
                                          │                      │
                                          │  watchlist_          │
                                          │  YYYY-MM-DD.md       │
                                          └──────────────────────┘
```

## Component Interactions

### 1. Main Application (main.py)
```
main.py
  ↓
  1. Load config.yaml
  2. Initialize DataLoader
  3. Initialize UnderdogChecker
  4. Initialize MedalsPerCapitaCalculator
  5. Initialize WatchlistGenerator
  6. Generate watchlist(s)
  7. Save to file
```

### 2. Data Loading Flow
```
schedule.json → DataLoader.load_schedule()
                    ↓
                get_events_for_date(date)
                    ↓
                get_competing_nations_for_date(date)
                    ↓
                Returns: Set of IOC codes
```

### 3. Underdog Detection Flow
```
Nation IOC code
    ↓
UnderdogChecker.is_underdog(ioc_code)
    ↓
    ├─→ check_never_medaled() → medals['total'] == 0?
    ├─→ check_never_won_gold() → medals['gold'] == 0?
    └─→ check_small_population() → population < threshold?
    ↓
Returns: (is_underdog: bool, criteria_met: list)
```

### 4. Medals Per Capita Flow
```
Nation IOC code
    ↓
MedalsPerCapitaCalculator.calculate_for_nation(ioc_code)
    ↓
    ├─→ Get medal count
    ├─→ Get population
    └─→ Calculate: (medals / population) × 1,000,000
    ↓
Returns: {total_per_capita, gold_per_capita, medals, population}
```

### 5. Watchlist Generation Flow
```
Date string (YYYY-MM-DD)
    ↓
WatchlistGenerator.generate_for_date(date)
    ↓
    1. Get all events for date
    2. Extract competing nations
    3. Filter to underdogs only
    4. Group by sport (if configured)
    5. Format event details
    6. Generate medals per capita sidebar
    7. Combine into markdown
    ↓
Returns: Formatted markdown string
```

## Configuration Flow

```
config.yaml
    ↓
    ├─→ olympics: {start_date, end_date, name}
    │       Used by: main.py (date range validation)
    │
    ├─→ criteria: {never_medaled, never_won_gold, population_threshold}
    │       Used by: UnderdogChecker (determine which criteria to apply)
    │
    ├─→ data_paths: {schedule, medals, population}
    │       Used by: DataLoader (locate data files)
    │
    ├─→ output: {directory, format, include_sidebar}
    │       Used by: WatchlistGenerator (save location, format)
    │
    └─→ display: {show_session_times, group_by_sport, max_nations_sidebar}
            Used by: WatchlistGenerator (formatting options)
```

## Module Dependencies

```
main.py
  │
  ├─→ utils.py
  │    ├─ load_config()
  │    ├─ date formatting functions
  │    ├─ IOC code mappings
  │    └─ calculation helpers
  │
  ├─→ data_loader.py
  │    ├─ Load schedule
  │    ├─ Load medals
  │    └─ Load population
  │
  ├─→ underdog_checker.py
  │    │ (depends on data_loader)
  │    ├─ Check criteria
  │    └─ Filter nations
  │
  ├─→ medals_per_capita.py
  │    │ (depends on data_loader)
  │    ├─ Calculate per capita
  │    └─ Generate leaderboard
  │
  └─→ watchlist_generator.py
       │ (depends on all above)
       ├─ Generate watchlist
       ├─ Format output
       └─ Save to file
```

## Execution Sequence

### Single Date Generation
```
1. python main.py --date 2026-02-07
         ↓
2. Parse arguments
         ↓
3. Load config.yaml
         ↓
4. Initialize all components
         ↓
5. Load all data sources (schedule, medals, population)
         ↓
6. Get events for 2026-02-07
         ↓
7. Extract competing nations
         ↓
8. Check each nation against criteria
         ↓
9. Build watchlist structure
         ↓
10. Calculate medals per capita leaderboard
         ↓
11. Format as markdown
         ↓
12. Save to outputs/daily_watchlists/watchlist_2026-02-07.md
         ↓
13. Print to console
         ↓
14. Done!
```

### All Dates Generation
```
1. python main.py --all
         ↓
2. Parse arguments (--all flag)
         ↓
3. Load config.yaml
         ↓
4. Get date range (start_date to end_date)
         ↓
5. For each date in range:
    ├─→ Generate watchlist for date
    └─→ Save to file
         ↓
6. Report total files generated
         ↓
7. Done!
```

## Error Handling

```
Data File Missing?
    ↓
DataLoader prints warning
    ↓
Returns empty dataset
    ↓
Watchlist continues with available data

No Events for Date?
    ↓
Generates "No events scheduled" watchlist

No Underdogs Found?
    ↓
Generates "No underdogs competing" watchlist
Still includes medals per capita sidebar

Invalid Date Format?
    ↓
Python datetime raises error
User sees error message
```

## Extension Points

Want to extend the system? Here's where to add features:

### New Data Source
```
1. Create new JSON file in data/
2. Add loading method to data_loader.py
3. Add access methods to DataLoader class
4. Use in checker/calculator/generator
```

### New Underdog Criterion
```
1. Add to config.yaml criteria section
2. Add check method to underdog_checker.py
3. Update is_underdog() to check new criterion
4. Add explanation text to criteria_met list
```

### New Output Format
```
1. Add format option to config.yaml
2. Create format method in watchlist_generator.py
3. Handle in save_watchlist() method
Example: format_as_html(), format_as_json()
```

### New Leaderboard Metric
```
1. Add calculation to medals_per_capita.py
2. Update calculate_for_nation() to include new metric
3. Update get_leaderboard() to support sorting by new metric
4. Update format_leaderboard() to display new metric
```

## Performance Considerations

- **Data loaded once**: All data cached in memory after first load
- **Parallel generation**: Could parallelize generation for --all flag
- **JSON parsing**: Fast enough for small datasets (< 100 nations)
- **File I/O**: Minimal - only reads data files and writes output files

## Testing Strategy

```
Unit Tests:
  ├─ utils.py: Test date formatting, calculations
  ├─ data_loader.py: Test data parsing, access methods
  ├─ underdog_checker.py: Test criteria checking logic
  ├─ medals_per_capita.py: Test per capita calculations
  └─ watchlist_generator.py: Test formatting logic

Integration Tests:
  ├─ Test full workflow with sample data
  ├─ Test edge cases (no events, no underdogs)
  └─ Test all command-line options

End-to-End Tests:
  └─ Generate watchlists for all dates, verify output
```
