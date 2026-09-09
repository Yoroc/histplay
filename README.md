# histplay

![CI](https://github.com/Yoroc/histplay/actions/workflows/ci.yml/badge.svg)
![PyPI - Version](https://img.shields.io/pypi/v/histplay?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/histplay?style=flat-square)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)

![Demo](./@yoro.svg)

Turn shell history into a clean, replayable session script.

## Installation

```bash
pip install histplay
```

## Usage

```bash
# Generate a replayable script from your last 20 history entries
histplay -n 20

# Output as Markdown code block
histplay --markdown -n 10

# Save to file
histplay -o session.sh -n 15

# Bare commands only (no headers or markdown)
histplay --bare -n 5
```

## Example

```bash
histplay --markdown -n 10
```

## How It Works

Reads your shell history, filters out noise (like wrapper scripts, typos, and redundant commands), and generates a clean, shareable session script.

## Requirements

- Python 3.8+
- typer

## License

MIT © Yoroc
