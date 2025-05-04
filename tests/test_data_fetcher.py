import pytest
import pandas as pd
from typing import Optional

import dynamic_watchlist_lib.data_fetcher as df_module
from dynamic_watchlist_lib.data_fetcher import (
    get_instrument_map,
    fetch_intraday_ohlc,
    fetch_daily_ohlc,
    fetch_futures_oi,
)

class DummyClient:
    def instruments(self, exchange: str):
        return [{"tradingsymbol": "TEST", "instrument_token": 123, "segment": "NSE"}]

    def ltp(self, symbol: str):
        return {symbol: {"instrument_token": 123}}

    def historical_data(self, token: int, from_ts, to_ts, interval: str):
        times = pd.date_range(start='2025-01-01', periods=3, freq='D')
        return [
            {"date": times[0], "open": 100, "high": 105, "low": 95, "close": 102, "volume": 1000},
            {"date": times[1], "open": 102, "high": 108, "low": 101, "close": 107, "volume": 1100},
            {"date": times[2], "open": 107, "high": 110, "low": 105, "close": 109, "volume": 1200},
        ]

@pytest.fixture(autouse=True)
def patch_kite_client(monkeypatch):
    dummy = DummyClient()
    monkeypatch.setattr(df_module, "get_kite_client", lambda: dummy)
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

def test_fetch_futures_oi_stub():
    oi = fetch_futures_oi("TEST")
    assert oi is None or isinstance(oi, int)
