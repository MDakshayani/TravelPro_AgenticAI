import urllib.request
import urllib.parse
import re

def search_unsplash_html(query):
    encoded = urllib.parse.quote(query)
    url = f"https://unsplash.com/s/photos/{encoded}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8')
            # find photo URLs in html like https://images.unsplash.com/photo-1548013146-72479768bada
            matches = re.findall(r'https://images\.unsplash\.com/photo-([a-zA-Z0-9\-]+)', html)
            # filter unique photo IDs
            unique_ids = []
            for m in matches:
                if m not in unique_ids and len(m) > 5:
                    unique_ids.append(m)
            return unique_ids[:5]
    except Exception as e:
        print(f"Error for '{query}': {e}")
        return []

queries = {
    "Bihar": "bihar bodh gaya temple india",
    "Tripura": "tripura ujjayanta palace india",
    "Punjab": "golden temple amritsar punjab india",
    "Jammu & Kashmir": "dal lake srinagar kashmir india",
    "Tamil Nadu": "meenakshi temple madurai tamil nadu india",
    "Arunachal Pradesh": "tawang monastery arunachal india",
    "Assam": "kaziranga assam tea india",
    "Goa": "goa beach sunset india",
    "Gujarat": "rann of kutch gujarat india",
    "Himachal Pradesh": "shimla manali mountain snow india",
    "Karnataka": "hampi mysore karnataka india",
    "Kerala": "alleppey houseboat backwaters kerala india",
    "Madhya Pradesh": "khajuraho sanchi madhya pradesh india",
    "Maharashtra": "gateway of india mumbai maharashtra",
    "Meghalaya": "living root bridge cherrapunji dawki meghalaya",
    "Odisha": "konark sun temple puri odisha",
    "Rajasthan": "hawa mahal jaipur desert rajasthan",
    "Sikkim": "gangtok kanchenjunga sikkim",
    "Telangana": "charminar hyderabad telangana",
    "Uttar Pradesh": "taj mahal agra varanasi uttar pradesh",
    "Uttarakhand": "kedarnath rishikesh uttarakhand",
    "West Bengal": "victoria memorial kolkata west bengal",
    "Andaman": "havelock island radhanagar beach andaman",
    "Delhi": "india gate delhi monument",
    "Ladakh": "pangong lake ladakh leh",
    "Lakshadweep": "coral reef lagoon lakshadweep island",
    "Puducherry": "pondicherry french quarter puducherry"
}

results = {}
for name, q in queries.items():
    ids = search_unsplash_html(q)
    print(f"=== {name} ===")
    for i in ids:
        full = f"https://images.unsplash.com/photo-{i}?q=80&w=1200"
        print(f"   {full}")
    results[name] = ids
