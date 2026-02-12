"""Basic tests for Chess API MCP server.

Note: These tests verify the function exists and has basic structure.
Full integration tests would require mocking the external Chess API.
"""


def test_analyze_position_function_exists():
    from chess_api_mcp import server as srv
    assert hasattr(srv, 'analyze_position')
    assert callable(srv.analyze_position)
