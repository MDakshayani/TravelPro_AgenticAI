import re

# Read indiaTravelData.ts
with open('frontend/src/data/indiaTravelData.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Bihar cover & places:
# Replace coverImage for Bihar
content = re.sub(
    r"(id:\s*'bihar'[\s\S]*?coverImage:\s*')https://images\.unsplash\.com/[^']+",
    r"\1https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?q=80&w=1200",
    content
)

# 2. Update Tripura cover & places:
content = re.sub(
    r"(id:\s*'tripura'[\s\S]*?coverImage:\s*')https://images\.unsplash\.com/[^']+",
    r"\1https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?q=80&w=1200",
    content
)

# 3. Update Punjab cover & places:
content = re.sub(
    r"(id:\s*'punjab'[\s\S]*?coverImage:\s*')https://images\.unsplash\.com/[^']+",
    r"\1https://images.unsplash.com/photo-1588096344356-9b7754b2d1c6?q=80&w=1200",
    content
)

# Fix Punjab place image for Golden Temple / Amritsar from human face (photo-1514222709107-a180c68d72b4)
content = content.replace(
    'https://images.unsplash.com/photo-1514222709107-a180c68d72b4?q=80&w=600',
    'https://images.unsplash.com/photo-1605649487212-47bdab064df7?q=80&w=600'
)

# Fix Agartala place image for Tripura (currently photo-1544735716-392fe2489ffa) to Ujjayanta Palace
content = re.sub(
    r"(name:\s*'Agartala'[\s\S]*?image:\s*')https://images\.unsplash\.com/[^']+",
    r"\1https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?q=80&w=600",
    content
)

# Save updated content back
with open('frontend/src/data/indiaTravelData.ts', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated indiaTravelData.ts successfully.")
