import json
import re

with open('scratch/parsed_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== CURRENT COVER IMAGES AND PLACES IN DATA ===")
for item in data:
    print(f"\n--- [{item['type']}] {item['name']} (id: {item['id']}) ---")
    print(f"Cover Image: {item['coverImage']}")
    for p in item['places']:
        print(f"  Place: {p['name']} ({p['category']}) -> {p['image']}")
