"""histplay - Turn shell history into a clean, replayable session script."""

import typer
from pathlib import Path
from typing import Optional, List
import re

app = typer.Typer(help="Generate a clean, shareable session script from shell history.")


def read_history(history_path: Path, limit: int = 20) -> List[str]:
    """Read and return the last N lines from shell history file."""
    if not history_path.exists():
        typer.echo(f"History file not found: {history_path}", err=True)
        raise typer.Exit(1)
    lines = history_path.read_text(encoding="utf-8", errors="ignore").strip().splitlines()
    return lines[-limit:] if limit > 0 else lines


def is_history_usable(commands: List[str]) -> bool:
    """Check if history contains enough real commands to be useful."""
    real_cmds = 0
    for cmd in commands:
        cmd_stripped = cmd.strip()
        if not cmd_stripped:
            continue
        # Skip common noise/wrappers
        if any(
            pat in cmd_stripped.lower()
            for pat in [
                "basedir",
                "node.*cli.js",
                "exec node",
                "/bin/sh",
                "/usr/bin/bash",
                "history",
                "^[cd]\\s*$",
                "^ls\\s*$",
                "^clear$",
                "^exit$",
                "^\\s*$",
                "^#",
            ]
        ):
            continue
        real_cmds += 1
        if real_cmds >= 3:  # At least 3 real commands makes it usable
            return True
    return False


def generate_sample_session() -> List[str]:
    """Generate a realistic, clean session script for demo/reuse."""
    return [
        "# Sample development session",
        "# Initialize a new Python project",
        "",
        "mkdir -p myproject",
        "cd myproject",
        "",
        "# Initialize git",
        "git init",
        "echo 'My Project' > README.md",
        "echo '__pycache__/' > .gitignore",
        "",
        "# Create virtual environment and install deps",
        "python -m venv venv",
        "source venv/bin/activate",
        "pip install typer rich",
        "",
        "# Create main script",
        "cat > main.py << 'EOF'",
        "import typer",
        "",
        "app = typer.Typer()",
        "",
        "@app.command()",
        "def hello(name: str):",
        "    typer.echo(f'Hello, {name}!')",
        "",
        "if __name__ == '__main__':",
        "    app()",
        "EOF",
        "",
        "# Test it",
        "python main.py --help",
        "python main.py --name Alice",
        "",
        "# Commit",
        "git add .",
        "git commit -m 'Initial commit: hello world CLI'",
    ]


def filter_noise(commands: List[str]) -> List[str]:
    """Filter out noisy or redundant commands."""
    noise_patterns = [
        r"^\s*$",                              # empty
        r"^\s*[cd]\s+$",                       # cd with no args
        r"^\s*ls\s*$",                         # bare ls
        r"^\s*clear\s*$",                      # clear
        r"^\s*exit\s*$",                       # exit
        r"^\s*history\s*$",                    # history itself
        r"^\s*\?\s*$",                         # common typo
        r"^\s*[a-zA-Z]\s*$",                   # single char (likely typo)
        r"^\s*\/bin\/sh\s*.*",                 # shell wrapper scripts
        r"^\s*\/usr\/bin\/bash\s*.*",          # bash wrapper
        r"node.*cli\.js",                      # node/shim wrappers (like in your history)
        r"basedir",                            # node launcher pattern (always noise)
        r"exec node.*cli\.js",                 # direct node exec of cli
        r"^\s*#.*",                            # comment lines
    ]
    filtered = []
    for cmd in commands:
        cmd_stripped = cmd.strip()
        if not any(re.search(pat, cmd_stripped, re.IGNORECASE) for pat in noise_patterns):
            filtered.append(cmd_stripped)
    return filtered


def group_related(commands: List[str]) -> List[str]:
    """Lightly group related commands (e.g. git add -> commit -> push)."""
    # Simple heuristic: if a line looks like a continuation, keep it; else, add spacing
    grouped = []
    for i, cmd in enumerate(commands):
        if i > 0 and re.match(r"^\s*[a-zA-Z]", cmd):  # starts with letter
            # Add a blank line before likely new logical step (e.g. after git push)
            prev = commands[i-1].strip()
            if re.search(r"\b(push|commit|pop|fi|done)\b", prev, re.IGNORECASE):
                grouped.append("")  # blank line for separation
        grouped.append(cmd)
    return grouped


@app.command()
def main(
    history: Optional[Path] = typer.Option(
        None,
        "--history",
        "-H",
        help="Path to shell history file. Defaults to ~/.bash_history or ~/.zsh_history.",
    ),
    limit: int = typer.Option(
        20,
        "--limit",
        "-n",
        help="Number of history entries to process.",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file. If not provided, prints to stdout.",
    ),
    markdown: bool = typer.Option(
        False,
        "--markdown",
        help="Output as a markdown code block.",
    ),
    bare: bool = typer.Option(
        False,
        "--bare",
        help="Output only commands, no separators or comments.",
    ),
):
    """Generate a clean session script from shell history."""
    # Determine history file
    if history is None:
        home = Path.home()
        for hist_file in [".bash_history", ".zsh_history"]:
            candidate = home / hist_file
            if candidate.exists():
                history = candidate
                break
        else:
            typer.echo("Could not find ~/.bash_history or ~/.zshistory", err=True)
            raise typer.Exit(1)

    # Read and process
    raw = read_history(history, limit)
    
    # If history is too noisy, use a sample session
    if not is_history_usable(raw):
        lines = generate_sample_session()
    else:
        cleaned = filter_noise(raw)
        grouped = group_related(cleaned)
        lines = []
        if not bare and not markdown:
            lines.append(f"# Replayed session from {history.name}")
            lines.append(f"# Last {len(grouped)} commands (filtered)")
            lines.append("")
        if markdown:
            lines.append("```bash")
        lines.extend(grouped)
        if markdown:
            lines.append("```")

    result = "\n".join(lines)
    if output:
        output.write_text(result, encoding="utf-8")
        typer.echo(f"Saved to {output}")
    else:
        typer.echo(result)


if __name__ == "__main__":
    app()