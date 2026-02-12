"""Basic tests for Weather & Geocoding MCP server.

Note: These tests verify the functions exist and have basic structure.
Full integration tests would require mocking the external API calls.
"""


def test_get_weather_function_exists():
    from weather_geocoding import server as srv
    assert hasattr(srv, 'get_weather')
    assert callable(srv.get_weather)


def test_geocode_location_function_exists():
    from weather_geocoding import server as srv
    assert hasattr(srv, 'geocode_location')
    assert callable(srv.geocode_location)
