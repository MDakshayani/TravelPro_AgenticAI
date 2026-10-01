import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

with open('frontend/src/data/indiaTravelData.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all image URLs
urls = re.findall(r'https?://[^\s\'\"\`]+', content)
print(f"Total URLs found in data file: {len(urls)}")

unique_urls = list(set(urls))
print(f"Unique URLs: {len(unique_urls)}")

broken = []
for url in unique_urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        res = urllib.request.urlopen(req, timeout=8, context=ctx)
        if res.status != 200:
            broken.append((url, res.status))
    except Exception as e:
        broken.append((url, str(e)))

print(f"\n--- BROKEN URLS ({len(broken)}) ---")
for b in broken:
    print("BROKEN:", b)
