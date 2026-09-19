# Mermaid Generator Skill

## Description
Generates valid Mermaid diagram code from structured input (JSON, YAML, natural language prompts, or DSL).

## Capabilities
- Flowchart generator (TD/TB/BT/RL/LR) with node shapes, edges, subgraphs
- Sequence diagram generator with participants, messages, activations, loops, alts
- Class diagram generator with classes, interfaces, relationships, generics
- State diagram generator with states, transitions, composite states
- ER diagram generator with entities, attributes, relationships
- Gantt chart generator with tasks, milestones, dependencies
- Git graph generator with branches, commits, tags
- Theme and style injection
- Output formatting (pretty, compact, minified)
- **GitHub-compatible output**: ASCII-only labels, escape sequence handling, emoji-free
- **Auto-validation pipeline**: validates generated code before output
- **Auto-fix**: corrects common issues (missing diagram type, emojis, encoding)
- **Template registry**: loads from unified template registry with metadata

## GitHub Compatibility Features
- **ASCII-only labels**: auto-replaces non-ASCII chars (ä→a, ö→o, etc.)
- **Escape sequence handling**: converts \n, \t, \r to safe placeholders
- **Emoji stripping**: removes emojis from labels and subgraph names
- **Subgraph label sanitization**: ensures ASCII-only in subgraph labels
- **Escape sequence normalization**: \n, \t, \r, \\, \", \' normalized before output

## Usage
```python
from generator import MermaidGenerator
from validator import GeneratorValidator

gen = MermaidGenerator()
validator = GeneratorValidator()

# Generate with auto-validation
code = gen.flowchart({
    "direction": "TD",
    "nodes": [
        {"id": "A", "shape": "rect", "label": "Start"},
        {"id": "B", "shape": "diamond", "label": "Decision?"}
    ],
    "edges": [
        {"from": "A", "to": "B", "label": "check"}
    ]
})

# Validate and auto-fix
result = GeneratorValidator().validate_and_fix(code)
if not result.valid:
    print("Validation errors:", result.errors)
    code = result.fixed_code  # auto-fixed version
```

## Files
- `generator.py` - Main generator class
- `validator.py` - Validator integration (auto-validate & auto-fix)
- `templates/` - Jinja2 templates per diagram type (with GitHub-compatible patterns)
- `dsl.py` - Internal DSL for programmatic construction
- `prompts/` - Natural language → Mermaid prompt templates
- `templates/REGISTRY.md` - Unified template registry with metadata