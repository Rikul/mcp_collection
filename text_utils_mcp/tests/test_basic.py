import asyncio

from text_utils import server as srv


def test_word_count_basic():
    result = asyncio.run(srv.word_count("hello world"))
    assert "chars: 11" in result
    assert "words: 2" in result
    assert "lines: 1" in result


def test_sha256_deterministic():
    result1 = asyncio.run(srv.sha256("test"))
    result2 = asyncio.run(srv.sha256("test"))
    assert result1 == result2
    assert len(result1) == 64  # SHA256 is 64 hex chars


def test_extract_urls_finds_urls():
    text = "Check out https://example.com and http://test.org"
    result = asyncio.run(srv.extract_urls(text))
    assert "https://example.com" in result
    assert "http://test.org" in result


def test_extract_urls_no_urls():
    result = asyncio.run(srv.extract_urls("no urls here"))
    assert "(no urls)" in result


def test_normalize_whitespace_collapses():
    result = asyncio.run(srv.normalize_whitespace("hello   \n\t  world"))
    assert result == "hello world"
