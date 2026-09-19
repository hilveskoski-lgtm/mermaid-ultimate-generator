# Mermaid Test Harness Skill

## Description
Testing framework for Mermaid diagrams: golden master comparison, regression detection, syntax validation, render verification. Includes GitHub-compatible testing.

## Capabilities
- Golden master testing: compare rendered output against approved baselines
- Syntax validation test suite (valid/invalid fixtures)
- Render regression detection (pixel diff, structural diff)
- Property-based testing for generator output
- CI/CD integration (GitHub Actions, GitLab CI)
- Test coverage reporting
- Snapshot management (update, approve, reject)
- **GitHub-compatible test fixtures**: ASCII-only, no emojis, escape-safe
- **Escape sequence test fixtures**: \n, \t, \r, \\, \", \' in labels
- **Subgraph label tests**: ASCII-only, non-ASCII rejection
- **Emoji rejection tests**: emoji in labels/subgraphs should fail

## Test Types
1. **Syntax Tests** - Validate parser accepts/rejects correctly
2. **Render Tests** - Compare PNG/SVG output to golden masters
3. **Generator Tests** - Round-trip: input → Mermaid → parse → verify
3. **Integration Tests** - Obsidian plugin compatibility
4. **GitHub Compatibility Tests** - ASCII-only, no emojis, escape-safe

## Fixture Categories
| Category | Location | Purpose |
|----------|----------|---------|
| Valid | `fixtures/valid/` | Should parse & render |
| Invalid | `fixtures/invalid/` | Should fail validation |
| Escape sequences | `fixtures/escapes/` | \n, \t, \r, \\, \", \' in labels |
| Non-ASCII | `fixtures/non-ascii/` | Should be sanitized |
| Emoji | `fixtures/emoji/` | Should be rejected/stripped |

## Fixture Metadata (Frontmatter)
```yaml
---
id: flowchart-basic
type: flowchart
status: valid
githubCompatible: true
expectedNodes: 5
expectedEdges: 2
tags: [basic, decision, loop]
---
```

## CI/CD Integration
```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install pytest
      - run: pytest tests/ --vault .
      - run: pytest tests/ --github-compat
```

## Usage
```bash
# Run all tests
pytest tests/

# Update golden masters
pytest tests/ --update-golden

# Visual diff report
pytest tests/ --visual-diff

# GitHub compatibility tests only
pytest tests/ -k "github_compat"

# Run with coverage
pytest tests/ --cov=validator --cov-report=html
```

## Fixture Consolidation
Fixtures consolidated from:
- `.opencode/skills/mermaid-syntax-validator/test/fixtures/`
- `.opencode/skills/mermaid-test-harness/fixtures/`

Into single source: `05-testaus/fixtures/`