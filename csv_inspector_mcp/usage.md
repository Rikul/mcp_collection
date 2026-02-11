# csv-inspector-mcp usage

## Start the server

```bash
csv-inspector-mcp
```

## Example calls

### Preview a file

- Tool: `csv_head`
- Args:
  - `file_path`: `/path/to/file.csv`
  - `n`: `10`
  - `delimiter`: `,`

### Profile a file (lightweight schema)

- Tool: `csv_profile`
- Args:
  - `file_path`: `/path/to/file.csv`
  - `max_rows`: `2000`

### See top values in a column

- Tool: `csv_top_values`
- Args:
  - `file_path`: `/path/to/file.csv`
  - `column`: `status`
  - `top_k`: `5`

## Output conventions

- All results are returned as plain text.
- This server never fetches any URLs; it only reads local files.
