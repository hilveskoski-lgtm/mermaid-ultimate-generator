import re

with open('03-esimerkit/service-design/daily_process_swimlane.mmd', 'r', encoding='utf-8') as f:
    content = f.read()

def fix_label(match):
    label = match.group(2)
    label = label.replace('ö', 'o').replace('ä', 'a').replace('Ö', 'O').replace('Ä', 'A')
    return f'subgraph {match.group(1)}["{label}"]'

content = re.sub(r'subgraph\s+(\w+)\["([^\"]*)"\]', fix_label, content)

with open('03-esimerkit/service-design/daily_process_swimlane.mmd', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed 03-esimerkit version')