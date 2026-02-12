# logfmt_tools_mcp

Small MCP server for working with **logfmt** (common key=value log lines).

## What it does

- Parse a logfmt line into JSON
- Format JSON into a logfmt line
- Parse the first N lines of a file (best-effort)

No network access. Pure local text processing.
