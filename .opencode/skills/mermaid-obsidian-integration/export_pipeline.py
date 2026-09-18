#!/usr/bin/env python3
"""
Export Pipeline: Vault -> HTML/PDF with Mermaid rendered
"""

import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import List
import re


class ExportPipeline:
    def __init__(self, vault_path: Path, output_dir: Path):
        self.vault_path = Path(vault_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_to_html(self, template: str = None) -> List[Path]:
        """Export vault to HTML with Mermaid rendered"""
        
        # Find all markdown files
        md_files = list(self.vault_path.rglob("*.md"))
        
        results = []
        for md_file in md_files:
            rel_path = md_file.relative_to(self.vault_path)
            out_file = self.output_dir / rel_path.with_suffix(".html")
            out_file.parent.mkdir(parents=True, exist_ok=True)
            
            content = md_file.read_text(encoding="utf-8")
            html = self._markdown_to_html(content, md_file)
            out_file.write_text(html, encoding="utf-8")
            results.append(out_file)
        
        # Copy assets
        self._copy_assets()
        
        return results

    def _markdown_to_html(self, content: str, source_file: Path) -> str:
        """Convert markdown with mermaid to HTML"""
        
        # Extract and render mermaid blocks
        html_parts = []
        lines = content.splitlines()
        in_mermaid = False
        mermaid_lines = []
        mermaid_count = 0
        
        for line in lines:
            if line.strip().startswith("```mermaid"):
                in_mermaid = True
                mermaid_lines = []
                continue
            elif line.strip().startswith("```") and in_mermaid:
                in_mermaid = False
                mermaid_code = "\n".join(mermaid_lines)
                mermaid_html = self._render_mermaid_to_html(mermaid_code, mermaid_count)
                html_parts.append(mermaid_html)
                mermaid_count += 1
                continue
            elif in_mermaid:
                mermaid_lines.append(line)
                continue
            
            html_parts.append(line)
        
        # Join and convert markdown to HTML (simplified)
        markdown_text = "\n".join(html_parts)
        html = self._simple_markdown_to_html(markdown_text)
        
        # Wrap in full HTML document
        return self._wrap_html(html, source_file.stem)

    def _render_mermaid_to_html(self, mermaid_code: str, index: int) -> str:
        """Render mermaid to HTML using mermaid-cli or embed as-is for client-side rendering"""
        
        # Option 1: Client-side rendering (simpler, works offline)
        return f'''
<div class="mermaid" id="mermaid-{index}">
{mermaid_code}
</div>
<script>
if (typeof mermaid !== 'undefined') {{
    mermaid.init(undefined, document.querySelectorAll('#mermaid-{index} .mermaid'));
}}
</script>
'''

    def _simple_markdown_to_html(self, text: str) -> str:
        """Basic markdown to HTML conversion"""
        # Headers
        text = re.sub(r'^### (.*$)', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.*$)', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        text = re.sub(r'^# (.*$)', r'<h1>\1</h1>', text, flags=re.MULTILINE)
        
        # Bold/italic
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        
        # Code
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        
        # Links
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        
        # Wikilinks
        text = re.sub(r'\[\[([^\]]+)\]\]', r'<a href="#\1">\1</a>', text)
        
        # Lists
        text = re.sub(r'^- (.*$)', r'<li>\1</li>', text, flags=re.MULTILINE)
        text = re.sub(r'(<li>.*</li>\n)+', r'<ul>\n\1</ul>', text)
        
        # Paragraphs
        text = re.sub(r'\n\n+', '</p>\n<p>', text)
        text = '<p>' + text + '</p>'
        text = re.sub(r'<p></p>', '', text)
        
        return text

    def _wrap_html(self, body: str, title: str) -> str:
        """Wrap content in full HTML document with Mermaid.js"""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose',
            flowchart: {{ useMaxWidth: true, htmlLabels: true }}
        }});
    </script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 0 auto; padding: 2rem; line-height: 1.6; }}
        .mermaid {{ text-align: center; margin: 2rem 0; }}
        pre {{ background: #f4f4f4; padding: 1rem; border-radius: 4px; overflow-x: auto; }}
        code {{ background: #f4f4f4; padding: 0.2rem 0.4rem; border-radius: 3px; }}
        pre code {{ background: none; padding: 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
        th, td {{ border: 1px solid #ddd; padding: 0.5rem; text-align: left; }}
        th {{ background: #f4f4f4; }}
        img {{ max-width: 100%; height: auto; }}
        blockquote {{ border-left: 4px solid #ddd; margin: 1rem 0; padding-left: 1rem; color: #666; }}
    </style>
</head>
<body>
{body}
</body>
</html>'''

    def _copy_assets(self):
        """Copy images and other assets"""
        for asset in self.vault_path.rglob("*.png"):
            rel = asset.relative_to(self.vault_path)
            dest = self.output_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset, dest)
        
        for asset in self.vault_path.rglob("*.jpg"):
            rel = asset.relative_to(self.vault_path)
            dest = self.output_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset, dest)

    def export_to_pdf(self) -> List[Path]:
        """Export to PDF via pandoc"""
        html_files = self.export_to_html()
        pdf_files = []
        
        for html_file in html_files:
            pdf_file = html_file.with_suffix(".pdf")
            try:
                subprocess.run([
                    "pandoc", str(html_file),
                    "-o", str(pdf_file),
                    "--pdf-engine=weasyprint",
                    "-V", "margin-top=2cm",
                    "-V", "margin-bottom=2cm",
                    "-V", "margin-left=2cm",
                    "-V", "margin-right=2cm"
                ], check=True, capture_output=True)
                pdf_files.append(pdf_file)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"Pandoc not available or failed for {html_file}")
        
        return pdf_files


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Export Obsidian vault with Mermaid")
    parser.add_argument("vault", type=Path, help="Vault path")
    parser.add_argument("output", type=Path, help="Output directory")
    parser.add_argument("--pdf", action="store_true", help="Also generate PDF")
    args = parser.parse_args()

    pipeline = ExportPipeline(args.vault, args.output)
    
    print("Exporting to HTML...")
    html_files = pipeline.export_to_html()
    print(f"Generated {len(html_files)} HTML files")
    
    if args.pdf:
        print("Generating PDFs...")
        pdf_files = pipeline.export_to_pdf()
        print(f"Generated {len(pdf_files)} PDF files")


if __name__ == "__main__":
    main()