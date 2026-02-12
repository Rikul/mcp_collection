# Usage (LLM guide)

Start the server (one example):

```bash
ini-tools-mcp
```

## Example: inspect INI

Input INI:

```ini
[app]
name = demo
port = 8080

[auth]
enabled = true
```

- Call `ini_to_json` to get a structured view.
- Call `ini_get(text, "app", "port")` to extract a single value.

## Example: edit INI

- Call `ini_set` to set/update a value. The tool returns the rewritten INI text.
- Call `ini_remove_option` / `ini_remove_section` to delete entries.

### Important limitations

- `configparser` may rewrite formatting and will generally drop comments.
- Sections/options are treated case-insensitively by default.
