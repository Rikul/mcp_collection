"""Basic tests for News MCP server.

Note: These tests verify the functions exist and have basic structure.
Full integration tests would require mocking the external RSS feed calls.
"""


def test_google_us_news_function_exists():
    from news_mcp import server as srv
    assert hasattr(srv, 'google_us_news')
    assert callable(srv.google_us_news)


def test_guardian_us_news_function_exists():
    from news_mcp import server as srv
    assert hasattr(srv, 'guardian_us_news')
    assert callable(srv.guardian_us_news)


def test_tech_hacker_news_function_exists():
    from news_mcp import server as srv
    assert hasattr(srv, 'tech_hacker_news')
    assert callable(srv.tech_hacker_news)
