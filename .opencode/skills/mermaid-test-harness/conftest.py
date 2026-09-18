# Pytest configuration for Mermaid Test Harness

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from mermaid_test_harness import MermaidTestHarness, TestCase


@pytest.fixture(scope="session")
def test_harness():
    fixtures = Path(__file__).parent / "fixtures"
    golden = Path(__file__).parent / "golden"
    renderer = Path(__file__).parent.parent / "mermaid-renderer" / "render.py"
    harness = MermaidTestHarness(fixtures, golden, renderer)
    harness.discover_tests()
    return harness


@pytest.fixture
def valid_flowchart():
    return TestCase(
        name="flowchart_basic",
        input_path=Path(__file__).parent / "fixtures" / "valid" / "flowchart_basic.mmd",
        golden_path=Path(__file__).parent / "golden" / "flowchart_basic.png",
        diagram_type="flowchart",
        tags=["flowchart", "basic"]
    )


@pytest.fixture
def valid_sequence():
    return TestCase(
        name="sequence_basic",
        input_path=Path(__file__).parent / "fixtures" / "valid" / "sequence_basic.mmd",
        golden_path=Path(__file__).parent / "golden" / "sequence_basic.png",
        diagram_type="sequenceDiagram",
        tags=["sequenceDiagram", "basic"]
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "syntax: syntax validation tests")
    config.addinivalue_line("markers", "render: render regression tests")
    config.addinivalue_line("markers", "slow: slow running tests")
    config.addinivalue_line("markers", "golden: golden master tests")