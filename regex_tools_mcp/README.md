# Regex Tools MCP Server

A tiny MCP server that exposes a few safe, local regex utilities (Python `re`).

## Tools

- `regex_validate` — compile a pattern with flags and return any error details.
- `regex_find` — find matches with spans and capture groups.
- `regex_replace` — perform a regex substitution.

No network calls. Pure in-memory string processing.
