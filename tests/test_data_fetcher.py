import pytest
import pandas as pd
from typing import Optional

import dynamic_watchlist_lib.data_fetcher as df_module
from dynamic_watchlist_lib.data_fetcher import (
    get_instrument_map,
    fetch_intraday_ohlc,
    fetch_daily_ohlc,
    fetch_futures_oi,
    fetch_latest_news,
    fetch_corporate_events,
)
import dynamic_watchlist_lib.config as config_module

class DummyClient:
    def __init__(self):
        self._data_called = False

    def instruments(self, exchange: str):
        # Return dummy instrument list
        return [
            {"tradingsymbol": "TEST", "instrument_token": 123, "segment": "NSE"},
            {"tradingsymbol": "TESTFUT", "instrument_token": 456, "segment": "NFO-FUT", "expiry": "2025-05-01"},
        ]

    def ltp(self, symbol: str):
        # Return dummy OI and token mapping
        if "TESTFUT" in symbol:
            return {symbol: {"oi": 1000}}
        return {symbol: {"instrument_token": 123}}

    def historical_data(self, token: int, from_ts, to_ts, interval: str):
        # Return dummy OHLC data
        times = pd.date_range(start=pd.Timestamp('2025-01-01'), periods=3, freq='5T')
        return [
            {"date": times[0], "open": 100, "high": 105, "low": 95, "close": 102, "volume": 1000},
            {"date": times[1], "open": 102, "high": 108, "low": 101, "close": 107, "volume": 1100},
            {"date": times[2], "open": 107, "high": 110, "low": 105, "close": 109, "volume": 1200},
        ]

@pytest.fixture(autouse=True)
def patch_kite_client(monkeypatch):
    dummy = DummyClient()
    # Patch Kite client creation
    monkeypatch.setattr(df_module, "get_kite_client", lambda: dummy)
    # Stub out news API credentials in config
    monkeypatch.setattr(config_module, "FT_NEWS_API_KEY", "dummy", raising=False)
    monkeypatch.setattr(config_module, "FT_NEWS_ENDPOINT", "https://dummy", raising=False)
    return dummy

def test_get_instrument_map():
    inst_map = get_instrument_map()
    assert isinstance(inst_map, dict)
    assert inst_map["TEST"] == 123

def test_fetch_intraday_ohlc_stub():
    df = fetch_intraday_ohlc("TEST")
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert len(df) == 3

def test_fetch_daily_ohlc_stub():
    df = fetch_daily_ohlc("TEST")
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert len(df) == 3

def test_fetch_futures_oi_stub():
    oi = fetch_futures_oi("TEST")
    # Our stub picks TESTFUT nearest expiry
    assert oi == 1000

def test_fetch_latest_news_stub(monkeypatch):
    # Ensure FT_NEWS_API_KEY and ENDPOINT are set in config
    # Monkeypatch requests.get to return dummy structure
    class DummyResponse:
        status_code = 200
        def json(self):
            return {"articles": [{"title": "News1"}, {"title": "News2"}]}
    monkeypatch.setattr(df_module.requests, "get", lambda url, params, timeout: DummyResponse())
    news = fetch_latest_news(count=2)
    assert isinstance(news, list)
    assert len(news) == 2
    assert news[0]["title"] == "News1"

def test_fetch_corporate_events_stub():
    events = fetch_corporate_events("TEST")
    assert isinstance(events, list)
    assert events == []
