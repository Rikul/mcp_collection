import asyncio
from pathlib import Path

from file_inspector import server as srv


def test_path_stat_file(tmp_path: Path):
    p = tmp_path / "test.txt"
    p.write_text("hello")
    result = asyncio.run(srv.path_stat(str(p)))
    assert "type: file" in result
    assert "size_bytes:" in result
    assert "mtime_utc:" in result


def test_path_stat_directory(tmp_path: Path):
    result = asyncio.run(srv.path_stat(str(tmp_path)))
    assert "type: dir" in result or "type: directory" in result


def test_path_stat_missing():
    result = asyncio.run(srv.path_stat("/nonexistent/path/12345"))
    assert "missing" in result or "not found" in result.lower()
