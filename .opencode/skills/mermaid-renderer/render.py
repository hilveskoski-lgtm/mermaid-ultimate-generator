#!/usr/bin/env python3
"""
Mermaid Renderer
Renders Mermaid diagrams to PNG, SVG, PDF using multiple backends.
"""

import asyncio
import json
import subprocess
import sys
import tempfile
import os
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass
import argparse


@dataclass
class RenderConfig:
    theme: str = "default"
    background: str = "transparent"
    width: Optional[int] = None
    height: Optional[int] = None
    scale: float = 1.0
    format: str = "png"
    output_dir: Optional[Path] = None


class MermaidRenderer:
    def __init__(self, config: RenderConfig = None):
        self.config = config or RenderConfig()
        self._check_dependencies()

    def _check_dependencies(self):
        self.has_mmdc = self._check_command("mmdc")
        self.has_playwright = self._check_python_module("playwright")
        self.has_puppeteer = self._check_command("npx") and self._check_npx_puppeteer()

    def _check_command(self, cmd: str) -> bool:
        try:
            subprocess.run([cmd, "--version"], capture_output=True, check=False)
            return True
        except FileNotFoundError:
            return False

    def _check_python_module(self, module: str) -> bool:
        try:
            __import__(module)
            return True
        except ImportError:
            return False

    def _check_npx_puppeteer(self) -> bool:
        try:
            result = subprocess.run(["npx", "puppeteer", "--version"], capture_output=True, check=False, timeout=5)
            return result.returncode == 0
        except Exception:
            return False

    def render_file(self, input_path: Path, output_path: Path = None) -> Path:
        content = input_path.read_text(encoding="utf-8")
        return self.render_string(content, output_path or input_path.with_suffix(f".{self.config.format}"))

    def render_string(self, content: str, output_path: Path) -> Path:
        mermaid_code = self._extract_mermaid(content)
        
        if self.has_mmdc:
            return self._render_mmdc(mermaid_code, output_path)
        elif self.has_playwright:
            return asyncio.run(self._render_playwright(mermaid_code, output_path))
        elif self.has_puppeteer:
            return self._render_puppeteer(mermaid_code, output_path)
        else:
            raise RuntimeError("No rendering backend available. Install @mermaid-js/mermaid-cli or playwright.")

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
        
        if mermaid_lines:
            return "\n".join(mermaid_lines)
        return content

    def _render_mmdc(self, mermaid_code: str, output_path: Path) -> Path:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False, encoding="utf-8") as f:
            f.write(mermaid_code)
            temp_input = f.name
        
        try:
            cmd = [
                "mmdc",
                "-i", temp_input,
                "-o", str(output_path),
                "-t", self.config.theme,
                "-b", self.config.background,
            ]
            if self.config.width:
                cmd.extend(["-w", str(self.config.width)])
            if self.config.scale != 1.0:
                cmd.extend(["-s", str(self.config.scale)])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                raise RuntimeError(f"mmdc failed: {result.stderr}")
            
            return output_path
        finally:
            os.unlink(temp_input)

    async def _render_playwright(self, mermaid_code: str, output_path: Path) -> Path:
        from playwright.async_api import async_playwright
        
        html = self._generate_html(mermaid_code)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.set_content(html, wait_until="networkidle")
            
            # Wait for mermaid to render
            await page.wait_for_function("typeof mermaid !== 'undefined' && document.querySelector('.mermaid')")
            await page.wait_for_timeout(1000)
            
            element = await page.query_selector(".mermaid")
            if element:
                await element.screenshot(path=str(output_path))
            else:
                await page.screenshot(path=str(output_path), full_page=True)
            
            await browser.close()
        
        return output_path

    def _render_puppeteer(self, mermaid_code: str, output_path: Path) -> Path:
        html = self._generate_html(mermaid_code)
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(html)
            temp_html = f.name
        
        try:
            cmd = [
                "npx", "puppeteer",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--screenshot", str(output_path),
                temp_html
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                raise RuntimeError(f"Puppeteer failed: {result.stderr}")
            return output_path
        finally:
            os.unlink(temp_html)

    def _generate_html(self, mermaid_code: str) -> str:
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: '{self.config.theme}',
            themeVariables: {{
                background: '{self.config.background}'
            }},
            flowchart: {{
                htmlLabels: true,
                curve: 'basis'
            }}
        }});
    </script>
    <style>
        body {{ margin: 0; padding: 20px; background: {self.config.background}; }}
        .mermaid {{ display: flex; justify-content: center; }}
    </style>
</head>
<body>
    <div class="mermaid">
{mermaid_code}
    </div>
</body>
</html>"""

    def render_batch(self, input_dir: Path, pattern: str = "*.mmd") -> List[Path]:
        files = list(input_dir.rglob(pattern))
        results = []
        
        for input_file in files:
            rel_path = input_file.relative_to(input_dir)
            output_file = (self.config.output_dir or input_dir) / rel_path.with_suffix(f".{self.config.format}")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                result = self.render_file(input_file, output_file)
                results.append(result)
                print(f"Rendered: {input_file} -> {result}")
            except Exception as e:
                print(f"Failed: {input_file} - {e}")
        
        return results


def main():
    parser = argparse.ArgumentParser(description="Render Mermaid diagrams")
    parser.add_argument("input", type=Path, help="Input file or directory")
    parser.add_argument("-o", "--output", type=Path, help="Output file or directory")
    parser.add_argument("-t", "--theme", default="default", choices=["default", "dark", "forest", "neutral", "base"])
    parser.add_argument("-b", "--background", default="transparent")
    parser.add_argument("-w", "--width", type=int, help="Output width")
    parser.add_argument("-s", "--scale", type=float, default=1.0, help="Scale factor")
    parser.add_argument("-f", "--format", default="png", choices=["png", "svg", "pdf"])
    parser.add_argument("--batch", action="store_true", help="Render all files in directory")
    parser.add_argument("--pattern", default="*.mmd", help="File pattern for batch")
    
    args = parser.parse_args()
    
    config = RenderConfig(
        theme=args.theme,
        background=args.background,
        width=args.width,
        scale=args.scale,
        format=args.format,
        output_dir=args.output
    )
    
    renderer = MermaidRenderer(config)
    
    if args.batch or args.input.is_dir():
        if not args.output:
            args.output = args.input
        results = renderer.render_batch(args.input, args.pattern)
        print(f"Rendered {len(results)} files")
    else:
        output = args.output or args.input.with_suffix(f".{args.format}")
        result = renderer.render_file(args.input, output)
        print(f"Rendered: {result}")


if __name__ == "__main__":
    main()