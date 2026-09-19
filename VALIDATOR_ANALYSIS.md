# Mermaid Syntax Validator - Bug Analysis & Fix

## Root Cause

The validator incorrectly identified **Finnish words inside labels as node IDs** due to escape sequences (`\n`, `\t`, etc.) inside labels creating fake word boundaries.

### The Real Bug: Escape Sequences Creating Fake Word Boundaries

**Example:** Label `tehtava\n(Mobile: Start Task)` contains literal `\n` (two characters: backslash + n).

The regex `ID_PATTERN = [A-Za-z][A-Za-z0-9_]*` matched `n` from the literal `\n` sequence because:
- Backslash `\` is NOT a word character
- `n` IS a word character (matches `[A-Za-z]`)
- The rounded pattern `NodeID\(Label\)` matched `n(Mobile` from `\n(Mobile`

**Evidence:**
```
ERROR  [38:19] Duplicate node ID: n
ERROR  [40:30] Duplicate node ID: n
```
Line 38: `WB1[Aloita tehtava\n(Mobile: Start Task)]` → regex matched `n` from `\n`
Line 40: `WB3 -->|Ei| WB4[Ilmoita puute\n(Mobile: Block Task)]` → matched `n` from `\n`

## The Fix: Escape Sequence Normalization

Added `_normalize_escapes()` method that replaces escape sequences with non-printable placeholders BEFORE parsing:

```python
def _normalize_escapes(self, line: str) -> str:
    escape_patterns = [
        (r'\\n', '\x01'),   # \n -> placeholder
        (r'\\t', '\x02'),   # \t -> placeholder
        (r'\\r', '\x03'),   # \r -> placeholder
        (r'\\\\', '\x04'),  # \\ -> placeholder
        (r'\\"', '\x05'),   # \" -> placeholder
        (r"\\'", '\x06'),   # \' -> placeholder
    ]
    # Replace each escape sequence with unique placeholder
    # Parse on normalized line
    # (No need to restore for validation)
```

**Applied to:**
- `_parse_flowchart_nodes()` - normalizes before node parsing
- `_parse_flowchart_edges()` - normalizes before edge parsing

## Results

All main diagram files now pass validation:

| File | Status | Nodes | Edges |
|------|--------|-------|-------|
| `daily_process_swimlane.mmd` | ✅ VALID | 90 | 30 |
| `daily_process_swimlane_pure.mmd` | ✅ VALID | 70 | 42 |
| `material_logistics_er.mmd` | ✅ VALID | 12 | 5 |
| `material_logistics_sequence.mmd` | ✅ VALID | 7 | 43 |

## Files Changed

- `.opencode/skills/mermaid-syntax-validator/validate.py` - Added `_normalize_escapes()` and integrated into parsing

## Test Fixtures Status

The fix correctly handles intentionally invalid test fixtures:
- `duplicate_id.mmd` → FAIL (correct)
- `invalid_id.mmd` → FAIL (correct)
- `no_diagram_type.mmd` → FAIL (correct)
- `state_basic.mmd` (stateDiagram-v2) → Known limitation: implicit nodes from edges not captured

## Usage

```bash
# Validate single file
python .opencode/skills/mermaid-syntax-validator/validate.py diagram.mmd

# Validate entire vault
python .opencode/skills/mermaid-syntax-validator/validate.py --vault .

# JSON output for CI/CD
python .opencode/skills/mermaid-syntax-validator/validate.py --vault . --json
```