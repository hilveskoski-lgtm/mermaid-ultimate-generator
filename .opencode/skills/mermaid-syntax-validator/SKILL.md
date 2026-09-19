# Mermaid Syntax Validator Skill

## Description
Validates Mermaid diagram syntax against EBNF grammar rules and best practices. Catches errors before rendering.

## Capabilities
- Parse diagram type, config, nodes, edges, styles
- Validate required elements (diagram type, at least one node, balanced brackets)
- Check ID naming conventions (alphanumeric + underscore, starts with letter)
- Detect duplicate IDs
- Verify edge references point to existing nodes
- Validate theme names
- Check classDef syntax
- **Escape sequence normalization** (\n, \t, \r, \\, \", \') to prevent false duplicate ID detection
- **Bracket-depth tracking** to only parse structural elements (ignore content inside labels)
- **GitHub compatibility checks**: ASCII-only labels, no emojis, no special chars in subgraph labels
- **Markdown extraction** from code blocks for `.md` file validation
- State diagram implicit node detection from edge targets

## Known Limitations
- State diagrams: implicit nodes from edges (e.g., `[*] --> Idle`) not registered as nodes
- Markdown files with embedded mermaid: need `--extract` flag for proper validation
- Finnish/non-ASCII characters in labels: validator accepts but GitHub rendering may fail

## Usage
```bash
# Validate a single file
python validate.py diagram.mmd

# Validate all diagrams in vault
python validate.py --vault .

# Validate with strict mode (warnings as errors)
python validate.py --strict diagram.mmd

# Validate with JSON output
python validate.py --json diagram.mmd

# Validate with markdown extraction
python validate.py --extract diagram.md
```

## Files
- `validate.py` - Main validator script (with escape normalization & bracket-depth tracking)
- `grammar.py` - EBNF grammar definitions, GitHub compatibility rules
- `rules.yaml` - Validation rules configuration
- `test/` - Test fixtures (valid/invalid diagrams)
- `normalize.py` - Escape sequence normalization utilities