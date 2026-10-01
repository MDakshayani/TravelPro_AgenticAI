import urllib.request
import urllib.parse
import json
import re

# Function to search unsplash for a query and return top photo URLs with descriptions
def search_unsplash_photos(query, count=5):
    encoded = urllib.parse.quote(query)
    # Use unsplash search page or API endpoint to extract photo IDs and descriptions
    url = f"https://unsplash.com/napi/search/photos?query={encoded}&per_page={count}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results = []
            for item in data.get('results', []):
                raw_url = item['urls']['raw']
                photo_id = item['id']
                description = item.get('description') or item.get('alt_description') or 'No desc'
                clean_url = f"https://images.unsplash.com/photo-{photo_id}?q=80&w=1200"
                results.append({'id': photo_id, 'url': clean_url, 'desc': description})
            return results
    except Exception as e:
        print(f"Error searching Unsplash for '{query}': {e}")
        return []

states_and_uts = [
    # 28 States
    ("Andhra Pradesh", "tirupati temple andhra pradesh india"),
    ("Arunachal Pradesh", "tawang monastery arunachal pradesh india"),
    ("Assam", "kaziranga assam tea garden india"),
    ("Bihar", "mahabodhi temple bodh gaya bihar india"),
    ("Chhattisgarh", "chitrakote falls bastar chhattisgarh india"),
    ("Goa", "goa beach palm trees sea sunset india"),
    ("Gujarat", "rann of kutch gujarat india"),
    ("Haryana", "kurukshetra haryana landmark india"),
    ("Himachal Pradesh", "shimla manali himachal pradesh snow mountain india"),
    ("Jharkhand", "hundru falls ranchi jharkhand waterfall india"),
    ("Karnataka", "hampi mysore palace karnataka temple india"),
    ("Kerala", "alleppey houseboat backwaters kerala tea hills india"),
    ("Madhya Pradesh", "sanchi stupa khajuraho madhya pradesh india"),
    ("Maharashtra", "gateway of india mumbai maharashtra landmark"),
    ("Manipur", "loktak lake manipur hills north east india"),
    ("Meghalaya", "cherrapunji living root bridge dawki meghalaya india"),
    ("Mizoram", "aizawl Mizoram landscape hills north east india"),
    ("Nagaland", "dzukou valley kohima nagaland north east india"),
    ("Odisha", "konark sun temple puri odisha india"),
    ("Punjab", "golden temple amritsar punjab india"),
    ("Rajasthan", "hawa mahal jaipur desert fortress rajasthan india"),
    ("Sikkim", "gangtok kanchenjunga Sikkim mountains india"),
    ("Tamil Nadu", "meenakshi temple madurai mahabalipuram tamil nadu india"),
    ("Telangana", "charminar hyderabad telangana monument india"),
    ("Tripura", "ujjayanta palace neermahal tripura landmark india"),
    ("Uttar Pradesh", "taj mahal agra varanasi ghats uttar pradesh india"),
    ("Uttarakhand", "kedarnath rishikesh ganga uttarakhand mountains india"),
    ("West Bengal", "victoria memorial kolkata darjeeling tea West Bengal india"),
    
    # 8 UTs
    ("Andaman & Nicobar Islands", "havelock island radhanagar beach andaman nicobar lagoon india"),
    ("Chandigarh", "rock garden sukhna lake chandigarh india"),
    ("Dadra & Nagar Haveli and Daman & Diu", "diu fort beach daman sea landscape india"),
    ("Delhi", "india gate red fort delhi monument landmark india"),
    ("Jammu & Kashmir", "dal lake shikara srinagar gulmarg kashmir valley india"),
    ("Ladakh", "pangong lake nubra valley leh ladakh mountains india"),
    ("Lakshadweep", "bangaram island agatti lagoon lakshadweep coral reef india"),
    ("Puducherry", "pondicherry french quarter promenade white town puducherry india")
]

verified_mapping = {}

for name, query in states_and_uts:
    print(f"=== {name} ===")
    photos = search_unsplash_photos(query, count=3)
    if photos:
        for p in photos:
            print(f"   URL: {p['url']}")
            print(f"   Desc: {p['desc']}")
        verified_mapping[name] = photos
    else:
        print("   FAILED to get photos")

with open('scratch/unsplash_results.json', 'w', encoding='utf-8') as f:
    json.dump(verified_mapping, f, indent=2)

print("\nSaved search results to scratch/unsplash_results.json")
