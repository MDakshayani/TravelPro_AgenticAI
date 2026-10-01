import json

with open('scratch/parsed_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total entries: {len(data)}")
state_names = [d['name'] for d in data if d['type'] == 'State']
ut_names = [d['name'] for d in data if d['type'] == 'Union Territory']

print(f"\nStates ({len(state_names)}):")
for s in state_names:
    print(f" - {s}")

print(f"\nUnion Territories ({len(ut_names)}):")
for u in ut_names:
    print(f" - {u}")
