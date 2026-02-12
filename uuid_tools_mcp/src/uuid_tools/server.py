from __future__ import annotations

import uuid

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("UUID Tools")


def _parse_namespace(namespace: str) -> uuid.UUID:
    ns = (namespace or "").strip().lower()
    if ns in {"dns", "namespace_dns"}:
        return uuid.NAMESPACE_DNS
    if ns in {"url", "namespace_url"}:
        return uuid.NAMESPACE_URL
    if ns in {"oid", "namespace_oid"}:
        return uuid.NAMESPACE_OID
    if ns in {"x500", "namespace_x500"}:
        return uuid.NAMESPACE_X500
    return uuid.UUID(namespace)


@mcp.tool()
async def uuid_v4() -> str:
    """Generate a random UUIDv4 and return it as a string."""
    return str(uuid.uuid4())


@mcp.tool()
async def uuid_v5(namespace: str, name: str) -> str:
    """Generate a deterministic UUIDv5 from a namespace + name.

    `namespace` may be one of: dns, url, oid, x500, or an explicit UUID string.
    """
    ns = _parse_namespace(namespace)
    return str(uuid.uuid5(ns, name or ""))


@mcp.tool()
async def uuid_validate(value: str) -> str:
    """Validate a UUID string.

    Returns "ok" if valid, otherwise a human-readable error.
    """
    try:
        uuid.UUID(value)
    except Exception as e:  # noqa: BLE001
        return f"invalid: {e}"
    return "ok"


@mcp.tool()
async def uuid_inspect(value: str) -> str:
    """Parse a UUID string and return basic metadata."""
    u = uuid.UUID(value)
    return "\n".join(
        [
            f"uuid: {str(u)}",
            f"hex: {u.hex}",
            f"version: {u.version}",
            f"variant: {u.variant}",
        ]
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
