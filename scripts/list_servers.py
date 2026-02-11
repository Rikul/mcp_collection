#!/usr/bin/env python3
"""List MCP servers in this repo.

Heuristics:
- A "server" is any immediate subdirectory containing a pyproject.toml.
- We parse [project] metadata and [project.scripts] entrypoints.

This script is intentionally dependency-free (stdlib only).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path


try:
    import tomllib  # py>=3.11
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Server:
    directory: str
    name: str | None
    version: str | None
    scripts: dict[str, str]


def _read_pyproject(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)


def discover(requested: list[str] | None = None) -> list[Server]:
    """Discover server packages in the repo.

    If `requested` is provided, only those server directory names are returned.
    """

    if requested:
        dirs: list[Path] = []
        for name in requested:
            p = ROOT / name
            if not p.is_dir():
                raise ValueError(f"unknown server directory: {name!r}")
            if not (p / "pyproject.toml").exists():
                raise ValueError(
                    f"{name!r} does not look like a server (missing pyproject.toml)"
                )
            dirs.append(p)
    else:
        dirs = [
            p
            for p in sorted(ROOT.iterdir())
            if p.is_dir() and not p.name.startswith(".") and (p / "pyproject.toml").exists()
        ]

    servers: list[Server] = []
    for child in dirs:
        data = _read_pyproject(child / "pyproject.toml")
        project = data.get("project", {})
        scripts = project.get("scripts", {}) or {}
        servers.append(
            Server(
                directory=child.name,
                name=project.get("name"),
                version=project.get("version"),
                scripts=dict(scripts),
            )
        )
    return servers


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--format",
        choices=("text", "json"),
        default=os.environ.get("MCP_LIST_FORMAT", "text"),
        help="Output format (default: env MCP_LIST_FORMAT or 'text').",
    )
    p.add_argument(
        "servers",
        nargs="*",
        help="Optional list of server directory names to list (defaults to all).",
    )
    return p.parse_args(sys.argv[1:] if argv is None else argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    try:
        servers = discover(args.servers)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    # Machine-readable output
    if args.format == "json":
        print(
            json.dumps(
                [
                    {
                        "directory": s.directory,
                        "name": s.name,
                        "version": s.version,
                        "scripts": s.scripts,
                    }
                    for s in servers
                ],
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    if not servers:
        print("No servers found.")
        return 0

    for s in servers:
        header = f"{s.directory}"
        if s.name:
            header += f"  ({s.name}{' ' + s.version if s.version else ''})"
        print(header)
        if s.scripts:
            for k, v in sorted(s.scripts.items()):
                print(f"  - script: {k} = {v}")
            # Suggest a likely run command.
            first = sorted(s.scripts.keys())[0]
            print(f"  - run:    cd {s.directory} && uv run {first}")
        else:
            print("  - (no [project.scripts] entrypoints)")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
