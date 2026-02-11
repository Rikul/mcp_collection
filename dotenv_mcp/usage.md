# Usage (dotenv-mcp)

## parse_env

Input:

```text
# comment
DATABASE_URL=postgres://user:pass@localhost:5432/db
export DEBUG=true
EMPTY=
QUOTED="hello world"
SINGLE='hi'
```

Output: JSON (as a string)

## render_env

Provide a JSON object string like:

```json
{"DEBUG":"true","EMPTY":"","QUOTED":"hello world"}
```

Output: `.env` text (keys sorted).

## diff_env

Compares two dotenv blobs by key and reports:

- added keys
- removed keys
- changed keys (old → new)

Notes:
- Comments and blank lines are ignored.
- Values are treated as strings.
