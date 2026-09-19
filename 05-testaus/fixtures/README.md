# Test Fixtures

Consolidated test fixtures for Mermaid validation and rendering tests.

## Structure

```
fixtures/
├── valid/          # Valid Mermaid diagrams (should pass validation)
└── invalid/        # Invalid diagrams with specific errors (should fail validation)
```

## Valid Fixtures

| File | Diagram Type | Description |
|------|-------------|-------------|
| `class_basic.mmd` | classDiagram | Basic inheritance |
| `er_basic.mmd` | erDiagram | E-commerce ER model |
| `flowchart_basic.mmd` | flowchart | Simple login flow |
| `flowchart_subgraph.mmd` | flowchart | With subgraphs and styling |
| `sequence_basic.mmd` | sequenceDiagram | Request-response with activations |
| `state_basic.mmd` | stateDiagram-v2 | Order state machine |
| `flowchart_variants.md` | flowchart | Multiple flowchart variants |

## Invalid Fixtures

| File | Expected Error |
|------|----------------|
| `duplicate_id.mmd` | Duplicate node ID |
| `invalid_id.mmd` | Invalid node ID (starts with digit) |
| `invalid_theme.mmd` | Unknown theme |
| `no_diagram_type.mmd` | Missing diagram type |
| `unbalanced_brackets.mmd` | Unbalanced brackets |
| `undefined_node.mmd` | Edge references undefined node |

## Usage

```bash
# Validate all
python .opencode/skills/mermaid-syntax-validator/validate.py 05-testaus/fixtures/valid/*.mmd 05-testaus/fixtures/invalid/*.mmd

# Validate only valid (should all pass)
python .opencode/skills/mermaid-syntax-validator/validate.py 05-testaus/fixtures/valid/*.mmd

# Validate only invalid (should all fail)
python .opencode/skills/mermaid-syntax-validator/validate.py 05-testaus/fixtures/invalid/*.mmd
```

## Adding New Fixtures

1. Add `.mmd` file to appropriate folder
2. Follow naming: `{description}_{type}.mmd`
3. For invalid: add expected error in comment at top
3. Run validation to confirm behavior