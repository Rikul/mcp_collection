# Text Utilities MCP Server

## What it does

Small deterministic text helpers (counts, hashing, URL extraction, whitespace normalization).

## When to use it

- Clean/normalize text before passing it to other tools.
- Extract URLs as plain strings (no fetching).
- Produce stable hashes for caching/dedup.

## Tools

- `word_count(text)`
- `sha256(text)`
- `extract_urls(text)`
- `normalize_whitespace(text)`

## How to run

```bash
uv run text-utils-mcp
```
