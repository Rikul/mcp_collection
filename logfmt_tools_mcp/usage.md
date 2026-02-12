# Logfmt Tools MCP — Usage

This server helps with logfmt, a simple logging format where each line contains tokens like:

`ts=2026-02-11T21:00:00Z level=info msg="hello world" user_id=123 ok=true`

## Tools

### `logfmt_parse`
Parse one logfmt line to JSON.

**Args**
- `line` (string): logfmt line

**Returns**
- JSON (string) with keys/values parsed from the line.

Notes:
- Tokens without `=` are collected under `_bare` (array).
- Repeated keys become arrays.

### `logfmt_format`
Format a JSON object into a logfmt line.

**Args**
- `record_json` (string): JSON object (e.g. `{ "level": "info", "ok": true }`)

**Returns**
- logfmt line (string)

Notes:
- Strings are quoted if needed.
- Arrays become repeated keys: `k=v k=v`.

### `logfmt_parse_file_head`
Parse the first N lines of a file and return JSON lines (one object per line).

**Args**
- `file_path` (string): path to a local file
- `max_lines` (int, default 50, max 500)

**Returns**
- A JSON array (string) of parsed records.
