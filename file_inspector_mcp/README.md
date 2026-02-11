# File Inspector MCP Server

Small, local-only file utilities: stats, previews, hashes, and directory trees.

## Available tools

- `path_stat(path)` – basic info (type, size, mtime)
- `file_head(path, lines=40, max_chars=8000)` – preview the start of a text file
- `file_sha256(path, max_bytes=10485760)` – SHA-256 of a file (streamed)
- `dir_tree(path, max_depth=2, max_entries=200)` – simple directory tree

## Running

```bash
uv run file-inspector-mcp
```
