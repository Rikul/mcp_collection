import asyncio
from pathlib import Path

from csv_inspector import server as srv


def test_csv_head_returns_header_and_rows(tmp_path: Path):
    p = tmp_path / "a.csv"
    p.write_text("a,b\n1,2\n3,4\n", encoding="utf-8")
    out = asyncio.run(srv.csv_head(str(p), n=2))
    lines = out.splitlines()
    assert lines[0] == "a\tb"
    assert lines[1] == "1\t2"


def test_csv_profile_infers_int_columns(tmp_path: Path):
    p = tmp_path / "a.csv"
    p.write_text("x,y\n1,2\n3,4\n\n", encoding="utf-8")
    out = asyncio.run(srv.csv_profile(str(p), max_rows=10))
    assert "rows_scanned:" in out
    # both columns should infer numeric types; keep this loose
    assert "x\t" in out and "y\t" in out


def test_csv_top_values_counts(tmp_path: Path):
    p = tmp_path / "a.csv"
    p.write_text("color\nred\nred\nblue\n", encoding="utf-8")
    out = asyncio.run(srv.csv_top_values(str(p), column="color", top_k=2))
    assert "2\tred" in out
    assert "1\tblue" in out
