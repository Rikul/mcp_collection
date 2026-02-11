# diff-tools-mcp (usage)

## Tools

### `unified_diff`
Generate a unified diff between `a` and `b`.

Inputs:
- `a` (string): original text
- `b` (string): updated text
- `fromfile` (string, optional): label for the original (default: `a`)
- `tofile` (string, optional): label for the updated (default: `b`)
- `context_lines` (int, optional): lines of context (default: 3)

Returns:
- A unified diff string (or `(no changes)`)

### `ndiff`
Generate an `ndiff` (character-level) diff view, good for spotting whitespace changes.

Inputs:
- `a` (string): original text
- `b` (string): updated text

Returns:
- An `ndiff` formatted diff string

## Run

```bash
diff-tools-mcp
```
