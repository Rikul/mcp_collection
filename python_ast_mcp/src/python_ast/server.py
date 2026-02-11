from __future__ import annotations

import ast

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Python AST Tools")


def _parse(code: str) -> ast.Module:
    return ast.parse(code or "")


@mcp.tool()
async def list_imports(code: str) -> str:
    """List import statements in the provided Python source.

    Returns one normalized import per line.
    """

    try:
        tree = _parse(code)
    except SyntaxError as e:
        return f"syntax error: {e.msg} (line {e.lineno})"

    out: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    out.append(f"import {alias.name} as {alias.asname}")
                else:
                    out.append(f"import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            mod = "." * node.level + (node.module or "")
            for alias in node.names:
                if alias.asname:
                    out.append(f"from {mod} import {alias.name} as {alias.asname}")
                else:
                    out.append(f"from {mod} import {alias.name}")

    return "\n".join(out) if out else "(no imports)"


@mcp.tool()
async def list_definitions(code: str) -> str:
    """List top-level function/class definitions with line numbers."""

    try:
        tree = _parse(code)
    except SyntaxError as e:
        return f"syntax error: {e.msg} (line {e.lineno})"

    out: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            kind = "class" if isinstance(node, ast.ClassDef) else "def"
            if isinstance(node, ast.AsyncFunctionDef):
                kind = "async def"
            lineno = getattr(node, "lineno", 0)
            out.append(f"L{lineno}: {kind} {node.name}")

    return "\n".join(out) if out else "(no top-level defs)"


@mcp.tool()
async def extract_docstring(code: str, name: str = "") -> str:
    """Extract docstring from module or a named top-level function/class."""

    try:
        tree = _parse(code)
    except SyntaxError as e:
        return f"syntax error: {e.msg} (line {e.lineno})"

    if not name:
        ds = ast.get_docstring(tree)
        return ds if ds else "(no docstring)"

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == name:
            ds = ast.get_docstring(node)
            return ds if ds else "(no docstring)"

    return "(not found)"


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
