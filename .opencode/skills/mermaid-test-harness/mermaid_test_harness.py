#!/usr/bin/env python3
"""
Mermaid Test Harness
Testing framework for Mermaid diagrams: golden master, regression, syntax validation.
"""

import pytest
import subprocess
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Union
from dataclasses import dataclass, asdict
import difflib


@dataclass
class TestCase:
    name: str
    input_path: Path
    golden_path: Path
    diagram_type: str
    tags: List[str]


@dataclass
class TestResult:
    name: str
    passed: bool
    message: str
    diff: str = ""
    render_time_ms: float = 0.0


class GoldenMaster:
    def __init__(self, golden_dir: Union[str, Path]):
        self.golden_dir = Path(golden_dir)
        self.golden_dir.mkdir(parents=True, exist_ok=True)

    def get_golden_path(self, test_name: str, format: str = "png") -> Path:
        return self.golden_dir / f"{test_name}.{format}"

    def save_golden(self, test_name: str, content: bytes, format: str = "png") -> Path:
        path = self.get_golden_path(test_name, format)
        path.write_bytes(content)
        return path

    def load_golden(self, test_name: str, format: str = "png") -> bytes:
        path = self.get_golden_path(test_name, format)
        if path.exists():
            return path.read_bytes()
        return None

    def compare(self, test_name: str, actual: bytes, format: str = "png") -> bool:
        golden = self.load_golden(test_name, format)
        if golden is None:
            return False
        return golden == actual


class MermaidTestHarness:
    def __init__(self, fixtures_dir: Union[str, Path], golden_dir: Union[str, Path], renderer_path: Union[str, Path], validator_path: Union[str, Path] = None):
        self.fixtures_dir = Path(fixtures_dir)
        self.golden = GoldenMaster(golden_dir)
        self.renderer_path = Path(renderer_path)
        self.validator_path = Path(validator_path) if validator_path else self.renderer_path.parent.parent / "mermaid-syntax-validator" / "validate.py"
        self.test_cases: List[TestCase] = []

    def discover_tests(self, patterns: List[str] = None) -> List[TestCase]:
        if patterns is None:
            patterns = ["*.mmd", "*.mermaid"]
        
        test_cases = []
        for pattern in patterns:
            for input_file in self.fixtures_dir.rglob(pattern):
                if "invalid" in str(input_file):
                    continue
                
                rel = input_file.relative_to(self.fixtures_dir)
                name = str(rel).replace("/", "_").replace(".mmd", "").replace(".mermaid", "")
                
                diagram_type = self._detect_diagram_type(input_file)
                
                test_cases.append(TestCase(
                    name=name,
                    input_path=input_file,
                    golden_path=self.golden.get_golden_path(name),
                    diagram_type=diagram_type,
                    tags=self._extract_tags(input_file)
                ))
            self.test_cases = test_cases
            return test_cases
        
        self.test_cases = test_cases
        return test_cases

    def _detect_diagram_type(self, file_path: Path) -> str:
        content = file_path.read_text(encoding="utf-8")
        for line in content.splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("%%"):
                first_word = stripped.split()[0] if stripped.split() else ""
                return first_word
        return "unknown"

    def _extract_tags(self, file_path: Path) -> List[str]:
        tags = []
        for part in file_path.parts:
            if part in ["flowchart", "sequenceDiagram", "classDiagram", "stateDiagram", "erDiagram",
                       "gantt", "gitGraph", "journey", "pie", "quadrantChart", "requirementDiagram",
                       "mindmap", "kanban", "architecture-beta", "timeline", "useCaseDiagram",
                       "objectDiagram", "componentDiagram", "packageDiagram", "c4", "service-design"]:
                tags.append(part)
        return tags

    def run_syntax_tests(self) -> List[TestResult]:
        results = []
        for tc in self.test_cases:
            result = self._run_syntax_test(tc)
            results.append(result)
        return results

    def _run_syntax_test(self, tc: TestCase) -> TestResult:
        try:
            result = subprocess.run(
                ["python", str(self.validator_path), str(tc.input_path)],
                capture_output=True, text=True, timeout=30
            )
            passed = result.returncode == 0
            return TestResult(
                name=tc.name,
                passed=passed,
                message=result.stdout if passed else result.stderr
            )
        except subprocess.TimeoutExpired:
            return TestResult(name=tc.name, passed=False, message="Syntax validation timeout")
        except Exception as e:
            return TestResult(name=tc.name, passed=False, message=str(e))

    def run_render_tests(self, format: str = "png", update_golden: bool = False) -> List[TestResult]:
        results = []
        for tc in self.test_cases:
            result = self._run_render_test(tc, format, update_golden)
            results.append(result)
        return results

    def _run_render_test(self, tc: TestCase, format: str, update_golden: bool) -> TestResult:
        import time
        start = time.time()
        
        try:
            output_file = tc.golden_path.with_suffix(f".{format}")
            result = subprocess.run(
                ["python", str(self.renderer_path), str(tc.input_path), "-o", str(output_file), "-f", format],
                capture_output=True, text=True, timeout=60
            )
            render_time = (time.time() - start) * 1000
            
            if result.returncode != 0:
                return TestResult(
                    name=tc.name,
                    passed=False,
                    message=f"Render failed: {result.stderr}",
                    render_time_ms=render_time
                )
            
            actual = output_file.read_bytes()
            
            if update_golden:
                self.golden.save_golden(tc.name, actual, format)
                return TestResult(
                    name=tc.name,
                    passed=True,
                    message="Golden master updated",
                    render_time_ms=render_time
                )
            
            if self.golden.compare(tc.name, actual, format):
                return TestResult(
                    name=tc.name,
                    passed=True,
                    message="Matches golden master",
                    render_time_ms=render_time
                )
            else:
                diff = self._compute_diff(tc.name, actual, format)
                return TestResult(
                    name=tc.name,
                    passed=False,
                    message="Visual regression detected",
                    diff=diff,
                    render_time_ms=render_time
                )
        except subprocess.TimeoutExpired:
            return TestResult(name=tc.name, passed=False, message="Render timeout")
        except Exception as e:
            return TestResult(name=tc.name, passed=False, message=str(e))

    def _compute_diff(self, name: str, actual: bytes, format: str) -> str:
        golden = self.golden.load_golden(name, format)
        if not golden:
            return "No golden master"
        
        if format in ["svg", "pdf"]:
            golden_text = golden.decode("utf-8", errors="replace")
            actual_text = actual.decode("utf-8", errors="replace")
            diff = difflib.unified_diff(
                golden_text.splitlines(),
                actual_text.splitlines(),
                lineterm=""
            )
            return "\n".join(diff)
        else:
            return f"Binary diff: {len(golden)} vs {len(actual)} bytes, hash: {hashlib.md5(actual).hexdigest()}"

    def generate_report(self, results: List[TestResult], output_path: Path):
        report = {
            "summary": {
                "total": len(results),
                "passed": sum(1 for r in results if r.passed),
                "failed": sum(1 for r in results if not r.passed),
                "total_time_ms": sum(r.render_time_ms for r in results)
            },
            "results": [asdict(r) for r in results]
        }
        output_path.write_text(json.dumps(report, indent=2))


