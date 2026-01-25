# Discipline Schedule Refinement Guide

## Overview

This document defines the process for analyzing all 16 Winter Olympic disciplines, mapping their complete schedules, and refining our underdog watchlists to include specific competition dates for each underdog nation across all events.

**Current Phase**: Documentation & Methodology Definition  
**Next Phase**: Implementation of discipline-specific schedule mapping  
**Target**: Full calendar refinement with granular day-by-day tracking

---

## 1. The 16 Winter Olympic Disciplines

### 2026 Winter Olympics Disciplines

1. **Alpine Skiing** - Downhill, Super-G, Giant Slalom, Slalom, Combined
2. **Biathlon** - Individual, Sprint, Pursuit, Mass Start, Relay, Mixed Relay
3. **Bobsleigh** - 2-man, 4-man, 2-woman, Monobob
4. **Cross-Country Skiing** - Sprints, Distance, Pursuit, Relays, Team Sprints, Skiathlon
5. **Curling** - Men's, Women's, Mixed Doubles
6. **Figure Skating** - Men's Singles, Women's Singles, Pairs, Ice Dance, Team Event
7. **Freestyle Skiing** - Moguls, Aerials, Ski Cross, Half-pipe, Slopestyle, Big Air
8. **Ice Hockey** - Men's, Women's
9. **Luge** - Men's Singles, Women's Singles, Doubles, Team Relay
10. **Nordic Combined** - Individual (Normal/Large Hill), Team, Large Hill
11. **Short Track Speed Skating** - 500m, 1500m, 1000m, Relays, Mass Start
12. **Skeleton** - Men's, Women's
13. **Ski Jumping** - Normal Hill Individual, Normal Hill Team, Large Hill Individual, Large Hill Team, Mixed Team
14. **Snowboard** - Halfpipe, Slopestyle, Cross, Parallel Giant Slalom, Parallel Slalom, Big Air
15. **Speed Skating** - 500m, 1000m, 1500m, 3000m/5000m, Team Pursuit, Mass Start
16. **Ski Mountaineering** - Individual, Team

### Discipline Checklist (medal event counts)

- [ ] Alpine skiing (10)
- [ ] Biathlon (11)
- [ ] Bobsleigh (4)
- [ ] Cross-country skiing (12)
- [ ] Curling (3)
- [ ] Figure skating (5)
- [ ] Freestyle skiing (15)
- [ ] Ice hockey (2)
- [ ] Luge (5)
- [ ] Nordic combined (3)
- [ ] Short-track speed skating (9)
- [ ] Skeleton (3)
- [ ] Ski jumping (6)
- [ ] Ski mountaineering (3)
- [ ] Snowboarding (11)
- [ ] Speed skating (14)

---

## 2. Schedule Categories

Each discipline has multiple events, each with specific competition schedules:

### Schedule Types (what we include)

- **First Competitive Round** - The first official racing/playing round (heats, qualification runs, group openers). **Include.**
- **Early Qualification Heats** - Any initial heat or group-stage session that determines progression. **Include.**

### Exclusions (what we omit)

- **Training** - All practice sessions. **Exclude.**
- **Semifinals and Finals** - We intentionally drop these to focus on first-touch competitions. **Exclude.**

### Schedule Phases by Discipline

For each discipline, map **only first competitive touch points**:
- **First-Round Date(s)** - Earliest heats/qualifiers where underdogs appear
- **Events Included** - Specific events and the round label (e.g., "Heat 1", "Qualification", "Group A opener")
- **Peak Early Days** - Dates with the most first-round underdog participation (helps watchlist focus)

---

## 3. Mapping Framework: Probable vs. Possible

For each underdog nation, we track their competition dates using two categories:

### PROBABLE (High Confidence)

**Criteria (must have at least one):**
- Official quota/entry list shows the nation in that event/discipline
- Discipline where nearly all underdog nations routinely contest at least one first-round event (e.g., broad-participation sports)

**Data Needed**:
- Official Olympic quota/entry lists (preferred)
- Discipline-level participation density ("almost every underdog fields someone")

