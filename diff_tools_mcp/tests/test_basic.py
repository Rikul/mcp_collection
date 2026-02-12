import asyncio

from diff_tools_mcp import server as srv


def test_unified_diff_no_changes():
    result = asyncio.run(srv.unified_diff("hello\nworld", "hello\nworld"))
    assert result == "(no changes)"


def test_unified_diff_with_changes():
    result = asyncio.run(srv.unified_diff("hello\nworld", "hello\nuniverse"))
    assert "---" in result
    assert "+++" in result
    assert "universe" in result


def test_ndiff_no_changes():
    result = asyncio.run(srv.ndiff("test", "test"))
    assert result == "(no changes)"


def test_ndiff_with_changes():
    result = asyncio.run(srv.ndiff("line1\nline2", "line1\nline3"))
    assert "-" in result or "+" in result
    assert "line3" in result
