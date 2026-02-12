from __future__ import annotations

import json

from bullet_tree.server import bullet_tree_parse, bullet_tree_render


def test_parse_and_render_roundtrip() -> None:
    text = """- A
  - B
    - C
- D
"""
    parsed = json.loads(__import__("asyncio").run(bullet_tree_parse(text)))
    assert parsed["indent_size"] == 2
    assert parsed["tree"][0]["text"] == "A"
    rendered = __import__("asyncio").run(bullet_tree_render(json.dumps(parsed)))
    assert "- A" in rendered
    assert "  - B" in rendered
    assert "    - C" in rendered
    assert "- D" in rendered