**Use Case**: High-priority watchlist items focused on first competitive rounds only

### POSSIBLE (Lower Confidence)

**Criteria:**
- No quota/entry list yet; fall back to Beijing 2022 participation for the discipline/event

**Data Needed:**
- Beijing 2022 participation records by discipline/event (per nation)

**Use Case**: Secondary watchlist; flagged until quota lists confirm or deny

---

## 4. Data Structure for Refined Schedules

### Nation Discipline Map

```json
{
  "nation_ioc_code": "LIE",
  "nation_name": "Liechtenstein",
  "disciplines": {
    "Alpine Skiing": {
      "participation": "probable",
      "events": [
        {
          "event_name": "Women's Giant Slalom",
          "round": "Qualification / Run 1",
          "event_type": "first_round",
          "competition_dates": ["2026-02-10"],
          "is_probable": true,
          "notes": "Quota list shows entry"
        }
      ],
      "first_competition": "2026-02-10",
      "last_competition": "2026-02-10",
      "total_events": 1
    },
    "Bobsleigh": {
      "participation": "possible",
      "events": [
        {
          "event_name": "2-man Bobsleigh",
          "round": "Heat 1",
          "event_type": "first_round",
          "competition_dates": ["2026-02-18"],
          "is_probable": false,
          "notes": "Based on Beijing 2022 participation"
        }
      ],
      "first_competition": "2026-02-18",
      "last_competition": "2026-02-18",
      "total_events": 1
    }
  },
  "competing_dates": {
    "probable": ["2026-02-10"],
    "possible": ["2026-02-18"],
    "all": ["2026-02-10", "2026-02-18"]
  }
}
```

---

## 5. Refinement Process Workflow

### Phase 1: Schedule Data Collection
**Objective**: Compile complete schedule for all 16 disciplines

1. **Extract from Official Sources**
   - Olympic.com official schedule
   - Each discipline's governing body schedules
   - Event-specific dates and session times

2. **Create Master Schedule**
   - Discipline → Event → Session → Date/Time
   - Identify all competition dates (Feb 4-22, 2026)
   - Mark medal events vs. qualifiers vs. training

### Phase 2: Nation Participation Mapping
**Objective**: Identify which nations compete in which events

1. **Entry Lists**
   - Obtain official entries from Olympic.com
   - National team rosters
   - Event-specific participant lists

2. **Historical Analysis**
   - Review past Olympic participation (2022, 2018, 2014)
   - Identify consistent competitors vs. occasional participants
   - Note any nations expanding programs

3. **Classification**
   - Mark confirmed entries as "probable"
   - Mark historical patterns without confirmation as "possible"
   - Flag emerging nations with recent improvements

### Phase 3: Underdog Intersection
**Objective**: Cross-reference underdog nations with discipline participation

1. **Filter by Underdog Tier**
   - Apply existing tier system (Tier 1-5)
   - Consider each discipline separately

2. **Create Discipline-Underdog Matrix**
   - Which underdogs compete in each discipline?
   - Which disciplines have the most underdog participation?
   - Identify underdog "concentration dates" (most competition)

3. **Ranking & Priority**
   - Rank by tier (Tier 5 highest priority)
   - Rank by probability (probable > possible)
   - Identify "must-watch" dates with multiple underdogs

### Phase 4: Calendar Generation
**Objective**: Create refined watchlists with specific competition dates

1. **Expanded Watchlist Format**
   - Daily view: All underdogs competing that day, by discipline
   - Discipline view: All underdog nations competing in that sport
   - Nation view: All competition dates for each underdog

2. **Metadata Additions**
   - Session type (training, heats, semis, finals)
   - Event number of competition (helpful for streaming/broadcast times)
   - Probability indicator (probable vs. possible)
   - Underdog tier (for priority)

3. **Calendar Outputs**
   - Daily watchlists (existing format, enhanced)
   - Discipline-based schedules
   - Nation-focused calendars
   - "Peak underdog days" highlights

---

## 6. Key Definitions

### Discipline
A major Olympic sport category with multiple events (e.g., "Alpine Skiing" includes Downhill, Slalom, etc.)

