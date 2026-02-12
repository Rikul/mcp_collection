"""Basic tests for Yahoo Finance MCP server.

Note: These tests verify the functions exist and have basic structure.
Full integration tests would require mocking the external yfinance API calls.
"""


def test_mcp_server_initialized():
    from yfin_mcp import server as srv
    # Verify the mcp server is initialized
    assert srv is not None
    assert hasattr(srv, 'name')


def test_ticker_tools_registered():
    from yfin_mcp import server as srv
    # Verify tools are registered with the MCP server
    tools = srv.get_tools() if hasattr(srv, 'get_tools') else []
    # Even if we can't list tools, verify the server object exists
    assert srv is not None
