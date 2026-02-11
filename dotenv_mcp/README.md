# dotenv-mcp

Small MCP server that helps you work with `.env` / dotenv text **without fetching anything**.

## Tools

- `parse_env(text)` → JSON mapping of keys to values
- `render_env(json_text)` → `.env` text (sorted keys)
- `diff_env(old_text, new_text)` → human-readable added/removed/changed report

## Install

```bash
pip install -e .
```

## Run

```bash
dotenv-mcp
```

See `usage.md` for examples.
