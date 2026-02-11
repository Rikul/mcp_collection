from __future__ import annotations

import json
import re
from typing import Dict, Tuple

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("dotenv (.env) Utilities")

_LINE_RE = re.compile(
    r"^\s*(?:export\s+)?(?P<key>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?P<val>.*)\s*$"
)


def _strip_inline_comment(value: str) -> str:
    """Remove inline comments, respecting simple single/double quotes.

    Examples:
      FOO=bar # comment -> bar
      FOO="bar # not comment" -> bar # not comment
    """
    s = value.strip()
    if not s:
        return ""

    if (s.startswith("\"") and s.endswith("\"")) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]

    out: list[str] = []
    in_squote = False
    in_dquote = False
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "'" and not in_dquote:
            in_squote = not in_squote
            out.append(ch)
            i += 1
            continue
        if ch == '"' and not in_squote:
            in_dquote = not in_dquote
            out.append(ch)
            i += 1
            continue
        if ch == "#" and not in_squote and not in_dquote:
            break
        out.append(ch)
        i += 1

    s2 = "".join(out).rstrip()
    if (s2.startswith("\"") and s2.endswith("\"")) or (s2.startswith("'") and s2.endswith("'")):
        return s2[1:-1]
    return s2


def _parse_env(text: str) -> Tuple[Dict[str, str], list[str]]:
    data: Dict[str, str] = {}
    errors: list[str] = []

    for idx, raw in enumerate((text or "").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        m = _LINE_RE.match(raw)
        if not m:
            errors.append(f"line {idx}: could not parse: {raw!r}")
            continue

        key = m.group("key")
        val_raw = m.group("val")
        val = _strip_inline_comment(val_raw)
        data[key] = val

    return data, errors


@mcp.tool()
async def parse_env(text: str) -> str:
    """Parse dotenv (.env) content into a JSON object string.

    - Ignores blank lines and comments.
    - Supports optional leading `export `.
    - Supports basic single/double-quoted values.
    - Does not expand variables; values are returned as strings.
    """
    data, errors = _parse_env(text)
    payload = {"env": data}
    if errors:
        payload["errors"] = errors
    return json.dumps(payload, indent=2, sort_keys=True)


@mcp.tool()
async def render_env(json_text: str) -> str:
    """Render a JSON object into dotenv (.env) text.

    Input must be a JSON object mapping keys to string-ish values.
    Output is sorted by key for stable diffs.
    """
    obj = json.loads(json_text or "{}")
    if not isinstance(obj, dict):
        raise ValueError("render_env expects a JSON object")

    lines: list[str] = []
    for key in sorted(obj.keys()):
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", str(key)):
            raise ValueError(f"Invalid env var name: {key!r}")
        val = obj[key]
        if val is None:
            sval = ""
        else:
            sval = str(val)

        if any(c.isspace() for c in sval) or "#" in sval:
            escaped = sval.replace('"', r"\"")
            lines.append(f'{key}="{escaped}"')
        else:
            lines.append(f"{key}={sval}")

    return "\n".join(lines) + ("\n" if lines else "")


@mcp.tool()
async def diff_env(old_text: str, new_text: str) -> str:
    """Diff two dotenv blobs by key (added/removed/changed)."""
    old, old_err = _parse_env(old_text)
    new, new_err = _parse_env(new_text)

    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = sorted(k for k in set(old) & set(new) if old[k] != new[k])

    parts: list[str] = []
    if old_err:
        parts.append("Old parse errors:\n" + "\n".join(f"- {e}" for e in old_err))
    if new_err:
        parts.append("New parse errors:\n" + "\n".join(f"- {e}" for e in new_err))

    if not (added or removed or changed):
        parts.append("(no changes)")
        return "\n\n".join(parts)

    if added:
        parts.append("Added:\n" + "\n".join(f"+ {k}={new[k]}" for k in added))
    if removed:
        parts.append("Removed:\n" + "\n".join(f"- {k}={old[k]}" for k in removed))
    if changed:
        parts.append(
            "Changed:\n" + "\n".join(f"~ {k}: {old[k]} -> {new[k]}" for k in changed)
        )

    return "\n\n".join(parts)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
