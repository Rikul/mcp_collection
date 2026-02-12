# Usage (LLM-facing)

## What this server is good for

- Inspecting a Markdown document and listing its fenced code blocks
- Extracting a specific fenced code block by index
- Removing code blocks (optionally by language) to produce a “clean text” version

## Tools

### list_fenced_code_blocks(markdown)

Returns a JSON array. Each element includes:

- `index` (0-based)
- `info` (the raw fence info string after ```)
- `language` (best-effort first token of `info`, lowercased)
- `start_line` / `end_line` (1-based, inclusive)
- `content_preview` (first ~120 chars)

### extract_fenced_code_block(markdown, index=0)

Returns just the code block contents (no fences). If the index is out of range, returns a helpful error message.

### strip_fenced_code_blocks(markdown, language=None)

Removes fenced code blocks.

- If `language` is omitted, removes all fenced code blocks.
- If `language` is provided (e.g. `python`), removes only blocks whose language matches (case-insensitive).

Note: indentation-based code blocks are not handled.

## Example workflow

1) Call `list_fenced_code_blocks` to find what’s inside.
2) Extract what you need with `extract_fenced_code_block`.
3) Optionally remove blocks with `strip_fenced_code_blocks` to summarize the prose.
