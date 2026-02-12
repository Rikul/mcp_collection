"""Basic tests for Yahoo Finance MCP server.

Note: These tests verify the functions exist and have basic structure.
Full integration tests would require mocking the external yfinance API calls.
"""


def test_get_stock_info_function_exists():
    from yfin_mcp import server as srv
    assert hasattr(srv, 'get_stock_info')
    assert callable(srv.get_stock_info)


def test_get_stock_history_function_exists():
    from yfin_mcp import server as srv
    assert hasattr(srv, 'get_stock_history')
    assert callable(srv.get_stock_history)
