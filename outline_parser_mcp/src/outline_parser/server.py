from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Outline Parser")

_MARKER_RE = re.compile(r"^(?:[-*+]|\d+\.)\s+")


@dataclass
class Node:
    text: str
    children: list["Node"] = field(default_factory=list)


def _strip_marker(s: str) -> str:
    return _MARKER_RE.sub("", s, count=1).rstrip()


def _leading_spaces(s: str) -> int:
    return len(s) - len(s.lstrip(" "))


def _parse_outline(text: str) -> list[Node]:
    lines = (text or "").splitlines()

    root: list[Node] = []
    stack: list[tuple[int, list[Node]]] = [(0, root)]  # (indent, children)
    last_node: Node | None = None

    for raw in lines:
        if not raw.strip():
            continue

        indent = _leading_spaces(raw)
        content = raw.strip(" ")

        is_item = bool(_MARKER_RE.match(content))
        if not is_item:
            # Continuation line: append to previous node when possible.
            if last_node is not None:
                last_node.text = f"{last_node.text}\n{content.rstrip()}"
            continue

        content = _strip_marker(content)

        # Pop until we find a parent indentation <= current.
        while len(stack) > 1 and indent < stack[-1][0]:
            stack.pop()

        # If indentation increases, nest under previous item.
        if indent > stack[-1][0] and last_node is not None:
            stack.append((indent, last_node.children))

        node = Node(text=content)
        stack[-1][1].append(node)
        last_node = node

    return root


def _to_plain(obj: list[Node]) -> list[dict]:
    return [
        {
            "text": n.text,
            "children": _to_plain(n.children),
        }
        for n in obj
    ]


def _from_plain(obj: object) -> list[Node]:
    if not isinstance(obj, list):
        raise ValueError("root must be a list")

    nodes: list[Node] = []
    for item in obj:
        if not isinstance(item, dict):
            raise ValueError("each node must be an object")
        text = item.get("text")
        children = item.get("children", [])
        if not isinstance(text, str):
            raise ValueError("node.text must be a string")
        nodes.append(Node(text=text, children=_from_plain(children)))
    return nodes


def _render(nodes: list[Node], *, bullet: str, indent: int, level: int = 0) -> list[str]:
    lines: list[str] = []
    pad = " " * (indent * level)
    for n in nodes:
        # Preserve multi-line text blocks as an item + continuations.
        parts = n.text.splitlines() or [""]
        lines.append(f"{pad}{bullet} {parts[0]}")
        for cont in parts[1:]:
            lines.append(f"{pad}{' ' * (len(bullet) + 1)}{cont}")
        lines.extend(_render(n.children, bullet=bullet, indent=indent, level=level + 1))
    return lines


@mcp.tool()
async def outline_to_json(text: str) -> str:
    """Parse a simple bullet outline to a JSON tree (no I/O, no fetching)."""
    tree = _parse_outline(text)
    return json.dumps(_to_plain(tree), ensure_ascii=False, indent=2)


@mcp.tool()
async def json_to_outline(json_text: str, bullet: str = "-", indent: int = 2) -> str:
    """Render an outline JSON tree back into a bullet outline."""
    data = json.loads(json_text or "[]")
    nodes = _from_plain(data)
    if not bullet.strip():
        bullet = "-"
    indent = max(0, int(indent))
    return "\n".join(_render(nodes, bullet=bullet.strip(), indent=indent))


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
