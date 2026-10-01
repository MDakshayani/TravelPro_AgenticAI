import re
import json

with open('frontend/src/data/indiaTravelData.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's write a python script to extract all state/UT definitions
# We can extract the block for INDIA_STATES_AND_UTS
match = re.search(r'export const INDIA_STATES_AND_UTS: RegionData\[\] = \[(.*?)\];\s*export', content, re.DOTALL)
if not match:
    # try end of file
    match = re.search(r'export const INDIA_STATES_AND_UTS: RegionData\[\] = \[(.*)', content, re.DOTALL)

data_text = match.group(1) if match else content

# split by state objects (id: '...')
state_chunks = re.split(r'\{\s*id:\s*[\'\"]', data_text)

results = []
for chunk in state_chunks[1:]:
    id_m = re.match(r'([^\'\"]+)', chunk)
    name_m = re.search(r'name:\s*[\'\"]([^\'\"]+)[\'\"]', chunk)
    type_m = re.search(r'type:\s*[\'\"]([^\'\"]+)[\'\"]', chunk)
    cover_m = re.search(r'coverImage:\s*[\'\"]([^\'\"]+)[\'\"]', chunk)
    
    s_id = id_m.group(1) if id_m else ''
    s_name = name_m.group(1) if name_m else ''
    s_type = type_m.group(1) if type_m else ''
    s_cover = cover_m.group(1) if cover_m else ''
    
    # places
    places = []
    places_part = chunk.split("places: [")
    if len(places_part) > 1:
        p_str = places_part[1]
        p_blocks = re.findall(r'\{\s*name:\s*[\'\"]([^\'\"]+)[\'\"][\s\S]*?category:\s*[\'\"]([^\'\"]+)[\'\"][\s\S]*?image:\s*[\'\"]([^\'\"]+)[\'\"]', p_str)
        for pname, pcat, pimg in p_blocks:
            places.append({"name": pname, "category": pcat, "image": pimg})
            
    results.append({
        "id": s_id,
        "name": s_name,
        "type": s_type,
        "coverImage": s_cover,
        "places": places
    })

print(f"Parsed {len(results)} States/UTs.")
with open('scratch/parsed_data.json', 'w', encoding='utf-8') as f_out:
    json.dump(results, f_out, indent=2)

states = [r for r in results if r['type'] == 'State']
uts = [r for r in results if r['type'] == 'Union Territory']
print(f"States: {len(states)}, UTs: {len(uts)}")

for r in results:
    print(f"[{r['type']}] {r['name']} ({r['id']}): Cover -> {r['coverImage']}")
    for p in r['places']:
        print(f"   - Place: {p['name']} -> {p['image']}")
