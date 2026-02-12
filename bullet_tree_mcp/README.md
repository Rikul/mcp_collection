# bullet-tree-mcp

An MCP server with small utilities for turning indented bullet lists into a simple tree structure (and rendering them back).

This is useful when you want structured data without committing to YAML/JSON everywhere — an outline can *be* the data.

## Tools

- `bullet_tree_parse(text, indent_size=None)` → JSON (`{"indent_size": N, "tree": [...]}`)
- `bullet_tree_render(tree_json, bullet='-', indent_size=2)` → outline text
- `bullet_tree_paths(text, indent_size=None, sep=' / ')` → one path per line

See `usage.md` for examples.
