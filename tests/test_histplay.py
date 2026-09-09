"""Test histplay CLI functionality."""

import os
import tempfile
from pathlib import Path
from histplay.histplay import app

from typer.testing import CliRunner

runner = CliRunner()


def test_histplay_help():
    """Test that help runs and returns success."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Generate a clean session script" in result.output


def test_histplay_bare_output():
    """Test --bare flag returns only commands."""
    result = runner.invoke(app, ["--bare", "-n", "5"])
    assert result.exit_code == 0
    output = result.output.strip()
    # Should not contain headers or markdown
    assert not output.startswith("#")
    assert "```" not in output
    # Should have content (from sample session)
    assert len(output) > 10


def test_histplay_markdown_output():
    """Test --markdown flag returns code block."""
    result = runner.invoke(app, ["--markdown", "-n", "5"])
    assert result.exit_code == 0
    output = result.output.strip()
    assert output.startswith("```bash")
    assert output.endswith("```")
    assert "mkdir -p" in output or "git init" in output


def test_histplay_output_file():
    """Test -o flag writes to file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        outfile = Path(tmpdir) / "test.sh"
        result = runner.invoke(app, ["-o", str(outfile), "-n", "5"])
        assert result.exit_code == 0
        assert outfile.exists()
        content = outfile.read_text().strip()
        assert len(content) > 10
        assert "# Sample development session" in content or "mkdir -p" in content


def test_histplay_default_output():
    """Test default output is not empty."""
    result = runner.invoke(app, ["-n", "5"])
    assert result.exit_code == 0
    output = result.stdout.strip()
    assert len(output) > 10