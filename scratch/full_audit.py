import os
import re
import urllib.request
from collections import defaultdict

def check_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status
    except Exception as e:
        return str(e)

print("=== AUDITING ALL FILES IN FRONTEND ===")
url_file_map = defaultdict(list)
all_urls = set()
url_regex = re.compile(r'https://images\.unsplash\.com/photo-[a-zA-Z0-9\-_?=&\.]+')

frontend_dir = os.path.join('frontend', 'src')
for root, dirs, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith('.ts') or f.endswith('.tsx'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file_obj:
                content = file_obj.read()
                matches = url_regex.findall(content)
                for m in matches:
                    clean_url = m.strip('"\'`,;')
                    url_file_map[clean_url].append(filepath)
                    all_urls.add(clean_url)

print(f"Found {len(all_urls)} unique Unsplash image URLs.\n")

results = {}
for i, url in enumerate(sorted(all_urls), 1):
    status = check_url(url)
    results[url] = status
    print(f"[{i}/{len(all_urls)}] [{status}] {url}")

print("\n=== SUMMARY OF BROKEN URLS (Non-200) ===")
broken_count = 0
for url, st in results.items():
    if st != 200:
        broken_count += 1
        print(f"BROKEN [{st}]: {url}")
        for f in url_file_map[url]:
            print(f"   in file: {f}")

if broken_count == 0:
    print("No broken URLs found!")

print("\n=== SEARCHING FOR TAMIL NADU REFERENCES ACROSS CODEBASE ===")
for root, dirs, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith('.ts') or f.endswith('.tsx'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file_obj:
                text = file_obj.read()
                if 'tamil' in text.lower():
                    print(f"Tamil Nadu reference found in: {filepath}")
