# Usage: python-ast-mcp

## Run

```bash
python-ast-mcp
```

## Tools

### `list_imports(code: str) -> str`
Returns a newline-delimited list of import statements, normalized.

Example output:

```
import os
import sys
from pathlib import Path
from x import y as z
```

### `list_definitions(code: str) -> str`
Lists top-level `class` and `def`/`async def` definitions with line numbers.

Example output:

```
L1: def main
L10: class Thing
L22: async def fetch
```

### `extract_docstring(code: str, name: str = "") -> str`
- If `name` is empty, returns the module docstring.
- If `name` matches a top-level function/class, returns its docstring.

If no docstring is found, returns `(no docstring)`.
