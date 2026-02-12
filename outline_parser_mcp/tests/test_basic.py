import asyncio

from outline_parser import server as srv


def test_outline_to_json_basic():
    outline_text = "- Item 1\n- Item 2\n  - Subitem 2.1"
    result = asyncio.run(srv.outline_to_json(outline_text))
    assert "Item 1" in result
    assert "Item 2" in result
    assert "Subitem 2.1" in result


def test_outline_to_json_numbered():
    outline_text = "1. First\n2. Second"
    result = asyncio.run(srv.outline_to_json(outline_text))
    assert "First" in result
    assert "Second" in result


def test_json_to_outline_basic():
    json_text = '[{"text": "Item 1", "children": []}]'
    result = asyncio.run(srv.json_to_outline(json_text))
    assert "Item 1" in result
    assert "-" in result or "*" in result
