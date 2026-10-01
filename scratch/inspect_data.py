import re
import json

with open('frontend/src/data/indiaTravelData.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse region objects from typescript array
regions_raw = content.split("export const INDIA_STATES_AND_UTS: RegionData[] = [")[1]

# split by { id:
region_blocks = re.split(r'\{\s*id:\s*[\'"]', regions_raw)

print(f"Total region blocks found: {len(region_blocks)-1}\n")

regions = []
for block in region_blocks[1:]:
    lines = block.split('\n')
    reg_id = lines[0].split("'")[0].split('"')[0]
    
    name_match = re.search(r'name:\s*[\'"]([^\'"]+)[\'"]', block)
    type_match = re.search(r'type:\s*[\'"]([^\'"]+)[\'"]', block)
    cover_match = re.search(r'coverImage:\s*[\'"]([^\'"]+)[\'"]', block)
    
    reg_name = name_match.group(1) if name_match else "UNKNOWN"
    reg_type = type_match.group(1) if type_match else "UNKNOWN"
    reg_cover = cover_match.group(1) if cover_match else "UNKNOWN"
    
    # find places inside this region block
    places = []
    place_matches = re.findall(r'name:\s*[\'"]([^\'"]+)[\'"].*?image:\s*[\'"]([^\'"]+)[\'"]', block, re.DOTALL)
    for pm in place_matches:
        if pm[0] != reg_name: # skip state name match if any
            places.append({'place_name': pm[0], 'image': pm[1]})
            
    regions.append({
        'id': reg_id,
        'name': reg_name,
        'type': reg_type,
        'coverImage': reg_cover,
        'places': places
    })

for r in regions:
    print(f"[{r['type']}] {r['name']} (ID: {r['id']})")
    print(f"   Cover: {r['coverImage']}")
    for p in r['places']:
        print(f"   - Place: {p['place_name']} -> {p['image']}")
    print("-" * 50)
