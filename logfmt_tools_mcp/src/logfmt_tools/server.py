from __future__ import annotations

import json
import shlex
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Logfmt Tools")


def _file_path(file_path: str) -> Path:
    p = Path(file_path).expanduser()
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"file not found: {p}")
    return p


def _maybe_coerce_scalar(s: str) -> Any:
    sl = s.lower()
    if sl == "true":
        return True
    if sl == "false":
        return False
    if sl in {"null", "none"}:
        return None

    # int first (avoid turning "01" into 1)
    if s.isdigit() and not (len(s) > 1 and s.startswith("0")):
        try:
            return int(s)
        except ValueError:
            pass

    # float (avoid NaN/Inf surprises; keep as string)
    try:
        f = float(s)
    except ValueError:
        return s
    if f != f or f in (float("inf"), float("-inf")):
        return s
    return f


def _add_kv(out: dict[str, Any], k: str, v: Any) -> None:
    if k in out:
        prev = out[k]
        if isinstance(prev, list):
            prev.append(v)
        else:
            out[k] = [prev, v]
    else:
        out[k] = v


def _parse_logfmt(line: str) -> dict[str, Any]:
    # shlex handles quotes/escapes in a reasonable, pythonic way.
    tokens = shlex.split(line, posix=True)
    out: dict[str, Any] = {}
    bare: list[str] = []

    for t in tokens:
        if "=" not in t:
            bare.append(t)
            continue
        k, v = t.split("=", 1)
        k = k.strip()
        if not k:
            bare.append(t)
            continue
        _add_kv(out, k, _maybe_coerce_scalar(v))

    if bare:
        out["_bare"] = bare
    return out


def _needs_quotes(s: str) -> bool:
    if s == "":
        return True
    # space or characters that would break tokenization
    return any(c.isspace() for c in s) or any(c in s for c in '"=')


def _quote(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def _format_value(v: Any) -> str:
    if v is True:
        return "true"
    if v is False:
        return "false"
    if v is None:
        return "null"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    return _quote(s) if _needs_quotes(s) else s


def _format_logfmt(record: dict[str, Any]) -> str:
    parts: list[str] = []
    for k in sorted(record.keys()):
        if k == "_bare":
            continue
        v = record[k]
        if isinstance(v, list):
            for item in v:
                parts.append(f"{k}={_format_value(item)}")
        else:
            parts.append(f"{k}={_format_value(v)}")

    bare = record.get("_bare")
    if isinstance(bare, list):
        for b in bare:
            bs = str(b)
            parts.append(_quote(bs) if _needs_quotes(bs) else bs)

    return " ".join(parts)


@mcp.tool()
async def logfmt_parse(line: str) -> str:
    """Parse one logfmt line and return a JSON object (as a string)."""
    obj = _parse_logfmt(line)
    return json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True)


@mcp.tool()
async def logfmt_format(record_json: str) -> str:
    """Format a JSON object (string) into a logfmt line."""
    try:
        obj = json.loads(record_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"invalid JSON: {e}")
    if not isinstance(obj, dict):
        raise ValueError("record_json must be a JSON object")
    return _format_logfmt(obj)


@mcp.tool()
async def logfmt_parse_file_head(file_path: str, max_lines: int = 50) -> str:
    """Parse the first N lines of a file containing logfmt records."""
    max_lines = max(1, min(int(max_lines), 500))
    p = _file_path(file_path)

    records: list[dict[str, Any]] = []
    with p.open("r", encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f):
            if i >= max_lines:
                break
            s = line.strip("\n")
            if not s.strip():
                continue
            try:
                records.append(_parse_logfmt(s))
            except Exception as e:
                records.append({"_error": str(e), "_line": s})

    return json.dumps(records, indent=2, ensure_ascii=False)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
