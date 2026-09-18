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

## Usage
```bash
# Validate a single file
python validate.py diagram.mmd

# Validate all diagrams in vault
python validate.py --vault .
```

## Files
- `validate.py` - Main validator script
- `grammar.py` - EBNF grammar definitions
- `rules.yaml` - Validation rules configuration
- `test/` - Test fixtures (valid/invalid diagrams)