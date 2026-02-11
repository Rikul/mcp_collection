#!/usr/bin/env python3
"""Scaffold a new MCP server package in this collection.

Usage:
  python3 scripts/new_server.py <directory> <package_name> <display_name> <script_name>

Example:
  python3 scripts/new_server.py text_utils_mcp text_utils "Text Utilities" text-utils-mcp

This keeps the repo consistent without forcing a full monorepo build.
"""

from __future__ import annotations

import sys
from pathlib import Path


TEMPLATE_PYPROJECT = """[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "0.1.0"
dependencies = [
    "mcp",
]

[project.scripts]
{script_name} = "{package_name}.server:main"
"""

TEMPLATE_SERVER = """from mcp.server.fastmcp import FastMCP

mcp = FastMCP(\"{display_name}\")


@mcp.tool()
async def ping() -> str:
    return \"pong\"


def main():
    mcp.run()


if __name__ == \"__main__\":
    main()
"""

TEMPLATE_README = """# {display_name} MCP Server

## Available tools

- `ping()`

## Running

```bash
uv run {script_name}
```
"""

TEMPLATE_USAGE = """# {display_name}

This is an MCP server.

## What it does

(Describe the capability in 1–3 sentences.)

## When to use it

- (Example use case)

## Tools

- `ping()` — returns `pong`

## How to run

```bash
uv run {script_name}
```
"""


def die(msg: str) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(2)


def main() -> None:
    if len(sys.argv) != 5:
        die(__doc__.strip())

    directory, package_name, display_name, script_name = sys.argv[1:]

    root = Path(__file__).resolve().parents[1]
    d = root / directory

    if d.exists():
        die(f"Refusing to overwrite existing directory: {d}")

    (d / "src" / package_name).mkdir(parents=True)

    project_name = script_name  # good enough default

    (d / "pyproject.toml").write_text(
        TEMPLATE_PYPROJECT.format(
            project_name=project_name,
            package_name=package_name,
            display_name=display_name,
            script_name=script_name,
        ),
        encoding="utf-8",
    )

    (d / "README.md").write_text(
        TEMPLATE_README.format(display_name=display_name, script_name=script_name),
        encoding="utf-8",
    )

    (d / "usage.md").write_text(
        TEMPLATE_USAGE.format(display_name=display_name, script_name=script_name),
        encoding="utf-8",
    )

    (d / "src" / package_name / "__init__.py").write_text("", encoding="utf-8")

    (d / "src" / package_name / "server.py").write_text(
        TEMPLATE_SERVER.format(display_name=display_name),
        encoding="utf-8",
    )

    print(f"Created: {directory}")


if __name__ == "__main__":
    main()
