# Quick Reference: Adding Event Mappings

## Basic Syntax

```python
mapper.add_event_mapping(
    discipline="Sport Name",           # Official discipline name
    event="Event Name",                # Specific event (e.g., "Men's 500m")
    date="YYYY-MM-DD",                 # ISO format date
    underdog_nations=["IOC", "CODES"], # List of 3-letter IOC codes
    stage="Stage Name"                 # Optional: "Final", "Heat 1", "Qualification"
)
```

## Common Patterns

### Single Event, Multiple Underdogs
```python
mapper.add_event_mapping(
    discipline="Speed Skating",
    event="Women's 500m",
    date="2026-02-15",
    underdog_nations=["TPE", "DEN", "POR"],
    stage="Final"
)
```

### Multiple Heats, Same Underdogs
```python
# Heat 1
mapper.add_event_mapping(
    discipline="Skeleton",
    event="Men's Skeleton",
    date="2026-02-12",
    underdog_nations=["DEN", "ISR"],
    stage="Heat 1"
)

# Heat 2 (same day, same competitors)
mapper.add_event_mapping(
    discipline="Skeleton",
    event="Men's Skeleton",
    date="2026-02-12",
    underdog_nations=["DEN", "ISR"],
    stage="Heat 2"
)
```

### Qualification + Final
```python
# Qualification round
mapper.add_event_mapping(
    discipline="Ski Jumping",
    event="Men's Individual Normal Hill",
    date="2026-02-08",
    underdog_nations=["TUR"],
    stage="Qualification"
)

# Final (only if qualified)
mapper.add_event_mapping(
    discipline="Ski Jumping",
    event="Men's Individual Normal Hill",
    date="2026-02-09",
    underdog_nations=["TUR"],  # Only add if athlete qualifies
    stage="Final"
)
```

### Multi-Day Events
```python
# Day 1
mapper.add_event_mapping(
    discipline="Alpine Skiing",
    event="Men's Downhill",
    date="2026-02-09",
    underdog_nations=["ALB", "CYP", "IND"],
    stage="Training Run 1"
)

# Day 2
mapper.add_event_mapping(
    discipline="Alpine Skiing",
    event="Men's Downhill",
    date="2026-02-10",
    underdog_nations=["ALB", "CYP", "IND"],
    stage="Final"
)
```

### Team Events
```python
mapper.add_event_mapping(
    discipline="Skeleton",
    event="Mixed Team Skeleton",
    date="2026-02-15",
    underdog_nations=["DEN"],  # Only nations with qualified teams
    stage="Final"
)
```

## IOC Codes Reference

### All 56 Underdog Nations
```
ALB - Albania          IRI - Iran             MNE - Montenegro
AND - Andorra          IRL - Ireland          MON - Monaco
ARG - Argentina        ISL - Iceland          NGR - Nigeria
ARM - Armenia          ISR - Israel           NZL - New Zealand
AUS - Australia        JAM - Jamaica          PAK - Pakistan
AZE - Azerbaijan       KEN - Kenya            PHI - Philippines
BIH - Bosnia & Herz    KGZ - Kyrgyzstan       POR - Portugal
BRA - Brazil           KOS - Kosovo           ROM - Romania
CHI - Chile            KSA - Saudi Arabia     RSA - South Africa
COL - Colombia         LIB - Lebanon          SGP - Singapore
CYP - Cyprus           LIE - Liechtenstein    SMR - San Marino
DEN - Denmark          LTU - Lithuania        SRB - Serbia
ECU - Ecuador          LUX - Luxembourg       THA - Thailand
GEO - Georgia          MAR - Morocco          TPE - Chinese Taipei
GRE - Greece           MAS - Malaysia         TTO - Trinidad & Tobago
HKG - Hong Kong        MDA - Moldova          TUR - Turkey
IND - India            MEX - Mexico           UAE - United Arab Emirates
                       MGL - Mongolia         URU - Uruguay
                       MKD - North Macedonia  VEN - Venezuela
                       MLT - Malta
```

## Finding Event Dates

### Method 1: IOC Schedule
Check `data/schedules/ioc_schedule_authoritative.json`:
```json
{
  "discipline": "Skeleton",
  "event": "Men's Skeleton",
  "instances": [
    {
      "date": "2026-02-12",
      "time_est": "03:30",
      "round": "Heat 1"
    }
  ]
}
```

### Method 2: Wikipedia
Search: `"[Sport] at 2026 Winter Olympics"` → Click "Schedule" section

### Method 3: Olympics.com
Visit: https://olympics.com/en/olympic-games/milano-cortina-2026/schedule

## Tips

### ✅ Do's
- Always use ISO date format (YYYY-MM-DD)
- Use official IOC 3-letter codes
- Include stage information for clarity
- Add comments explaining athlete counts
- Verify nation actually qualified

### ❌ Don'ts
- Don't guess dates - verify from schedule
- Don't add nations without qualification proof
- Don't use full country names
- Don't skip optional stage parameter (helps debugging)
- Don't forget to run script after editing

## Validation

The system automatically:
- ✅ Filters out non-underdog nations
- ✅ Validates nation codes against official list
- ✅ Groups events by discipline
- ✅ Counts unique nations per event
- ✅ Tracks competition dates

## Example Workflow

1. **Research**: Find qualification page on Wikipedia
2. **Identify**: Note which underdogs qualified
3. **Schedule**: Find event dates in IOC schedule
4. **Add**: Edit populate_event_mappings.py
5. **Run**: `python scripts/populate_event_mappings.py`
6. **Verify**: Check discipline summary in output

## Testing Your Mappings

After running the script, check output shows:
```
Adding [Your Sport] mappings...
✓ Added X [Sport] event mappings

[Sport]:
  Event instances: X
  Competition dates: YYYY-MM-DD, YYYY-MM-DD
  Underdog nations (X): CODE1, CODE2, CODE3
```

## Need Help?

See complete documentation: [docs/SCHEDULE_REFINEMENT_SYSTEM.md](SCHEDULE_REFINEMENT_SYSTEM.md)
