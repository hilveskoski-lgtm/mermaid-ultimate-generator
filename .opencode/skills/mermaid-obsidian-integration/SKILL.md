# Mermaid Obsidian Integration Skill

## Description
Automation and tooling for seamless Mermaid workflow in Obsidian: plugin management, canvas sync, live preview, export pipelines. Includes GitHub-compatible sync and sanitization.

## Capabilities
- **Plugin management**: Install/update Mermaid Tools, Mermaid Export, Diagrammer
- **Canvas ↔ Mermaid sync**: Convert Canvas nodes ↔ Mermaid flowcharts bidirectionally
- **Live preview server**: Local HTTP server with hot reload for diagram editing
- **Export pipeline**: Vault → HTML/PDF with diagrams rendered
- **Dataview queries**: Query diagrams by type, tags, folder
- **Template insertion**: Hotkey/snippet insertion of diagram templates
- **Lint on save**: Auto-validate syntax when saving `.mmd` or `.md` with mermaid blocks
- **Mermaid Live Editor integration**: Open in live editor, import from live editor
- **GitHub-compatible sync**: ASCII-safe labels, emoji stripping for GitHub rendering
- **Canvas ↔ GitHub sync**: Bidirectional sync with GitHub-compatible label sanitization

## GitHub Compatibility Features
- **Label sanitization on save**: Auto-replace non-ASCII chars in labels
- **Emoji stripping**: Remove emojis from labels and subgraph names on save
- **Escape sequence normalization**: Convert `\n`, `\t` to safe placeholders
- **Subgraph label sanitization**: ASCII-only subgraph labels
- **Snippet sanitization**: Templates auto-sanitized on insertion

## Files
- `plugins/` - Plugin configs, recommended versions
- `canvas_sync.py` - Canvas ↔ Mermaid converter
- `sanitizer.py` - GitHub-compatible sanitization (emoji strip, ASCII labels, escape handling)
- `preview_server.py` - Live preview with WebSocket reload
- `export_pipeline.py` - Vault → HTML/PDF (pandoc + mermaid-cli)
- `dataview_queries.md` - Useful Dataview queries for diagrams
- `snippets/` - Obsidian snippets for diagram templates (sanitized)
- `hooks/` - Obsidian URI hooks, event triggers (lint on save, auto-sanitize)