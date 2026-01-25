# 2026 Winter Olympics - Preliminary Round Schedule by Discipline

## Overview

This document maps the first competitive rounds (qualifications, preliminary heats, group stages) for each Olympic discipline during the 2026 Winter Olympics (Feb 4-22, 2026), and now also tracks finals/playoff rounds plus the primary broadcast network(s) for live coverage. Replays are excluded; live-only. Training is excluded.

### Broadcast + Finals Tracking Rules
- Capture **network(s)** per event when available in the TV schedule (NBC, USA Network, CNBC, Peacock). If unknown, mark **Network: TBD**.
- Keep **is_replay: false** (replays ignored).
- Add **finals/playoffs** even if underdog participation is unconfirmed; they may advance.
- Times are EST as provided in the TV schedule CSV; refine with official schedule as needed.

### Data model (per event instance)
```json
{
	"date": "2026-02-07",
	"time_est": "05:30",
	"round": "Qualification" or "Final" or "Group Play",
	"stage": "prelim" | "final" | "playoff",
	"network": ["USA Network", "Peacock"],
	"is_replay": false
}
```

---

## Skeleton (3 medal events)

### Men's Skeleton
- **Heat 1**: February 12 (3:30 AM EST) — Network: TBD (live)
- **Heat 2**: February 12 (5:08 AM EST) — Network: TBD (live)
- **Heat 3**: February 13 (1:30 PM EST) — Network: TBD (live)
- **Heat 4 / Final Classification**: February 13 (3:05 PM EST) — Network: TBD (live)

### Women's Skeleton
- **Heat 1**: February 13 (10:00 AM EST) — Network: TBD (live)
- **Heat 2**: February 13 (11:48 AM EST) — Network: TBD (live)
- **Heat 3**: February 14 (12:00 PM EST) — Network: TBD (live)
- **Heat 4 / Final Classification**: February 14 (1:44 PM EST) — Network: TBD (live)

### Mixed Team Skeleton
- **Final**: February 15 (12:00 PM EST) — Network: TBD (live)

**Underdog Nations (qualified quota)**: Brazil, Denmark, Estonia, Israel, Puerto Rico, South Africa

---

## Curling (3 medal events)

### Mixed Doubles
- **Preliminary Round**: February 4-17 (Round-robin group play) — Networks: Peacock; USA Network on select matchups (live)
- **First Session**: February 4, 1:05 AM EST (multiple matches) — Network: Peacock (live)
- **Last Preliminary**: February 17 — Network: TBD (live)
- **Playoffs / Medal Round**: February 18-20 — Networks: TBD (live)

### Men's & Women's
- **Group Play**: February 9-20 (Round-robin format) — Networks: Peacock; USA/NBC for feature draws (live)
- **Playoffs / Medal Round**: February 20-22 — Networks: TBD (live)

**Underdog Nations**: Limited - most underdogs don't field curling teams

---

## Nordic Combined (3 medal events)

### Individual (Normal Hill)
- **Ski Jumping Qualification**: February 11 (~4:00 AM EST) — Network: TBD (live)
- **Cross-Country 10km**: February 11 (~6:00 AM EST) — Network: TBD (live)
- **Final Classification**: February 11 (later session) — Network: TBD (live)

### Individual (Large Hill)
- **Ski Jumping Qualification**: February 15 (~4:00 AM EST) — Network: TBD (live)
- **Cross-Country 10km**: February 15 (~6:00 AM EST) — Network: TBD (live)
- **Final Classification**: February 15 (later session) — Network: TBD (live)

### Team
- **Ski Jumping Qualification**: February 18 (~4:00 AM EST) — Network: TBD (live)
- **Cross-Country Relay**: February 18 (~6:00 AM EST) — Network: TBD (live)
- **Final Classification**: February 18 (later session) — Network: TBD (live)

**Underdog Nations**: Limited - very niche sport

---

## Figure Skating (5 medal events)

### Men's Singles
- **Short Program**: February 10 (~5:30 AM EST) — Networks: TBD (live; likely USA/Peacock)
- **Free Skate / Final**: February 12 (~TBD) — Networks: TBD (live)

### Women's Singles
- **Short Program**: February 12 (~5:30 AM EST) — Networks: TBD (live; likely USA/Peacock)
- **Free Skate / Final**: February 14 (~TBD) — Networks: TBD (live)

### Pairs
- **Short Program**: February 14 (~5:30 AM EST) — Networks: TBD (live; likely USA/Peacock)
- **Free Skate / Final**: February 16 (~TBD) — Networks: TBD (live)

