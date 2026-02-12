from __future__ import annotations

import json
import re
from dataclasses import dataclass

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Codeblock Tools")


_FENCE_OPEN_RE = re.compile(r"^(?P<indent>[ \t]*)(?P<fence>`{3,})(?P<info>.*)$")


@dataclass(frozen=True)
class _Block:
    index: int
    info: str
    language: str | None
    start_line: int
    end_line: int
    content: str


def _parse_language(info: str) -> str | None:
    info = (info or "").strip()
    if not info:
        return None
    # GitHub-style: first token is language; ignore the rest.
    return info.split()[0].strip().lower() or None


def _iter_fenced_blocks(markdown: str) -> list[_Block]:
    lines = (markdown or "").splitlines(keepends=True)
    blocks: list[_Block] = []

    i = 0
    idx = 0
    while i < len(lines):
        m = _FENCE_OPEN_RE.match(lines[i].rstrip("\n"))
        if not m:
            i += 1
            continue

        indent = m.group("indent")
        fence = m.group("fence")
        info = m.group("info").strip()
        lang = _parse_language(info)

        start_line = i + 1  # 1-based
        i += 1
        content_lines: list[str] = []

        # Closing fence must be at least as long as opening and can be indented.
        close_re = re.compile(rf"^{re.escape(indent)}`{{{len(fence)},}}\s*$")

        while i < len(lines):
            if close_re.match(lines[i].rstrip("\n")):
                end_line = i + 1
                i += 1
                break
            content_lines.append(lines[i])
            i += 1
        else:
            # Unterminated fence; treat rest of doc as content.
            end_line = len(lines)

        blocks.append(
            _Block(
                index=idx,
                info=info,
                language=lang,
                start_line=start_line,
                end_line=end_line,
                content="".join(content_lines),
            )
        )
        idx += 1

    return blocks


@mcp.tool()
async def list_fenced_code_blocks(markdown: str) -> str:
    """List fenced code blocks in a Markdown string as JSON.

    Only handles backtick fences (```), not tilde fences (~~~) and not indented code.
    """

    blocks = _iter_fenced_blocks(markdown)
    out = []
    for b in blocks:
        preview = b.content.replace("\r\n", "\n").replace("\r", "\n")
        preview = preview[:120]
        out.append(
            {
                "index": b.index,
                "info": b.info,
                "language": b.language,
                "start_line": b.start_line,
                "end_line": b.end_line,
                "content_preview": preview,
            }
        )
    return json.dumps(out, indent=2, sort_keys=True)


@mcp.tool()
async def extract_fenced_code_block(markdown: str, index: int = 0) -> str:
    """Extract a fenced code block's content (no fences) by 0-based index."""

    blocks = _iter_fenced_blocks(markdown)
    if not blocks:
        return "(no fenced code blocks found)"
    if index < 0 or index >= len(blocks):
        return f"index out of range: {index} (valid: 0..{len(blocks)-1})"
    return blocks[index].content


@mcp.tool()
async def strip_fenced_code_blocks(markdown: str, language: str | None = None) -> str:
    """Remove fenced code blocks from Markdown.

    If language is provided, only remove blocks that match that language.
    """

    blocks = _iter_fenced_blocks(markdown)
    if not blocks:
        return markdown or ""

    want = (language or "").strip().lower() or None

    # Re-scan line-by-line and skip ranges.
    lines = (markdown or "").splitlines(keepends=True)
    skip: set[int] = set()
    for b in blocks:
        if want is not None and (b.language or "") != want:
            continue
        # include fence lines too
        for ln in range(b.start_line, b.end_line + 1):
            skip.add(ln)

    out_lines: list[str] = []
    for lineno, line in enumerate(lines, start=1):
        if lineno in skip:
            continue
        out_lines.append(line)

    return "".join(out_lines)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
