# Mermaid Diagram Templates Skill

## Description
Curated, tested template library for all 14+ Mermaid diagram types. Each template includes variants, annotations, and rendering verification. All templates are GitHub-compatible (ASCII-only labels, no emojis, escape-sequence-safe).

## Template Categories

### Structural
- `classDiagram/` - OO design, inheritance, composition, generics
- `objectDiagram/` - Instance snapshots, links
- `componentDiagram/` - System components, interfaces, ports
- `packageDiagram/` - Package dependencies, layering
- `useCaseDiagram/` - Actors, use cases, relationships

### Behavioral
- `sequenceDiagram/` - Sync/async messages, lifelines, fragments (alt, opt, loop, par)
- `stateDiagram-v2/` - Simple/composite states, history, choice, junctions
- `activityDiagram/` - Fork/join, swimlanes, pins, expansion regions
- `timeline/` - Periods, events, milestones

### Specialized
- `flowchart/` - All shapes, subgraphs, clickable, styled
- `gantt/` - Tasks, milestones, deps, resources, critical path
- `gitGraph/` - Branches, merges, tags, cherry-pick
- `erDiagram/` - Chen/Crow's foot, cardinality, weak entities
- `journey/` - Sections, tasks, scores, actors
- `pie/` - Simple, donut, labeled, colored
- `quadrantChart/` - Quadrants, points, labels
- `requirementDiagram/` - Requirements, elements, relationships
- `C4Context/` `C4Container/` `C4Component/` `C4Code/` - C4 model levels
- `mindmap/` - Central topic, branches, icons, folding
- `kanban/` - Columns, cards, limits, swimlanes
- `architecture-beta/` - Services, databases, clusters, zones

## GitHub Compatibility Rules
**All templates follow these rules for GitHub rendering compatibility:**

1. **ASCII-only labels**: No non-ASCII characters (ä, ö, etc.) in labels or subgraph names
2. **No emojis**: No emojis in labels, subgraph names, or content
3. **Escape sequences**: Use `<br/>` instead of `\n` in labels; avoid `\t`, `\r`
4. **Subgraph labels**: ASCII-only, no special characters
4. **ASCII arrows**: Use `-->`, `---`, `-.->`, `==>` (not Unicode arrows)
5. **Safe characters**: Only ASCII 32-126 in labels and subgraph names

## Template Metadata (Frontmatter)
```yaml
---
id: flowchart-basic
title: Basic Flowchart
category: flowchart
difficulty: beginner
tags: [basic, decision, loop, subgraph]
description: "Perusvirta (Flowchart) - Kirjautuminen"
mermaidVersion: "10.0"
validated: true
rendered: renders/flowchart-basic.png
liveEditor: https://mermaid.live/edit#...
githubCompatible: true
---
```

## Structure
```
templates/
├── flowchart/
│   ├── basic.md
│   ├── with-subgraphs.md
│   ├── styled.md
│   └── clickable.md
├── sequenceDiagram/
│   ├── basic.md
│   ├── with-fragments.md
│   └── async.md
...
├── snippets/          # Obsidian snippet triggers
│   ├── arch-beta.md
│   ├── c4context.md
│   └── ...
└── examples/          # Curated examples from vault
    ├── index.md
    └── flowchart/
        └── basic.md
```

## Verification
Each template has:
- Rendered PNG/SVG in `renders/`
- Validation status badge (validated with mermaid-syntax-validator)
- Mermaid Live Editor link
- GitHub compatibility badge
- Render test in CI

## Validation Checklist
- [ ] Validates with `mermaid-syntax-validator`
- [ ] Renders without errors locally
- [ ] Renders on GitHub (tested via CI)
- [ ] No non-ASCII in labels/subgraphs
- [ ] No emojis
- [ ] No raw escape sequences in labels
- [ ] Subgraph labels ASCII-only