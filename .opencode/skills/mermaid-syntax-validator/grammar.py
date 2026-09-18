# Mermaid EBNF Grammar Definitions

DIAGRAM_TYPES = {
    "flowchart", "graph",
    "sequenceDiagram",
    "classDiagram",
    "stateDiagram-v2",
    "erDiagram",
    "gantt",
    "gitGraph",
    "journey",
    "pie",
    "quadrantChart",
    "requirementDiagram",
    "C4Context", "C4Container", "C4Component", "C4Code",
    "mindmap",
    "kanban",
    "architecture-beta",
    "timeline",
    "useCaseDiagram",
    "objectDiagram",
    "componentDiagram",
    "packageDiagram",
}

FLOWCHART_DIRECTIONS = {"TD", "TB", "BT", "RL", "LR"}

NODE_SHAPES = {
    "rect": ("[", "]"),
    "rounded": ("(", ")"),
    "diamond": ("{", "}"),
    "circle": ("((", "))"),
    "asymmetric": (">", "]"),
    "parallelogram_left": ("[/", "/]"),
    "parallelogram_right": ("[\\", "\\]"),
    "subroutine": ("[[", "]]"),
    "cylindrical": ("[(", ")]"),
    "stadium": ("[/", "/]"),
}

EDGE_TYPES = {
    "arrow": "-->",
    "line": "---",
    "dotted": "-.->",
    "thick": "==>",
    "seq_sync": "->>",
    "seq_reply": "-->>",
    "seq_activate": "->>+",
    "seq_deactivate": "->>-",
    "seq_async": "-x",
    "seq_async_reply": "--x",
    "inherit": "<|--",
    "compose": "*--",
    "aggregate": "o--",
    "assoc": "-->",
    "depend": "..>",
    "realize": "--|>",
}

THEMES = {"default", "dark", "forest", "neutral", "base"}

CONFIG_PATTERN = r"%%\{init:\s*(\{.*?\})\s*\}%%"
CONFIG_PATTERN_SINGLE = r"%%\{init:\s*(\{.*?\})\s*\}%%"

ID_PATTERN = r"[A-Za-z][A-Za-z0-9_]*"

VALIDATION_RULES = {
    "required_diagram_type": "Diagram type must be declared",
    "at_least_one_node": "At least one node required",
    "balanced_brackets": "Brackets must be balanced",
    "valid_ids": "IDs must start with letter, contain only alphanumeric/underscore",
    "no_duplicate_ids": "Duplicate node IDs not allowed",
    "valid_edges": "Edges must reference existing nodes",
    "valid_theme": "Theme must be one of: default, dark, forest, neutral, base",
    "valid_direction": "Flowchart direction must be one of: TD, TB, BT, RL, LR",
}