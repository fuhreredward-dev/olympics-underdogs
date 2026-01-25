# Documentation Index

Welcome to the Olympic Underdogs & GOATs Watchlist project! This index will help you find the information you need.

## 📖 Quick Start

New to the project? Start here:

1. **[README.md](README.md)** - Project overview and introduction
2. **[QUICKSTART.md](QUICKSTART.md)** - Installation and basic usage (5 minutes)
3. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project summary and status

## 🎯 Core Documentation

### Getting Started
- **[README.md](README.md)** - Complete project overview
  - What the project does
  - Key features
  - Project structure
  - Installation instructions

- **[QUICKSTART.md](QUICKSTART.md)** - Fast setup guide
  - Installation steps
  - Basic commands
  - Example output
  - Customization basics

### Usage Guides
- **[FAQ.md](FAQ.md)** - Frequently Asked Questions
  - Common questions
  - Troubleshooting
  - Configuration help
  - Technical questions

- **[AUTOMATION.md](AUTOMATION.md)** - Scheduling and automation
  - Windows Task Scheduler setup
  - PowerShell scripts
  - Daily automation
  - Integration ideas

### Data Management
- **[DATA_GUIDE.md](DATA_GUIDE.md)** - Data templates and expansion
  - Schedule data format
  - Medal data sources
  - Population data sources
  - How to add more data

### Technical Documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and architecture
  - Data flow diagrams
  - Component interactions
  - Module dependencies
  - Extension points

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project status
  - What's implemented
  - File structure
  - Sample outputs
  - Next steps

### Olympics Context
- **[UNDERDOGS_TO_WATCH.md](UNDERDOGS_TO_WATCH.md)** - Notable underdogs
  - Inspiring stories
  - Historic facts
  - Nations by sport
  - Why underdogs matter

## 📁 File Reference

### Configuration Files
- **[config.yaml](config.yaml)** - Main configuration
  - Underdog criteria settings
  - Data file paths
  - Display options
  - Output settings

- **[requirements.txt](requirements.txt)** - Python dependencies
  - pyyaml, pandas, python-dateutil, requests

- **[.gitignore](.gitignore)** - Git ignore rules

### Source Code
All source code is in the `src/` directory:

- **[src/data_loader.py](src/data_loader.py)** - Data loading and parsing
  - Loads schedule, medals, population data
  - Provides data access methods
  - Caches data in memory

- **[src/underdog_checker.py](src/underdog_checker.py)** - Underdog detection
  - Checks if nations meet criteria
  - Returns reasons for underdog status
  - Filters nation lists

- **[src/medals_per_capita.py](src/medals_per_capita.py)** - Per capita calculations
  - Calculates medals per million people
  - Generates ranked leaderboards
  - Formats leaderboard display

- **[src/watchlist_generator.py](src/watchlist_generator.py)** - Watchlist generation
  - Combines all components
  - Formats daily watchlists
  - Saves to markdown files

- **[src/utils.py](src/utils.py)** - Utility functions
  - Config loading
  - Date formatting
  - IOC code mappings
  - Helper functions

- **[main.py](main.py)** - Main application entry point
  - Command-line interface
  - Coordinates all components
  - Handles arguments

### Data Files
All data files are in the `data/` directory:

- **[data/schedule/schedule.json](data/schedule/schedule.json)** - Olympic schedule
  - Events by date
  - Sports and disciplines
  - Competing nations
  - Session times

- **[data/medals/historical_medals.json](data/medals/historical_medals.json)** - Medal counts
  - Historical Olympic medals by nation
  - Gold, silver, bronze, total
  - All-time (Summer + Winter)

- **[data/population/population.json](data/population/population.json)** - Population data
  - Population by nation (IOC code)
  - Current estimates

### Output Files
Generated watchlists are in `outputs/daily_watchlists/`:
- Format: `watchlist_YYYY-MM-DD.md`
- Markdown formatted
- One file per date

## 🎓 Learning Path

### For Users
1. Read [README.md](README.md) for overview
2. Follow [QUICKSTART.md](QUICKSTART.md) to get running
3. Check [FAQ.md](FAQ.md) for common questions
4. Explore [UNDERDOGS_TO_WATCH.md](UNDERDOGS_TO_WATCH.md) for context
5. Set up automation with [AUTOMATION.md](AUTOMATION.md)

### For Data Contributors
1. Start with [DATA_GUIDE.md](DATA_GUIDE.md)
2. Understand the schedule format
3. Find data sources (FIS, IBU, ISU, etc.)
4. Add events to `data/schedule/schedule.json`
5. Update medal and population data as needed

