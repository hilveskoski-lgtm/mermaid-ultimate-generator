# Mermaid Obsidian Integration

Automation and tooling for seamless Mermaid workflow in Obsidian.

## Features

| Component | Description |
|-----------|-------------|
| **Plugin Management** | Install/configure recommended plugins |
| **Canvas ↔ Mermaid Sync** | Bidirectional conversion |
| **Live Preview** | Local server with hot reload |
| **Export Pipeline** | Vault → HTML/PDF with rendered diagrams |
| **Dataview Queries** | Query diagrams by type, tags, folder |
| **Template Snippets** | Quick insertion via Templater |
| **Lint on Save** | Auto-validate syntax |

## Quick Start

```bash
# Install recommended plugins
python obsidian_integration.py /path/to/vault --install-plugins

# Convert canvas to mermaid
python obsidian_integration.py /path/to/vault --sync-canvas diagram.canvas --output diagram.mmd

# Convert mermaid to canvas
python obsidian_integration.py /path/to/vault --sync-mermaid diagram.mmd --output diagram.canvas

# Export vault to HTML
python export_pipeline.py /path/to/vault ./output --pdf

# Lint file on save
python obsidian_integration.py /path/to/vault --lint note.md
```

## Recommended Plugins

| Plugin | Purpose |
|--------|---------|
| Mermaid Tools | Render, export, edit diagrams |
| Dataview | Query diagrams (`TABLE type FROM "03-esimerkit"`) |
| Canvas | Visual editing ↔ Mermaid sync |
| Git | Version control for vault |
| Templater | Snippet insertion (`flow`, `seq`, `class`, etc.) |

## Canvas ↔ Mermaid Sync

### Canvas → Mermaid
```python
from obsidian_integration import ObsidianIntegration
integration = ObsidianIntegration(vault_path)
mermaid_code = integration.sync_canvas_to_mermaid(Path("diagram.canvas"))
```

### Mermaid → Canvas
```python
canvas_json = integration.sync_mermaid_to_canvas(Path("diagram.mmd"))
```

## Snippets (Templater)

Type trigger in note:
- `flow` → Basic flowchart
- `seq` → Sequence diagram
- `class` → Class diagram
- `state` → State diagram
- `er` → ER diagram
- `gantt` → Gantt chart
- `git` → Git graph
- `journey` → User journey
- `pie` → Pie chart
- `quad` → Quadrant chart
- `mindmap` → Mindmap
- `kanban` → Kanban board
- `c4context` → C4 Context
- `arch` → Architecture beta

## Dataview Queries

See `dataview_queries.md` for 20+ ready-to-use queries:
- All diagrams by type
- Count by type
- Recent diagrams
- Diagrams with specific patterns
- Health checks
- Dashboard views

## Export Pipeline

```bash
# HTML export (client-side Mermaid rendering)
python export_pipeline.py vault output

# PDF export (requires pandoc + weasyprint)
python export_pipeline.py vault output --pdf
```

## Lint on Save

Add to Templater `on_save` hook or use Obsidian's `QuickAdd`:

```javascript
// QuickAdd macro
const { lint_on_save } = require('mermaid-obsidian-integration');
await lint_on_save(currentFile);
```

## Configuration

```yaml
# .obsidian/plugins/mermaid-tools/data.json
{
  "autoRender": true,
  "exportFormat": "svg",
  "theme": "default"
}
```

## File Structure

```
mermaid-obsidian-integration/
├── obsidian_integration.py    # Main CLI
├── export_pipeline.py         # HTML/PDF export
├── dataview_queries.md        # 20+ Dataview queries
├── snippets/                  # Templater snippets
│   ├── flowchart-basic.md
│   ├── sequence-basic.md
│   ├── class-basic.md
│   ├── state-basic.md
│   ├── er-basic.md
│   ├── gantt-basic.md
│   ├── gitgraph-basic.md
│   ├── journey-basic.md
│   ├── pie-basic.md
│   ├── quadrant-basic.md
│   ├── mindmap-basic.md
│   ├── kanban-basic.md
│   ├── c4context.md
│   └── arch-beta.md
└── hooks/                     # QuickAdd/Obsidian hooks
```

## Requirements

- Python 3.8+
- Obsidian with Community Plugins enabled
- Node.js (for Mermaid CLI, live preview)
- Pandoc + WeasyPrint (for PDF export)

## Integration with Other Skills

- `mermaid-syntax-validator` - Lint on save
- `mermaid-renderer` - Server-side rendering for export
- `mermaid-diagram-templates` - Snippet source
- `mermaid-test-harness` - CI/CD for diagram quality