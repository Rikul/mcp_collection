import asyncio

from text_fingerprint import server as srv


def test_hash_text_basic():
    result = asyncio.run(srv.hash_text("hello"))
    # SHA256 of "hello"
    assert len(result) == 64
    assert result == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_hash_text_deterministic():
    result1 = asyncio.run(srv.hash_text("test"))
    result2 = asyncio.run(srv.hash_text("test"))
    assert result1 == result2


def test_hash_text_normalize():
    result = asyncio.run(srv.hash_text("hello  world", normalize="collapse_ws"))
    # Should normalize whitespace before hashing
    assert len(result) == 64


def test_hash_lines_basic():
    result = asyncio.run(srv.hash_lines("line1\nline2"))
    lines = result.splitlines()
    assert len(lines) == 2
    assert lines[0].startswith("1\t")
    assert lines[1].startswith("2\t")


def test_fingerprint_bundle():
    result = asyncio.run(srv.fingerprint_bundle("hello"))
    assert "bytes:" in result
    assert "lines:" in result
    assert "sha256:" in result
    assert "blake2b:" in result
