# Mermaid ASCII Sanitizer Skill

## Description
Standalone utility to sanitize Mermaid diagram code for GitHub-compatible rendering. Removes emojis, replaces non-ASCII characters, normalizes escape sequences, and sanitizes subgraph labels.

## Capabilities
- **Emoji stripping**: Removes all emojis from labels, subgraph names, and content
- **Non-ASCII replacement**: Replaces non-ASCII characters with ASCII equivalents (ä→a, ö→o, ü→u, ß→ss, etc.)
- **Escape sequence normalization**: Converts \n, \t, \r, \\, \", \' to safe placeholders or spaces
- **Subgraph label sanitization**: Ensures ASCII-only in subgraph labels
- **Label sanitization**: Replaces non-ASCII in all label types (rect, rounded, diamond, etc.)
- **Escape sequence normalization**: \n, \t, \r, \\, \", \' → safe placeholders
- **Emoji stripping**: Complete emoji removal from all content
- **GitHub-compatible output**: Guaranteed to render on GitHub

## Supported Replacements

### Non-ASCII Characters
| Char | Replacement | Char | Replacement |
|------|-------------|------|-------------|
| ä, Ä | a, A | ö, Ö | o, O |
| ü, Ü | u, U | ß | ss |
| å, Å | a, A | ø, Ø | o, O |
| é, É | e, E | ñ, Ñ | n, N |
| ç, Ç | c, C | etc. | ... |

### Escape Sequences
| Sequence | Replacement |
|----------|-------------|
| `\n` | `<br/>` or space |
| `\t` | space |
| `\r` | space |
| `\\` | `\` |
| `\"` | `"` |
| `\'` | `'` |

### Emojis
Complete removal (all Unicode emoji ranges)

## Usage

### CLI
```bash
# Sanitize single file
python sanitize.py input.mmd -o output.mmd

# Sanitize with options
python sanitize.py input.mmd -o output.mmd --replace-non-ascii --strip-emojis --normalize-escapes

# Sanitize stdin
cat diagram.mmd | python sanitize.py -o output.mmd
```

### Python API
```python
from sanitizer import MermaidSanitizer

sanitizer = MermaidSanitizer(
    replace_non_ascii=True,
    strip_emojis=True,
    normalize_escapes=True,
    newline_replacement="<br/>"
)

# Sanitize string
clean_code = sanitizer.sanitize(mermaid_code)

# Sanitize file
sanitizer.sanitize_file("input.mmd", "output.mmd")

# Check if sanitization needed
if sanitizer.needs_sanitization(code):
    clean_code = sanitizer.sanitize(code)
```

### Obsidian Integration
```python
# Hook for Obsidian on-save
from sanitizer import MermaidSanitizer

sanitizer = MermaidSanitizer()

def on_save(file_path):
    if file_path.suffix in ['.mmd', '.md']:
        with open(file_path) as f:
            content = f.read()
        if sanitizer.needs_sanitization(content):
            clean = sanitizer.sanitize(content)
            with open(file_path, 'w') as f:
                f.write(clean)
```

## Configuration
```python
sanitizer = MermaidSanitizer(
    replace_non_ascii=True,      # Replace non-ASCII chars
    ascii_replacements={         # Custom replacements
        'ä': 'a', 'ö': 'o', 'ü': 'u',
        'Ä': 'A', 'Ö': 'O', 'Ü': 'U',
        'ß': 'ss', '€': 'EUR',
    },
    strip_emojis=True,           # Remove all emojis
    normalize_escapes=True,      # Normalize \n, \t, etc.
    newline_replacement="<br/>", # Replacement for \n
    tab_replacement="  ",        # Replacement for \t
    subgraph_only=False,         # Sanitize only subgraph labels
)
```

## GitHub Actions Integration
```yaml
- name: Sanitize diagrams
  run: |
    python -m sanitizer --vault . --output ./sanitized
```

## Files
- `sanitizer.py` - Main sanitizer class
- `replacements.py` - Character replacement maps
- `cli.py` - CLI entry point
- `test_sanitizer.py` - Tests