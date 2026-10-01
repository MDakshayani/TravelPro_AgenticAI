import json

with open('scratch/parsed_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    print(f"[{item['type']}] {item['name']}")
    print(f"  Cover: {item['coverImage']}")
    for p in item['places']:
        print(f"   * {p['name']}: {p['image']}")