# Pytest fixtures
@pytest.fixture
def test_harness():
    fixtures = Path(__file__).parent / "fixtures"
    golden = Path(__file__).parent / "golden"
    renderer = Path(__file__).parent.parent / "mermaid-renderer" / "render.py"
    return MermaidTestHarness(fixtures, golden, renderer)


def test_syntax_valid(test_harness):
    test_harness.discover_tests()
    results = test_harness.run_syntax_tests()
    failed = [r for r in results if not r.passed]
    assert not failed, f"Syntax failures: {[r.name for r in failed]}"


def test_render_matches_golden(test_harness):
    test_harness.discover_tests()
    results = test_harness.run_render_tests()
    failed = [r for r in results if not r.passed]
    assert not failed, f"Render failures: {[r.name for r in failed]}"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, default="fixtures")
    parser.add_argument("--golden", type=Path, default="golden")
    parser.add_argument("--renderer", type=Path, default="../mermaid-renderer/render.py")
    parser.add_argument("--update-golden", action="store_true")
    parser.add_argument("--format", default="png")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    harness = MermaidTestHarness(args.fixtures, args.golden, args.renderer)
    harness.discover_tests()
    
    print(f"Discovered {len(harness.test_cases)} test cases")
    
    print("Running syntax tests...")
    syntax_results = harness.run_syntax_tests()
    syntax_failed = [r for r in syntax_results if not r.passed]
    print(f"Syntax: {len(syntax_results) - len(syntax_failed)}/{len(syntax_results)} passed")
    
    print("Running render tests...")
    render_results = harness.run_render_tests(args.format, args.update_golden)
    render_failed = [r for r in render_results if not r.passed]
    print(f"Render: {len(render_results) - len(render_failed)}/{len(render_results)} passed")
    
    if args.report:
        all_results = syntax_results + render_results
        harness.generate_report(all_results, args.report)
        print(f"Report saved to {args.report}")
    
    if render_failed and not args.update_golden:
        for r in render_failed:
            print(f"  FAIL: {r.name} - {r.message}")
            if r.diff:
                print(f"    Diff: {r.diff[:200]}...")
        exit(1)