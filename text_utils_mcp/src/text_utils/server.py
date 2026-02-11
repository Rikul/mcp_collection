from __future__ import annotations

import hashlib
import re

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Text Utilities")

_URL_RE = re.compile(r"https?://[^\s)\]}>\"']+", re.IGNORECASE)


@mcp.tool()
async def word_count(text: str) -> str:
    """Return counts for a text blob."""
    chars = len(text)
    # Split on whitespace; ignore empty.
    words = len([w for w in re.split(r"\s+", text.strip()) if w]) if text.strip() else 0
    lines = 0 if text == "" else text.count("\n") + 1
    return f"chars: {chars}\nwords: {words}\nlines: {lines}"


@mcp.tool()
async def sha256(text: str) -> str:
    """Compute SHA-256 of the provided text (utf-8) and return hex digest."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@mcp.tool()
async def extract_urls(text: str) -> str:
    """Extract URLs from text as plain strings. Does not fetch."""
    urls = _URL_RE.findall(text or "")
    if not urls:
        return "(no urls)"
    # Deduplicate, preserve order.
    seen: set[str] = set()
    unique: list[str] = []
    for u in urls:
        if u in seen:
            continue
        seen.add(u)
        unique.append(u)
    return "\n".join(unique)


@mcp.tool()
async def normalize_whitespace(text: str) -> str:
    """Collapse all whitespace runs to single spaces and trim."""
    return re.sub(r"\s+", " ", text or "").strip()


def main():
    mcp.run()


if __name__ == "__main__":
    main()
