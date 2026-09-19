import re

with open('03-esimerkit/service-design/daily_process_swimlane.mmd', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all non-ASCII chars
non_ascii = set()
for c in content:
    if ord(c) > 127:
        non_ascii.add(c)

with open('non_ascii.txt', 'w', encoding='utf-8') as f:
    f.write(str(non_ascii))