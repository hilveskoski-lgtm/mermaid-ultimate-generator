# Mermaid Renderer Skill

## Description
Renders Mermaid diagrams to PNG, SVG, PDF using headless Chrome (Puppeteer/Playwright) or Mermaid CLI. Supports batch rendering and CI/CD integration.

## Capabilities
- Single file rendering: `mermaid.mmd` → `mermaid.png/svg/pdf`
- Batch rendering: entire vault or folder
- Theme injection (default, dark, forest, neutral, base, custom CSS)
- Configurable output dimensions, background, scale
- Mermaid CLI wrapper (`mmdc`)
- Puppeteer/Playwright headless Chrome for complex diagrams
- Kubernetes job support for scalable rendering
- Watch mode for development
- Obsidian-compatible output (transparency, sizing)

## Usage
```bash
# CLI
python render.py input.mmd -o output.png --theme dark --width 1920

# Batch
python render.py --vault . --output ./renders --format svg

# Kubernetes
kubectl apply -f k8s/render-job.yaml
```

## Files
- `render.py` - Main CLI entry point
- `renderers/` - Backend implementations (mmdc, puppeteer, playwright)
- `k8s/` - Kubernetes Job/CronJob manifests
- `config.yaml` - Default render settings
- `watch.py` - File watcher for live reload