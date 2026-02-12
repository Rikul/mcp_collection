"""Basic tests for Wikipedia MCP server.

Note: These tests verify the functions exist and have basic structure.
Full integration tests would require mocking the external Wikipedia API calls.
"""


def test_search_function_exists():
    from wikipedia_mcp import server as srv
    assert hasattr(srv, 'search')
    assert callable(srv.search)


def test_get_page_function_exists():
    from wikipedia_mcp import server as srv
    assert hasattr(srv, 'get_page')
    assert callable(srv.get_page)
