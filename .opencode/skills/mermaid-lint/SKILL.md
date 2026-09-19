# Mermaid Lint Skill

## Description
Linter for Mermaid diagrams with GitHub-compatible rules. Integrates with Obsidian, VS Code, CLI, and CI/CD. Enforces best practices, GitHub rendering compatibility, and diagram quality.

## Rules

### Core Rules (Always Enforced)

| Rule ID | Name | Description | Severity |
|---------|------|-------------|----------|
| `ML001` | `missing-diagram-type` | Diagram must start with valid type | Error |
| `ML002` | `no-nodes` | At least one node required | Error |
| `ML003` | `unbalanced-brackets` | Brackets must be balanced | Error |
| `ML004` | `invalid-node-id` | Node IDs: alphanumeric + underscore, start with letter | Error |
| `ML005` | `duplicate-node-id` | No duplicate node IDs | Error |
| `ML006` | `undefined-node-ref` | Edge references must exist | Error |
| `ML007` | `unbalanced-parentheses` | Parentheses must be balanced | Error |
| `ML008` | `unbalanced-braces` | Braces must be balanced | Error |
| `ML009` | `invalid-arrow-type` | Valid arrow types only | Error |

### GitHub Compatibility Rules (Recommended)

| Rule ID | Name | Description | Severity |
|---------|------|-------------|----------|
| `ML101` | `non-ascii-label` | Labels must be ASCII-only | Warning |
| `ML102` | `emoji-in-label` | No emojis in labels | Warning |
| `ML103` | `raw-escape-sequence` | Raw `\n`, `\t`, `\r` in labels | Warning |
| `ML104` | `non-ascii-subgraph` | Subgraph labels must be ASCII-only | Warning |
| `ML105` | `emoji-in-subgraph` | No emojis in subgraph names | Warning |
| `ML106` | `unicode-arrow` | Use ASCII arrows (`-->`, not `→`) | Warning |
| `ML107` | `non-ascii-click` | Click URLs must be ASCII | Warning |

### Best Practice Rules (Optional)

| Rule ID | Name | Description | Severity |
|---------|------|-------------|----------|
| `ML201` | `isolated-node` | Node with no edges | Info |
| `ML202` | `long-label` | Label > 50 chars | Info |
| `ML203` | `missing-direction` | Flowchart missing TD/TB/BT/RL/LR | Info |
| `ML204` | `unused-classdef` | Defined but unused classDef | Info |
| `ML205` | `deep-nesting` | Subgraph nesting > 3 levels | Info |
| `ML206` | `complex-subgraph` | Subgraph with > 20 nodes | Info |

## Configuration

### `.mermaid-lint.yml`
```yaml
# Extend default rules
extends: "recommended"

# Rule severity overrides
rules:
  ML001: error
  ML002: error
  ML101: warning    # non-ascii-label
  ML102: warning    # emoji-in-label
  ML103: warning    # raw-escape-sequence
  ML104: warning    # non-ascii-subgraph
  ML105: warning    # emoji-in-subgraph
  ML201: info       # isolated-node
  ML202: off        # long-label (disable)

# Custom replacements for non-ASCII
ascii_replacements:
  ä: a
  ö: o
  ü: u
  ß: ss
  Ä: A
  Ö: O
  Ü: U
  €: EUR

# Ignore patterns
ignore:
  - "node_modules/**"
  - ".git/**"
  - "*.backup.mmd"

# Per-file overrides
overrides:
  - files: ["**/drafts/**"]
    rules:
      ML101: off
      ML102: off
```

## Usage

### CLI
```bash
# Lint single file
mermaid-lint diagram.mmd

# Lint with config
mermaid-lint --config .mermaid-lint.yml diagram.mmd

# Lint entire vault
mermaid-lint --vault .

# Auto-fix (where possible)
mermaid-lint --fix diagram.mmd

# JSON output for CI
mermaid-lint --json diagram.mmd

# GitHub compatibility check only
mermaid-lint --github-compat diagram.mmd
```

### Editor Integration

#### VS Code
```json
// .vscode/settings.json
{
  "mermaid-lint.enable": true,
  "mermaid-lint.configPath": ".mermaid-lint.yml",
  "mermaid-lint.run": "onSave",
  "mermaid-lint.autoFix": true
}
```

#### Obsidian
```javascript
// QuickAdd macro or Templater script
const { lint, fix } = require('mermaid-lint');

async function onSave(file) {
  if (file.ext === 'mmd' || file.ext === 'md') {
    const content = await file.read();
    const results = await lint(content, { config: '.mermaid-lint.yml' });
    
    if (results.errors.length > 0) {
      new Notice(`Mermaid lint: ${results.errors.length} errors`);
      // Show in problems panel
    }
    
    if (results.fixable) {
      await file.write(results.fixedCode);
    }
  }
```

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/lint.yml
name: Mermaid Lint
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install mermaid-lint
      - run: mermaid-lint --vault . --strict
```

### GitLab CI
```yaml
# .gitlab-ci.yml
mermaid_lint:
  image: python:3.11
  script:
    - pip install mermaid-lint
    - mermaid-lint --vault . --json > lint-report.json
  artifacts:
    reports:
      sast: lint-report.json
```

## IDE Integration

### VS Code Extension
```json
// package.json contributes
{
  "commands": [
    { "command": "mermaid-lint.lint", "title": "Lint Mermaid" },
    { "command": "mermaid-lint.fix", "title": "Fix Mermaid" }
  ],
  "keybindings": [
    { "key": "ctrl+shift+m", "command": "mermaid-lint.lint" }
  ]
}
```

### Neovim (null-ls)
```lua
-- lua/plugins/null-ls.lua
local null_ls = require("null-ls")
null_ls.setup({
  sources = {
    null_ls.builtins.diagnostics.mermaid_lint,
    null_ls.builtins.code_actions.mermaid_lint_fix,
  },
})
```

## Auto-Fix Capabilities

| Rule | Auto-Fixable |
|------|--------------|
| `ML101` non-ascii-label | ✅ Replace with ASCII |
| `ML102` emoji-in-label | ✅ Strip emoji |
| `ML103` raw-escape-sequence | ✅ Normalize escapes |
| `ML104` non-ascii-subgraph | ✅ Replace with ASCII |
| `ML105` emoji-in-subgraph | ✅ Strip emoji |
| `ML106` unicode-arrow | ✅ Replace with ASCII |
| `ML004` invalid-node-id | ❌ Manual |
| `ML005` duplicate-node-id | ❌ Manual |
| `ML006` undefined-node-ref | ❌ Manual |

## Files
- `lint.py` - Main linter engine
- `rules/` - Rule implementations
- `config.py` - Configuration loader
- `fixer.py` - Auto-fix engine
- `cli.py` - CLI entry point
- `integrations/` - Editor/IDE integrations