### Ice Dance
- **Rhythm Dance**: February 9 (~3:55 AM EST) — Networks: USA Network, Peacock (live)
- **Free Dance / Final**: February 10 (~TBD) — Networks: TBD (live)

### Team Event
- **Rhythm Dance**: February 6 (~3:55 AM EST) — Networks: USA Network, Peacock (live)
- **Pairs Short Program**: February 6 (~5:35 AM EST) — Networks: USA Network, Peacock (live)
- **Women's Short Program**: February 6 (~7:35 AM EST) — Networks: USA Network, Peacock (live)
- **Men's Short Program**: February 7 (~1:45 PM EST) — Networks: NBC, Peacock (live)
- **Pairs Free Skate**: February 8 (~1:30 PM EST) — Networks: USA Network, Peacock (live)
- **Women's Free Skate**: February 8 (~2:45 PM EST) — Networks: USA Network, Peacock (live)
- **Men's Free Skate**: February 8 (~3:55 PM EST) — Networks: USA Network, Peacock (live)

**Underdog Nations**: Some European underdogs (Ukraine, Lithuania) may have entries

---

## Luge (5 medal events)

### Men's Singles
- **Run 1**: February 6 (~11:00 AM EST) — Networks: Peacock (live); NBC for highlights
- **Run 2**: February 6 (~12:45 PM EST) — Networks: NBC, Peacock (live)
- **Runs 3 & 4 / Final Classification**: February 8 (~11:00 AM EST) — Networks: USA Network, Peacock (live)

### Women's Singles
- **Run 1**: February 8 (~3:00 AM EST) — Network: USA Network, Peacock (live)
- **Run 2**: February 8 (~5:30 AM EST) — Network: USA Network, Peacock (live)
- **Runs 3 & 4 / Final Classification**: February 8 (~11:45 AM EST) — Networks: NBC (live), Peacock

### Doubles
- **Run 1**: February 11 (~4:00 AM EST) — Network: Peacock (live)
- **Run 2**: February 11 (~5:30 AM EST) — Network: Peacock (live)
- **Runs 3 & 4 / Final Classification**: February 11 (~TBD) — Network: TBD (live)

### Team Relay
- **Run 1 / Final**: February 15 (~4:00 AM EST) — Network: TBD (live)

**Underdog Nations**: Limited - few underdogs field luge teams

---

## Ski Jumping (6 medal events)

### Women's Normal Hill
- **Qualification**: February 6 (~12:45 PM EST) — Networks: Peacock (live)
- **Final**: February 6 (~later session) — Networks: Peacock (live)

### Men's Normal Hill
- **Qualification**: February 8 (~4:00 AM EST) — Networks: Peacock (live)
- **Final**: February 8 (~later session) — Networks: Peacock (live)

### Women's Large Hill
- **Qualification**: February 10 (~4:00 AM EST) — Networks: Peacock (live)
- **Final**: February 10 (~later session) — Networks: TBD (live)

### Men's Large Hill
- **Qualification**: February 12 (~4:00 AM EST) — Networks: Peacock (live)
- **Final**: February 12 (~later session) — Networks: TBD (live)

### Mixed Team
- **Qualification**: February 14 (~4:00 AM EST) — Networks: Peacock (live)
- **Final**: February 14 (~later session) — Networks: TBD (live)

**Underdog Nations**: Limited - most underdogs don't field jumping teams

---

## Short-Track Speed Skating (9 medal events)

### Men's 500m
- **Heats**: February 9 (~11:00 AM EST) — Networks: TBD (live)
- **Final**: February 9 (~later session) — Networks: TBD (live)

### Women's 500m
- **Heats**: February 10 (~11:00 AM EST) — Networks: TBD (live)
- **Final**: February 10 (~later session) — Networks: TBD (live)

### Men's 1000m
- **Heats**: February 11 (~11:00 AM EST) — Networks: TBD (live)
- **Final**: February 11 (~later session) — Networks: TBD (live)

### Women's 1000m
- **Heats**: February 12 (~11:00 AM EST) — Networks: TBD (live)
- **Final**: February 12 (~later session) — Networks: TBD (live)

### Men's 1500m
- **Heats**: February 13 (~11:00 AM EST) — Networks: TBD (live)
- **Final**: February 13 (~later session) — Networks: TBD (live)

### Women's 1500m
- **Heats**: February 14 (~11:00 AM EST) — Networks: TBD (live)
- **Final**: February 14 (~later session) — Networks: TBD (live)

