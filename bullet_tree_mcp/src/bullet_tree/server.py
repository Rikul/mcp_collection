from __future__ import annotations

import json
from dataclasses import dataclass, field

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Bullet Tree")


@dataclass
class Node:
    text: str
    children: list["Node"] = field(default_factory=list)


def _detect_indent_size(lines: list[str]) -> int:
    indents: list[int] = []
    for line in lines:
        if not line.strip():
            continue
        leading = len(line) - len(line.lstrip(" "))
        if leading > 0:
            indents.append(leading)
    if not indents:
        return 2
    return max(1, min(indents))


def _parse_bullet_line(line: str) -> tuple[int, str] | None:
    raw = line.rstrip("\n")
    if not raw.strip():
        return None
    indent = len(raw) - len(raw.lstrip(" "))
    s = raw.lstrip(" ")
    if len(s) >= 2 and s[0] in "-*+" and s[1] == " ":
        return indent, s[2:]
    return None


def _nodes_to_obj(nodes: list[Node]) -> list[dict]:
    return [
        {
            "text": n.text,
            "children": _nodes_to_obj(n.children),
        }
        for n in nodes
    ]


def _obj_to_nodes(obj: object) -> list[Node]:
    if not isinstance(obj, list):
        raise ValueError("tree must be a list of nodes")

    def conv(item: object) -> Node:
        if not isinstance(item, dict):
            raise ValueError("node must be an object")
        text = item.get("text")
        if not isinstance(text, str):
            raise ValueError("node.text must be a string")
        children = item.get("children", [])
        return Node(text=text, children=[conv(c) for c in children])

    return [conv(i) for i in obj]


def _render_nodes(nodes: list[Node], *, bullet: str, indent_size: int, level: int = 0) -> str:
    out: list[str] = []
    prefix = " " * (level * indent_size)
    for n in nodes:
        out.append(f"{prefix}{bullet} {n.text}")
        if n.children:
            out.append(
                _render_nodes(
                    n.children, bullet=bullet, indent_size=indent_size, level=level + 1
                )
            )
    return "\n".join(out)


@mcp.tool()
async def bullet_tree_parse(text: str, indent_size: int | None = None) -> str:
    """Parse an indented bullet list into JSON.

    Supported bullets: -, *, + (must be followed by a space).

    Returns a JSON array of nodes: [{"text": str, "children": [...]}, ...]
    """
    lines = (text or "").splitlines()
    ind = indent_size or _detect_indent_size(lines)

    root: list[Node] = []
    stack: list[tuple[int, Node]] = []

    for line in lines:
        parsed = _parse_bullet_line(line)
        if parsed is None:
            continue
        indent, item_text = parsed
        level = indent // ind
        node = Node(text=item_text)

        while stack and stack[-1][0] >= level:
            stack.pop()

        if not stack:
            root.append(node)
        else:
            stack[-1][1].children.append(node)

        stack.append((level, node))

    return json.dumps(
        {"indent_size": ind, "tree": _nodes_to_obj(root)},
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
async def bullet_tree_render(tree_json: str, bullet: str = "-", indent_size: int = 2) -> str:
    """Render a bullet-tree JSON structure back into an indented bullet list."""
    if bullet not in {"-", "*", "+"}:
        raise ValueError("bullet must be one of: '-', '*', '+'")
    obj = json.loads(tree_json or "{}")
    tree_obj = obj.get("tree") if isinstance(obj, dict) else obj
    nodes = _obj_to_nodes(tree_obj)
    return _render_nodes(nodes, bullet=bullet, indent_size=max(1, int(indent_size)))


@mcp.tool()
async def bullet_tree_paths(text: str, indent_size: int | None = None, sep: str = " / ") -> str:
    """List leaf-to-root paths for each node in an indented bullet list.

    Useful for quickly turning an outline into stable "paths" you can reference.
    """
    parsed = json.loads(await bullet_tree_parse(text, indent_size=indent_size))
    nodes = _obj_to_nodes(parsed["tree"])

    out: list[str] = []

    def walk(ns: list[Node], prefix: list[str]) -> None:
        for n in ns:
            path = prefix + [n.text]
            out.append(sep.join(path))
            if n.children:
                walk(n.children, path)

    walk(nodes, [])
    return "\n".join(out)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
