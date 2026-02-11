# File Inspector MCP Server

## What it does

Deterministic, local-only helpers for inspecting files and directories.

## When to use it

- Quickly understand a path without opening it manually.
- Preview a config/log file head.
- Generate stable file hashes for caching/dedup.
- Summarize a directory shape with a depth limit.

## Tools

- `path_stat(path)`
- `file_head(path, lines=40, max_chars=8000)`
- `file_sha256(path, max_bytes=10485760)`
- `dir_tree(path, max_depth=2, max_entries=200)`

## Notes / safety

- No network access.
- `file_sha256` streams and refuses to read more than `max_bytes` (default 10MB).
- `file_head` is for text; it will return a best-effort UTF-8 decode.

## How to run

```bash
uv run file-inspector-mcp
```
