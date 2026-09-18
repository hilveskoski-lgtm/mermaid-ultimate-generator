#!/usr/bin/env python3
"""
Mermaid Obsidian Integration
Automation and tooling for seamless Mermaid workflow in Obsidian.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import argparse


@dataclass
class PluginConfig:
    id: str
    name: str
    version: str
    enabled: bool = True
    settings: Dict = None


RECOMMENDED_PLUGINS = [
    PluginConfig("mermaid-tools", "Mermaid Tools", "1.0.0", True, {
        "autoRender": True,
        "exportFormat": "svg",
        "theme": "default"
    }),
    PluginConfig("dataview", "Dataview", "0.5.0", True, {}),
    PluginConfig("canvas", "Canvas", "1.0.0", True, {}),
    PluginConfig("git", "Git", "1.0.0", True, {}),
    PluginConfig("templater-obsidian", "Templater", "1.0.0", True, {}),
]


class ObsidianIntegration:
    def __init__(self, vault_path: Path):
        self.vault_path = Path(vault_path)
        self.plugins_dir = self.vault_path / ".obsidian" / "plugins"
        self.config_file = self.vault_path / ".obsidian" / "community-plugins.json"

    def install_plugins(self, plugin_ids: List[str] = None) -> List[str]:
        if plugin_ids is None:
            plugin_ids = [p.id for p in RECOMMENDED_PLUGINS]
        
        installed = []
        for plugin_id in plugin_ids:
            plugin_dir = self.plugins_dir / plugin_id
            if not plugin_dir.exists():
                try:
                    result = subprocess.run(
                        ["obsidian", "--install-plugin", plugin_id],
                        capture_output=True, text=True, cwd=self.vault_path
                    )
                    if result.returncode == 0:
                        installed.append(plugin_id)
                except FileNotFoundError:
                    print(f"Obsidian CLI not found. Manual install: {plugin_id}")
        
        return installed

    def enable_plugins(self, plugin_ids: List[str]) -> None:
        if not self.config_file.exists():
            return
        
        config = json.loads(self.config_file.read_text())
        enabled = config.get("enabledPlugins", [])
        
        for pid in plugin_ids:
            if pid not in enabled:
                enabled.append(pid)
        
        config["enabledPlugins"] = enabled
        self.config_file.write_text(json.dumps(config, indent=2))

    def configure_plugins(self) -> None:
        for plugin in RECOMMENDED_PLUGINS:
            if plugin.settings:
                plugin_config = self.plugins_dir / plugin.id / "data.json"
                if plugin_config.exists():
                    current = json.loads(plugin_config.read_text())
                    current.update(plugin.settings)
                    plugin_config.write_text(json.dumps(current, indent=2))

    def sync_canvas_to_mermaid(self, canvas_file: Path, output_file: Path = None) -> str:
        canvas = json.loads(canvas_file.read_text())
        
        nodes = {}
        edges = []
        
        for node in canvas.get("nodes", []):
            if node.get("type") == "text":
                node_id = node["id"][:8]
                text = node.get("text", "").replace("\n", "<br>")
                nodes[node_id] = f'{node_id}["{text}"]'
            elif node.get("type") == "file":
                node_id = node["id"][:8]
                file_name = Path(node.get("file", "")).stem
                nodes[node_id] = f'{node_id}[[{file_name}]]'
        
        for edge in canvas.get("edges", []):
            from_id = edge["from"]["node"][:8]
            to_id = edge["to"]["node"][:8]
            label = edge.get("label", "")
            if label:
                edges.append(f"{from_id} -->|{label}| {to_id}")
            else:
                edges.append(f"{from_id} --> {to_id}")
        
        mermaid = ["flowchart TD"]
        mermaid.extend(nodes.values())
        mermaid.extend(edges)
        
        result = "\n".join(mermaid)
        
        if output_file:
            output_file.write_text(f"```mermaid\n{result}\n```")
        
        return result

    def sync_mermaid_to_canvas(self, mermaid_file: Path, output_file: Path = None) -> Dict:
        content = mermaid_file.read_text()
        mermaid_code = self._extract_mermaid(content)
        
        nodes = []
        edges = []
        node_positions = {}
        
        import re
        node_pattern = re.compile(r'(\w+)\s*(\[.*?\]|\(.*?\)|\{.*?\}|\(\(.*?\)\)|>.*?\]|\[/.*?/\]|\[\\.*?\\\]|\[\[.*?\]\]|\[\(.*?\)\])')
        edge_pattern = re.compile(r'(\w+)\s*(-->|---|-\.->|==>|->>|-->>|->>\+|->>-|-x|--x)\s*(\w+)')
        
        for match in node_pattern.finditer(mermaid_code):
            node_id, shape = match.groups()
            if node_id not in node_positions:
                node_positions[node_id] = len(node_positions)
            
            x = 100 + (node_positions[node_id] % 5) * 200
            y = 100 + (node_positions[node_id] // 5) * 150
            
            text = shape.strip("[](){}<>/\\")
            nodes.append({
                "id": node_id,
                "type": "text",
                "x": x,
                "y": y,
                "width": 150,
                "height": 60,
                "text": text
            })
        
        for match in edge_pattern.finditer(mermaid_code):
            from_id, edge_type, to_id = match.groups()
            edges.append({
                "id": f"{from_id}-{to_id}",
                "from": {"node": from_id, "side": "right"},
                "to": {"node": to_id, "side": "left"}
            })
        
        canvas = {
            "nodes": nodes,
            "edges": edges
        }
        
        if output_file:
            output_file.write_text(json.dumps(canvas, indent=2))
        
        return canvas

    def _extract_mermaid(self, content: str) -> str:
        lines = content.splitlines()
        in_mermaid = False
        mermaid_lines = []
        
        for line in lines:
            if line.strip().startswith("```mermaid"):
                in_mermaid = True
                continue
            elif line.strip().startswith("```") and in_mermaid:
                in_mermaid = False
                continue
            elif in_mermaid:
                mermaid_lines.append(line)
        
        return "\n".join(mermaid_lines) if mermaid_lines else content

    def export_vault(self, output_dir: Path, format: str = "html") -> List[Path]:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            result = subprocess.run(
                ["obsidian", "export", str(self.vault_path), "--output", str(output_dir), "--format", format],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                print(f"Export failed: {result.stderr}")
                return []
        except FileNotFoundError:
            print("Obsidian CLI not found for export")
            return []
        
        return list(output_dir.rglob(f"*.{format}"))

    def run_live_preview(self, port: int = 3000) -> None:
        try:
            subprocess.run(
                ["npx", "obsidian-live-preview", "--vault", str(self.vault_path), "--port", str(port)],
                check=True
            )
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print(f"Live preview failed: {e}")

    def lint_on_save(self, file_path: Path) -> bool:
        if file_path.suffix not in [".md", ".mmd"]:
            return True
        
        content = file_path.read_text()
        mermaid_code = self._extract_mermaid(content)
        
        if not mermaid_code.strip():
            return True
        
        try:
            result = subprocess.run(
                ["python", "-m", "mermaid_syntax_validator.validate", "-"],
                input=mermaid_code,
                capture_output=True, text=True, timeout=10
            )
            if result.returncode != 0:
                print(f"Lint failed for {file_path}:")
                print(result.stdout)
                return False
        except Exception as e:
            print(f"Lint error: {e}")
        
        return True


def main():
    parser = argparse.ArgumentParser(description="Obsidian Mermaid Integration")
    parser.add_argument("vault", type=Path, help="Path to Obsidian vault")
    parser.add_argument("--install-plugins", action="store_true", help="Install recommended plugins")
    parser.add_argument("--sync-canvas", type=Path, help="Convert canvas to mermaid")
    parser.add_argument("--sync-mermaid", type=Path, help="Convert mermaid to canvas")
    parser.add_argument("--output", type=Path, help="Output file")
    parser.add_argument("--export", type=Path, help="Export vault to HTML/PDF")
    parser.add_argument("--lint", type=Path, help="Lint file on save")
    parser.add_argument("--preview", action="store_true", help="Run live preview server")
    
    args = parser.parse_args()
    
    integration = ObsidianIntegration(args.vault)
    
    if args.install_plugins:
        installed = integration.install_plugins()
        integration.enable_plugins(installed)
        integration.configure_plugins()
        print(f"Installed and configured: {installed}")
    
    if args.sync_canvas:
        result = integration.sync_canvas_to_mermaid(args.sync_canvas, args.output)
        print(result)
    
    if args.sync_mermaid:
        result = integration.sync_mermaid_to_canvas(args.sync_mermaid, args.output)
        print(json.dumps(result, indent=2))
    
    if args.export:
        files = integration.export_vault(args.export)
        print(f"Exported {len(files)} files")
    
    if args.lint:
        ok = integration.lint_on_save(args.lint)
        print("OK" if ok else "FAIL")
        sys.exit(0 if ok else 1)
    
    if args.preview:
        integration.run_live_preview()


if __name__ == "__main__":
    main()