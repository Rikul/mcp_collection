import asyncio
import re

from uuid_tools import server as srv


def test_uuid_v4_returns_valid_uuid():
    result = asyncio.run(srv.uuid_v4())
    # UUIDv4 should match the standard UUID format
    uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$', re.IGNORECASE)
    assert uuid_pattern.match(result)


def test_uuid_v5_deterministic():
    result1 = asyncio.run(srv.uuid_v5("dns", "example.com"))
    result2 = asyncio.run(srv.uuid_v5("dns", "example.com"))
    # UUIDv5 should be deterministic
    assert result1 == result2
    assert len(result1) == 36


def test_uuid_validate_accepts_valid():
    result = asyncio.run(srv.uuid_validate("550e8400-e29b-41d4-a716-446655440000"))
    assert result == "ok"


def test_uuid_validate_rejects_invalid():
    result = asyncio.run(srv.uuid_validate("not-a-uuid"))
    assert "invalid" in result


def test_uuid_inspect_returns_metadata():
    result = asyncio.run(srv.uuid_inspect("550e8400-e29b-41d4-a716-446655440000"))
    assert "uuid:" in result
    assert "hex:" in result
    assert "version:" in result
    assert "variant:" in result
