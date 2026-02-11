# csv-inspector-mcp

Small MCP server for inspecting local CSV files (no network access).

## Tools

- `csv_head(file_path, n=5, delimiter=",")` – preview first rows
- `csv_profile(file_path, delimiter=",", max_rows=5000)` – basic dataset + per-column type/missing stats
- `csv_top_values(file_path, column, delimiter=",", max_rows=20000, top_k=10)` – most common values for a column

## Notes

- Reads files from the local filesystem only.
- Uses Python's built-in `csv` module; no pandas dependency.
