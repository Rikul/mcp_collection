# regex-tools-mcp (usage)

## Run

```bash
regex-tools-mcp
```

This server runs over stdio.

## Tool: regex_validate

Validate a regex pattern and optional flags.

Args:
- `pattern` (str)
- `flags` (list[str], optional): any of `IGNORECASE`, `MULTILINE`, `DOTALL`, `VERBOSE`, `ASCII`, `LOCALE`, `UNICODE`

Returns:
- `{ "ok": true }` or `{ "ok": false, "error": "..." }`

## Tool: regex_find

Find matches and return structured results.

Args:
- `pattern` (str)
- `text` (str)
- `flags` (list[str], optional)
- `max_matches` (int, optional; default 200)

Returns:
- `{ "count": int, "matches": [ {"match": str, "span": [start,end], "groups": [...], "groupdict": {...} } ] }`

## Tool: regex_replace

Replace using a regex.

Args:
- `pattern` (str)
- `repl` (str)
- `text` (str)
- `flags` (list[str], optional)
- `count` (int, optional; default 0 meaning replace all)

Returns:
- `{ "result": str, "replacements": int }`
