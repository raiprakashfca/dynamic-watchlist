import pytest
import pandas as pd
from dynamic_watchlist_lib import sector_mapping as sm

# Helper to create OHLC DataFrame with sequential close values
def make_df_for_change(closes):
    df = pd.DataFrame({
        'close': closes,
        'high': closes,
        'low': closes,
        'volume': [1]*len(closes)
    })
    return df


def test_get_sector_index_known():
    # Test known mapping
    assert sm.get_sector_index('CIPLA') == 'NIFTY PHARMA'
    assert sm.get_sector_index('ICICIBANK') == 'NIFTY BANK'


def test_get_sector_index_default():
    # Test fallback for unmapped symbol
    assert sm.get_sector_index('UNKNOWN') == sm.DEFAULT_SECTOR


def test_get_intraday_change_positive(monkeypatch):
    # Stub fetch_intraday_ohlc to return a DataFrame with known closes
    monkeypatch.setattr(sm, 'fetch_intraday_ohlc', lambda sym: make_df_for_change([100, 110]))
    change = sm.get_intraday_change('ANY')
    assert pytest.approx(change, rel=1e-6) == (110 - 100)/100*100


def test_get_intraday_change_empty(monkeypatch):
    # Stub fetch_intraday_ohlc to return empty DataFrame
    monkeypatch.setattr(sm, 'fetch_intraday_ohlc', lambda sym: pd.DataFrame())
    assert sm.get_intraday_change('ANY') == 0.0


def test_get_sector_deviation(monkeypatch):
    # Prepare stubs: equity symbol change = 10%, sector index change = 4%
    def stub_fetch(sym):
        if sym == 'TESTSYM':
            return make_df_for_change([100, 110])  # 10% increase
        elif sym == 'NIFTY BANK':
            return make_df_for_change([100, 104])  # 4% increase
        else:
            return pd.DataFrame()

    monkeypatch.setattr(sm, 'fetch_intraday_ohlc', stub_fetch)
    # Ensure mapping from TESTSYM -> NIFTY BANK for this test
    monkeypatch.setitem(sm.SECTOR_INDEX_MAP, 'TESTSYM', 'NIFTY BANK')
    deviation = sm.get_sector_deviation('TESTSYM')
    assert pytest.approx(deviation, rel=1e-6) == (10 - 4)


def test_get_sector_deviation_default(monkeypatch):
    # Equity and default sector both no change
    monkeypatch.setattr(sm, 'fetch_intraday_ohlc', lambda sym: pd.DataFrame())
    # Unmapped symbol => DEFAULT_SECTOR; both changes zero => deviation zero
    dev = sm.get_sector_deviation('UNMAPPED')
    assert dev == 0.0
