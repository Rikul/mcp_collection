from __future__ import annotations

import pandas as pd
import pytest

import importlib

mod = importlib.import_module("yfin_mcp.server")


class _Ticker:
    def __init__(self, ticker: str):
        self.ticker = ticker

    def history(self, start=None, end=None, interval=None, auto_adjust=None):
        idx = pd.DatetimeIndex([pd.Timestamp("2024-01-02")])
        return pd.DataFrame(
            {
                "Open": [1.0],
                "High": [2.0],
                "Low": [0.5],
                "Close": [1.5],
                "Volume": [100],
            },
            index=idx,
        )


def test_get_ticker_data_monkeypatched(monkeypatch):
    import yfinance as yf

    monkeypatch.setattr(yf, "Ticker", _Ticker)
    out = mod.get_ticker_data.fn("AAPL", last_n_days=1)
    assert out["ticker"] == "AAPL"
    assert out["candles"][0]["close"] == 1.5


def test_validate_request_errors():
    with pytest.raises(ValueError):
        mod.get_ticker_data.fn("", last_n_days=1)
