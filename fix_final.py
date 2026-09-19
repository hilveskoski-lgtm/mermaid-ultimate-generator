import re

with open('03-esimerkit/service-design/daily_process_swimlane.mmd', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all remaining non-ASCII with ASCII equivalents
replacements = {
    'ö': 'o',
    'ä': 'a',
    'Ö': 'O',
    'Ä': 'A',
    '→': '->',
}

for old, new in replacements.items():
    content = content.replace(old, new)

# Also fix any remaining in subgraph labels
def fix_label(match):
    label = match.group(2)
    for old, new in replacements.items():
        label = label.replace(old, new)
    return f'subgraph {match.group(1)}["{label}"]'

content = re.sub(r'subgraph\s+(\w+)\["([^\"]*)"\]', fix_label, content)

with open('03-esimerkit/service-design/daily_process_swimlane.mmd', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed all non-ASCII')