### Men's 3000m Relay
- **Heats**: February 16 (~11:00 AM EST) — Networks: TBD (live)
- **Final**: February 16 (~later session) — Networks: TBD (live)

### Women's 3000m Relay
- **Heats**: February 17 (~11:00 AM EST) — Networks: TBD (live)
- **Final**: February 17 (~later session) — Networks: TBD (live)

### Mass Start
- **Heats**: February 18 (~11:00 AM EST) — Networks: TBD (live)
- **Final**: February 18 (~later session) — Networks: TBD (live)

**Underdog Nations**: Check entries for Eastern European nations

**Broadcast/Finals Note**: Networks largely TBD; expect Peacock primary with USA/NBC for marquee finals. Live-only; no replays.

---

## Ski Mountaineering (3 medal events)

### Individual
- **First Day Race**: February 12 (~TBD - early morning)

### Team
- **First Day Race**: February 14 (~TBD - early morning)

**Underdog Nations**: Limited - very emerging discipline

**Broadcast/Finals Note**: Networks TBD (expect Peacock). Medal races to be added once official times are confirmed. Live-only; no replays.

---

## Speed Skating (14 medal events)

### Women's 500m
- **Heats/Preliminary/Final**: February 8 (~TBD) — Networks: TBD (live)

### Men's 500m
- **Heats/Preliminary/Final**: February 9 (~TBD) — Networks: TBD (live)

### Women's 3000m
- **Heats/Preliminary/Final**: February 6 (~10:00 AM EST) — Networks: NBC, Peacock (live)

### Men's 5000m
- **Heats/Preliminary/Final**: February 7 (~10:00 AM EST) — Networks: NBC, Peacock (live)

### Women's 1500m
- **Heats/Preliminary/Final**: February 10 (~TBD) — Networks: TBD (live)

### Men's 1500m
- **Heats/Preliminary/Final**: February 11 (~TBD) — Networks: TBD (live)

### Women's 1000m
- **Heats/Preliminary/Final**: February 12 (~TBD) — Networks: TBD (live)

### Men's 1000m
- **Heats/Preliminary/Final**: February 13 (~TBD) — Networks: TBD (live)

### Team Pursuit (Women's)
- **Heats/Preliminary/Final**: February 15 (~TBD) — Networks: TBD (live)

### Team Pursuit (Men's)
- **Heats/Preliminary/Final**: February 16 (~TBD) — Networks: TBD (live)

### Mass Start (Women's)
- **Heats/Preliminary/Final**: February 19 (~TBD) — Networks: TBD (live)

### Mass Start (Men's)
- **Heats/Preliminary/Final**: February 20 (~TBD) — Networks: TBD (live)

**Underdog Nations**: Check for emerging Eastern European entries

---

## Snowboarding (11 medal events)

### Men's Big Air
- **Qualification**: February 4 (~1:30 PM EST) — Networks: USA Network, Peacock (live)
- **Final**: February 7 (~1:30 PM EST) — Networks: USA Network, Peacock (live)

### Women's Big Air
- **Qualification**: February 8 (~1:30 PM EST) — Networks: Peacock (live)
- **Final**: February 8 (~7:30 AM EST) — Networks: NBC/Peacock (live) (time approximate)

### Men's Slopestyle
- **Qualification**: February 9 (~TBD) — Networks: TBD (live); early runs often on NBC/Peacock
- **Final**: February 10 (~TBD) — Networks: TBD (live)

### Women's Slopestyle
- **Qualification**: February 7 (~4:30 AM EST) — Networks: USA Network, Peacock (live)
- **Final**: February 8 (~TBD) — Networks: TBD (live)

### Men's Halfpipe
- **Qualification**: February 11 (~TBD) — Networks: TBD (live)
- **Final**: February 13 (~TBD) — Networks: TBD (live)

### Women's Halfpipe
- **Qualification**: February 12 (~TBD) — Networks: TBD (live)
- **Final**: February 14 (~TBD) — Networks: TBD (live)

### Men's Parallel Giant Slalom
- **Qualification**: February 8 (~3:00 AM EST) — Networks: USA Network, Peacock (live)
- **Final**: February 8 (~7:30 AM EST) — Networks: NBC, Peacock (live)

### Women's Parallel Giant Slalom
- **Qualification**: February 8 (~3:00 AM EST) — Networks: USA Network, Peacock (live)
- **Final**: February 8 (~7:30 AM EST) — Networks: NBC, Peacock (live)

### Men's Parallel Slalom
- **Qualification**: February 14 (~TBD) — Networks: TBD (live)
- **Final**: February 14 (~TBD) — Networks: TBD (live)

