import os
import re

urls = {}
for root, dirs, files in os.walk('frontend/src'):
    for file in files:
        if file.endswith(('.ts', '.tsx', '.json', '.css', '.html')):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
                matches = re.findall(r'https?://[^\s\'\"\`<>]+', text)
                if matches:
                    urls[path] = matches

for path, ulist in urls.items():
    print(f"=== {path} ({len(ulist)} URLs) ===")
    for u in ulist[:5]:
        print("  ", u)
