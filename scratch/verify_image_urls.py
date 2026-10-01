import json
import urllib.request
import re

with open('scratch/parsed_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Checking HTTP status for all state/UT images...")

broken = []
for item in data:
    # check cover
    cover_url = item['coverImage']
    try:
        req = urllib.request.Request(cover_url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=5)
        if res.status != 200:
            broken.append((item['name'], 'Cover', cover_url, res.status))
    except Exception as e:
        broken.append((item['name'], 'Cover', cover_url, str(e)))

    for p in item['places']:
        purl = p['image']
        try:
            req = urllib.request.Request(purl, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req, timeout=5)
            if res.status != 200:
                broken.append((item['name'], f"Place: {p['name']}", purl, res.status))
        except Exception as e:
            broken.append((item['name'], f"Place: {p['name']}", purl, str(e)))

print(f"\nTotal broken images: {len(broken)}")
for b in broken:
    print("Broken:", b)
