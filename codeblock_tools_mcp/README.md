# codeblock_tools_mcp

MCP server providing small utilities for working with fenced code blocks inside Markdown.

It is intentionally dependency-light and does **not** fetch or execute any code.

## Tools

- `list_fenced_code_blocks(markdown)`
- `extract_fenced_code_block(markdown, index=0)`
- `strip_fenced_code_blocks(markdown, language=None)`

See `usage.md` for examples.
