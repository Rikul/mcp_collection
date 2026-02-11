# Countries & Currencies MCP Server

A small MCP server that provides:

- Country lookups via **REST Countries** (`restcountries.com`)
- Exchange rates and currency conversion via **ExchangeRate-API** (`api.exchangerate-api.com`)

## Available tools

- `get_country_info(country)`
- `search_countries_by_region(region)`
- `search_countries_by_currency(currency_code)`
- `search_countries_by_language(language)`
- `get_exchange_rates(base_currency="USD")`
- `convert_currency(amount, from_currency, to_currency)`
- `compare_countries(country1, country2)`

## Running

```bash
uv run countries-currencies-mcp
```
