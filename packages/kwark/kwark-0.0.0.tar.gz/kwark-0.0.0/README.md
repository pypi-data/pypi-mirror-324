# Kwark

## Tap into AI brilliance from a simple shell command

The tool currently has one command, `rize`, short for "summarize", which uses the Anthropic API to summarize the conculsions from a discussion or thread. It's designed to allow capturing discussion from e.g. Slack and use the output for documentation.

## Usage

The `rize` command processes text from standard input.

```bash
pbpaste | kwark rize
```

## Quick installation (MacOS)

```bash
brew install python@3.11
python3.11 -m pip install pipx
pipx install kwark
```

