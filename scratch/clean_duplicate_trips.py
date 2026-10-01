import json

with open('local_db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

trips = db.get('trips', [])
print(f"Initial total trips in database: {len(trips)}")

seen = set()
unique_trips = []

for t in trips:
    # create signature based on destination, user_id, start_date, created_at up to minute
    sig = (
        t.get('user_id'),
        t.get('destination'),
        t.get('start_date'),
        t.get('created_at', '')[:16] # match YYYY-MM-DDTHH:MM
    )
    if sig not in seen:
        seen.add(sig)
        unique_trips.append(t)
    else:
        print(f"Removing duplicate trip: ID {t.get('_id')} for {t.get('destination')}")

db['trips'] = unique_trips
print(f"Final unique trips count: {len(unique_trips)}")

with open('local_db.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=4)

print("Deduplicated local_db.json successfully!")
