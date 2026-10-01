import re

with open('frontend/src/pages/SmartCalendarPage.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'name:\s*[\'\"]([^\'\"]+)[\'\"][\s\S]*?image:\s*[\'\"]([^\'\"]+)[\'\"]', text)
for name, img in matches:
    print(f"Calendar Sample: {name} -> {img}")