### Women's Parallel Slalom
- **Qualification**: February 15 (~TBD) — Networks: TBD (live)
- **Final**: February 15 (~TBD) — Networks: TBD (live)

**Underdog Nations**: Some nations may enter in halfpipe/slopestyle

---

## Freestyle Skiing (15 medal events)

### Women's Slopestyle
- **Qualification**: February 7 (~4:30 AM EST) — Networks: USA Network, Peacock (live)
- **Final**: February 8 (~TBD) — Networks: TBD (live)

### Men's Slopestyle
- **Qualification**: February 7 (~8:00 AM EST) — Networks: NBC, Peacock (live)
- **Final**: February 8 (~TBD) — Networks: TBD (live)

### Women's Big Air
- **Qualification**: February 11 (~TBD) — Networks: TBD (live)
- **Final**: February 12 (~TBD) — Networks: TBD (live)

### Men's Big Air
- **Qualification**: February 12 (~TBD) — Networks: TBD (live)
- **Final**: February 13 (~TBD) — Networks: TBD (live)

### Women's Halfpipe
- **Qualification**: February 13 (~TBD) — Networks: TBD (live)
- **Final**: February 14 (~TBD) — Networks: TBD (live)

### Men's Halfpipe
- **Qualification**: February 14 (~TBD) — Networks: TBD (live)
- **Final**: February 15 (~TBD) — Networks: TBD (live)

### Women's Moguls
- **Qualification**: February 16 (~TBD) — Networks: TBD (live)
- **Final**: February 16 (~TBD) — Networks: TBD (live)

### Men's Moguls
- **Qualification**: February 17 (~TBD) — Networks: TBD (live)
- **Final**: February 17 (~TBD) — Networks: TBD (live)

### Women's Ski Cross
- **Qualification**: February 19 (~TBD) — Networks: TBD (live)
- **Final**: February 19 (~TBD) — Networks: TBD (live)

### Men's Ski Cross
- **Qualification**: February 20 (~TBD) — Networks: TBD (live)
- **Final**: February 20 (~TBD) — Networks: TBD (live)

### Mixed Team Aerials
- **Qualification**: TBD — Networks: TBD (live)
- **Final**: TBD — Networks: TBD (live)

### Women's Aerials
- **Qualification**: February 18 (~TBD) — Networks: TBD (live)
- **Final**: February 18 (~TBD) — Networks: TBD (live)

### Men's Aerials
- **Qualification**: February 19 (~TBD) — Networks: TBD (live)
- **Final**: February 19 (~TBD) — Networks: TBD (live)

**Underdog Nations**: Check for entries in moguls, slopestyle

---

## Ice Hockey (2 medal events)

### Women's Tournament
- **Group Play Begins**: February 4 (Multiple preliminary matches) — Networks: Peacock primary; USA/NBC for feature games (live)
- **First Underdog Match**: Check entries — Network: TBD (live)
- **Quarterfinals/Semis/Final**: February 17-22 — Networks: NBC/USA/Peacock (live)

### Men's Tournament
- **Group Play Begins**: February 9 (Multiple preliminary matches) — Networks: Peacock primary; USA/NBC for feature games (live)
- **First Underdog Match**: Check entries — Network: TBD (live)
- **Quarterfinals/Semis/Final**: February 19-22 — Networks: NBC/USA/Peacock (live)

**Underdog Nations**: Some nations (Kazakhstan, Belarus) field teams

---

## Alpine Skiing (10 medal events)

### Women's Downhill
- **Race (Medal)**: February 8 (~5:30 AM EST) — Networks: USA Network, Peacock (live)

### Men's Downhill
- **Race (Medal)**: February 7 (~5:30 AM EST) — Networks: USA Network, Peacock (live)

### Women's Super-G
- **Race (Medal)**: February 9 (~5:30 AM EST) — Networks: USA Network, Peacock (live)

### Men's Super-G
- **Race (Medal)**: February 10 (~5:30 AM EST) — Networks: USA Network, Peacock (live)

### Women's Giant Slalom
- **Run 1**: February 11 (~5:30 AM EST) — Networks: TBD (live)
- **Run 2 / Medal**: February 11 (~TBD) — Networks: TBD (live)

### Men's Giant Slalom
- **Run 1**: February 12 (~5:30 AM EST) — Networks: TBD (live)
- **Run 2 / Medal**: February 12 (~TBD) — Networks: TBD (live)

### Women's Slalom
- **Run 1**: February 16 (~5:30 AM EST) — Networks: TBD (live)
- **Run 2 / Medal**: February 16 (~TBD) — Networks: TBD (live)

