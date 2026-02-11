# Weather & Geocoding MCP Server

An MCP server that combines:

- Forward + reverse geocoding via **OpenStreetMap Nominatim**
- Weather and forecasts via **Open-Meteo**

## Available tools

- `geocode_location(location)`
- `reverse_geocode(latitude, longitude)`
- `get_current_weather(location)`
- `get_weather_forecast(location, days=7)`
- `get_weather_by_coordinates(latitude, longitude)`

## Running

```bash
uv run weather-geocoding-mcp
```

## API etiquette

Nominatim requires a descriptive User-Agent. This server sets one by default.
