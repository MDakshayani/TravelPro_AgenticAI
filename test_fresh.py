import urllib.request

test_list = [
    'https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=800',
    'https://images.unsplash.com/photo-1518837695005-2083093ee35b?q=80&w=800',
    'https://images.unsplash.com/photo-1596402184320-417e7178b2cd?q=80&w=800',
    'https://images.unsplash.com/photo-1540555700478-4be289fbecef?q=80&w=800',
    'https://images.unsplash.com/photo-1575550959106-5a7defe28b56?q=80&w=800',
    'https://images.unsplash.com/photo-1544551763-46a013bb70d5?q=80&w=800',
    'https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?q=80&w=800',
    'https://images.unsplash.com/photo-1586375300773-8384e3e4916f?q=80&w=800',
    'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=80&w=800',
    'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=800',
    'https://images.unsplash.com/photo-1548013146-72479768bada?q=80&w=800',
    'https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?q=80&w=800',
    'https://images.unsplash.com/photo-1545569341-9eb8b30979d9?q=80&w=800',
    'https://images.unsplash.com/photo-1571536802807-30451e3955d8?q=80&w=800',
    'https://images.unsplash.com/photo-1514222709107-a180c68d72b4?q=80&w=800'
]

for url in test_list:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=4)
        print(f"200 OK: {url}")
    except Exception as e:
        print(f"FAIL ({e}): {url}")
