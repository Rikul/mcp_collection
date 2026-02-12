import asyncio

from ini_tools_mcp import server as srv


def test_ini_to_json():
    ini_text = "[section1]\nkey1=value1\n"
    result = asyncio.run(srv.ini_to_json(ini_text))
    assert "section1" in result
    assert "key1" in result
    assert "value1" in result


def test_ini_get():
    ini_text = "[section1]\nkey1=value1\n"
    result = asyncio.run(srv.ini_get(ini_text, "section1", "key1"))
    assert result == "value1"


def test_ini_get_fallback():
    ini_text = "[section1]\nkey1=value1\n"
    result = asyncio.run(srv.ini_get(ini_text, "section1", "missing", fallback="default"))
    assert result == "default"


def test_ini_set():
    ini_text = "[section1]\nkey1=value1\n"
    result = asyncio.run(srv.ini_set(ini_text, "section1", "key2", "value2"))
    assert "key2" in result
    assert "value2" in result


def test_ini_remove_option():
    ini_text = "[section1]\nkey1=value1\nkey2=value2\n"
    result = asyncio.run(srv.ini_remove_option(ini_text, "section1", "key1"))
    assert "key1" not in result or "value1" not in result


def test_ini_remove_section():
    ini_text = "[section1]\nkey1=value1\n[section2]\nkey2=value2\n"
    result = asyncio.run(srv.ini_remove_section(ini_text, "section1"))
    # Section1 should be removed but section2 should remain
    assert "section2" in result
