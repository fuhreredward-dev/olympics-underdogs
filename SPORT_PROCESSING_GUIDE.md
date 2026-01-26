# Sport Data Processing Guide

## Overview
This guide documents the standardized process for adding underdog-specific data to Olympic sports. This ensures that daily watchlists show only the specific events where underdog nations are competing, not all events in a sport.

## Process Summary

### 1. Research & Data Collection
- **Source**: Wikipedia official Olympic pages for the sport
- **Example**: [Skeleton at 2026 Winter Olympics – Qualification](https://en.wikipedia.org/wiki/Skeleton_at_the_2026_Winter_Olympics_%E2%80%93_Qualification)
- **Target**: Quota allocation or participant list showing which countries have athletes in the sport

### 2. Identify Underdog Nations
From the qualification/participation data, identify which underdog nations have competitors:
- Check each event's participant table
- List all underdog nations that appear
- Map which specific events each underdog is competing in

**Example (Skeleton)**:
- Men's events: Denmark (1 athlete), Israel (1 athlete)
- Women's events: Brazil, Denmark, Puerto Rico, South Africa (1 athlete each)
- Mixed Team: Denmark

### 3. Update Schedule Data
Update `data/schedules/ioc_schedule_all_events.json` with `underdog_nations` field for each event:

```json
{
  "date": "2026-02-12",
  "event": "Men's Heat 1",
  "underdog_nations": ["DEN", "ISR"]
},
{
  "date": "2026-02-13", 
  "event": "Women's Heat 1",
  "underdog_nations": ["BRA", "DEN", "EST", "PUR", "RSA"]
}
```

This allows tracking which nations are actually competing in each specific event (vs all nations in the sport).

### 4. Update Website Display
Add skeleton-specific date ranges to each underdog nation's profile card in `index.html`:

- **Field**: `competing-days` section
- **Format**: Append event-specific dates to overall competing dates
- **Example**: `"📅 Competing: 18 days (Feb 04 - Feb 22); Skeleton: Feb 13-14"`

Also update `sports-list` to include the sport tag if missing:
```html
<span class="sport-tag">Skeleton</span>
```

**Nations Updated**:
- South Africa: Added Skeleton date range and tag
- Brazil: Added Skeleton date range (tag already present)
- Israel: Added Skeleton date range (tag already present)
- Denmark: Added Skeleton date range (tag already present)
- Puerto Rico: New nation card added with Skeleton tag and date range

### 5. Fix Watchlist Generation ✓ (Completed)
The watchlist generator has been updated to respect the `underdog_nations` field:

**Changes Made**:
- Updated `_format_by_sport()` to use `underdog_nations` field when available, falling back to `nations`
- Updated `_format_chronologically()` to use `underdog_nations` field when available
- This ensures daily watchlists show only the specific events where each underdog is competing
- Updated `data/schedule/schedule.json` to include all 9 skeleton events with `underdog_nations` arrays

**Implementation**:
```python
# Check if nation is in underdog_nations (preferred) or nations field
competing_nations = event.get('underdog_nations', event.get('nations', []))
if nation in competing_nations:
    nation_events.append(e)
```

**Backward Compatibility**: This approach is backward-compatible - sports without `underdog_nations` field will continue to use the `nations` field.

**Updated Files**:
- `src/watchlist_generator.py` - Updated event filtering logic
- `data/schedule/schedule.json` - Added all 9 skeleton events with underdog_nations field

### 6. Verification
- Confirm daily watchlists show skeleton events only for nations competing in those specific events
- Verify website displays correct date ranges for each nation's skeleton participation
- Check that all underdog nations with skeleton athletes are represented

## Data Files Reference

### Primary Sources
- `data/schedules/ioc_schedule_all_events.json` - Master schedule with all events and underdog_nations arrays
- `data/schedule/schedule.json` - Current watchlist schedule (needs update to filter by underdogs)
- `index.html` - Website nation profiles with competing-days and sport tags

### Scripts
- `src/watchlist_generator.py` - Generates daily watchlists from schedule data
- `src/data_loader.py` - Loads and parses schedule data

## Next Sports to Process
Remaining 11 sports following this process:
1. Alpine Skiing
2. Biathlon
3. Bobsleigh
4. Cross-Country Skiing
5. Curling
6. Figure Skating
7. Freestyle Skiing
8. Ice Hockey
9. Luge
10. Nordic Combined
11. Short Track

## Completed Sports
✓ **Skeleton** (3 underdogs: Brazil, Denmark, Israel)
✓ **Ski Jumping** (1 underdog: Turkey)
✓ **Ski Mountaineering** (1 underdog: Australia)
✓ **Speed Skating** (4 underdogs: Chinese Taipei, Denmark, Estonia, Portugal)
✓ **Snowboard** (2 underdogs: Australia, Brazil)
