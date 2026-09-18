# Mermaid Test Harness Skill

## Description
Testing framework for Mermaid diagrams: golden master comparison, regression detection, syntax validation, render verification.

## Capabilities
- Golden master testing: compare rendered output against approved baselines
- Syntax validation test suite (valid/invalid fixtures)
- Render regression detection (pixel diff, structural diff)
- Property-based testing for generator output
- CI/CD integration (GitHub Actions, GitLab CI)
- Test coverage reporting
- Snapshot management (update, approve, reject)

## Test Types
1. **Syntax Tests** - Validate parser accepts/rejects correctly
2. **Render Tests** - Compare PNG/SVG output to golden masters
3. **Generator Tests** - Round-trip: input → Mermaid → parse → verify
4. **Integration Tests** - Obsidian plugin compatibility

## Structure
```
tests/
├── fixtures/
│   ├── valid/          # Should parse & render
│   └── invalid/        # Should fail validation
├── golden/
│   ├── flowchart/
│   ├── sequenceDiagram/
│   └── ...
├── snapshots/          # Current render outputs
├── conftest.py         # Pytest configuration
├── test_syntax.py
├── test_render.py
├── test_generator.py
└── test_integration.py
```

## Usage
```bash
# Run all tests
pytest tests/

# Update golden masters
pytest tests/ --update-golden

# Visual diff report
pytest tests/ --visual-diff
```