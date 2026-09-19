# Mermaid Renderer Skill

## Description
Renders Mermaid diagrams to PNG, SVG, PDF using headless Chrome (Puppeteer/Playwright) or Mermaid CLI. Supports batch rendering and CI/CD integration. Includes GitHub-compatible rendering mode.

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
- **GitHub-compatible rendering**: ASCII-safe output, emoji stripping, escape handling
- **GitHub Actions integration**: CI/CD rendering with artifact upload
- **Visual regression testing**: pixel-diff against baseline

## GitHub-Compatible Rendering Mode
```bash
# GitHub-compatible render (ASCII-safe, emoji-free)
python render.py input.mmd -o output.png --github-compat

# With custom sanitization
python render.py input.mmd -o output.png --github-compat --sanitize-labels --strip-emojis
```

## GitHub Actions Integration
```yaml
# .github/workflows/render.yml
- name: Render diagrams
  run: |
    python render.py --vault . --output ./renders --format png --github-compat
```

## Files
- `render.py` - Main CLI entry point
- `renderers/` - Backend implementations (mmdc, puppeteer, playwright)
- `sanitizer.py` - GitHub-compatible sanitization (emoji strip, ASCII labels, escape handling)
- `k8s/` - Kubernetes Job/CronJob manifests
- `config.yaml` - Default render settings
- `watch.py` - File watcher for live reload