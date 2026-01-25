# Automation Guide

## Running Daily Watchlist Updates

### Option 1: Windows Task Scheduler

1. **Create a batch file** (`run_daily_watchlist.bat`):
```batch
@echo off
cd /d "c:\Users\emf48\OneDrive\Documents\Olympic Underdogs and GOATs"
python main.py --date %date:~10,4%-%date:~4,2%-%date:~7,2%
pause
```

2. **Create the task**:
   - Open Task Scheduler
   - Create Basic Task
   - Name: "Olympic Underdogs Watchlist"
   - Trigger: Daily at 6:00 AM
   - Action: Start a program
   - Program: `c:\Users\emf48\OneDrive\Documents\Olympic Underdogs and GOATs\run_daily_watchlist.bat`

### Option 2: PowerShell Script

Create `run_daily_watchlist.ps1`:
```powershell
Set-Location "c:\Users\emf48\OneDrive\Documents\Olympic Underdogs and GOATs"

$today = Get-Date -Format "yyyy-MM-dd"
python main.py --date $today

# Optional: Open the generated file
$outputFile = "outputs\daily_watchlists\watchlist_$today.md"
if (Test-Path $outputFile) {
    Start-Process $outputFile
}
```

Run with:
```powershell
powershell -ExecutionPolicy Bypass -File run_daily_watchlist.ps1
```

### Option 3: Manual Daily Run

During the Olympics (Feb 6-22, 2026), simply run each morning:
```bash
python main.py
```

This will generate the watchlist for today's date automatically.

## Batch Generation for Entire Olympics

Before the Olympics start, generate all watchlists at once:

```bash
python main.py --all
```

This creates watchlists for all dates from Feb 6-22, 2026.

## Scheduling Tips

### When to Run
- **6:00 AM local time**: Before most events start
- **Day before**: Generate next day's watchlist in advance
- **Multiple times**: Morning update + evening preview

### What to Check
1. **Data updates**: Has the schedule changed?
2. **Late entries**: Any new nations added?
3. **Withdrawals**: Any nations pulled out?

## Integration Ideas

### Email Notification
Add to your script:
```python
import smtplib
from email.mime.text import MIMEText

def send_watchlist(watchlist_content):
    msg = MIMEText(watchlist_content)
    msg['Subject'] = f'Olympic Underdogs Watchlist - {date}'
    msg['From'] = 'your@email.com'
    msg['To'] = 'recipient@email.com'
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your@email.com', 'password')
        server.send_message(msg)
```

### Social Media Posting
Post to Twitter/X, Bluesky, etc.:
```python
# Example: Post highlights to social media
def create_social_post(underdogs_count, top_nations):
    return f"🏅 {underdogs_count} underdog nations competing today!\n\n" + \
           f"Watch for: {', '.join(top_nations[:3])}\n\n" + \
           f"#Olympics2026 #Underdogs"
```

### Web Dashboard
Serve watchlists via simple web server:
```python
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

os.chdir('outputs/daily_watchlists')
server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
```

Then access at http://localhost:8000/

## Monitoring During Olympics

### Daily Checklist
- [ ] Watchlist generated successfully
- [ ] Underdog nations identified
- [ ] No errors in schedule parsing
- [ ] Events match official schedule
- [ ] Session times are correct

### Update Data As Needed
During the games, update:
1. **Schedule data**: If events are added/rescheduled
2. **Entry lists**: If nations are added/removed
3. **Medal counts**: After each medal ceremony (for next day's leaderboard)

### Log Files
Add logging to track generation:
```python
import logging

logging.basicConfig(
    filename='watchlist.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

logging.info(f"Generated watchlist for {date}")
logging.info(f"Found {len(underdogs)} underdog nations")
```

## Testing Automation

Test your automation before the Olympics:

1. **Dry run**: Generate watchlists for sample dates
2. **Schedule verification**: Confirm Task Scheduler triggers correctly
3. **Error handling**: Test with missing data files
4. **Output verification**: Check generated files are correct

## Troubleshooting

### Task doesn't run
- Check Task Scheduler history/logs
- Verify Python is in PATH
- Test batch file manually first

### Wrong date format
- Windows date format varies by region
- Use Python's datetime instead of batch date parsing
- Or hardcode date format in config

### File access issues
- Ensure full path is specified
- Check file permissions
- Run Task Scheduler with appropriate user account

## Advanced: Real-Time Updates

For more sophisticated automation:

```python
# Watch for schedule updates
import time
from pathlib import Path

schedule_file = Path('data/schedule/schedule.json')
last_modified = schedule_file.stat().st_mtime

while True:
    current_modified = schedule_file.stat().st_mtime
    if current_modified > last_modified:
        print("Schedule updated! Regenerating watchlist...")
        # Regenerate watchlist
        last_modified = current_modified
    time.sleep(300)  # Check every 5 minutes
```

## During the Olympics

The 2026 Winter Olympics run **February 6-22, 2026** (17 days).

Set reminders to:
- Start automation on **February 5, 2026** (day before)
- Monitor daily during the games
- Archive final watchlists on **February 23, 2026**

Enjoy tracking the underdogs! 🎿⛸️🏅
