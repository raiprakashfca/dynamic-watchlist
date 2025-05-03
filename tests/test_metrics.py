import pytest
import pandas as pd
from dynamic_watchlist_lib.metrics import calculate_vwap, calculate_pivots, detect_volume_surge


def make_ohlc_df(prices, volumes, times=None):
    """Helper to create OHLC DataFrame with 'high', 'low', 'close', 'volume'."""
    data = {
        'high': prices,
        'low': prices,
        'close': prices,
        'volume': volumes
    }
    df = pd.DataFrame(data)
    if times is not None:
        df.index = pd.to_datetime(times)
    return df


def test_calculate_vwap_basic():
    prices = [100, 102, 101]
    volumes = [10, 20, 30]
    df = make_ohlc_df(prices, volumes)
    # VWAP = (100*10 + 102*20 + 101*30) / (10+20+30)
    expected = (100*10 + 102*20 + 101*30) / 60
    assert pytest.approx(calculate_vwap(df), rel=1e-6) == expected


def test_calculate_vwap_empty_or_zero_volume():
    df_empty = pd.DataFrame()
    assert calculate_vwap(df_empty) == 0.0
    df_zero_vol = make_ohlc_df([100, 100], [0, 0])
    assert calculate_vwap(df_zero_vol) == 0.0


def test_calculate_pivots_basic():
    prices = [100, 105, 102, 108]
    df = make_ohlc_df(prices, [1]*4)
    # Using last values: high=108, low=108, close=108
    pivot, r1, r2, s1, s2 = calculate_pivots(df)
    # high=108, low=108, close=108 => pivot=108
    assert pivot == pytest.approx(108)
    assert r1 == pytest.approx(2*pivot - 108)
    assert r2 == pytest.approx(pivot + (108-108))
    assert s1 == pytest.approx(2*pivot - 108)
    assert s2 == pytest.approx(pivot - (108-108))


def test_calculate_pivots_empty():
    df_empty = pd.DataFrame()
    assert calculate_pivots(df_empty) == (0.0, 0.0, 0.0, 0.0, 0.0)


def test_detect_volume_surge_true():
    # window=3, factor=2 => avg of first 3 volumes = (10+20+30)/3=20
    # next volume 50 > 2*20=40 => surge
    volumes = [10, 20, 30, 50]
    prices = [100, 100, 100, 100]
    df = make_ohlc_df(prices, volumes)
    assert detect_volume_surge(df, window=3, factor=2.0) is True


def test_detect_volume_surge_false():
    volumes = [10, 20, 30, 35]
    prices = [100, 100, 100, 100]
    df = make_ohlc_df(prices, volumes)
    assert detect_volume_surge(df, window=3, factor=2.0) is False


def test_detect_volume_surge_insufficient_data():
    # fewer than window+1 rows
    df = make_ohlc_df([100, 100, 100], [10, 20, 30])
    assert detect_volume_surge(df, window=5, factor=2.0) is False