### For Developers
1. Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design
2. Explore source code in `src/`
3. Understand data flow and component interactions
4. Check [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for status
5. Identify extension points for new features

## 🔍 Find Information By Topic

### Installation & Setup
- [QUICKSTART.md](QUICKSTART.md) - Installation steps
- [README.md](README.md) - Requirements
- [requirements.txt](requirements.txt) - Dependencies

### Running the Application
- [QUICKSTART.md](QUICKSTART.md) - Basic commands
- [main.py](main.py) - Command-line options
- [FAQ.md](FAQ.md) - Usage questions

### Configuration
- [config.yaml](config.yaml) - Main config file
- [FAQ.md](FAQ.md) - Configuration questions
- [QUICKSTART.md](QUICKSTART.md) - Customization

### Data Format & Sources
- [DATA_GUIDE.md](DATA_GUIDE.md) - Complete data guide
- [data/schedule/schedule.json](data/schedule/schedule.json) - Schedule format
- [data/medals/historical_medals.json](data/medals/historical_medals.json) - Medal data
- [data/population/population.json](data/population/population.json) - Population data

### Underdog Criteria
- [README.md](README.md) - Criteria explanation
- [config.yaml](config.yaml) - Criteria settings
- [src/underdog_checker.py](src/underdog_checker.py) - Implementation
- [FAQ.md](FAQ.md) - Criteria questions

### Automation & Scheduling
- [AUTOMATION.md](AUTOMATION.md) - Complete automation guide
- Task Scheduler setup
- PowerShell scripts
- Integration ideas

### Medals Per Capita
- [README.md](README.md) - Feature description
- [src/medals_per_capita.py](src/medals_per_capita.py) - Implementation
- [FAQ.md](FAQ.md) - Per capita questions

### Olympics Context
- [UNDERDOGS_TO_WATCH.md](UNDERDOGS_TO_WATCH.md) - Notable underdogs
- [DATA_GUIDE.md](DATA_GUIDE.md) - Sports and events
- [FAQ.md](FAQ.md) - Olympics 2026 specifics

### Technical Details
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Implementation status
- [src/](src/) - Source code documentation

### Troubleshooting
- [FAQ.md](FAQ.md) - Common problems
- [QUICKSTART.md](QUICKSTART.md) - Setup issues
- [AUTOMATION.md](AUTOMATION.md) - Automation problems

## 🎯 Common Tasks

### "I want to..."

#### ...get started quickly
→ Read [QUICKSTART.md](QUICKSTART.md)

#### ...understand what this project does
→ Read [README.md](README.md)

#### ...run the application
→ See [QUICKSTART.md](QUICKSTART.md) Usage section

#### ...add more schedule data
→ See [DATA_GUIDE.md](DATA_GUIDE.md)

#### ...change underdog criteria
→ Edit [config.yaml](config.yaml), see [FAQ.md](FAQ.md)

#### ...automate daily generation
→ Follow [AUTOMATION.md](AUTOMATION.md)

#### ...understand the code
→ Read [ARCHITECTURE.md](ARCHITECTURE.md)

#### ...learn about interesting underdogs
→ Read [UNDERDOGS_TO_WATCH.md](UNDERDOGS_TO_WATCH.md)

#### ...troubleshoot a problem
→ Check [FAQ.md](FAQ.md)

#### ...understand medals per capita
→ See [FAQ.md](FAQ.md) and [src/medals_per_capita.py](src/medals_per_capita.py)

#### ...customize the output
→ Edit [config.yaml](config.yaml), see [FAQ.md](FAQ.md)

#### ...add a new feature
→ Read [ARCHITECTURE.md](ARCHITECTURE.md) Extension Points

## 📚 Complete File List

### Documentation (10 files)
1. README.md - Project overview
2. QUICKSTART.md - Quick start guide  
3. FAQ.md - Frequently asked questions
4. DATA_GUIDE.md - Data expansion guide
5. AUTOMATION.md - Automation guide
6. ARCHITECTURE.md - System architecture
7. PROJECT_SUMMARY.md - Project summary
8. UNDERDOGS_TO_WATCH.md - Notable underdogs
9. INDEX.md - This file
10. .gitignore - Git ignore rules

### Configuration (2 files)
11. config.yaml - Main configuration
12. requirements.txt - Python dependencies

### Source Code (6 files)
13. main.py - Main entry point
14. src/__init__.py - Package init
15. src/data_loader.py - Data loading
16. src/underdog_checker.py - Underdog detection
17. src/medals_per_capita.py - Per capita calculations
18. src/watchlist_generator.py - Watchlist generation
19. src/utils.py - Utility functions

### Data Files (3 files)
20. data/schedule/schedule.json - Olympic schedule
21. data/medals/historical_medals.json - Medal counts
22. data/population/population.json - Population data

### Output Directory
23. outputs/daily_watchlists/ - Generated watchlists

## 🤝 Contributing

Want to help improve the project?

1. **Add Data**: Expand schedule with more events
2. **Update Medals**: Keep medal counts current
3. **Improve Code**: Enhance features or fix bugs
4. **Write Docs**: Improve documentation
5. **Share Stories**: Add underdog narratives

## 📞 Support

Can't find what you need?

1. Check [FAQ.md](FAQ.md) first
2. Review relevant documentation from this index
3. Examine source code comments
4. Check configuration in [config.yaml](config.yaml)

## 🎉 Ready to Start!

Now that you know where everything is, dive in!

**Quick Path**: [README.md](README.md) → [QUICKSTART.md](QUICKSTART.md) → Run the app!

**Olympics 2026**: February 6-22, 2026 in Milano-Cortina, Italy

Let's track those underdogs! 🏅⛷️🛷⛸️
