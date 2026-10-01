import urllib.request
import urllib.parse
import json

candidate_urls = {
    # 28 States
    "Andhra Pradesh": [
        "https://images.unsplash.com/photo-1627894483216-2138af692e32", # Tirupati / AP temple
        "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1", # Vizag sea
    ],
    "Arunachal Pradesh": [
        "https://images.unsplash.com/photo-1609137144813-7d9921338f24", # Tawang monastery
        "https://images.unsplash.com/photo-1571536802807-30451e3955d8", # NE valley
    ],
    "Assam": [
        "https://images.unsplash.com/photo-1561731216-c3a4d99437d5", # Kaziranga / Assam tea
    ],
    "Bihar": [
        "https://images.unsplash.com/photo-1609946850027-e43503f88636", # Bodh Gaya Mahabodhi
        "https://images.unsplash.com/photo-1625480827154-159c3a372e9d", # Nalanda / Stupa
    ],
    "Chhattisgarh": [
        "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23", # Waterfall / Chitrakote
        "https://images.unsplash.com/photo-1544551763-77ef2d0cfc6c", 
    ],
    "Goa": [
        "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2", # Goa beach
    ],
    "Gujarat": [
        "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7", # Rann of kutch / Dwarka
    ],
    "Haryana": [
        "https://images.unsplash.com/photo-1605649487210-478a24211612", # Kurukshetra / North India landscape
        "https://images.unsplash.com/photo-1596484552834-6a58f850e0a1",
    ],
    "Himachal Pradesh": [
        "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23",
        "https://images.unsplash.com/photo-1597074866923-dc05885a2c68", # Shimla / Spiti
    ],
    "Jharkhand": [
        "https://images.unsplash.com/photo-1596176530529-78163a4f7af2", # Hundru Falls / green hills
    ],
    "Karnataka": [
        "https://images.unsplash.com/photo-1600100395160-b6f790252cfb", # Hampi stone chariot / temple
        "https://images.unsplash.com/photo-1609766857041-ed402ea8069a", # Mysore Palace
    ],
    "Kerala": [
        "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944", # Backwaters house boat
    ],
    "Madhya Pradesh": [
        "https://images.unsplash.com/photo-1605007493699-af65834f8a00", # Khajuraho / MP fort
        "https://images.unsplash.com/photo-1622396481328-9b1b78cdd9fd", # Sanchi / MP temple
    ],
    "Maharashtra": [
        "https://images.unsplash.com/photo-1570168007204-dfb528c6958f", # Gateway of India Mumbai
    ],
    "Manipur": [
        "https://images.unsplash.com/photo-1627894483216-2138af692e32", # Loktak lake / NE
    ],
    "Meghalaya": [
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb", # Dawki / Living root bridge landscape
    ],
    "Mizoram": [
        "https://images.unsplash.com/photo-1519046904884-53103b34b206", # Mizoram green hills
    ],
    "Nagaland": [
        "https://images.unsplash.com/photo-1548013146-72479768bada", # Dzukou valley Nagaland
    ],
    "Odisha": [
        "https://images.unsplash.com/photo-1609766857041-ed402ea8069a", # Puri Konark temple
    ],
    "Punjab": [
        "https://images.unsplash.com/photo-1588096344316-f71c8f1f2a88", # Old broken one
        "https://images.unsplash.com/photo-1605649487210-478a24211612", # Golden Temple / Amritsar
        "https://images.unsplash.com/photo-1609766857041-ed402ea8069a",
        "https://images.unsplash.com/photo-1600100397986-40a7088f57d6"
    ],
    "Rajasthan": [
        "https://images.unsplash.com/photo-1477587458883-47145ed94245", # Hawa Mahal Jaipur
    ],
    "Sikkim": [
        "https://images.unsplash.com/photo-1544735716-392fe2489ffa", # Sikkim mountains
    ],
    "Tamil Nadu": [
        "https://images.unsplash.com/photo-1582510003544-4d00b7f74220", # Meenakshi Temple / Mahabalipuram shore temple
    ],
    "Telangana": [
        "https://images.unsplash.com/photo-1605007493699-af65834f8a00", # Charminar Hyderabad
    ],
    "Tripura": [
        "https://images.unsplash.com/photo-1561361513-2d000a50f0dc", # Ujjayanta Palace Tripura
    ],
    "Uttar Pradesh": [
        "https://images.unsplash.com/photo-1564507592333-c60657eea523", # Taj Mahal Agra
    ],
    "Uttarakhand": [
        "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5", # Rishikesh Kedarnath hills
    ],
    "West Bengal": [
        "https://images.unsplash.com/photo-1558431382-27e303142255", # Howrah Bridge / Victoria Memorial Kolkata
    ],
    
    # 8 UTs
    "Andaman & Nicobar Islands": [
        "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5", # Havelock island
    ],
    "Chandigarh": [
        "https://images.unsplash.com/photo-1596484552834-6a58f850e0a1", # Chandigarh garden / modern architecture
    ],
    "Dadra & Nagar Haveli and Daman & Diu": [
        "https://images.unsplash.com/photo-1593181629936-11c609b8db9b", # Diu fort / sea shore
    ],
    "Delhi": [
        "https://images.unsplash.com/photo-1587474260584-136574528ed5", # India Gate / Red Fort Delhi
    ],
    "Jammu & Kashmir": [
        "https://images.unsplash.com/photo-1566837945700-30057527ade0", # Dal Lake Shikara Srinagar
    ],
    "Ladakh": [
        "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2", # Pangong Lake Ladakh
    ],
    "Lakshadweep": [
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e", # Bangaram coral island lagoon
    ],
    "Puducherry": [
        "https://images.unsplash.com/photo-1584551246679-0daf3d275d0f", # Pondicherry French Quarter Yellow house
    ]
}

def check(url):
    full_url = url + "?q=80&w=1200"
    try:
        req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status
    except Exception as e:
        return f"ERR: {e}"

for name, urls in candidate_urls.items():
    print(f"=== {name} ===")
    for u in urls:
        st = check(u)
        print(f"   [{st}] {u}")
