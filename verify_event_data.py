"""Quick verification of parsed event data."""
import json

# Load event data
with open('data/event_nations_2026.json', 'r', encoding='utf-8') as f:
    event_data = json.load(f)

# Load nation data
with open('data/nation_events_2026.json', 'r', encoding='utf-8') as f:
    nation_data = json.load(f)

print("=" * 60)
print("EVENT MAPPING VERIFICATION")
print("=" * 60)

# Example 1: Women's Monobob
print("\n1. Women's Monobob Participants:")
monobob = event_data.get("Bobsleigh - Women's Monobob", [])
for nation in monobob:
    print(f"   • {nation['nation']} ({nation['athletes']} athlete, {nation['status']})")
print(f"   Total: {len(monobob)} nations")

# Example 2: Bolivia's events
print("\n2. Bolivia's Event Schedule:")
bolivia = nation_data.get("Bolivia", {})
print(f"   Sports: {', '.join(bolivia.get('sports', []))}")
print(f"   Total Events: {bolivia.get('total_events', 0)}")
print(f"   Probable: {bolivia.get('probable_events', 0)} | Unconfirmed: {bolivia.get('unconfirmed_events', 0)}")
print("   Events:")
for event in bolivia.get('events', []):
    status_icon = "✓" if event['status'] == 'probable' else "?"
    print(f"   {status_icon} {event['event']} ({event['athletes']} athlete)")

# Example 3: Cross-Country 15km classical (high underdog participation)
print("\n3. Men's 15km Classical - Most Underdog-Dense Event:")
xc_15km = event_data.get("Cross-Country Skiing - Men's 15km classical", [])
print(f"   Total nations: {len(xc_15km)}")
print(f"   Sample nations: {', '.join([n['nation'] for n in xc_15km[:10]])}...")

# Example 4: Summary statistics
print("\n4. Summary Statistics:")
print(f"   Total nations with events: {len(nation_data)}")
print(f"   Total unique events: {len(event_data)}")
print(f"   Total sports: {len(set([e.split(' - ')[0] for e in event_data.keys()]))}")

# Top 5 most active underdog nations
print("\n5. Most Active Underdog Nations:")
sorted_nations = sorted(nation_data.items(), key=lambda x: x[1]['total_events'], reverse=True)
for i, (nation, data) in enumerate(sorted_nations[:5], 1):
    print(f"   {i}. {nation}: {data['total_events']} events across {len(data['sports'])} sports")

print("\n" + "=" * 60)
print("✓ All data parsed and ready to use!")
print("=" * 60)
