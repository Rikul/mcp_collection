"""Regex Tools MCP Server.

Provides small, safe helpers around Python's `re` module.
"""

from __future__ import annotations

import re
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Regex Tools")


_FLAG_MAP: dict[str, int] = {
    "ASCII": re.ASCII,
    "DOTALL": re.DOTALL,
    "IGNORECASE": re.IGNORECASE,
    "LOCALE": re.LOCALE,
    "MULTILINE": re.MULTILINE,
    "UNICODE": re.UNICODE,
    "VERBOSE": re.VERBOSE,
}


def _parse_flags(flags: list[str] | None) -> int:
    if not flags:
        return 0

    unknown = [f for f in flags if f.upper() not in _FLAG_MAP]
    if unknown:
        raise ValueError(
            "Unknown flag(s): "
            + ", ".join(sorted(set(unknown)))
            + ". Allowed: "
            + ", ".join(sorted(_FLAG_MAP))
        )

    out = 0
    for f in flags:
        out |= _FLAG_MAP[f.upper()]
    return out


def _compile(pattern: str, flags: list[str] | None) -> re.Pattern[str]:
    if not isinstance(pattern, str) or not pattern:
        raise ValueError("pattern must be a non-empty string")
    return re.compile(pattern, _parse_flags(flags))


@mcp.tool()
def regex_validate(pattern: str, flags: list[str] | None = None) -> dict[str, Any]:
    """Validate that a regex pattern compiles.

    Returns {"ok": true} on success, or {"ok": false, "error": "..."}.
    """

    try:
        _compile(pattern, flags)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def regex_find(
    pattern: str,
    text: str,
    flags: list[str] | None = None,
    max_matches: int = 200,
) -> dict[str, Any]:
    """Find regex matches and return structured results.

    Notes:
    - `max_matches` is a safety valve against huge outputs.
    """

    if max_matches <= 0:
        return {"count": 0, "matches": [], "truncated": False}
    if max_matches > 5000:
        return {"error": "max_matches too large (max 5000)"}

    try:
        rx = _compile(pattern, flags)
    except Exception as e:
        return {"error": str(e)}

    matches: list[dict[str, Any]] = []
    truncated = False

    for i, m in enumerate(rx.finditer(text)):
        if i >= max_matches:
            truncated = True
            break
        matches.append(
            {
                "match": m.group(0),
                "span": [m.start(), m.end()],
                "groups": list(m.groups()),
                "groupdict": m.groupdict(),
            }
        )

    return {"count": len(matches), "matches": matches, "truncated": truncated}


@mcp.tool()
def regex_replace(
    pattern: str,
    repl: str,
    text: str,
    flags: list[str] | None = None,
    count: int = 0,
) -> dict[str, Any]:
    """Perform a regex substitution.

    `count=0` means replace all occurrences (Python `re.sub` semantics).
    """

    if count < 0:
        return {"error": "count must be >= 0"}

    try:
        rx = _compile(pattern, flags)
    except Exception as e:
        return {"error": str(e)}

    try:
        result, n = rx.subn(repl, text, count=count)
        return {"result": result, "replacements": n}
    except Exception as e:
        return {"error": str(e)}


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
