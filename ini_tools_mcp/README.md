# INI Tools MCP

Small MCP server that parses and edits INI config text using Python's standard library (`configparser`).

Notes:
- This server **does not** read/write files or make network calls.
- When rewriting INI text, comments and exact formatting may not be preserved (this is a `configparser` limitation).

## Tools

- `ini_to_json(text, *, include_defaults=False)`
- `ini_get(text, section, option, *, fallback="")`
- `ini_set(text, section, option, value)`
- `ini_remove_option(text, section, option)`
- `ini_remove_section(text, section)`
