import os
import re

for root, dirs, files in os.walk('frontend/src'):
    for file in files:
        if file.endswith(('.tsx', '.ts')):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
                imgs = re.findall(r'<img[^>]+>', text)
                if imgs:
                    print(f"\n=== {path} ({len(imgs)} <img> tags) ===")
                    for img in imgs[:5]:
                        print("  ", img[:120])
