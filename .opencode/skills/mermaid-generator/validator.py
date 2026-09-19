"""
Validator integration for Mermaid Generator.
Wraps the fixed syntax validator for use in the generator pipeline.
"""

import sys
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass

# Add validator path - go up to mermaid root then into syntax validator
VALIDATOR_PATH = Path(__file__).parent.parent / "mermaid-syntax-validator"
sys.path.insert(0, str(VALIDATOR_PATH))

from validate import MermaidValidator, ValidationResult, ValidationError


@dataclass
class GeneratorValidationResult:
    """Result of generator validation."""
    valid: bool
    errors: List[str]
    warnings: List[str]
    diagram_type: Optional[str] = None
    node_count: int = 0
    edge_count: int = 0


class GeneratorValidator:
    """Validator wrapper for generator pipeline."""

    def __init__(self, strict: bool = True, auto_fix: bool = False):
        self.validator = MermaidValidator()
        self.strict = strict
        self.auto_fix = auto_fix

    def validate(self, mermaid_code: str) -> GeneratorValidationResult:
        """Validate generated Mermaid code."""
        result = self.validator.validate(mermaid_code)

        errors = [f"[{e.line}:{e.column}] {e.message}" for e in result.errors]
        warnings = [f"[{w.line}:{w.column}] {w.message}" for w in result.warnings]

        if self.strict and result.warnings:
            errors.extend(warnings)
            warnings = []

        return GeneratorValidationResult(
            valid=result.valid and (not self.strict or len(result.warnings) == 0),
            errors=errors,
            warnings=warnings,
            diagram_type=result.diagram_type,
            node_count=result.node_count,
            edge_count=result.edge_count,
        )

    def validate_and_fix(self, mermaid_code: str) -> tuple[GeneratorValidationResult, str]:
        """Validate and attempt auto-fix if enabled."""
        result = self.validate(mermaid_code)
        fixed_code = mermaid_code

        if not result.valid and self.auto_fix:
            fixed_code = self._attempt_fix(mermaid_code, result)
            fix_result = self.validate(fixed_code)
            if fix_result.valid:
                return fix_result, fixed_code

        return result, fixed_code

    def _attempt_fix(self, code: str, result: GeneratorValidationResult) -> str:
        """Attempt to auto-fix common errors."""
        lines = code.splitlines()

        # Fix: Add missing diagram type if first line doesn't have one
        if any("Diagram type must be declared" in e for e in result.errors):
            if lines and not lines[0].strip().startswith("%%"):
                first_word = lines[0].strip().split()[0] if lines[0].strip() else ""
                if first_word not in ["flowchart", "sequenceDiagram", "classDiagram",
                                      "stateDiagram-v2", "erDiagram", "gantt",
                                      "gitGraph", "journey", "pie", "quadrantChart",
                                      "mindmap", "kanban", "timeline", "C4Context"]:
                    lines.insert(0, "flowchart TD")

        # Fix: Remove emojis from subgraph names
        fixed_lines = []
        for line in lines:
            line = line.replace("🌅", "").replace("☕", "").replace("🥪", "")
            line = line.replace("🔨", "").replace("🍽️", "").replace("🌤️", "")
            line = line.replace("🔄", "").replace("👷", "").replace("👨‍💼", "")
            line = line.replace("🛡️", "").replace("📋", "")
            fixed_lines.append(line)

        return "\n".join(fixed_lines)


class ValidationPipeline:
    """Pipeline for validating generated Mermaid code in the generator."""

    def __init__(self, strict: bool = True, auto_fix: bool = True):
        self.validator = GeneratorValidator(strict=strict, auto_fix=auto_fix)

    def run(self, mermaid_code: str) -> GeneratorValidationResult:
        """Run full validation pipeline."""
        # Stage 1: Syntax validation
        result = self.validator.validate(mermaid_code)

        # Stage 2: Auto-fix if needed
        if not result.valid:
            result, fixed_code = self.validator.validate_and_fix(mermaid_code)

        return result


# Convenience function for generator
def validate_generated_mermaid(mermaid_code: str, strict: bool = True) -> GeneratorValidationResult:
    """Validate generated Mermaid code."""
    pipeline = ValidationPipeline(strict=strict, auto_fix=True)
    return pipeline.run(mermaid_code)


if __name__ == "__main__":
    # Test
    test_code = """flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[Other]
    """

    result = validate_generated_mermaid(test_code)
    print(f"Valid: {result.valid}")
    print(f"Type: {result.diagram_type}")
    print(f"Nodes: {result.node_count}, Edges: {result.edge_count}")
    for e in result.errors:
        print(f"ERROR: {e}")
    for w in result.warnings:
        print(f"WARN: {w}")