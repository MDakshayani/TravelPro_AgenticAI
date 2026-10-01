import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Read indiaTravelData.ts
with open('frontend/src/data/indiaTravelData.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# We want to extract each region object
# Regex matching regions
region_matches = re.findall(r"id:\s*'([^']+)',\s*name:\s*'([^']+)',\s*type:\s*'([^']+)',[\s\S]*?coverImage:\s*'([^']+)'", text)

print(f"Total region matches: {len(region_matches)}")

# Map of coverImage to list of region names
cover_map = {}
for r_id, name, r_type, img in region_matches:
    if img not in cover_map:
        cover_map[img] = []
    cover_map[img].append(f"{name} ({r_type})")

print("\n--- REUSED / DUPLICATE COVER IMAGES ---")
for img, names in cover_map.items():
    if len(names) > 1:
        print(f"DUPLICATE ({len(names)}): {names} -> {img}")

print("\n--- ALL REGION COVER IMAGES ---")
for r_id, name, r_type, img in region_matches:
    # Test HTTP request
    status = "UNKNOWN"
    try:
        req = urllib.request.Request(img, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=5, context=ctx)
        status = res.status
    except Exception as e:
        status = f"ERROR: {e}"
    print(f"[{status}] {name} ({r_type}) -> {img}")
