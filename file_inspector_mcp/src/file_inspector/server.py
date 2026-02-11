from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("File Inspector")


def _fmt_mtime(ts: float) -> str:
    # Stable, explicit timezone.
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


@dataclass(frozen=True)
class _TreeLine:
    depth: int
    name: str
    is_dir: bool


def _iter_tree(root: Path, *, max_depth: int, max_entries: int) -> list[_TreeLine]:
    lines: list[_TreeLine] = []

    def walk(p: Path, depth: int) -> None:
        if len(lines) >= max_entries:
            return
        if depth > max_depth:
            return

        try:
            entries = sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        except OSError:
            return

        for child in entries:
            if len(lines) >= max_entries:
                return
            is_dir = child.is_dir()
            lines.append(_TreeLine(depth=depth, name=child.name, is_dir=is_dir))
            if is_dir:
                walk(child, depth + 1)

    walk(root, 1)
    return lines


@mcp.tool()
async def path_stat(path: str) -> str:
    """Return basic info about a filesystem path.

    Output includes: type (file/dir/other/missing), size (bytes for files), and
    mtime (UTC ISO-8601).
    """

    p = Path(path).expanduser()
    try:
        st = p.lstat()
    except FileNotFoundError:
        return "type: missing"
    except OSError as e:
        return f"error: {e}"

    if p.is_file():
        kind = "file"
        size = st.st_size
    elif p.is_dir():
        kind = "dir"
        size = None
    else:
        kind = "other"
        size = None

    out = [f"type: {kind}", f"mtime_utc: {_fmt_mtime(st.st_mtime)}"]
    if size is not None:
        out.append(f"size_bytes: {size}")
    out.append(f"path: {p}")
    return "\n".join(out)


@mcp.tool()
async def file_head(path: str, lines: int = 40, max_chars: int = 8000) -> str:
    """Return the first N lines of a text file (best-effort UTF-8).

    This is meant for quick previews of logs/configs. It does not follow network
    paths; it just reads local files.
    """

    p = Path(path).expanduser()
    if not p.exists():
        return "(missing)"
    if not p.is_file():
        return "(not a file)"

    # Read incrementally to avoid slurping huge files.
    out_lines: list[str] = []
    chars = 0
    try:
        with p.open("rb") as f:
            for _ in range(max(0, int(lines))):
                b = f.readline()
                if b == b"":
                    break
                s = b.decode("utf-8", errors="replace")
                if chars + len(s) > max_chars:
                    remaining = max_chars - chars
                    if remaining > 0:
                        out_lines.append(s[:remaining])
                    out_lines.append("\n…(truncated)…")
                    break
                out_lines.append(s)
                chars += len(s)
    except OSError as e:
        return f"error: {e}"

    if not out_lines:
        return "(empty)"
    return "".join(out_lines).rstrip("\n")


@mcp.tool()
async def file_sha256(path: str, max_bytes: int = 10 * 1024 * 1024) -> str:
    """Compute SHA-256 of a local file (streamed).

    Refuses to read more than `max_bytes` bytes (default 10MB).
    """

    p = Path(path).expanduser()
    if not p.exists():
        return "(missing)"
    if not p.is_file():
        return "(not a file)"

    # If the file is clearly too large, bail out early.
    try:
        size = p.stat().st_size
    except OSError as e:
        return f"error: {e}"
    if size > int(max_bytes):
        return f"error: file too large ({size} > {int(max_bytes)} bytes)"

    h = hashlib.sha256()
    read_total = 0
    try:
        with p.open("rb") as f:
            while True:
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                read_total += len(chunk)
                if read_total > int(max_bytes):
                    return f"error: exceeded max_bytes ({int(max_bytes)})"
                h.update(chunk)
    except OSError as e:
        return f"error: {e}"

    return h.hexdigest()


@mcp.tool()
async def dir_tree(path: str, max_depth: int = 2, max_entries: int = 200) -> str:
    """Return a simple directory tree (names only) with depth/entry limits."""

    root = Path(path).expanduser()
    if not root.exists():
        return "(missing)"
    if not root.is_dir():
        return "(not a dir)"

    max_depth_i = max(0, int(max_depth))
    max_entries_i = max(1, int(max_entries))

    lines = _iter_tree(root, max_depth=max_depth_i, max_entries=max_entries_i)
    if not lines:
        return "(empty)"

    rendered: list[str] = [str(root)]
    for item in lines:
        indent = "  " * (item.depth - 1)
        suffix = "/" if item.is_dir else ""
        rendered.append(f"{indent}- {item.name}{suffix}")

    if len(lines) >= max_entries_i:
        rendered.append("…(max_entries reached)…")

    return "\n".join(rendered)


def main() -> None:
    # Keep the entrypoint tiny for validate_collection.py's AST checks.
    mcp.run()


if __name__ == "__main__":
    main()
