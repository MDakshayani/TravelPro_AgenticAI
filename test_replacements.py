import urllib.request

# Candidate photo URLs for packages needing replacement
replacements = {
    # Spiritual replacements
    "Golden Temple Amritsar & Wagah Border": "https://images.unsplash.com/photo-1605649487210-478a24211612?q=80&w=800",
    "Sacred Varanasi Ganga Aarti & Kashi Temples": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?q=80&w=800",
    "Ayodhya Ram Mandir Divine Darshan": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=800",
    "Kedarnath & Badrinath Sacred Himalayan Yatra": "https://images.unsplash.com/photo-1584551246679-0daf3d275d0f?q=80&w=800",
    "Madurai Meenakshi & Rameshwaram Jyotirlinga": "https://images.unsplash.com/photo-1609766857041-ed402ea8069a?q=80&w=800",
    "Haridwar & Rishikesh Holy Ganga Circuit": "https://images.unsplash.com/photo-1571536802807-30451e3955d8?q=80&w=800",
    
    # Broken 404 replacements
    "Khajuraho Temple Art & Fort Circuit": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?q=80&w=800",
    "Periyar Elephant & Tiger Sanctuary": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?q=80&w=800",
    "Tadoba Andhari Tiger Reserve Safari": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?q=80&w=800",
    "Dharamshala & Triund Hill Ridge Trek": "https://images.unsplash.com/photo-1593181629936-11c609b8db9b?q=80&w=800",
    "Coorg Coffee Estates & Abbey Waterfalls": "https://images.unsplash.com/photo-1519046904884-53103b34b206?q=80&w=800",
    "Shimla Mall Road & Kufri Pine Hills": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?q=80&w=800",
    "Munnar Tea Gardens & Anamudi Peak": "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?q=80&w=800"
}

for name, url in replacements.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=5)
        print(f"STATUS {res.status} for {name}")
    except Exception as e:
        print(f"FAILED {e} for {name}")
