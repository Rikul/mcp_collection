#!/usr/bin/env python3
"""Validate repo structure for the MCP collection.

Checks (best-effort):
- Each server directory (subdir with pyproject.toml) has a README.md
- Each server directory has a usage.md (LLM-facing usage guide)
- [build-system] exists with build-system.requires/build-system.build-backend
- [project] exists with name/version
- [project.scripts] exists with at least one entrypoint
- Each [project.scripts] entrypoint references a module that exists in the repo
- If an entrypoint points at a *.py module, the referenced attr is defined (AST check)

Exit code:
- 0: all good
- 1: validation issues found

No third-party dependencies.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import sys
from pathlib import Path


try:
    import tomllib  # py>=3.11
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore


ROOT = Path(__file__).resolve().parents[1]


def _read_pyproject(path: Path) -> dict:
    """Read and parse a pyproject.toml file.

    We keep this tiny (and dependency-free), but we still want nice error
    reporting if a file is malformed.
    """

    with path.open("rb") as f:
        return tomllib.load(f)


def _find_module_file(server_dir: Path, module: str) -> Path | None:
    """Best-effort check that an entrypoint module exists.

    Supports both flat-layout and src-layout packages.
    """

    rel = Path(*module.split("."))
    candidates = [
        server_dir / f"{rel}.py",
        server_dir / rel / "__init__.py",
        server_dir / "src" / f"{rel}.py",
        server_dir / "src" / rel / "__init__.py",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def _module_defines_attr(module_file: Path, attr: str) -> bool:
    """Best-effort check that `attr` is defined in the given module.

    We avoid importing/executing server code; instead we parse the module AST and
    look for top-level definitions (functions/classes) or simple assignments.
    """

    try:
        source = module_file.read_text(encoding="utf-8")
    except OSError:
        return False

    try:
        tree = ast.parse(source, filename=str(module_file))
    except SyntaxError:
        return False

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name == attr:
                return True
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = []
            if isinstance(node, ast.Assign):
                targets = node.targets
            else:  # AnnAssign
                targets = [node.target]
            for t in targets:
                if isinstance(t, ast.Name) and t.id == attr:
                    return True

    return False


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--format",
        choices=("text", "json"),
        default=os.environ.get("MCP_VALIDATE_FORMAT", "text"),
        help="Output format (default: env MCP_VALIDATE_FORMAT or 'text').",
    )
    p.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop at the first problem (useful for CI/debugging).",
    )
    p.add_argument(
        "servers",
        nargs="*",
        help="Optional list of server directory names to validate (defaults to all).",
    )
    return p.parse_args(argv)


def _iter_server_dirs(requested: list[str] | None) -> list[Path]:
    if not requested:
        return [
            p
            for p in sorted(ROOT.iterdir())
            if p.is_dir() and not p.name.startswith(".") and (p / "pyproject.toml").exists()
        ]

    dirs: list[Path] = []
    for name in requested:
        p = ROOT / name
        if not p.is_dir():
            raise ValueError(f"unknown server directory: {name!r}")
        if not (p / "pyproject.toml").exists():
            raise ValueError(f"{name!r} does not look like a server (missing pyproject.toml)")
        dirs.append(p)
    return dirs


def _print_json(*, ok: bool, servers_checked: int, problems: list[str]) -> None:
    print(
        json.dumps(
            {
                "ok": ok,
                "servers_checked": servers_checked,
                "problems": problems,
            },
            indent=2,
            sort_keys=True,
        )
    )


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(list(sys.argv[1:] if argv is None else argv))

    problems: list[str] = []
    servers_checked = 0
    project_names: dict[str, str] = {}  # project.name -> server dir
    stop = False

    def add_problem(msg: str) -> None:
        nonlocal stop
        problems.append(msg)
        if args.fail_fast:
            stop = True

    try:
        server_dirs = _iter_server_dirs(args.servers)
    except ValueError as e:
        if args.format == "json":
            _print_json(ok=False, servers_checked=0, problems=[f"error: {e}"])
        else:
            print(f"error: {e}")
        return 1

    for child in server_dirs:
        servers_checked += 1
        pyproject = child / "pyproject.toml"

        try:
            data = _read_pyproject(pyproject)
        except Exception as e:  # best-effort: tomllib raises various errors
            add_problem(
                f"{child.name}: failed to parse pyproject.toml ({e.__class__.__name__}: {e})"
            )
            if stop:
                break
            continue

        build_system = data.get("build-system")
        if not isinstance(build_system, dict):
            add_problem(f"{child.name}: missing [build-system] in pyproject.toml")
            if stop:
                break
        else:
            requires = build_system.get("requires")
            build_backend = build_system.get("build-backend")
            if not isinstance(requires, list) or not requires:
                add_problem(f"{child.name}: missing/empty build-system.requires")
                if stop:
                    break
            if not isinstance(build_backend, str) or not build_backend.strip():
                add_problem(f"{child.name}: missing build-system.build-backend")
                if stop:
                    break

        if stop:
            break

        project = data.get("project")
        if not isinstance(project, dict):
            add_problem(f"{child.name}: missing [project] in pyproject.toml")
            if stop:
                break
            continue

        name = project.get("name")
        version = project.get("version")
        if not isinstance(name, str) or not name.strip():
            add_problem(f"{child.name}: missing project.name")
            if stop:
                break
        else:
            prev = project_names.get(name)
            if prev is not None and prev != child.name:
                add_problem(
                    f"{child.name}: duplicate project.name {name!r} (also used by {prev})"
                )
                if stop:
                    break
            else:
                project_names[name] = child.name

        if stop:
            break

        if not isinstance(version, str) or not version.strip():
            add_problem(f"{child.name}: missing project.version")
            if stop:
                break

        if stop:
            break

        requires_py = project.get("requires-python")
        if not isinstance(requires_py, str) or not requires_py.strip():
            add_problem(f"{child.name}: missing project.requires-python")
            if stop:
                break

        if stop:
            break

        deps = project.get("dependencies")
        if not isinstance(deps, list) or not deps:
            add_problem(f"{child.name}: missing/empty project.dependencies")
            if stop:
                break
        else:
            has_mcp = any(
                isinstance(d, str) and d.strip().lower().startswith("mcp") for d in deps
            )
            if not has_mcp:
                add_problem(f"{child.name}: project.dependencies missing 'mcp'")
                if stop:
                    break

        if stop:
            break

        scripts = project.get("scripts")
        if not isinstance(scripts, dict) or not scripts:
            add_problem(f"{child.name}: missing/empty [project.scripts] entrypoints")
            if stop:
                break
        else:
            for script_name, target in sorted(scripts.items()):
                if not isinstance(target, str) or ":" not in target:
                    add_problem(
                        f"{child.name}: script '{script_name}' has invalid target: {target!r}"
                    )
                    if stop:
                        break
                    continue
                module, _sep, attr = target.partition(":")
                module = module.strip()
                attr = attr.strip()
                if not module or not attr:
                    add_problem(
                        f"{child.name}: script '{script_name}' has invalid target: {target!r}"
                    )
                    if stop:
                        break
                    continue

                module_file = _find_module_file(child, module)
                if module_file is None:
                    add_problem(
                        f"{child.name}: script '{script_name}' points to missing module '{module}'"
                    )
                    if stop:
                        break
                    continue

                if module_file.suffix == ".py" and not _module_defines_attr(module_file, attr):
                    add_problem(
                        f"{child.name}: script '{script_name}' points to missing attr '{attr}' in '{module}'"
                    )
                    if stop:
                        break

            if stop:
                break

        readme = child / "README.md"
        if not readme.exists():
            add_problem(f"{child.name}: missing README.md")
            if stop:
                break

        usage = child / "usage.md"
        if not usage.exists():
            add_problem(f"{child.name}: missing usage.md")
            if stop:
                break

    ok = not problems

    if args.format == "json":
        _print_json(ok=ok, servers_checked=servers_checked, problems=problems)
        return 0 if ok else 1

    if problems:
        print("Validation issues:\n")
        for p in problems:
            print(f"- {p}")
        return 1

    print(f"OK: collection looks consistent ({servers_checked} servers validated)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
