"""Basic tests for News MCP server.

Note: These tests verify the functions exist and have basic structure.
Full integration tests would require mocking the external RSS feed calls.
"""


def test_get_google_news_function_exists():
    from news_mcp import server as srv
    assert hasattr(srv, 'get_google_news')
    assert callable(srv.get_google_news)


def test_get_guardian_news_function_exists():
    from news_mcp import server as srv
    assert hasattr(srv, 'get_guardian_news')
    assert callable(srv.get_guardian_news)


def test_get_hacker_news_function_exists():
    from news_mcp import server as srv
    assert hasattr(srv, 'get_hacker_news')
    assert callable(srv.get_hacker_news)
