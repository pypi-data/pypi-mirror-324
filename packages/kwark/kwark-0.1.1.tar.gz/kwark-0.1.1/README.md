# Kwark

## Tap into AI brilliance from a simple shell command

The tool currently has one command, `rize`, short for "summarize", which uses the Anthropic API to summarize the conculsions from a discussion or thread. It's designed to allow capturing discussion from e.g. Slack and use the output for documentation.

<a href="https://www.flaticon.com/">Logo by Freepik-Flaticon</a>

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

## Authentication

Currently only works with Anthropic and requires a token set in the standard environment variable. Here's my trick to use 1Password.

```bash
export ANTHROPIC_API_KEY=$(op read "op://Private/Anthropic/api-key")
```