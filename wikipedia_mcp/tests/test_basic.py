"""Basic tests for Wikipedia MCP server.

Note: These tests verify the functions exist and have basic structure.
Full integration tests would require mocking the external Wikipedia API calls.
"""


def test_search_articles_function_exists():
    from wikipedia_mcp import server as srv
    assert hasattr(srv, 'search_articles')
    assert callable(srv.search_articles)


def test_get_page_summary_function_exists():
    from wikipedia_mcp import server as srv
    assert hasattr(srv, 'get_page_summary')
    assert callable(srv.get_page_summary)
