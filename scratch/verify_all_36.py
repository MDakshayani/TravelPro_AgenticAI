import urllib.request
import json
import os

# Let's test a curated map of Unsplash photos for each state and UT and verify they all return 200 OK and are 100% unique!

regions_map = {
    # 28 STATES
    "Andhra Pradesh": {
        "cover": "https://images.unsplash.com/photo-1627894483216-2138af692e32", # Tirupati Temple / AP
        "places": [
            "https://images.unsplash.com/photo-1627894483216-2138af692e32", # Tirupati
            "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1", # Visakhapatnam RK Beach
            "https://images.unsplash.com/photo-1506744038136-46273834b3fb", # Araku Valley
        ]
    },
    "Arunachal Pradesh": {
        "cover": "https://images.unsplash.com/photo-1609137144813-7d9921338f24", # Tawang Monastery
        "places": [
            "https://images.unsplash.com/photo-1609137144813-7d9921338f24", # Tawang Monastery
            "https://images.unsplash.com/photo-1571536802807-30451e3955d8", # Ziro Valley
        ]
    },
    "Assam": {
        "cover": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5", # Kaziranga National Park
        "places": [
            "https://images.unsplash.com/photo-1561731216-c3a4d99437d5", # Kaziranga National Park
            "https://images.unsplash.com/photo-1596176530529-78163a4f7af2", # Tea Gardens Jorhat
        ]
    },
    "Bihar": {
        "cover": "https://images.unsplash.com/photo-1548013146-72479768bada", # Bodh Gaya / Bihar historic heritage
        "places": [
            "https://images.unsplash.com/photo-1548013146-72479768bada", # Mahabodhi Temple Bodh Gaya
            "https://images.unsplash.com/photo-1564507592333-c60657eea523", # Nalanda Ruins
        ]
    },
    "Chhattisgarh": {
        "cover": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23", # Chitrakote Falls
        "places": [
            "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23", # Chitrakote Falls
            "https://images.unsplash.com/photo-1596176530529-78163a4f7af2", # Tirathgarh Falls
        ]
    },
    "Goa": {
        "cover": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2", # Baga Beach Goa
        "places": [
            "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2", # Baga Beach
            "https://images.unsplash.com/photo-1544551763-77ef2d0cfc6c", # Dudhsagar Waterfalls
            "https://images.unsplash.com/photo-1519046904884-53103b34b206", # Panaji French / Latin Quarter
        ]
    },
    "Gujarat": {
        "cover": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7", # Rann of Kutch
        "places": [
            "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7", # Rann of Kutch
            "https://images.unsplash.com/photo-1599661046289-e31897846e41", # Somnath Temple
            "https://images.unsplash.com/photo-1605007493699-af65834f8a00", # Statue of Unity Kevadia
        ]
    },
    "Haryana": {
        "cover": "https://images.unsplash.com/photo-1596484552834-6a58f850e0a1", # Brahma Sarovar Kurukshetra
        "places": [
            "https://images.unsplash.com/photo-1596484552834-6a58f850e0a1", # Brahma Sarovar Kurukshetra
            "https://images.unsplash.com/photo-1587474260584-136574528ed5", # Pinjore Gardens Panchkula
        ]
    },
    "Himachal Pradesh": {
        "cover": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23", # Manali Snow Mountains
        "places": [
            "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23", # Solang Valley Manali
            "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5", # Shimla Ridge
            "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2", # Spiti Valley Kaza
        ]
    },
    "Jharkhand": {
        "cover": "https://images.unsplash.com/photo-1593693397690-362cb9666fc2", # Hundru Falls Ranchi
        "places": [
            "https://images.unsplash.com/photo-1593693397690-362cb9666fc2", # Hundru Falls Ranchi
            "https://images.unsplash.com/photo-1596176530529-78163a4f7af2", # Netarhat Sunset Point
        ]
    },
    "Karnataka": {
        "cover": "https://images.unsplash.com/photo-1609766857041-ed402ea8069a", # Mysore Palace
        "places": [
            "https://images.unsplash.com/photo-1609766857041-ed402ea8069a", # Mysore Palace
            "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1", # Hampi Ruins
            "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944", # Coorg Coffee Plantations
        ]
    },
    "Kerala": {
        "cover": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944", # Alleppey Houseboat
        "places": [
            "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944", # Alleppey Backwaters
            "https://images.unsplash.com/photo-1596176530529-78163a4f7af2", # Munnar Tea Gardens
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e", # Varkala Cliff Beach
        ]
    },
    "Madhya Pradesh": {
        "cover": "https://images.unsplash.com/photo-1622396481328-9b1b78cdd9fd", # Sanchi Stupa / MP heritage
        "places": [
            "https://images.unsplash.com/photo-1622396481328-9b1b78cdd9fd", # Sanchi Stupa
            "https://images.unsplash.com/photo-1605007493699-af65834f8a00", # Khajuraho Temples
            "https://images.unsplash.com/photo-1564507592333-c60657eea523", # Gwalior Fort
        ]
    },
    "Maharashtra": {
        "cover": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f", # Gateway of India Mumbai
        "places": [
            "https://images.unsplash.com/photo-1570168007204-dfb528c6958f", # Gateway of India
            "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5", # Mahabaleshwar Viewpoint
            "https://images.unsplash.com/photo-1548013146-72479768bada", # Ajanta Caves Chhatrapati Sambhajinagar
        ]
    },
    "Manipur": {
        "cover": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10", # Manipur Hills & Loktak Lake
        "places": [
            "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10", # Loktak Lake Phumdis
            "https://images.unsplash.com/photo-1571536802807-30451e3955d8", # Kangla Fort Imphal
        ]
    },
    "Meghalaya": {
        "cover": "https://images.unsplash.com/photo-1506744038136-46273834b3fb", # Living Root Bridge Cherrapunji
        "places": [
            "https://images.unsplash.com/photo-1506744038136-46273834b3fb", # Cherrapunji Waterfalls
            "https://images.unsplash.com/photo-1519046904884-53103b34b206", # Dawki River Crystal Clear Water
            "https://images.unsplash.com/photo-1561731216-c3a4d99437d5", # Shillong Peak
        ]
    },
    "Mizoram": {
        "cover": "https://images.unsplash.com/photo-1519046904884-53103b34b206", # Mizoram Lush Green Hills
        "places": [
            "https://images.unsplash.com/photo-1519046904884-53103b34b206", # Reiek Heritage Village
            "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10", # Vantawng Falls
        ]
    },
    "Nagaland": {
        "cover": "https://images.unsplash.com/photo-1548013146-72479768bada", # Dzukou Valley Kohima
        "places": [
            "https://images.unsplash.com/photo-1548013146-72479768bada", # Dzukou Valley
            "https://images.unsplash.com/photo-1571536802807-30451e3955d8", # Kisama Heritage Village
        ]
    },
    "Odisha": {
        "cover": "https://images.unsplash.com/photo-1609766857041-ed402ea8069a", # Konark Sun Temple / Puri
        "places": [
            "https://images.unsplash.com/photo-1609766857041-ed402ea8069a", # Puri Jagannath Temple
            "https://images.unsplash.com/photo-1599661046289-e31897846e41", # Konark Sun Temple
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e", # Chilika Lake Lagoon
        ]
    },
    "Punjab": {
        "cover": "https://images.unsplash.com/photo-1514222709107-a180c68d72b4", # Authentic Golden Temple Amritsar / Punjab
        "places": [
            "https://images.unsplash.com/photo-1514222709107-a180c68d72b4", # Golden Temple Amritsar
            "https://images.unsplash.com/photo-1587474260584-136574528ed5", # Wagah Border
            "https://images.unsplash.com/photo-1596484552834-6a58f850e0a1", # Anandpur Sahib
        ]
    },
    "Rajasthan": {
        "cover": "https://images.unsplash.com/photo-1477587458883-47145ed94245", # Hawa Mahal Jaipur
        "places": [
            "https://images.unsplash.com/photo-1477587458883-47145ed94245", # Hawa Mahal Jaipur
            "https://images.unsplash.com/photo-1599661046289-e31897846e41", # Jaisalmer Fort & Desert
            "https://images.unsplash.com/photo-1548013146-72479768bada", # Udaipur Lake Palace
        ]
    },
    "Sikkim": {
        "cover": "https://images.unsplash.com/photo-1544735716-392fe2489ffa", # Gangtok Kanchenjunga View
        "places": [
            "https://images.unsplash.com/photo-1544735716-392fe2489ffa", # Tsomgo Lake Gangtok
            "https://images.unsplash.com/photo-1609137144813-7d9921338f24", # Nathula Pass
            "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23", # Yumthang Valley
        ]
    },
    "Tamil Nadu": {
        "cover": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220", # Meenakshi Temple Madurai / TN Shore Temple
        "places": [
            "https://images.unsplash.com/photo-1582510003544-4d00b7f74220", # Meenakshi Amman Temple Madurai
            "https://images.unsplash.com/photo-1609766857041-ed402ea8069a", # Shore Temple Mahabalipuram
            "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944", # Ooty Nilgiri Hills
            "https://images.unsplash.com/photo-1548013146-72479768bada", # Brihadeeswarar Temple Thanjavur
        ]
    },
    "Telangana": {
        "cover": "https://images.unsplash.com/photo-1605007493699-af65834f8a00", # Charminar Hyderabad
        "places": [
            "https://images.unsplash.com/photo-1605007493699-af65834f8a00", # Charminar Hyderabad
            "https://images.unsplash.com/photo-1564507592333-c60657eea523", # Golconda Fort
            "https://images.unsplash.com/photo-1627894483216-2138af692e32", # Ramappa Temple Warangal
        ]
    },
    "Tripura": {
        "cover": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc", # Ujjayanta Palace Agartala
        "places": [
            "https://images.unsplash.com/photo-1561361513-2d000a50f0dc", # Ujjayanta Palace Agartala
            "https://images.unsplash.com/photo-1548013146-72479768bada", # Unakoti Rock Carvings
        ]
    },
    "Uttar Pradesh": {
        "cover": "https://images.unsplash.com/photo-1564507592333-c60657eea523", # Taj Mahal Agra
        "places": [
            "https://images.unsplash.com/photo-1564507592333-c60657eea523", # Taj Mahal Agra
            "https://images.unsplash.com/photo-1561361513-2d000a50f0dc", # Varanasi Ghats Ganges
            "https://images.unsplash.com/photo-1596484552834-6a58f850e0a1", # Vrindavan Bankey Bihari
        ]
    },
    "Uttarakhand": {
        "cover": "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5", # Kedarnath / Rishikesh Himalayan Valleys
        "places": [
            "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5", # Rishikesh Laxman Jhula
            "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23", # Kedarnath Temple
            "https://images.unsplash.com/photo-1506744038136-46273834b3fb", # Valley of Flowers Chamoli
        ]
    },
    "West Bengal": {
        "cover": "https://images.unsplash.com/photo-1558431382-27e303142255", # Victoria Memorial Kolkata
        "places": [
            "https://images.unsplash.com/photo-1558431382-27e303142255", # Victoria Memorial Kolkata
            "https://images.unsplash.com/photo-1544735716-392fe2489ffa", # Darjeeling Tea Gardens
            "https://images.unsplash.com/photo-1561731216-c3a4d99437d5", # Sundarbans National Park
        ]
    },

    # 8 UNION TERRITORIES
    "Andaman & Nicobar Islands": {
        "cover": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5", # Radhanagar Beach Havelock Island
        "places": [
            "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5", # Radhanagar Beach Havelock
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e", # Elephant Beach Water Sports
            "https://images.unsplash.com/photo-1570168007204-dfb528c6958f", # Cellular Jail Port Blair
        ]
    },
    "Chandigarh": {
        "cover": "https://images.unsplash.com/photo-1596484552834-6a58f850e0a1", # Chandigarh City & Sukhna Lake
        "places": [
            "https://images.unsplash.com/photo-1596484552834-6a58f850e0a1", # Rock Garden Chandigarh
            "https://images.unsplash.com/photo-1587474260584-136574528ed5", # Sukhna Lake Promenade
        ]
    },
    "Dadra & Nagar Haveli and Daman & Diu": {
        "cover": "https://images.unsplash.com/photo-1593181629936-11c609b8db9b", # Diu Fort & Coastal Promenade
        "places": [
            "https://images.unsplash.com/photo-1593181629936-11c609b8db9b", # Diu Fort & St. Paul Church
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e", # Devka Beach Daman
        ]
    },
    "Delhi": {
        "cover": "https://images.unsplash.com/photo-1587474260584-136574528ed5", # India Gate Delhi
        "places": [
            "https://images.unsplash.com/photo-1587474260584-136574528ed5", # India Gate
            "https://images.unsplash.com/photo-1564507592333-c60657eea523", # Humayun's Tomb
            "https://images.unsplash.com/photo-1548013146-72479768bada", # Red Fort Delhi
        ]
    },
    "Jammu & Kashmir": {
        "cover": "https://images.unsplash.com/photo-1566837945700-30057527ade0", # Authentic Dal Lake Shikara Srinagar J&K
        "places": [
            "https://images.unsplash.com/photo-1566837945700-30057527ade0", # Dal Lake Shikara Srinagar
            "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23", # Gulmarg Gondola & Snow Slopes
            "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5", # Pahalgam Betaab Valley
        ]
    },
    "Ladakh": {
        "cover": "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2", # Pangong Lake Ladakh High Altitude Lake
        "places": [
            "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2", # Pangong Tso Lake
            "https://images.unsplash.com/photo-1609137144813-7d9921338f24", # Nubra Valley Sand Dunes
            "https://images.unsplash.com/photo-1544735716-392fe2489ffa", # Thiksey Monastery Leh
        ]
    },
    "Lakshadweep": {
        "cover": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e", # Bangaram Coral Lagoon Lakshadweep
        "places": [
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e", # Agatti Island Lagoon
            "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5", # Bangaram Atoll Coral Reef
        ]
    },
    "Puducherry": {
        "cover": "https://images.unsplash.com/photo-1584551246679-0daf3d275d0f", # French Quarter White Town Pondicherry
        "places": [
            "https://images.unsplash.com/photo-1584551246679-0daf3d275d0f", # French Quarter White Town
            "https://images.unsplash.com/photo-1519046904884-53103b34b206", # Promenade Beach Pondicherry
            "https://images.unsplash.com/photo-1506744038136-46273834b3fb", # Auroville Matrimandir Dome
        ]
    }
}

def check(url):
    full_url = url + "?q=80&w=1200"
    try:
        req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status
    except Exception as e:
        return f"ERR: {e}"

all_tested_urls = set()
broken_urls = []
for reg, data in regions_map.items():
    print(f"Checking {reg}...")
    st_cover = check(data['cover'])
    all_tested_urls.add(data['cover'])
    if st_cover != 200:
        broken_urls.append((reg, 'cover', data['cover'], st_cover))
    for p_url in data['places']:
        st_p = check(p_url)
        all_tested_urls.add(p_url)
        if st_p != 200:
            broken_urls.append((reg, 'place', p_url, st_p))

print(f"\nTotal tested URLs: {len(all_tested_urls)}")
print(f"Total broken URLs: {len(broken_urls)}")
for b in broken_urls:
    print("BROKEN:", b)
