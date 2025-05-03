import pandas as pd
import pytest
from dynamic_watchlist_lib import sector_mapping as sm
from dynamic_watchlist_lib.data_fetcher import fetch_intraday_ohlc

LIVE_SYMBOL = "RELIANCE"  # example live-traded symbol


def test_get_sector_index_known():
    # Test known mapping returns a non-empty string
    idx = sm.get_sector_index('CIPLA')
    assert isinstance(idx, str) and len(idx) > 0


def test_get_sector_index_default():
    # Test fallback for unmapped symbol
    idx = sm.get_sector_index('UNKNOWN_SYMBOL')
    assert idx == sm.DEFAULT_SECTOR


def test_get_intraday_change_live():
    # Fetch live intraday OHLC and calculate change; should return a float
    df = fetch_intraday_ohlc(LIVE_SYMBOL)
    change = sm.get_intraday_change(LIVE_SYMBOL)
    assert isinstance(change, float)
    # DataFrame should have close column
    assert 'close' in df.columns


def test_get_sector_deviation_live():
    # Calculate live sector deviation; should return a float
    deviation = sm.get_sector_deviation(LIVE_SYMBOL)
    assert isinstance(deviation, float)


def test_get_intraday_change_zero_if_no_data():
    # Simulate no data scenario by using an unlikely symbol
    with pytest.raises(ValueError):
        sm.get_intraday_change('NON_EXISTENT')


def test_get_sector_deviation_zero_if_no_data():
    # Simulate no data scenario for sector deviation
    with pytest.raises(ValueError):
        sm.get_sector_deviation('NON_EXISTENT')
