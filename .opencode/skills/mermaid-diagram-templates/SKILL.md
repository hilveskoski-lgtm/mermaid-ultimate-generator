# Mermaid Diagram Templates Skill

## Description
Curated, tested template library for all 14+ Mermaid diagram types. Each template includes variants, annotations, and rendering verification.

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
```

## Verification
Each template has:
- Rendered PNG/SVG in `renders/`
- Validation status badge
- Mermaid Live Editor link