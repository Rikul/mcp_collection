from __future__ import annotations

import hashlib
import re
from typing import Iterable

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Text Fingerprint")


_NORMALIZE_MODES = {
    "none",
    "rstrip",
    "strip",
    "collapse_ws",
}


def _get_hasher(algo: str) -> "hashlib._Hash":
    a = (algo or "").strip().lower()
    if not a:
        a = "sha256"
    try:
        return hashlib.new(a)
    except ValueError as e:
        raise ValueError(
            f"Unknown hash algorithm: {algo!r}. Try one of: {sorted(hashlib.algorithms_available)}"
        ) from e


def _normalize_text(text: str, mode: str) -> str:
    m = (mode or "none").strip().lower()
    if m not in _NORMALIZE_MODES:
        raise ValueError(f"Unknown normalize mode: {mode!r}. Expected one of: {sorted(_NORMALIZE_MODES)}")

    s = text or ""
    if m == "none":
        return s
    if m == "rstrip":
        return "\n".join(line.rstrip() for line in s.splitlines())
    if m == "strip":
        return "\n".join(line.strip() for line in s.splitlines())

    # collapse_ws: normalize runs of whitespace to a single space on each line.
    return "\n".join(re.sub(r"\s+", " ", line).strip() for line in s.splitlines())


def _iter_lines(text: str) -> Iterable[str]:
    # splitlines() drops the trailing empty line if the text ends with "\n";
    # for line-level fingerprints that's usually desirable and more stable.
    return (text or "").splitlines()


@mcp.tool()
async def hash_text(text: str, algo: str = "sha256", normalize: str = "none") -> str:
    """Hash `text` with the selected algorithm and return a hex digest.

    Parameters:
    - algo: any algorithm supported by hashlib (e.g. sha256, sha1, md5, blake2b).
    - normalize: one of none|rstrip|strip|collapse_ws
    """
    s = _normalize_text(text, normalize)
    h = _get_hasher(algo)
    h.update(s.encode("utf-8"))
    return h.hexdigest()


@mcp.tool()
async def hash_lines(text: str, algo: str = "sha256", normalize: str = "rstrip") -> str:
    """Hash each line of `text` and return `line_number<TAB>digest` rows.

    This is useful for quick anchors when diffing or caching transforms.

    Parameters:
    - algo: any algorithm supported by hashlib.
    - normalize: one of none|rstrip|strip|collapse_ws
    """
    h_template = _get_hasher(algo)
    rows: list[str] = []

    for i, line in enumerate(_iter_lines(text), start=1):
        line_n = _normalize_text(line, normalize)
        h = h_template.copy()
        h.update(line_n.encode("utf-8"))
        rows.append(f"{i}\t{h.hexdigest()}")

    return "\n".join(rows)


@mcp.tool()
async def fingerprint_bundle(text: str) -> str:
    """Return a small bundle of common fingerprints for `text`.

    Intended for quick, human-friendly identification.
    """
    s = text or ""
    sha256 = hashlib.sha256(s.encode("utf-8")).hexdigest()
    blake2b = hashlib.blake2b(s.encode("utf-8")).hexdigest()
    return "\n".join(
        [
            f"bytes: {len(s.encode('utf-8'))}",
            f"lines: {len(s.splitlines())}",
            f"sha256: {sha256}",
            f"blake2b: {blake2b}",
        ]
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
