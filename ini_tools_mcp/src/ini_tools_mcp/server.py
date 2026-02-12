from __future__ import annotations

import configparser
import io
import json

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("INI Tools")


def _parser() -> configparser.ConfigParser:
    # Keep behavior close to typical INI semantics:
    # - case-insensitive keys
    # - allow entries without values
    return configparser.ConfigParser(
        interpolation=None,
        allow_no_value=True,
        delimiters=("=", ":"),
        strict=False,
    )


def _load(text: str) -> configparser.ConfigParser:
    p = _parser()
    try:
        p.read_string(text or "")
    except (configparser.Error, UnicodeDecodeError) as e:
        raise ValueError(f"Invalid INI: {e}")
    return p


def _dump(p: configparser.ConfigParser) -> str:
    buf = io.StringIO()
    p.write(buf)
    out = buf.getvalue()
    # configparser always ends with a newline; strip a single trailing newline.
    return out[:-1] if out.endswith("\n") else out


@mcp.tool()
async def ini_to_json(text: str, include_defaults: bool = False) -> str:
    """Convert INI text to JSON.

    Returns a JSON object mapping sections -> options.

    If include_defaults is true, include DEFAULT values for each section.
    """

    p = _load(text)

    result: dict[str, dict[str, str | None]] = {}
    for section in p.sections():
        items = dict(p.items(section, raw=True))
        if not include_defaults:
            # Remove DEFAULT-derived keys by comparing with defaults.
            for k in list(items.keys()):
                if k in p.defaults() and items[k] == p.defaults().get(k):
                    items.pop(k, None)
        # configparser can represent valueless options as None.
        cleaned: dict[str, str | None] = {}
        for k, v in items.items():
            cleaned[k] = v  # may be None when allow_no_value=True
        result[section] = cleaned

    if include_defaults and p.defaults():
        result.setdefault("DEFAULT", {})
        for k, v in p.defaults().items():
            result["DEFAULT"][k] = v

    return json.dumps(result, indent=2, sort_keys=True)


@mcp.tool()
async def ini_get(text: str, section: str, option: str, fallback: str = "") -> str:
    """Get a single option value from INI text.

    Returns fallback if the section/option does not exist.
    """

    p = _load(text)

    if not section:
        return fallback

    if section == "DEFAULT":
        return p.defaults().get(option, fallback)

    if not p.has_section(section):
        return fallback

    if not p.has_option(section, option):
        return fallback

    return p.get(section, option, raw=True, fallback=fallback)


@mcp.tool()
async def ini_set(text: str, section: str, option: str, value: str) -> str:
    """Set/update an option in an INI blob and return rewritten INI text."""

    p = _load(text)

    if not section or section == "DEFAULT":
        p["DEFAULT"][option] = value
        return _dump(p)

    if not p.has_section(section):
        p.add_section(section)

    p.set(section, option, value)
    return _dump(p)


@mcp.tool()
async def ini_remove_option(text: str, section: str, option: str) -> str:
    """Remove an option (if present) and return rewritten INI text."""

    p = _load(text)

    if not section:
        return _dump(p)

    if section == "DEFAULT":
        p.defaults().pop(option, None)
        return _dump(p)

    if p.has_section(section):
        p.remove_option(section, option)

    return _dump(p)


@mcp.tool()
async def ini_remove_section(text: str, section: str) -> str:
    """Remove a section (if present) and return rewritten INI text."""

    p = _load(text)

    if section and p.has_section(section):
        p.remove_section(section)

    return _dump(p)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
