# Mermaid Syntax-to-Template Converter Skill

## Description
Converts Mermaid syntax documentation (EBNF grammar, syntax docs) into generator template parameters. Automatically extracts template parameters from grammar rules and syntax documentation.

## Capabilities
- **EBNF → Template params**: Converts grammar rules to template parameter schemas
- **Syntax docs → Template params**: Extracts template variables from syntax documentation
- **Diagram type mapping**: Maps 14+ diagram types to template parameter schemas
- **Node/edge shape extraction**: Extracts valid shapes, edge types, attributes per diagram type
- **Config option extraction**: Extracts valid config options (themes, directions, etc.)
- **Validation rule extraction**: Converts grammar constraints to validation rules
- **Template generation**: Generates Jinja2 template skeletons from grammar

## Input Sources
1. **Grammar files** (`.pegjs`, `.ebnf`, `.bnf`) - formal grammar definitions
2. **Syntax docs** (`.md`) - syntax documentation with examples
3. **Mermaid.js source** - TypeScript definitions from mermaid.js repo
4. **Examples** - Curated examples from vault

## Output
- **Template parameter schemas** (JSON Schema)
- **Jinja2 template skeletons** (`.j2` files)
- **Validation rules** (JSON)
- **TypeScript interfaces** (for generator)
- **Documentation** (Markdown)

## Grammar → Template Mapping

### Example: Flowchart Grammar → Template

**Grammar Rule:**
```
flowchart = "flowchart" direction? node* edge* style* click* comment*
direction = "TD" | "TB" | "BT" | "RL" | "LR"
node = nodeId nodeShape? label?
nodeShape = "[" | "(" | "{" | "((" | ">]" | "[/" | "[\\" | "[[\"" | "[(\"" | "[/\""
edge = nodeId edgeType nodeId label?
edgeType = "-->" | "---" | "-.->" | "==>"
```

**Generated Template Params:**
```json
{
  "type": "object",
  "properties": {
    "direction": {
      "type": "string",
      "enum": ["TD", "TB", "BT", "RL", "LR"],
      "default": "TD"
    },
    "nodes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string", "pattern": "^[A-Za-z][A-Za-z0-9_]*$" },
          "label": { "type": "string" },
          "shape": {
            "type": "string",
            "enum": ["rect", "rounded", "diamond", "circle", "asymmetric", "parallelogram", "subroutine", "cylindrical"]
          }
        },
        "required": ["id"]
      }
    },
    "edges": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "from": { "type": "string" },
          "to": { "type": "string" },
          "label": { "type": "string" },
          "type": {
            "type": "string",
            "enum": ["arrow", "line", "dotted", "thick"]
          }
        },
        "required": ["from", "to"]
      }
    }
  },
  "required": ["nodes"]
}
```

## Syntax Docs → Template Params

### Input: `02-syntaksi/flowchart.md`
```markdown
## 4. Solmut (Nodes)

#### Flowchart
`id[teksti]`           # suorakulmio
`id(teksti)`           # pyöristetty
`id{teksti}`           # rombi (besluit)
```

### Extracted Template Params
```json
{
  "nodeShapes": {
    "rect": { "pattern": "id[label]", "description": "suorakulmio" },
    "rounded": { "pattern": "id(label)", "description": "pyöristetty" },
    "diamond": { "pattern": "id{label}", "description": "rombi (besluit)" }
  }
}
```

## Architecture

```
syntax-to-template/
├── parser/
│   ├── ebnf_parser.py      # PEG.js/EBNF parser
│   ├── markdown_parser.py  # Syntax docs parser
│   └── typescript_parser.py # TS definitions parser
├── extractor/
│   ├── param_extractor.py  # Extract template params
│   ├── shape_extractor.py  # Extract node/edge shapes
│   └── config_extractor.py # Extract config options
├── generator/
│   ├── template_generator.py # Generate .j2 templates
│   ├── schema_generator.py   # Generate JSON schemas
│   └── validation_generator.py # Generate validation rules
├── cli.py
└── main.py
```

## Usage

### CLI
```bash
# From grammar file
python syntax_to_template.py grammar.ebnf -o templates/

# From syntax docs
python syntax_to_template.py docs/02-syntaksi/ -o templates/

# From Mermaid.js source
python syntax_to_template.py --mermaid-source ../mermaid-js --output templates/

# Generate all
python syntax_to_template.py --all --output templates/
```

### Python API
```python
from syntax_to_template import SyntaxToTemplate

converter = SyntaxToTemplate()

# From grammar
templates = converter.from_grammar("grammar.ebnf")

# From syntax docs
templates = converter.from_docs("docs/02-syntaksi/")

# From Mermaid.js source
templates = converter.from_mermaid_source("../mermaid-js")

# Generate all outputs
converter.generate_all(
    templates,
    output_dir="templates/",
    generate_jinja2=True,
    generate_schema=True,
    generate_validation=True,
    generate_typescript=True
)
```

## Output Structure

```
templates/
├── flowchart/
│   ├── template.j2          # Jinja2 template
│   ├── schema.json          # JSON Schema for params
│   ├── validation.json      # Validation rules
│   └── types.ts             # TypeScript interfaces
├── sequenceDiagram/
│   ├── template.j2
│   ├── schema.json
│   ├── validation.json
│   └── types.ts
└── registry.json            # Master registry
```

## Registry Format
```json
{
  "version": "1.0",
  "generated": "2024-01-15T10:30:00Z",
  "diagramTypes": {
    "flowchart": {
      "template": "flowchart/template.j2",
      "schema": "flowchart/schema.json",
      "validation": "flowchart/validation.json",
      "params": { ... }
    }
  }
}
```

## Integration with Generator

```python
from generator import MermaidGenerator
from syntax_to_template import SyntaxToTemplate

# Auto-load templates from registry
converter = SyntaxToTemplate()
registry = converter.load_registry("templates/registry.json")

gen = MermaidGenerator(registry=registry)

# Generator now uses auto-generated templates
code = gen.flowchart(data)
```

## Files
- `parser/` - Grammar and doc parsers
- `extractor/` - Parameter extractors
- `generator/` - Template/code generators
- `cli.py` - CLI entry point
- `main.py` - Main entry point