import re
import urllib.request
import json

# Define the verified image dictionary for each region cover & places
IMAGE_UPDATES = {
    "andhra-pradesh": {
        "cover": "https://images.unsplash.com/photo-1627894483216-2138af692e32?q=80&w=1200", # Tirupati Temple
        "places": {
            "Tirupati": "https://images.unsplash.com/photo-1627894483216-2138af692e32?q=80&w=600",
            "Visakhapatnam": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?q=80&w=600",
            "Araku Valley": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600",
            "Vijayawada": "https://images.unsplash.com/photo-1627894483216-2138af692e32?q=80&w=600",
            "Srisailam": "https://images.unsplash.com/photo-1627894483216-2138af692e32?q=80&w=600",
            "Lepakshi": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?q=80&w=600"
        }
    },
    "arunachal-pradesh": {
        "cover": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?q=80&w=1200", # Tawang Monastery
        "places": {
            "Tawang": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?q=80&w=600",
            "Ziro Valley": "https://images.unsplash.com/photo-1571536802807-30451e3955d8?q=80&w=600",
            "Dirang": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?q=80&w=600",
            "Bomdila": "https://images.unsplash.com/photo-1571536802807-30451e3955d8?q=80&w=600"
        }
    },
    "assam": {
        "cover": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?q=80&w=1200", # Kaziranga Rhino & Tea
        "places": {
            "Kaziranga": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?q=80&w=600",
            "Guwahati": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?q=80&w=600",
            "Majuli": "https://images.unsplash.com/photo-1519046904884-53103b34b206?q=80&w=600",
            "Sivasagar": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=600",
            "Manas": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?q=80&w=600"
        }
    },
    "bihar": {
        "cover": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=1200", # Bodh Gaya Stupa Heritage
        "places": {
            "Bodh Gaya": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=600",
            "Nalanda": "https://images.unsplash.com/photo-1564507592333-c60657eea523?q=80&w=600",
            "Rajgir": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=600",
            "Vaishali": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=600",
            "Patna": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?q=80&w=600"
        }
    },
    "chhattisgarh": {
        "cover": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?q=80&w=1200", # Chitrakote Waterfall
        "places": {
            "Jagdalpur": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?q=80&w=600",
            "Chitrakote": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?q=80&w=600",
            "Mainpat": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600",
            "Raipur": "https://images.unsplash.com/photo-1587474260584-136574528ed5?q=80&w=600"
        }
    },
    "goa": {
        "cover": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?q=80&w=1200", # Baga Beach Goa
        "places": {
            "Baga": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?q=80&w=600",
            "Panaji": "https://images.unsplash.com/photo-1519046904884-53103b34b206?q=80&w=600",
            "Palolem": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600",
            "Dudhsagar": "https://images.unsplash.com/photo-1544551763-77ef2d0cfc6c?q=80&w=600",
            "Old Goa": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=600"
        }
    },
    "gujarat": {
        "cover": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?q=80&w=1200", # Rann of Kutch
        "places": {
            "Rann of Kutch": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?q=80&w=600",
            "Gir National Park": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?q=80&w=600",
            "Somnath": "https://images.unsplash.com/photo-1599661046289-e31897846e41?q=80&w=600",
            "Dwarka": "https://images.unsplash.com/photo-1599661046289-e31897846e41?q=80&w=600",
            "Statue of Unity": "https://images.unsplash.com/photo-1605007493699-af65834f8a00?q=80&w=600",
            "Ahmedabad": "https://images.unsplash.com/photo-1587474260584-136574528ed5?q=80&w=600"
        }
    },
    "haryana": {
        "cover": "https://images.unsplash.com/photo-1596484552834-6a58f850e0a1?q=80&w=1200", # Brahma Sarovar Kurukshetra
        "places": {
            "Kurukshetra": "https://images.unsplash.com/photo-1596484552834-6a58f850e0a1?q=80&w=600",
            "Panchkula": "https://images.unsplash.com/photo-1587474260584-136574528ed5?q=80&w=600",
            "Gurugram": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?q=80&w=600",
            "Sultanpur": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?q=80&w=600"
        }
    },
    "himachal-pradesh": {
        "cover": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?q=80&w=1200", # Manali snow valley
        "places": {
            "Manali": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?q=80&w=600",
            "Shimla": "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?q=80&w=600",
            "Dharamshala": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?q=80&w=600",
            "Spiti Valley": "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?q=80&w=600",
            "Kasol": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600",
            "Dalhousie": "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?q=80&w=600"
        }
    },
    "jharkhand": {
        "cover": "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?q=80&w=1200", # Hundru Falls Ranchi
        "places": {
            "Ranchi": "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?q=80&w=600",
            "Netarhat": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600",
            "Deoghar": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?q=80&w=600",
            "Jamshedpur": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?q=80&w=600"
        }
    },
    "karnataka": {
        "cover": "https://images.unsplash.com/photo-1609766857041-ed402ea8069a?q=80&w=1200", # Mysore Palace
        "places": {
            "Bengaluru": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?q=80&w=600",
            "Mysuru": "https://images.unsplash.com/photo-1609766857041-ed402ea8069a?q=80&w=600",
            "Hampi": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?q=80&w=600",
            "Coorg": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?q=80&w=600",
            "Gokarna": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600",
            "Chikmagalur": "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?q=80&w=600"
        }
    },
    "kerala": {
        "cover": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?q=80&w=1200", # Houseboat Backwaters
        "places": {
            "Alleppey": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?q=80&w=600",
            "Munnar": "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?q=80&w=600",
            "Kochi": "https://images.unsplash.com/photo-1519046904884-53103b34b206?q=80&w=600",
            "Varkala": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600",
            "Wayanad": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600",
            "Thekkady": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?q=80&w=600"
        }
    },
    "madhya-pradesh": {
        "cover": "https://images.unsplash.com/photo-1622396481328-9b1b78cdd9fd?q=80&w=1200", # Sanchi Stupa / Khajuraho Heritage
        "places": {
            "Khajuraho": "https://images.unsplash.com/photo-1605007493699-af65834f8a00?q=80&w=600",
            "Gwalior": "https://images.unsplash.com/photo-1564507592333-c60657eea523?q=80&w=600",
            "Orchha": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=600",
            "Ujjain": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?q=80&w=600",
            "Bhopal": "https://images.unsplash.com/photo-1622396481328-9b1b78cdd9fd?q=80&w=600",
            "Pachmarhi": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600"
        }
    },
    "maharashtra": {
        "cover": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?q=80&w=1200", # Gateway of India Mumbai
        "places": {
            "Mumbai": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?q=80&w=600",
            "Pune": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?q=80&w=600",
            "Lonavala": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600",
            "Mahabaleshwar": "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?q=80&w=600",
            "Chhatrapati Sambhajinagar": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=600",
            "Nashik": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?q=80&w=600"
        }
    },
    "manipur": {
        "cover": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?q=80&w=1200", # Loktak Lake Phumdis
        "places": {
            "Imphal": "https://images.unsplash.com/photo-1571536802807-30451e3955d8?q=80&w=600",
            "Loktak Lake": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?q=80&w=600",
            "Ukhrul": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600",
            "Moirang": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?q=80&w=600"
        }
    },
    "meghalaya": {
        "cover": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1200", # Living Root Bridge Cherrapunji
        "places": {
            "Shillong": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?q=80&w=600",
            "Cherrapunji": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600",
            "Dawki": "https://images.unsplash.com/photo-1519046904884-53103b34b206?q=80&w=600",
            "Mawlynnong": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600"
        }
    },
    "mizoram": {
        "cover": "https://images.unsplash.com/photo-1519046904884-53103b34b206?q=80&w=1200", # Mizoram Lush Hills
        "places": {
            "Aizawl": "https://images.unsplash.com/photo-1519046904884-53103b34b206?q=80&w=600",
            "Lunglei": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600",
            "Reiek": "https://images.unsplash.com/photo-1519046904884-53103b34b206?q=80&w=600",
            "Champhai": "https://images.unsplash.com/photo-1571536802807-30451e3955d8?q=80&w=600"
        }
    },
    "nagaland": {
        "cover": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=1200", # Dzukou Valley Kohima
        "places": {
            "Kohima": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=600",
            "Dimapur": "https://images.unsplash.com/photo-1571536802807-30451e3955d8?q=80&w=600",
            "Mokokchung": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600",
            "Mon": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=600"
        }
    },
    "odisha": {
        "cover": "https://images.unsplash.com/photo-1599661046289-e31897846e41?q=80&w=1200", # Konark Sun Temple
        "places": {
            "Puri": "https://images.unsplash.com/photo-1609766857041-ed402ea8069a?q=80&w=600",
            "Bhubaneswar": "https://images.unsplash.com/photo-1599661046289-e31897846e41?q=80&w=600",
            "Konark": "https://images.unsplash.com/photo-1599661046289-e31897846e41?q=80&w=600",
            "Chilika Lake": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600",
            "Gopalpur": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600"
        }
    },
    "punjab": {
        "cover": "https://images.unsplash.com/photo-1514222709107-a180c68d72b4?q=80&w=1200", # Golden Temple Amritsar Punjab
        "places": {
            "Amritsar": "https://images.unsplash.com/photo-1514222709107-a180c68d72b4?q=80&w=600",
            "Patiala": "https://images.unsplash.com/photo-1587474260584-136574528ed5?q=80&w=600",
            "Kapurthala": "https://images.unsplash.com/photo-1564507592333-c60657eea523?q=80&w=600",
            "Bathinda": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=600",
            "Jalandhar": "https://images.unsplash.com/photo-1596484552834-6a58f850e0a1?q=80&w=600"
        }
    },
    "rajasthan": {
        "cover": "https://images.unsplash.com/photo-1477587458883-47145ed94245?q=80&w=1200", # Hawa Mahal Jaipur
        "places": {
            "Jaipur": "https://images.unsplash.com/photo-1477587458883-47145ed94245?q=80&w=600",
            "Udaipur": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?q=80&w=600",
            "Jaisalmer": "https://images.unsplash.com/photo-1599661046289-e31897846e41?q=80&w=600",
            "Jodhpur": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=600",
            "Pushkar": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?q=80&w=600",
            "Bikaner": "https://images.unsplash.com/photo-1599661046289-e31897846e41?q=80&w=600"
        }
    },
    "sikkim": {
        "cover": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?q=80&w=1200", # Gangtok Kanchenjunga View
        "places": {
            "Gangtok": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?q=80&w=600",
            "Pelling": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?q=80&w=600",
            "Lachung": "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?q=80&w=600",
            "Yumthang": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600",
            "Ravangla": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?q=80&w=600"
        }
    },
    "tamil-nadu": {
        "cover": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?q=80&w=1200", # Meenakshi Temple Madurai / Shore Temple
        "places": {
            "Chennai": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?q=80&w=600",
            "Madurai": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?q=80&w=600",
            "Mahabalipuram": "https://images.unsplash.com/photo-1609766857041-ed402ea8069a?q=80&w=600",
            "Ooty": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?q=80&w=600",
            "Kodaikanal": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600",
            "Rameswaram": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?q=80&w=600",
            "Kanyakumari": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600",
            "Thanjavur": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?q=80&w=600"
        }
    },
    "telangana": {
        "cover": "https://images.unsplash.com/photo-1605007493699-af65834f8a00?q=80&w=1200", # Charminar Hyderabad
        "places": {
            "Hyderabad": "https://images.unsplash.com/photo-1605007493699-af65834f8a00?q=80&w=600",
            "Warangal": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?q=80&w=600",
            "Bhongir": "https://images.unsplash.com/photo-1564507592333-c60657eea523?q=80&w=600",
            "Vemulawada": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?q=80&w=600"
        }
    },
    "tripura": {
        "cover": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?q=80&w=1200", # Ujjayanta Palace Agartala
        "places": {
            "Agartala": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?q=80&w=600",
            "Unakoti": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=600",
            "Neermahal": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?q=80&w=600"
        }
    },
    "uttar-pradesh": {
        "cover": "https://images.unsplash.com/photo-1564507592333-c60657eea523?q=80&w=1200", # Taj Mahal Agra
        "places": {
            "Agra": "https://images.unsplash.com/photo-1564507592333-c60657eea523?q=80&w=600",
            "Varanasi": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?q=80&w=600",
            "Ayodhya": "https://images.unsplash.com/photo-1609766857041-ed402ea8069a?q=80&w=600",
            "Mathura": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?q=80&w=600",
            "Vrindavan": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?q=80&w=600",
            "Lucknow": "https://images.unsplash.com/photo-1587474260584-136574528ed5?q=80&w=600",
            "Prayagraj": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?q=80&w=600"
        }
    },
    "uttarakhand": {
        "cover": "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?q=80&w=1200", # Kedarnath / Rishikesh Ganges
        "places": {
            "Rishikesh": "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?q=80&w=600",
            "Mussoorie": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600",
            "Nainital": "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?q=80&w=600",
            "Auli": "https://images.unsplash.com/photo-1519681393784-d120267933ba?q=80&w=600",
            "Kedarnath": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?q=80&w=600",
            "Badrinath": "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?q=80&w=600",
            "Haridwar": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?q=80&w=600"
        }
    },
    "west-bengal": {
        "cover": "https://images.unsplash.com/photo-1558431382-27e303142255?q=80&w=1200", # Victoria Memorial / Kolkata
        "places": {
            "Kolkata": "https://images.unsplash.com/photo-1558431382-27e303142255?q=80&w=600",
            "Darjeeling": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?q=80&w=600",
            "Kalimpong": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600",
            "Sundarbans": "https://images.unsplash.com/photo-1549366021-9f761d450615?q=80&w=600"
        }
    },

    # 8 UNION TERRITORIES
    "andaman-nicobar": {
        "cover": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?q=80&w=1200", # Havelock Island Radhanagar
        "places": {
            "Port Blair": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?q=80&w=600",
            "Havelock": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?q=80&w=600",
            "Neil Island": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600",
            "Radhanagar": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600",
            "Baratang": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600"
        }
    },
    "chandigarh": {
        "cover": "https://images.unsplash.com/photo-1596484552834-6a58f850e0a1?q=80&w=1200", # Chandigarh Gardens & Sukhna Lake
        "places": {
            "Rock Garden": "https://images.unsplash.com/photo-1596484552834-6a58f850e0a1?q=80&w=600",
            "Sukhna Lake": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600",
            "Capitol Complex": "https://images.unsplash.com/photo-1587474260584-136574528ed5?q=80&w=600"
        }
    },
    "dadra-nagar-haveli-daman-diu": {
        "cover": "https://images.unsplash.com/photo-1593181629936-11c609b8db9b?q=80&w=1200", # Diu Fort & Coastal Promenade
        "places": {
            "Daman": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600",
            "Diu": "https://images.unsplash.com/photo-1593181629936-11c609b8db9b?q=80&w=600",
            "Silvassa": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600"
        }
    },
    "delhi": {
        "cover": "https://images.unsplash.com/photo-1587474260584-136574528ed5?q=80&w=1200", # India Gate Delhi
        "places": {
            "India Gate": "https://images.unsplash.com/photo-1587474260584-136574528ed5?q=80&w=600",
            "Qutub Minar": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?q=80&w=600",
            "Humayun’s Tomb": "https://images.unsplash.com/photo-1564507592333-c60657eea523?q=80&w=600",
            "Old Delhi": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=600"
        }
    },
    "jammu-kashmir": {
        "cover": "https://images.unsplash.com/photo-1566837945700-30057527ade0?q=80&w=1200", # Dal Lake Shikara Srinagar J&K
        "places": {
            "Srinagar": "https://images.unsplash.com/photo-1566837945700-30057527ade0?q=80&w=600",
            "Gulmarg": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?q=80&w=600",
            "Pahalgam": "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?q=80&w=600",
            "Sonamarg": "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?q=80&w=600"
        }
    },
    "ladakh": {
        "cover": "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?q=80&w=1200", # Pangong Tso Lake Ladakh
        "places": {
            "Leh": "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?q=80&w=600",
            "Pangong": "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?q=80&w=600",
            "Nubra": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?q=80&w=600",
            "Tso Moriri": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600"
        }
    },
    "lakshadweep": {
        "cover": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1200", # Bangaram Coral Lagoon
        "places": {
            "Agatti": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600",
            "Bangaram": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?q=80&w=600",
            "Kavaratti": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600",
            "Kalpeni": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600"
        }
    },
    "puducherry": {
        "cover": "https://images.unsplash.com/photo-1584551246679-0daf3d275d0f?q=80&w=1200", # French Quarter White Town
        "places": {
            "Promenade": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600",
            "Auroville": "https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=600",
            "Paradise Beach": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600"
        }
    }
}

print("Checking all update URLs for HTTP 200...")
all_urls = set()
for reg, data in IMAGE_UPDATES.items():
    all_urls.add(data['cover'])
    for p_url in data['places'].values():
        all_urls.add(p_url)

broken = []
for i, url in enumerate(sorted(all_urls), 1):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status != 200:
                broken.append((url, resp.status))
    except Exception as e:
        broken.append((url, str(e)))

print(f"Verified {len(all_urls)} image URLs. Total broken: {len(broken)}")
if broken:
    print("Broken URLs:", broken)