### Men's Slalom
- **Run 1**: February 17 (~5:30 AM EST) — Networks: TBD (live)
- **Run 2 / Medal**: February 17 (~TBD) — Networks: TBD (live)

### Team Event
- **Competition / Medal**: February 19 (~TBD) — Networks: TBD (live)

### Mixed Team Parallel
- **Competition / Medal**: February 22 (~TBD) — Networks: TBD (live)

**Underdog Nations**: Liechtenstein, possibly others - HIGH PRIORITY

---

## Biathlon (11 medal events)

### Women's Sprint 7.5km
- **Race (Medal)**: February 9 (~TBD) — Networks: TBD (live)

### Men's Sprint 10km
- **Race (Medal)**: February 10 (~TBD) — Networks: TBD (live)

### Women's Pursuit 10km
- **Race (Medal)**: February 12 (~TBD) — Networks: TBD (live)

### Men's Pursuit 12.5km
- **Race (Medal)**: February 13 (~TBD) — Networks: TBD (live)

### Women's Individual 15km
- **Race (Medal)**: February 15 (~TBD) — Networks: TBD (live)

### Men's Individual 20km
- **Race (Medal)**: February 16 (~TBD) — Networks: TBD (live)

### Women's Mass Start 12.5km
- **Race (Medal)**: February 18 (~TBD) — Networks: TBD (live)

### Men's Mass Start 15km
- **Race (Medal)**: February 19 (~TBD) — Networks: TBD (live)

### Mixed Relay 4x6km
- **Race (Medal)**: February 8 (~8:05 AM EST) — Networks: Peacock (live), NBC (live at ~8:45 AM)

### Women's Relay 4x6km
- **Race (Medal)**: February 20 (~TBD) — Networks: TBD (live)

### Men's Relay 4x6km
- **Race (Medal)**: February 21 (~TBD) — Networks: TBD (live)

**Underdog Nations**: Check entries for Eastern European/Asian nations - HIGH PRIORITY

---

## Cross-Country Skiing (12 medal events)

### Women's 10km Skiathlon
- **Race (Medal)**: February 7 (~7:00 AM EST) — Networks: NBC, Peacock (live) — *First event!*

### Men's 10km Skiathlon
- **Race (Medal)**: February 8 (~6:45 AM EST) — Networks: USA Network, Peacock (live)

### Women's Sprint 5km (Classic)
- **Race (Medal)**: February 9 (~TBD) — Networks: TBD (live)

### Men's Sprint 5km (Classic)
- **Race (Medal)**: February 10 (~TBD) — Networks: TBD (live)

### Women's 10km (Freestyle)
- **Race (Medal)**: February 12 (~TBD) — Networks: TBD (live)

### Men's 15km (Freestyle)
- **Race (Medal)**: February 13 (~TBD) — Networks: TBD (live)

### Women's Pursuit 10km
- **Race (Medal)**: February 15 (~TBD) — Networks: TBD (live)

### Men's Pursuit 15km
- **Race (Medal)**: February 16 (~TBD) — Networks: TBD (live)

### Women's Team Sprint 2x3km
- **Race (Medal)**: February 18 (~TBD) — Networks: TBD (live)

### Men's Team Sprint 2x3km
- **Race (Medal)**: February 19 (~TBD) — Networks: TBD (live)

### Women's Relay 4x5km
- **Race (Medal)**: February 21 (~TBD) — Networks: TBD (live)

### Men's Relay 4x5km
- **Race (Medal)**: February 22 (~TBD) — Networks: TBD (live)

**Underdog Nations**: Many nations participate in XC - HIGH PRIORITY

---

## Notes & Data Quality

### TBD Times
Several disciplines have "TBD" times because:
- The TV schedule CSV only covers broadcasts, not all session times
- Need to cross-reference with official Olympic.com detailed schedule
- Times in EST (Eastern Standard Time)

### Preliminary Round Definition Varies by Discipline
- **Alpine/Freestyle**: First run of multi-run events
- **Biathlon/XC/Speed Skating**: First heat or individual race
- **Figure Skating**: Short program (comes before free skate)
- **Curling/Ice Hockey**: Group play/preliminary round (first matches)
- **Jumping/Skeleton**: Qualification round

### Next Steps
1. Verify all preliminary round times against official Olympic schedule
2. Extract nationality/team entries from official qualification lists
3. Cross-reference with Beijing 2022 for disciplines lacking 2026 confirmations
4. Mark which preliminary rounds have confirmed underdog nation participants
