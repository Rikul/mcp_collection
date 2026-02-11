from __future__ import annotations

import difflib

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Diff Tools")


def _to_lines(text: str) -> list[str]:
    # Keep line endings out of the diff generator; difflib will add them back.
    return (text or "").splitlines()


@mcp.tool()
async def unified_diff(
    a: str,
    b: str,
    fromfile: str = "a",
    tofile: str = "b",
    context_lines: int = 3,
) -> str:
    """Generate a unified diff between two text blobs.

    Returns `(no changes)` when the inputs are identical.
    """

    if context_lines < 0:
        context_lines = 0

    a_lines = _to_lines(a)
    b_lines = _to_lines(b)

    diff = difflib.unified_diff(
        a_lines,
        b_lines,
        fromfile=fromfile,
        tofile=tofile,
        lineterm="",
        n=context_lines,
    )
    out = "\n".join(diff).strip("\n")
    return out if out else "(no changes)"


@mcp.tool()
async def ndiff(a: str, b: str) -> str:
    """Generate an ndiff view (good for whitespace changes)."""

    a_lines = _to_lines(a)
    b_lines = _to_lines(b)

    diff = difflib.ndiff(a_lines, b_lines)
    out = "\n".join(diff).strip("\n")
    return out if out else "(no changes)"


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
