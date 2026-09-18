#!/usr/bin/env python3
"""
Mermaid Generator
Generates valid Mermaid diagram code from structured input (JSON, YAML, DSL).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from enum import Enum
import json
import yaml


class NodeShape(Enum):
    RECT = "rect"
    ROUNDED = "rounded"
    DIAMOND = "diamond"
    CIRCLE = "circle"
    ASYMMETRIC = "asymmetric"
    PARALLELOGRAM = "parallelogram"
    SUBROUTINE = "subroutine"
    CYLINDRICAL = "cylindrical"


class EdgeType(Enum):
    ARROW = "-->"
    LINE = "---"
    DOTTED = "-.->"
    THICK = "==>"


class Direction(Enum):
    TD = "TD"
    TB = "TB"
    BT = "BT"
    RL = "RL"
    LR = "LR"


@dataclass
class FlowchartNode:
    id: str
    label: str = ""
    shape: NodeShape = NodeShape.RECT
    subgraph: Optional[str] = None


@dataclass
class FlowchartEdge:
    from_id: str
    to_id: str
    label: str = ""
    edge_type: EdgeType = EdgeType.ARROW


@dataclass
class FlowchartSubgraph:
    id: str
    label: str
    nodes: List[str] = field(default_factory=list)


@dataclass
class ClassDefinition:
    name: str
    fields: Dict[str, str] = field(default_factory=dict)
    methods: Dict[str, str] = field(default_factory=dict)
    visibility: Dict[str, str] = field(default_factory=dict)


@dataclass
class ClassRelationship:
    from_class: str
    to_class: str
    rel_type: str
    label: str = ""


@dataclass
class SequenceParticipant:
    id: str
    alias: str = ""
    type: str = "participant"


@dataclass
class SequenceMessage:
    from_id: str
    to_id: str
    message: str
    msg_type: str = "->>"
    activation: bool = False


class MermaidGenerator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.lines = []
        self.indent = "    "

    def flowchart(self, data: Dict[str, Any]) -> str:
        self.reset()
        direction = data.get("direction", "TD")
        self.lines.append(f"flowchart {direction}")
        
        # Subgraphs first
        for sg in data.get("subgraphs", []):
            self.lines.append(f"{self.indent}subgraph {sg['id']}[{sg['label']}]")
            for node_id in sg.get("nodes", []):
                node = next((n for n in data["nodes"] if n["id"] == node_id), None)
                if node:
                    self.lines.append(f"{self.indent}{self.indent}{self._node_line(node)}")
            self.lines.append(f"{self.indent}end")
        
        # Standalone nodes
        subgraph_nodes = set()
        for sg in data.get("subgraphs", []):
            subgraph_nodes.update(sg.get("nodes", []))
        
        for node in data.get("nodes", []):
            if node["id"] not in subgraph_nodes:
                self.lines.append(f"{self.indent}{self._node_line(node)}")
        
        # Edges
        for edge in data.get("edges", []):
            self.lines.append(f"{self.indent}{self._edge_line(edge)}")
        
        # Classes
        for cls in data.get("classes", []):
            self.lines.append(f"{self.indent}{self._class_def_line(cls)}")
        for cls_assign in data.get("class_assignments", []):
            self.lines.append(f"{self.indent}{self._class_assign_line(cls_assign)}")
        
        # Clicks
        for click in data.get("clicks", []):
            self.lines.append(f"{self.indent}{self._click_line(click)}")
        
        return "\n".join(self.lines)

    def _node_line(self, node: Dict) -> str:
        node_id = node["id"]
        label = node.get("label", node_id)
        shape = node.get("shape", "rect")
        
        shapes = {
            "rect": f"{node_id}[{label}]",
            "rounded": f"{node_id}({label})",
            "diamond": f"{node_id}{{{label}}}",
            "circle": f"{node_id}(({label}))",
            "asymmetric": f"{node_id}>{label}]",
            "parallelogram": f"{node_id}[/{label}/]",
            "subroutine": f"{node_id}[[{label}]]",
            "cylindrical": f"{node_id}[({label})]",
        }
        return shapes.get(shape, f"{node_id}[{label}]")

    def _edge_line(self, edge: Dict) -> str:
        from_id = edge["from"]
        to_id = edge["to"]
        label = edge.get("label", "")
        edge_type = edge.get("type", "arrow")
        
        edges = {
            "arrow": "-->",
            "line": "---",
            "dotted": "-.->",
            "thick": "==>",
        }
        edge_str = edges.get(edge_type, "-->")
        
        if label:
            return f"{from_id} {edge_str}|{label}| {to_id}"
        return f"{from_id} {edge_str} {to_id}"

    def _class_def_line(self, cls: Dict) -> str:
        return f"classDef {cls['name']} {cls['styles']}"

    def _class_assign_line(self, assign: Dict) -> str:
        nodes = ",".join(assign["nodes"])
        return f"class {nodes} {assign['class']}"

    def _click_line(self, click: Dict) -> str:
        url = click.get("url", "")
        tooltip = click.get("tooltip", "")
        if url and tooltip:
            return f'click {click["id"]} "{url}" "{tooltip}"'
        elif url:
            return f'click {click["id"]} "{url}"'
        return f'click {click["id"]}'

    def sequence_diagram(self, data: Dict[str, Any]) -> str:
        self.reset()
        self.lines.append("sequenceDiagram")
        
        # Participants
        for p in data.get("participants", []):
            p_type = p.get("type", "participant")
            alias = f" as {p['alias']}" if p.get("alias") else ""
            self.lines.append(f"{self.indent}{p_type} {p['id']}{alias}")
        
        # Messages
        for msg in data.get("messages", []):
            self.lines.append(f"{self.indent}{self._sequence_message(msg)}")
        
        # Fragments
        for frag in data.get("fragments", []):
            self.lines.append(f"{self.indent}{self._sequence_fragment(frag)}")
        
        return "\n".join(self.lines)

    def _sequence_message(self, msg: Dict) -> str:
        from_id = msg["from"]
        to_id = msg["to"]
        text = msg.get("message", "")
        msg_type = msg.get("type", "->>")
        
        types = {
            "sync": "->>",
            "reply": "-->>",
            "activate": "->>+",
            "deactivate": "->>-",
            "async": "-x",
            "async_reply": "--x",
        }
        arrow = types.get(msg_type, "->>")
        
        if text:
            return f"{from_id}{arrow}{to_id}: {text}"
        return f"{from_id}{arrow}{to_id}"

    def _sequence_fragment(self, frag: Dict) -> str:
        frag_type = frag["type"]
        label = frag.get("label", "")
        content = frag.get("content", [])
        
        if frag_type in ["alt", "opt", "loop", "par", "critical", "neg", "break"]:
            header = f"{frag_type} {label}" if label else frag_type
            lines = [header]
            for item in content:
                lines.append(f"{self.indent}{item}")
            lines.append("end")
            return "\n".join(lines)
        return ""

    def class_diagram(self, data: Dict[str, Any]) -> str:
        self.reset()
        self.lines.append("classDiagram")
        
        # Classes
        for cls in data.get("classes", []):
            self.lines.append(f"{self.indent}{self._class_def(cls)}")
        
        # Relationships
        for rel in data.get("relationships", []):
            self.lines.append(f"{self.indent}{self._class_rel(rel)}")
        
        return "\n".join(self.lines)

    def _class_def(self, cls: Dict) -> str:
        name = cls["name"]
        members = []
        
        for field_name, field_type in cls.get("fields", {}).items():
            vis = cls.get("visibility", {}).get(field_name, "+")
            members.append(f"  {vis}{field_name}: {field_type}")
        
        for method_name, return_type in cls.get("methods", {}).items():
            vis = cls.get("visibility", {}).get(method_name, "+")
            members.append(f"  {vis}{method_name}(): {return_type}")
        
        if members:
            return f"class {name} {{\n" + "\n".join(members) + "\n}"
        return f"class {name}"

    def _class_rel(self, rel: Dict) -> str:
        rel_types = {
            "inheritance": "<|--",
            "composition": "*--",
            "aggregation": "o--",
            "association": "-->",
            "dependency": "..>",
            "realization": "--|>",
        }
        arrow = rel_types.get(rel["type"], "-->")
        label = f" : {rel['label']}" if rel.get("label") else ""
        return f"{rel['from']} {arrow} {rel['to']}{label}"

    def state_diagram(self, data: Dict[str, Any]) -> str:
        self.reset()
        version = data.get("version", "v2")
        self.lines.append(f"stateDiagram-{version}")
        
        # States
        for state in data.get("states", []):
            if "substates" in state:
                self.lines.append(f"{self.indent}state {state['name']} {{")
                for sub in state["substates"]:
                    self.lines.append(f"{self.indent}{self.indent}{sub}")
                self.lines.append(f"{self.indent}}}")
            else:
                self.lines.append(f"{self.indent}{state}")
        
        # Transitions
        for trans in data.get("transitions", []):
            from_state = trans["from"]
            to_state = trans["to"]
            label = f" : {trans['label']}" if trans.get("label") else ""
            self.lines.append(f"{self.indent}{from_state} --> {to_state}{label}")
        
        return "\n".join(self.lines)

    def er_diagram(self, data: Dict[str, Any]) -> str:
        self.reset()
        self.lines.append("erDiagram")
        
        # Entities
        for entity in data.get("entities", []):
            self.lines.append(f"{self.indent}{self._er_entity(entity)}")
        
        # Relationships
        for rel in data.get("relationships", []):
            self.lines.append(f"{self.indent}{self._er_rel(rel)}")
        
        return "\n".join(self.lines)

    def _er_entity(self, entity: Dict) -> str:
        name = entity["name"]
        attrs = entity.get("attributes", {})
        if attrs:
            lines = [f"{name} {{"]
            for attr_name, attr_type in attrs.items():
                lines.append(f"  {attr_type} {attr_name}")
            lines.append("}")
            return "\n".join(lines)
        return name

    def _er_rel(self, rel: Dict) -> str:
        rel_types = {
            "one_to_many": "||--o{",
            "many_to_one": "}o--||",
            "one_to_one": "||--||",
            "many_to_many": "}o--o{",
            "zero_or_one_to_many": "|o--o{",
            "one_or_more_to_many": "||--o{",
        }
        arrow = rel_types.get(rel["type"], "||--o{")
        label = f" : {rel['label']}" if rel.get("label") else ""
        return f"{rel['from']} {arrow} {rel['to']}{label}"

    def gantt(self, data: Dict[str, Any]) -> str:
        self.reset()
        self.lines.append("gantt")
        if "title" in data:
            self.lines.append(f"{self.indent}title {data['title']}")
        if "dateFormat" in data:
            self.lines.append(f"{self.indent}dateFormat {data['dateFormat']}")
        if "axisFormat" in data:
            self.lines.append(f"{self.indent}axisFormat {data['axisFormat']}")
        
        for section in data.get("sections", []):
            self.lines.append(f"{self.indent}section {section['name']}")
            for task in section.get("tasks", []):
                task_line = f"{self.indent}{self.indent}{task['name']}"
                if "id" in task:
                    task_line += f" :{task['id']}"
                if "start" in task:
                    task_line += f", {task['start']}"
                if "duration" in task:
                    task_line += f", {task['duration']}"
                if "deps" in task:
                    task_line += f", after {','.join(task['deps'])}"
                if task.get("crit", False):
                    task_line += " :crit"
                if task.get("active", False):
                    task_line += " :active"
                if task.get("done", False):
                    task_line += " :done"
                self.lines.append(task_line)
        
        return "\n".join(self.lines)

    def git_graph(self, data: Dict[str, Any]) -> str:
        self.reset()
        self.lines.append("gitGraph")
        
        for cmd in data.get("commands", []):
            if cmd["type"] == "commit":
                self.lines.append(f"{self.indent}commit id: \"{cmd['id']}\"")
            elif cmd["type"] == "branch":
                self.lines.append(f"{self.indent}branch {cmd['name']}")
            elif cmd["type"] == "checkout":
                self.lines.append(f"{self.indent}checkout {cmd['name']}")
            elif cmd["type"] == "merge":
                self.lines.append(f"{self.indent}merge {cmd['name']} id: \"{cmd.get('id', '')}\"")
            elif cmd["type"] == "tag":
                self.lines.append(f"{self.indent}tag: \"{cmd['name']}\"")
            elif cmd["type"] == "cherry_pick":
                self.lines.append(f"{self.indent}cherry-pick id: \"{cmd['id']}\"")
        
        return "\n".join(self.lines)

    def journey(self, data: Dict[str, Any]) -> str:
        self.reset()
        self.lines.append("journey")
        if "title" in data:
            self.lines.append(f"{self.indent}title {data['title']}")
        
        for section in data.get("sections", []):
            self.lines.append(f"{self.indent}section {section['name']}")
            for task in section.get("tasks", []):
                actor = f": {task['actor']}" if task.get("actor") else ""
                score = task.get("score", 3)
                self.lines.append(f"{self.indent}{self.indent}{task['name']}: {score}{actor}")
        
        return "\n".join(self.lines)

    def pie(self, data: Dict[str, Any]) -> str:
        self.reset()
        title = data.get("title", "Chart")
        self.lines.append(f"pie title {title}")
        
        for slice_data in data.get("slices", []):
            self.lines.append(f"{self.indent}\"{slice_data['name']}\" : {slice_data['value']}")
        
        return "\n".join(self.lines)

    def quadrant_chart(self, data: Dict[str, Any]) -> str:
        self.reset()
        self.lines.append("quadrantChart")
        if "title" in data:
            self.lines.append(f"{self.indent}title {data['title']}")
        if "x_axis" in data:
            self.lines.append(f"{self.indent}x-axis {data['x_axis']['low']} --> {data['x_axis']['high']}")
        if "y_axis" in data:
            self.lines.append(f"{self.indent}y-axis {data['y_axis']['low']} --> {data['y_axis']['high']}")
        
        for q in data.get("quadrants", []):
            self.lines.append(f"{self.indent}quadrant-{q['num']} {q['label']}")
        
        for point in data.get("points", []):
            self.lines.append(f"{self.indent}\"{point['name']}\": [{point['x']}, {point['y']}]")
        
        return "\n".join(self.lines)

    def mindmap(self, data: Dict[str, Any]) -> str:
        self.reset()
        self.lines.append("mindmap")
        
        def add_node(node: Dict, level: int = 0):
            indent = "  " * level
            name = node["name"]
            self.lines.append(f"{indent}{name}")
            for child in node.get("children", []):
                add_node(child, level + 1)
        
        add_node(data["root"])
        return "\n".join(self.lines)

    def kanban(self, data: Dict[str, Any]) -> str:
        self.reset()
        self.lines.append("kanban")
        if "title" in data:
            self.lines.append(f"{self.indent}title {data['title']}")
        
        for col in data.get("columns", []):
            limit = f" [{col['limit']}]" if col.get("limit") else ""
            self.lines.append(f"{self.indent}column {col['name']}{limit}")
        
        for task in data.get("tasks", []):
            self.lines.append(f"{self.indent}task[{task['column']}] {task['name']}")
        
        return "\n".join(self.lines)

    def requirement(self, data: Dict[str, Any]) -> str:
        self.reset()
        self.lines.append("requirementDiagram")
        
        for req in data.get("requirements", []):
            self.lines.append(f"{self.indent}requirement \"{req['id']}\" {{")
            for key, val in req.get("properties", {}).items():
                self.lines.append(f"{self.indent}{self.indent}{key}: \"{val}\"")
            self.lines.append(f"{self.indent}}}")
        
        for elem in data.get("elements", []):
            self.lines.append(f"{self.indent}element \"{elem['id']}\" {{")
            self.lines.append(f"{self.indent}{self.indent}type: {elem['type']}")
            self.lines.append(f"{self.indent}}}")
        
        for rel in data.get("relationships", []):
            rel_type = rel.get("type", "-")
            self.lines.append(f"{self.indent}\"{rel['from']}\" {rel_type} \"{rel['to']}\"")
        
        return "\n".join(self.lines)

    def c4_context(self, data: Dict[str, Any]) -> str:
        self.reset()
        self.lines.append("C4Context")
        if "title" in data:
            self.lines.append(f"{self.indent}title {data['title']}")
        
        for person in data.get("people", []):
            desc = f", \"{person['description']}\"" if person.get("description") else ""
            self.lines.append(f"{self.indent}Person({person['id']}, \"{person['name']}\"{desc})")
        
        for system in data.get("systems", []):
            desc = f", \"{system['description']}\"" if system.get("description") else ""
            self.lines.append(f"{self.indent}System({system['id']}, \"{system['name']}\"{desc})")
        
        for ext in data.get("external_systems", []):
            desc = f", \"{ext['description']}\"" if ext.get("description") else ""
            self.lines.append(f"{self.indent}System_Ext({ext['id']}, \"{ext['name']}\"{desc})")
        
        for rel in data.get("relationships", []):
            tech = f", \"{rel['technology']}\"" if rel.get("technology") else ""
            self.lines.append(f"{self.indent}Rel({rel['from']}, {rel['to']}, \"{rel['label']}\"{tech})")
        
        return "\n".join(self.lines)

    def to_json(self, diagram_type: str, data: Dict[str, Any]) -> str:
        return json.dumps({"type": diagram_type, "data": data}, indent=2)

    def from_json(self, json_str: str) -> str:
        obj = json.loads(json_str)
        return getattr(self, obj["type"].replace("-", "_"))(obj["data"])


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate Mermaid diagrams")
    parser.add_argument("type", choices=[
        "flowchart", "sequence", "class", "state", "er", "gantt",
        "git", "journey", "pie", "quadrant", "mindmap", "kanban",
        "requirement", "c4context"
    ])
    parser.add_argument("input", type=str, help="JSON/YAML input file or '-' for stdin")
    parser.add_argument("-o", "--output", type=str, help="Output file")
    parser.add_argument("--format", choices=["mermaid", "json"], default="mermaid")
    
    args = parser.parse_args()
    
    if args.input == "-":
        import sys
        content = sys.stdin.read()
    else:
        content = Path(args.input).read_text()
    
    if args.input.endswith(".yaml") or args.input.endswith(".yml"):
        data = yaml.safe_load(content)
    else:
        data = json.loads(content)
    
    # Handle both formats: {type, data} or direct data
    if isinstance(data, dict) and "type" in data and "data" in data:
        diagram_type = data["type"]
        diagram_data = data["data"]
    else:
        diagram_type = args.type
        diagram_data = data
    
    gen = MermaidGenerator()
    method_map = {
        "flowchart": "flowchart",
        "sequence": "sequence_diagram",
        "class": "class_diagram",
        "state": "state_diagram",
        "er": "er_diagram",
        "gantt": "gantt",
        "git": "git_graph",
        "journey": "journey",
        "pie": "pie",
        "quadrant": "quadrant_chart",
        "mindmap": "mindmap",
        "kanban": "kanban",
        "requirement": "requirement",
        "c4context": "c4_context",
    }
    method_name = method_map.get(diagram_type, diagram_type.replace("-", "_"))
    method = getattr(gen, method_name)
    result = method(diagram_data)
    
    if args.output:
        Path(args.output).write_text(result)
    else:
        print(result)


if __name__ == "__main__":
    from pathlib import Path
    main()