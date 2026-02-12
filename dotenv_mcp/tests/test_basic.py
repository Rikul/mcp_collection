import asyncio

from dotenv_mcp import server as srv


def test_parse_env_basic():
    env_text = "KEY1=value1\nKEY2=value2"
    result = asyncio.run(srv.parse_env(env_text))
    assert "KEY1" in result
    assert "value1" in result
    assert "KEY2" in result
    assert "value2" in result


def test_parse_env_with_quotes():
    env_text = 'KEY="quoted value"'
    result = asyncio.run(srv.parse_env(env_text))
    assert "KEY" in result
    assert "quoted value" in result


def test_parse_env_ignores_comments():
    env_text = "# This is a comment\nKEY=value"
    result = asyncio.run(srv.parse_env(env_text))
    assert "KEY" in result
    assert "value" in result


def test_render_env_basic():
    json_text = '{"KEY1": "value1", "KEY2": "value2"}'
    result = asyncio.run(srv.render_env(json_text))
    assert "KEY1=value1" in result
    assert "KEY2=value2" in result


def test_render_env_with_spaces():
    json_text = '{"KEY": "value with spaces"}'
    result = asyncio.run(srv.render_env(json_text))
    assert 'KEY="value with spaces"' in result
