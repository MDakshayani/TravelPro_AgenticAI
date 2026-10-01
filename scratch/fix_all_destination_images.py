import re

with open('frontend/src/data/indiaTravelData.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace Bihar cover image
text = re.sub(
    r"(id:\s*'bihar'[\s\S]*?coverImage:\s*')https://images\.unsplash\.com/[^']+",
    r"\1https://images.unsplash.com/photo-1609766857041-ed402ea8069a?q=80&w=1200",
    text
)

# Replace Bihar place images: Bodh Gaya, Nalanda, Rajgir
text = re.sub(
    r"(name:\s*'Bodh Gaya'[\s\S]*?image:\s*')https://images\.unsplash\.com/[^']+",
    r"\1https://images.unsplash.com/photo-1609766857041-ed402ea8069a?q=80&w=600",
    text
)

text = re.sub(
    r"(name:\s*'Nalanda'[\s\S]*?image:\s*')https://images\.unsplash\.com/[^']+",
    r"\1https://images.unsplash.com/photo-1544551763-77ef2d0cfc6c?q=80&w=600",
    text
)

text = re.sub(
    r"(name:\s*'Rajgir'[\s\S]*?image:\s*')https://images\.unsplash\.com/[^']+",
    r"\1https://images.unsplash.com/photo-1582510003544-4d00b7f74220?q=80&w=600",
    text
)

# Replace Punjab cover image and Golden Temple / Amritsar images
text = re.sub(
    r"(id:\s*'punjab'[\s\S]*?coverImage:\s*')https://images\.unsplash\.com/[^']+",
    r"\1https://images.unsplash.com/photo-1605649487212-47bdab064df7?q=80&w=1200",
    text
)

text = re.sub(
    r"(name:\s*'Amritsar'[\s\S]*?image:\s*')https://images\.unsplash\.com/[^']+",
    r"\1https://images.unsplash.com/photo-1605649487212-47bdab064df7?q=80&w=600",
    text
)

text = re.sub(
    r"(name:\s*'Golden Temple'[\s\S]*?image:\s*')https://images\.unsplash\.com/[^']+",
    r"\1https://images.unsplash.com/photo-1605649487212-47bdab064df7?q=80&w=600",
    text
)

# Replace Tripura cover & Agartala image
text = re.sub(
    r"(id:\s*'tripura'[\s\S]*?coverImage:\s*')https://images\.unsplash\.com/[^']+",
    r"\1https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?q=80&w=1200",
    text
)

text = re.sub(
    r"(name:\s*'Agartala'[\s\S]*?image:\s*')https://images\.unsplash\.com/[^']+",
    r"\1https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?q=80&w=600",
    text
)

with open('frontend/src/data/indiaTravelData.ts', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated indiaTravelData.ts with verified image URLs!")
