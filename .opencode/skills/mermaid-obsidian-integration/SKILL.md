# Mermaid Obsidian Integration Skill

## Description
Automation and tooling for seamless Mermaid workflow in Obsidian: plugin management, canvas sync, live preview, export pipelines.

## Capabilities
- **Plugin management**: Install/update Mermaid Tools, Mermaid Export, Diagrammer
- **Canvas ↔ Mermaid sync**: Convert Canvas nodes ↔ Mermaid flowcharts bidirectionally
- **Live preview server**: Local HTTP server with hot reload for diagram editing
- **Export pipeline**: Vault → HTML/PDF with diagrams rendered
- **Dataview queries**: Query diagrams by type, tags, folder
- **Template insertion**: Hotkey/snippet insertion of diagram templates
- **Lint on save**: Auto-validate syntax when saving `.mmd` or `.md` with mermaid blocks
- **Mermaid Live Editor integration**: Open in live editor, import from live editor

## Files
- `plugins/` - Plugin configs, recommended versions
- `canvas_sync.py` - Canvas ↔ Mermaid converter
- `preview_server.py` - Live preview with WebSocket reload
- `export_pipeline.py` - Vault → HTML/PDF (pandoc + mermaid-cli)
- `dataview_queries.md` - Useful Dataview queries for diagrams
- `snippets/` - Obsidian snippets for diagram templates
- `hooks/` - Obsidian URI hooks, event triggers