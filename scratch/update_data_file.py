import re
import urllib.request

# Detailed replacement dictionary mapping region id -> new cover image and place image map
REGION_COVER_MAP = {
    "andhra-pradesh": "https://images.unsplash.com/photo-1627894483216-2138af692e32?q=80&w=1200",
    "arunachal-pradesh": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?q=80&w=1200",
    "assam": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?q=80&w=1200",
    "bihar": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=1200",
    "chhattisgarh": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?q=80&w=1200",
    "goa": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?q=80&w=1200",
    "gujarat": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?q=80&w=1200",
    "haryana": "https://images.unsplash.com/photo-1587474260584-136574528ed5?q=80&w=1200",
    "himachal-pradesh": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?q=80&w=1200",
    "jharkhand": "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?q=80&w=1200",
    "karnataka": "https://images.unsplash.com/photo-1609766857041-ed402ea8069a?q=80&w=1200",
    "kerala": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?q=80&w=1200",
    "madhya-pradesh": "https://images.unsplash.com/photo-1622396481328-9b1b78cdd9fd?q=80&w=1200",
    "maharashtra": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?q=80&w=1200",
    "manipur": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?q=80&w=1200",
    "meghalaya": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1200",
    "mizoram": "https://images.unsplash.com/photo-1519046904884-53103b34b206?q=80&w=1200",
    "nagaland": "https://images.unsplash.com/photo-1571536802807-30451e3955d8?q=80&w=1200",
    "odisha": "https://images.unsplash.com/photo-1599661046289-e31897846e41?q=80&w=1200",
    "punjab": "https://images.unsplash.com/photo-1514222709107-a180c68d72b4?q=80&w=1200",
    "rajasthan": "https://images.unsplash.com/photo-1477587458883-47145ed94245?q=80&w=1200",
    "sikkim": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?q=80&w=1200",
    "tamil-nadu": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?q=80&w=1200",
    "telangana": "https://images.unsplash.com/photo-1605007493699-af65834f8a00?q=80&w=1200",
    "tripura": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?q=80&w=1200",
    "uttar-pradesh": "https://images.unsplash.com/photo-1564507592333-c60657eea523?q=80&w=1200",
    "uttarakhand": "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?q=80&w=1200",
    "west-bengal": "https://images.unsplash.com/photo-1558431382-27e303142255?q=80&w=1200",

    # UTs
    "andaman-nicobar": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?q=80&w=1200",
    "chandigarh": "https://images.unsplash.com/photo-1596484552834-6a58f850e0a1?q=80&w=1200",
    "dadra-nagar-haveli-daman-diu": "https://images.unsplash.com/photo-1593181629936-11c609b8db9b?q=80&w=1200",
    "delhi": "https://images.unsplash.com/photo-1587474260584-136574528ed5?q=80&w=1200",
    "jammu-kashmir": "https://images.unsplash.com/photo-1566837945700-30057527ade0?q=80&w=1200",
    "ladakh": "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?q=80&w=1200",
    "lakshadweep": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1200",
    "puducherry": "https://images.unsplash.com/photo-1584551246679-0daf3d275d0f?q=80&w=1200"
}

with open('frontend/src/data/indiaTravelData.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Punjab cover & places
content = content.replace("https://images.unsplash.com/photo-1588096344316-f71c8f1f2a88?q=80&w=1200", "https://images.unsplash.com/photo-1514222709107-a180c68d72b4?q=80&w=1200")
content = content.replace("https://images.unsplash.com/photo-1588096344316-f71c8f1f2a88?q=80&w=600", "https://images.unsplash.com/photo-1514222709107-a180c68d72b4?q=80&w=600")

# Replace Tamil Nadu cover & broken places
content = content.replace("https://images.unsplash.com/photo-1600100397986-40a7088f57d6?q=80&w=1200", "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?q=80&w=1200")
content = content.replace("https://images.unsplash.com/photo-1600100397986-40a7088f57d6?q=80&w=600", "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?q=80&w=600")

# Replace Mizoram cover (was duplicate photo-1544735716-392fe2489ffa)
# Let's use regex or target replacement per region cover image
for reg_id, new_cover in REGION_COVER_MAP.items():
    pattern = rf"(id:\s*['\"]{reg_id}['\"].*?coverImage:\s*['\"])([^'\"]+)(['\"])"
    content = re.sub(pattern, rf"\g<1>{new_cover}\g<3>", content, flags=re.DOTALL)

with open('frontend/src/data/indiaTravelData.ts', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated indiaTravelData.ts successfully!")
