# diff-tools-mcp

A tiny MCP server that generates human-readable diffs between two text blobs.

This is useful for:
- showing what changed between two versions of a prompt, config, or document
- producing patch-like output for review

No network access. Pure Python stdlib (`difflib`).