### Event
A specific competition within a discipline (e.g., "Women's Downhill" within Alpine Skiing)

### Session
A specific instance of an event on a particular date/time (e.g., "Women's Downhill - Heat 1 - Feb 10, 10:00 AM")

### Probable Participation
Confirmed or very highly likely based on official entries and historical patterns. Source: Official Olympic entries or near-certain qualification.

### Possible Participation
Plausible based on historical participation but not yet confirmed. Source: Historical patterns or emerging trends.

### Underdog Tier
Classification based on meeting 1-7 underdogs criteria:
- **Tier 5** (6-7 criteria): Ultimate Underdogs 🔴
- **Tier 4** (4-5 criteria): Major Underdogs 🟠
- **Tier 3** (3 criteria): Strong Underdogs 🟡
- **Tier 2** (2 criteria): Moderate Underdogs 🟨
- **Tier 1** (1 criterion): Mild Underdogs 🔵

---

## 7. Implementation Roadmap

### Step 1: Master Schedule Compilation
- [ ] Extract all 16 discipline schedules
- [ ] Normalize date formats and times
- [ ] Create `data/schedules/disciplines/` folder structure
- [ ] One JSON file per discipline with all events and dates

### Step 2: Entry List Processing
- [ ] Gather official 2026 Olympic entry lists
- [ ] Create `data/entries/` folder with nation-event mappings
- [ ] Classify entries as probable/possible

### Step 3: Intersection Analysis
- [ ] Cross-reference underdogs with all discipline entries
- [ ] Create nation-discipline-event mapping
- [ ] Tag all competition dates for each underdog

### Step 4: Watchlist Generation
- [ ] Enhance `watchlist_generator.py` to use discipline data
- [ ] Create multiple output formats:
  - Daily watchlists (existing, enhanced)
  - Discipline calendars
  - Nation-specific calendars
  - Multi-discipline underdog events

### Step 5: Visualization & Exploration
- [ ] Update HTML interface with new data
- [ ] Add interactive discipline filters
- [ ] Show underdog "hotspots" (days with most competition)
- [ ] Enable nation-specific calendar views

---

## 8. Data Quality Considerations

### Validation Checks

- **Completeness**: All 16 disciplines represented
- **Consistency**: Date formats standardized
- **Accuracy**: Cross-reference multiple Olympic sources
- **Timeliness**: Update as new entries confirmed (through Feb 5, 2026)

### Uncertainty Handling

For nations where participation is uncertain:
1. Include in "possible" category initially
2. Update to "probable" as confirmations arrive
3. Track confidence level: High (>95%), Medium (50-95%), Low (<50%)
4. Document reason for uncertainty

---

## 9. Success Criteria

This refinement is complete when:

✅ All 16 disciplines have complete schedule data  
✅ All underdog nations mapped to their competition dates  
✅ Probability classifications (probable/possible) applied  
✅ Multiple output formats available (daily, discipline, nation)  
✅ Watchlists can be filtered by underdog tier, discipline, and probability  
✅ Clear documentation of data sources and confidence levels  

---

## 10. Resources & References

### Official Olympic Sources
- [Olympic.com - 2026 Winter Olympics Schedule](https://olympics.com)
- Individual discipline federation websites
- National Olympic Committee entry submissions

### Data Files to Create/Update
- `data/schedules/disciplines/` - All schedule files
- `data/entries/` - Nation-event participation
- `src/discipline_analyzer.py` - New analysis module
- `src/schedule_mapper.py` - Schedule processing module
- Updated `watchlist_generator.py` with new features

### Output Files
- `outputs/discipline_calendars/` - Discipline-specific schedules
- `outputs/nation_calendars/` - Nation-specific calendars
- Enhanced `outputs/daily_watchlists/` with new data

---

## Notes

This document serves as the foundation for precise, granular tracking of underdog competition schedules. By clearly defining "probable" vs. "possible" and organizing around all 16 disciplines, we create a comprehensive resource for following underdog nations throughout the 2026 Winter Olympics.
