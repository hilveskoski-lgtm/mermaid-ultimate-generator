#!/usr/bin/env python3
"""
Mermaid Syntax Validator
Validates Mermaid diagram syntax against grammar rules and best practices.
"""

import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from grammar import (
    DIAGRAM_TYPES, FLOWCHART_DIRECTIONS, NODE_SHAPES, EDGE_TYPES,
    THEMES, CONFIG_PATTERN, ID_PATTERN, VALIDATION_RULES
)


@dataclass
class ValidationError:
    rule: str
    message: str
    line: int
    column: int
    severity: str = "error"


@dataclass
class ValidationResult:
    valid: bool
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[ValidationError] = field(default_factory=list)
    diagram_type: Optional[str] = None
    node_count: int = 0
    edge_count: int = 0


class MermaidValidator:
    def __init__(self):
        self.errors: list[ValidationError] = []
        self.warnings: list[ValidationError] = []
        self.nodes: set[str] = set()
        self.edges: list[tuple[str, str]] = []
        self.diagram_type: Optional[str] = None
        self.direction: Optional[str] = None
        self.theme: Optional[str] = None
        self._edge_only_nodes: set[str] = set()

    def validate(self, content: str, filename: str = "<string>") -> ValidationResult:
        self.errors = []
        self.warnings = []
        self.nodes = set()
        self.edges = []
        self.diagram_type = None
        self.direction = None
        self.theme = None

        lines = content.splitlines()
        self._check_diagram_type(lines)
        self._check_config(lines)
        self._parse_content(lines)
        self._validate_structure()

        return ValidationResult(
            valid=len(self.errors) == 0,
            errors=self.errors,
            warnings=self.warnings,
            diagram_type=self.diagram_type,
            node_count=len(self.nodes),
            edge_count=len(self.edges),
        )

    def _check_diagram_type(self, lines: list[str]):
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith("%%"):
                continue
            first_word = stripped.split()[0] if stripped.split() else ""
            if first_word in DIAGRAM_TYPES:
                self.diagram_type = first_word
                return
            else:
                self._add_error("required_diagram_type", VALIDATION_RULES["required_diagram_type"], i + 1, 1)
                return

    def _check_config(self, lines: list[str]):
        for i, line in enumerate(lines):
            match = re.search(CONFIG_PATTERN, line)
            if match:
                try:
                    config_str = match.group(1).replace("'", '"')
                    config = json.loads(config_str)
                    if "theme" in config:
                        theme = config["theme"]
                        if theme not in THEMES:
                            self._add_warning("valid_theme", f"Unknown theme: {theme}", i + 1, match.start())
                        else:
                            self.theme = theme
                except json.JSONDecodeError:
                    self._add_error("valid_config", "Invalid JSON in config", i + 1, match.start())

    def _parse_content(self, lines: list[str]):
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith("%%"):
                continue

            if self.diagram_type in ("flowchart", "graph") and self.direction is None:
                dir_match = re.match(r"^(TD|TB|BT|RL|LR)\b", stripped)
                if dir_match:
                    self.direction = dir_match.group(1)
                    if self.direction not in FLOWCHART_DIRECTIONS:
                        self._add_error("valid_direction", f"Invalid direction: {self.direction}", i + 1, 1)
                    continue

            if self.diagram_type in ("flowchart", "graph"):
                self._parse_flowchart_nodes(stripped, i + 1)
                self._parse_flowchart_edges(stripped, i + 1)
            elif self.diagram_type == "sequenceDiagram":
                self._parse_sequence_nodes(stripped, i + 1)
                self._parse_sequence_edges(stripped, i + 1)
            elif self.diagram_type == "classDiagram":
                self._parse_class_nodes(stripped, i + 1)
                self._parse_class_edges(stripped, i + 1)
            elif self.diagram_type == "stateDiagram-v2":
                self._parse_state_nodes(stripped, i + 1)
                self._parse_state_edges(stripped, i + 1)
            elif self.diagram_type == "erDiagram":
                self._parse_er_nodes(stripped, i + 1)
                self._parse_er_edges(stripped, i + 1)

    def _parse_flowchart_nodes(self, line: str, line_num: int):
        # Ordered from most specific to least specific to avoid double-matching
        patterns = [
            (r"(" + ID_PATTERN + r")\s*\[\[([^\]]*)\]\]", "subroutine"),
            (r"(" + ID_PATTERN + r")\s*\[\(([^)]*)\)\]", "cylindrical"),
            (r"(" + ID_PATTERN + r")\s*\[/([^/]*)/\]", "parallelogram"),
            (r"(" + ID_PATTERN + r")\s*\[\\\\?([^\\]*)\\\\?\]", "parallelogram"),
            (r"(" + ID_PATTERN + r")\s*\(\(([^)]*)\)\)", "circle"),
            (r"(" + ID_PATTERN + r")\s*\{([^}]*)\}", "diamond"),
            (r"(" + ID_PATTERN + r")\s*>([^\]]*)\]", "asymmetric"),
            (r"(" + ID_PATTERN + r")\s*\(([^)]*)\)", "rounded"),
            # Rect: [text] but not [/.../], [\...], [[...]], [(...)]
            (r"(" + ID_PATTERN + r")\s*\[(?![/\\\[\(])([^\]\n]*)\]", "rect"),
        ]

        for pattern, _ in patterns:
            for match in re.finditer(pattern, line):
                node_id = match.group(1)
                self._register_node(node_id, line_num, match.start(1))

        # Check for invalid IDs (starting with digit) followed by node shape chars
        invalid_id_pattern = r"\b([0-9][A-Za-z0-9_]*)\s*(?:\[|\{|\(|>|\[/|\[\\|\[\[|\[\(|\(\))"
        for match in re.finditer(invalid_id_pattern, line):
            node_id = match.group(1)
            self._add_error("valid_ids", f"Invalid node ID (must start with letter): {node_id}", line_num, match.start(1))

    def _parse_flowchart_edges(self, line: str, line_num: int):
        edge_patterns = [
            r"(" + ID_PATTERN + r")\s*(--->|---|-\.->|==>|-->)\s*(" + ID_PATTERN + r")",
        ]
        for pattern in edge_patterns:
            for match in re.finditer(pattern, line):
                from_id, edge_type, to_id = match.groups()
                self.edges.append((from_id, to_id))
                self._check_edge_refs(from_id, to_id, line_num, match.start(1))

    def _parse_sequence_nodes(self, line: str, line_num: int):
        for match in re.finditer(r"participant\s+(" + ID_PATTERN + r")", line):
            self._register_node(match.group(1), line_num, match.start(1))
        for match in re.finditer(r"(actor|boundary|control|entity|database)\s+(" + ID_PATTERN + r")", line):
            self._register_node(match.group(2), line_num, match.start(2))

    def _parse_sequence_edges(self, line: str, line_num: int):
        edge_types = ["->>", "-->>", "->>+", "->>-", "-x", "--x"]
        pattern = r"(" + ID_PATTERN + r")\s*(" + "|".join(re.escape(e) for e in edge_types) + r")\s*(" + ID_PATTERN + r")"
        for match in re.finditer(pattern, line):
            from_id, edge_type, to_id = match.groups()
            self.edges.append((from_id, to_id))
            self._check_edge_refs(from_id, to_id, line_num, match.start(1))

    def _parse_class_nodes(self, line: str, line_num: int):
        for match in re.finditer(r"(class|interface|abstract)\s+(" + ID_PATTERN + r")", line):
            self._register_node(match.group(2), line_num, match.start(2))

    def _parse_class_edges(self, line: str, line_num: int):
        rel_types = ["<|--", "*--", "o--", "-->", "..>", "--|>"]
        pattern = r"(" + ID_PATTERN + r")\s*(" + "|".join(re.escape(e) for e in rel_types) + r")\s*(" + ID_PATTERN + r")"
        for match in re.finditer(pattern, line):
            from_id, rel, to_id = match.groups()
            self.edges.append((from_id, to_id))
            self._check_edge_refs(from_id, to_id, line_num, match.start(1))

    def _parse_state_nodes(self, line: str, line_num: int):
        for match in re.finditer(r"state\s+(\"[^\"]*\"|" + ID_PATTERN + r")(?:\s+as\s+(" + ID_PATTERN + r"))?", line):
            name = match.group(1).strip('"')
            alias = match.group(2)
            node_id = alias if alias else name
            self._register_node(node_id, line_num, match.start(1))
        for match in re.finditer(r"\[\*\]", line):
            pass

    def _parse_state_edges(self, line: str, line_num: int):
        pattern = r"(" + ID_PATTERN + r")\s*(-->)?\s*(" + ID_PATTERN + r")"
        for match in re.finditer(pattern, line):
            from_id, arrow, to_id = match.groups()
            if arrow:
                # Register nodes implicitly defined by edges
                self._register_node(from_id, line_num, match.start(1), explicit=False)
                self._register_node(to_id, line_num, match.start(3), explicit=False)
                self.edges.append((from_id, to_id))

    def _parse_er_nodes(self, line: str, line_num: int):
        # Match entity definitions: "EntityName {" at start of line (after indent)
        for match in re.finditer(r"^\s*(" + ID_PATTERN + r")\s*\{", line):
            self._register_node(match.group(1), line_num, match.start(1))

    def _parse_er_edges(self, line: str, line_num: int):
        rel_types = ["\\|\\|--o\\{", "\\|\\|--\\|\\{", "o\\{--o\\{", "\\|o--o\\{", "\\|\\|--\\|\\|", "\\|o--\\|\\|"]
        pattern = r"(" + ID_PATTERN + r")\s*(" + "|".join(rel_types) + r")\s*(" + ID_PATTERN + r")"
        for match in re.finditer(pattern, line):
            from_id, rel, to_id = match.groups()
            self.edges.append((from_id, to_id))
            self._check_edge_refs(from_id, to_id, line_num, match.start(1))

    def _register_node(self, node_id: str, line_num: int, col: int, explicit: bool = True):
        if not re.fullmatch(ID_PATTERN, node_id):
            self._add_error("valid_ids", f"Invalid node ID: {node_id}", line_num, col)
        if node_id in self.nodes:
            if explicit:
                self._add_error("no_duplicate_ids", f"Duplicate node ID: {node_id}", line_num, col)
            return
        self.nodes.add(node_id)

    def _check_edge_refs(self, from_id: str, to_id: str, line_num: int, col: int):
        for node_id in (from_id, to_id):
            if node_id not in self.nodes and node_id not in self._edge_only_nodes:
                self._add_warning("valid_edges", f"Edge references undefined node: {node_id}", line_num, col)
                self._edge_only_nodes.add(node_id)

    def _validate_structure(self):
        if not self.diagram_type:
            self._add_error("required_diagram_type", VALIDATION_RULES["required_diagram_type"], 1, 1)

        if len(self.nodes) == 0:
            self._add_error("at_least_one_node", VALIDATION_RULES["at_least_one_node"], 1, 1)

    def _add_error(self, rule: str, message: str, line: int, column: int):
        self.errors.append(ValidationError(rule, message, line, column, "error"))

    def _add_warning(self, rule: str, message: str, line: int, column: int):
        self.warnings.append(ValidationError(rule, message, line, column, "warning"))


