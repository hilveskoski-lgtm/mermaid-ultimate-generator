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

## Usage
```python
from generator import MermaidGenerator

gen = MermaidGenerator()
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
```

## Files
- `generator.py` - Main generator class
- `templates/` - Jinja2 templates per diagram type
- `dsl.py` - Internal DSL for programmatic construction
- `prompts/` - Natural language → Mermaid prompt templates