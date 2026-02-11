from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CSV Inspector")


@dataclass
class _ColStats:
    name: str
    missing: int = 0
    seen: int = 0
    ints: int = 0
    floats: int = 0
    bools: int = 0
    strings: int = 0

    def infer_type(self) -> str:
        non_missing = self.seen - self.missing
        if non_missing <= 0:
            return "empty"
        cands = {
            "int": self.ints,
            "float": self.floats,
            "bool": self.bools,
            "string": self.strings,
        }
        return max(cands, key=cands.get)


def _csv_path(file_path: str) -> Path:
    p = Path(file_path).expanduser()
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"file not found: {p}")
    return p


def _is_missing(v: str) -> bool:
    s = (v or "").strip()
    return s == "" or s.lower() in {"na", "n/a", "null", "none"}


def _classify_value(v: str) -> str:
    s = (v or "").strip()
    if _is_missing(s):
        return "missing"
    sl = s.lower()
    if sl in {"true", "false", "yes", "no"}:
        return "bool"
    try:
        int(s)
        # Avoid treating large numeric-like IDs with leading zeros as ints.
        if s.startswith("0") and len(s) > 1 and s.isdigit():
            return "string"
        return "int"
    except ValueError:
        pass
    try:
        float(s)
        return "float"
    except ValueError:
        return "string"


@mcp.tool()
async def csv_head(file_path: str, n: int = 5, delimiter: str = ",") -> str:
    """Return the first N rows of a CSV file (including header if present)."""
    n = max(0, min(int(n), 100))
    p = _csv_path(file_path)

    rows: list[list[str]] = []
    with p.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        for i, row in enumerate(reader):
            if i >= n:
                break
            rows.append(row)

    if not rows:
        return "(no rows)"

    out = []
    for r in rows:
        out.append("\t".join(c.replace("\n", "\\n") for c in r))
    return "\n".join(out)


@mcp.tool()
async def csv_profile(file_path: str, delimiter: str = ",", max_rows: int = 5000) -> str:
    """Lightweight profiling: column names, missing counts, and rough type inference."""
    max_rows = max(1, min(int(max_rows), 200_000))
    p = _csv_path(file_path)

    with p.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        try:
            header = next(reader)
        except StopIteration:
            return "empty file"

        cols = [_ColStats(name=h.strip() or f"col_{i}") for i, h in enumerate(header)]
        n_rows = 0

        for row in reader:
            n_rows += 1
            if n_rows > max_rows:
                break

            if len(row) < len(cols):
                row = row + [""] * (len(cols) - len(row))
            elif len(row) > len(cols):
                row = row[: len(cols)]

            for c, v in zip(cols, row):
                c.seen += 1
                k = _classify_value(v)
                if k == "missing":
                    c.missing += 1
                elif k == "int":
                    c.ints += 1
                elif k == "float":
                    c.floats += 1
                elif k == "bool":
                    c.bools += 1
                else:
                    c.strings += 1

    lines = []
    lines.append(f"file: {p}")
    lines.append(f"delimiter: {delimiter!r}")
    lines.append(f"rows_scanned: {n_rows}")
    lines.append(f"columns: {len(cols)}")
    lines.append("")
    lines.append("name\ttype\tmissing\tmissing_%")

    for c in cols:
        miss_pct = (100.0 * c.missing / float(c.seen)) if c.seen else 0.0
        lines.append(f"{c.name}\t{c.infer_type()}\t{c.missing}\t{miss_pct:.1f}")

    return "\n".join(lines)


@mcp.tool()
async def csv_top_values(
    file_path: str,
    column: str,
    delimiter: str = ",",
    max_rows: int = 20000,
    top_k: int = 10,
) -> str:
    """Return the most common (non-missing) values for a given column."""
    max_rows = max(1, min(int(max_rows), 500_000))
    top_k = max(1, min(int(top_k), 50))
    p = _csv_path(file_path)

    with p.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        try:
            header = next(reader)
        except StopIteration:
            return "empty file"

        idx = None
        for i, h in enumerate(header):
            if h == column:
                idx = i
                break
        if idx is None:
            for i, h in enumerate(header):
                if h.strip().lower() == column.strip().lower():
                    idx = i
                    break
        if idx is None:
            return f"unknown column: {column!r}. columns: {', '.join(header)}"

        counts: Counter[str] = Counter()
        scanned = 0
        for row in reader:
            scanned += 1
            if scanned > max_rows:
                break
            v = row[idx] if idx < len(row) else ""
            if _is_missing(v):
                continue
            counts[v.strip()] += 1

    if not counts:
        return f"(no non-missing values found in column {column!r}; rows_scanned={scanned})"

    lines = []
    lines.append(f"column: {header[idx]!r}")
    lines.append(f"rows_scanned: {scanned}")
    lines.append("")

    for val, c in counts.most_common(top_k):
        lines.append(f"{c}\t{val}")

    return "\n".join(lines)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
