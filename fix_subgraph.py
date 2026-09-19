import re

with open('daily_process_swimlane.mmd', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Finnish characters in subgraph labels with ASCII equivalents
replacements = {
    'Työntekijä': 'Työntekijä',
    'Työmaapäällikkö': 'Tyomaapallikko',
    'Turvallisuus': 'Turvallisuus',
    'Suunnittelija': 'Suunnittelija',
    'ILTAPÄIVÄ': 'ILTAPAIVA',
}

for old, new in replacements.items():
    content = content.replace(old, new)

# Fix subgraph labels - replace special chars in labels
def fix_label(match):
    label = match.group(2)
    # Replace Finnish chars with ASCII
    label = label.replace('ö', 'o').replace('ä', 'a').replace('Ö', 'O').replace('Ä', 'A')
    return f'subgraph {match.group(1)}["{label}"]'

content = re.sub(r'subgraph\s+(\w+)\["([^\"]*)"\]', fix_label, content)

with open('daily_process_swimlane.mmd', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed subgraph labels')