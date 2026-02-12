"""Basic tests for Countries & Currencies MCP server.

Note: These tests verify the functions exist and have basic structure.
Full integration tests would require mocking the external API calls.
"""


def test_get_country_info_function_exists():
    from countries_currencies import server as srv
    assert hasattr(srv, 'get_country_info')
    assert callable(srv.get_country_info)


def test_get_exchange_rates_function_exists():
    from countries_currencies import server as srv
    assert hasattr(srv, 'get_exchange_rates')
    assert callable(srv.get_exchange_rates)
