import pytest
import pandas as pd
from dynamic_watchlist_lib.data_fetcher import (
    get_instrument_map,
    fetch_intraday_ohlc,
    fetch_daily_ohlc,
    fetch_futures_oi,
    fetch_latest_news,
    fetch_corporate_events,
)

LIVE_SYMBOL = "RELIANCE"  # example live-traded symbol


def test_get_instrument_map_basic():
    inst_map = get_instrument_map()
    assert isinstance(inst_map, dict)
    assert LIVE_SYMBOL in inst_map
    # Values should be integer tokens
    assert isinstance(inst_map[LIVE_SYMBOL], int)


def test_fetch_intraday_ohlc_live():
    df = fetch_intraday_ohlc(LIVE_SYMBOL)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    # Check essential OHLCV columns
    for col in ['open', 'high', 'low', 'close', 'volume']:
        assert col in df.columns


def test_fetch_daily_ohlc_live():
    df = fetch_daily_ohlc(LIVE_SYMBOL)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    for col in ['open', 'high', 'low', 'close', 'volume']:
        assert col in df.columns


def test_fetch_futures_oi_live():
    oi = fetch_futures_oi(LIVE_SYMBOL)
    # Could be None if no futures OI available or an integer
    assert oi is None or isinstance(oi, (int, float))


def test_fetch_latest_news_returns_list():
    news = fetch_latest_news(LIVE_SYMBOL)
    assert isinstance(news, list)
    # Each item should be a dict if news exist
    if news:
        assert isinstance(news[0], dict)


def test_fetch_corporate_events_returns_list():
    events = fetch_corporate_events(LIVE_SYMBOL)
    assert isinstance(events, list)
    # Stub returns empty list; but type is correct
    for ev in events:
        assert isinstance(ev, dict)


def test_errors_for_invalid_symbol():
    with pytest.raises(ValueError):
        fetch_intraday_ohlc("NON_EXISTENT")
    with pytest.raises(ValueError):
        fetch_daily_ohlc("NON_EXISTENT")
    with pytest.raises(ValueError):
        fetch_futures_oi("NON_EXISTENT")
