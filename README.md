# histplay

![CI](https://github.com/Yoroc/histplay/actions/workflows/ci.yml/badge.svg)
![PyPI - Version](https://img.shields.io/pypi/v/histplay?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/histplay?style=flat-square)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)

![Demo](./@yoro.svg)

Histplay is a CLI tool that turns your shell history into a clean, replayable session script. It filters out noise (like wrapper scripts, typos, and repetitive commands) and generates a shareable, executable bash/zsh script — perfect for onboarding, debugging, or saving dev sessions.

## Installation

```bash
pip install typer
```

Or clone the repository and run the script directly.

## Usage

```bash
histplay [OPTIONS]
```

Options:
  -H, --history PATH     Path to shell history file. Defaults to ~/.bash_history or ~/.zsh_history.
  -n, --limit INTEGER    Number of history entries to process. [default: 20]
  -o, --output PATH      Output file. If not provided, prints to stdout.
  --markdown             Output as a markdown code block.
  --bare                 Output only commands, no separators or comments.
  --install-completion   Install completion for the current shell.
  --show-completion      Show completion for the current shell, to copy it or customize.
  --help                 Show this message and exit.

## Example

```bash
histplay -n 30 > session.sh
```

This will generate a clean session script from your last 30 history entries.

## How It Works

- **History Input**: Reads from `~/.bash_history` or `~/.zsh_history`.
- **Noise Filter**: Removes wrapper scripts, empty lines, typos, and repetitive noise (like `ls`, `clear`, `cd`).
- **Fallback**: If history is too noisy (e.g. filled with launcher shims), generates a realistic sample session.
- **Output**: Returns a clean, executable script — ready to share or rerun.

## Requirements

- Python 3.7+
- Typer

## License

MIT