def validate_file(filepath: Path) -> ValidationResult:
    content = filepath.read_text(encoding="utf-8")
    validator = MermaidValidator()
    return validator.validate(content, str(filepath))


def main():
    parser = argparse.ArgumentParser(description="Validate Mermaid diagram syntax")
    parser.add_argument("files", nargs="*", type=Path, help="Files to validate")
    parser.add_argument("--vault", type=Path, help="Validate all .md/.mmd files in vault")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()

    files = []
    if args.vault:
        files.extend(args.vault.rglob("*.md"))
        files.extend(args.vault.rglob("*.mmd"))
    files.extend(args.files)

    if not files:
        parser.error("No files specified. Use --vault or provide file paths.")

    all_valid = True
    results = []

    for filepath in files:
        if not filepath.exists():
            print(f"File not found: {filepath}", file=sys.stderr)
            all_valid = False
            continue

        result = validate_file(filepath)
        results.append({"file": str(filepath), **result.__dict__})

        if args.json:
            continue

        status = "[OK] VALID" if result.valid else "[FAIL] INVALID"
        print(f"{status} {filepath}")
        print(f"  Type: {result.diagram_type or 'unknown'}")
        print(f"  Nodes: {result.node_count}, Edges: {result.edge_count}")

        for err in result.errors:
            print(f"  ERROR  [{err.line}:{err.column}] {err.message}")
        for warn in result.warnings:
            prefix = "ERROR" if args.strict else "WARN"
            print(f"  {prefix}  [{warn.line}:{warn.column}] {warn.message}")

        if not result.valid or (args.strict and result.warnings):
            all_valid = False

    if args.json:
        print(json.dumps(results, indent=2, default=str))

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()