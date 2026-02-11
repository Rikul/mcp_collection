# outline_parser_mcp

Tiny MCP server for turning simple bullet outlines into a structured JSON tree (and back).

This is inspired by structured-text workflows (e.g., outline-first writing). It does **not** fetch URLs or touch the network.

## Tools

- `outline_to_json(text: str) -> str`
  - Parses a plain-text outline (typically `- item` with indentation) into JSON.
  - Supports `-`, `*`, `+`, and `1.`/`2.` style list markers.
  - Lines without a marker are treated as a continuation of the previous item.

- `json_to_outline(json_text: str, bullet: str = "-", indent: int = 2) -> str`
  - Renders JSON produced by `outline_to_json` back into a bullet outline.

## Run

```bash
outline-parser-mcp
```
