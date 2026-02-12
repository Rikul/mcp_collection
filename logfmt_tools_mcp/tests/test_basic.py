import asyncio
from pathlib import Path

from logfmt_tools import server as srv


def test_logfmt_parse_basic():
    result = asyncio.run(srv.logfmt_parse("level=info msg=test"))
    assert "level" in result
    assert "info" in result
    assert "msg" in result


def test_logfmt_format_basic():
    json_input = '{"level": "info", "msg": "test"}'
    result = asyncio.run(srv.logfmt_format(json_input))
    assert "level=info" in result
    assert "msg=test" in result


def test_logfmt_parse_with_quotes():
    result = asyncio.run(srv.logfmt_parse('msg="hello world"'))
    assert "hello world" in result


def test_logfmt_parse_file_head(tmp_path: Path):
    p = tmp_path / "test.log"
    p.write_text("level=info msg=line1\nlevel=debug msg=line2\n")
    result = asyncio.run(srv.logfmt_parse_file_head(str(p), max_lines=10))
    assert "level" in result
    assert "info" in result
    assert "debug" in result
