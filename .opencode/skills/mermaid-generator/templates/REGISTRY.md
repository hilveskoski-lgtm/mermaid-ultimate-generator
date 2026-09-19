# Unified Template Registry

This is the single source of truth for all Mermaid templates in the vault.

## Structure

```
templates/
├── flowchart/
│   ├── basic.md              # Core flowchart template
│   ├── with-subgraphs.md     # Subgraph usage
│   ├── styled.md             # Styling with classDef
│   └── clickable.md          # Clickable nodes/links
├── sequenceDiagram/
│   ├── basic.md              # Basic request-response
│   ├── with-fragments.md     # alt/opt/loop/par
│   └── async.md              # Async communication
├── classDiagram/
│   └── basic.md              # OO design, inheritance, composition
├── stateDiagram/
│   └── basic.md              # States, transitions, composite
├── erDiagram/
│   └── basic.md              # Chen/Crow's foot, cardinality
├── gantt/
│   └── basic.md              # Tasks, milestones, deps, resources
├── gitGraph/
│   └── basic.md              # Branching, merging, tags
├── journey/
│   └── basic.md              # User journey maps
├── pie/
│   └── basic.md              # Pie/donut charts
├── quadrantChart/
│   └── basic.md              # Priority matrices
├── requirementDiagram/
│   └── basic.md              # Requirements traceability
├── c4/
│   ├── context.md            # C4 Context level
│   ├── container.md          # C4 Container level
│   ├── component.md          # C4 Component level
│   └── code.md               # C4 Code level
├── mindmap/
│   └── basic.md              # Mind mapping
├── kanban/
│   └── basic.md              # Kanban boards
├── architecture-beta/
│   └── basic.md              # Architecture diagrams
├── timeline/
│   └── basic.md              # Timelines
├── useCaseDiagram/
│   └── basic.md              # Use case diagrams
├── objectDiagram/
│   └── basic.md              # Object snapshots
├── componentDiagram/
│   └── basic.md              # Component diagrams
├── packageDiagram/
│   └── basic.md              # Package diagrams
├── service-design/
│   └── basic.md              # Service blueprints, journeys
├── timeline/
│   └── basic.md              # Timeline diagrams
├── useCaseDiagram/
│   └── basic.md              # Use case diagrams
├── objectDiagram/
│   └── basic.md              # Object diagrams
├── componentDiagram/
│   └── basic.md              # Component diagrams
├── packageDiagram/
│   └── basic.md              # Package diagrams
├── snippets/                 # Obsidian snippet triggers
│   ├── arch-beta.md
│   ├── c4context.md
│   ├── class-basic.md
│   ├── er-basic.md
│   ├── flowchart-basic.md
│   ├── gantt-basic.md
│   ├── gitgraph-basic.md
│   ├── journey-basic.md
│   ├── kanban-basic.md
│   ├── mindmap-basic.md
│   ├── pie-basic.md
│   ├── quadrant-basic.md
│   ├── sequence-basic.md
│   └── state-basic.md
└── examples/                 # Curated examples from vault
    ├── index.md
    └── flowchart/
        └── basic.md
```

## Template Metadata Schema

Each template should have frontmatter:

```yaml
---
id: flowchart-basic
title: Basic Flowchart
category: flowchart
difficulty: beginner
tags: [basic, decision, loop, subgraph]
description: "Perusvirta (Flowchart) - Kirjautuminen"
tags: [flowchart, beginner, authentication, decision, loop]
mermaidVersion: "10.0"
validated: true
rendered: renders/flowchart-basic.png
liveEditor: https://mermaid.live/edit#...
---
```

## Generator Usage

```python
from generator import MermaidGenerator

gen = MermaidGenerator()

# Load template by ID
template = gen.load_template("flowchart-basic")

# Render with data
output = template.render({
    "direction": "TD",
    "nodes": [...],
    "edges": [...]
})

# Or use registry directly
from registry import TemplateRegistry

registry = TemplateRegistry()
templates = registry.find(category="flowchart", difficulty="beginner")
```

## Validation Status

| Template | Validated | Rendered | Live Editor |
|----------|-----------|----------|-------------|
| flowchart-basic | ✅ | ✅ | [Link](https://mermaid.live/edit#...) |
| sequence-basic | ✅ | ✅ | [Link](https://mermaid.live/edit#...) |
| class-basic | ✅ | ✅ | [Link](https://mermaid.live/edit#...) |
| state-basic | ✅ | ✅ | [Link](https://mermaid.live/edit#...) |
| er-basic | ✅ | ✅ | [Link](https://mermaid.live/edit#...) |
| ... | | | |

*Run `python validate.py --registry` to update*

## Adding New Templates

1. Add `.md` file to appropriate category folder
2. Add frontmatter metadata
2. Run validation: `python validate.py templates/category/new.md`
3. Render: `python render.py templates/category/new.md -o renders/category/new.png`
4. Add to registry index