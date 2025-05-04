import pandas as pd
import numpy as np
import pytest

from dynamic_watchlist_lib.metrics import calculate_vwap, calculate_pivots, detect_volume_surge

def make_ohlc_df(prices, volumes):
    times = pd.date_range(start=pd.Timestamp('2025-01-01 09:15'), periods=len(prices), freq='5T', tz='Asia/Kolkata')
    df = pd.DataFrame({
        'open': prices,
        'high': prices,
        'low': prices,
        'close': prices,
        'volume': volumes
    }, index=times)
    return df

def test_calculate_vwap_basic():
    prices = [100, 110, 120]
    volumes = [10, 20, 30]
    df = make_ohlc_df(prices, volumes)
    vwap = calculate_vwap(df)
    # (100*10 + 110*20 + 120*30) / (10+20+30) = (1000 + 2200 + 3600)/60 = 6800/60 = 113.333...
    assert pytest.approx(vwap, rel=1e-3) == 113.3333

def test_calculate_vwap_empty():
    df = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
    vwap = calculate_vwap(df)
    assert vwap == 0.0

def test_calculate_pivots_basic():
    # Create daily OHLC
    dates = pd.date_range('2025-01-01', periods=3, freq='D')
    df = pd.DataFrame({
        'open': [100, 105, 110],
        'high': [110, 115, 120],
        'low': [90, 95, 100],
        'close': [105, 110, 115],
    }, index=dates)
    pivots = calculate_pivots(df)
    # Pivot for last day: (110+120+100)/3 = 330/3 = 110
    assert pytest.approx(pivots['pivot'], rel=1e-6) == 110
    assert pytest.approx(pivots['r1'], rel=1e-6) == 120  # 2*pivot - low = 220 - 100
    assert pytest.approx(pivots['s1'], rel=1e-6) == 100  # 2*pivot - high = 220 - 120

def test_calculate_pivots_empty():
    df = pd.DataFrame(columns=['open', 'high', 'low', 'close'])
    pivots = calculate_pivots(df)
    assert pivots == {'pivot': 0, 'r1': 0, 'r2': 0, 's1': 0, 's2': 0}

def test_detect_volume_surge_true():
    # window=3, factor=2 => avg of first 3 volumes = (10+20+30)/3=20
    # next volume 50 > 2*20=40 => surge
    volumes = [10, 20, 30, 50]
    prices = [100, 100, 100, 100]
    df = make_ohlc_df(prices, volumes)
    assert detect_volume_surge(df, window=3, factor=2.0)

def test_detect_volume_surge_false():
    # window=3, factor=3 => avg of first 3 volumes = 20, threshold=60, 50 < 60 => no surge
    volumes = [10, 20, 30, 50]
    prices = [100, 100, 100, 100]
    df = make_ohlc_df(prices, volumes)
    assert not detect_volume_surge(df, window=3, factor=3.0)

def test_detect_volume_surge_insufficient():
    # Less data than window => should return False
    volumes = [10, 20]
    prices = [100, 100]
    df = make_ohlc_df(prices, volumes)
    assert not detect_volume_surge(df, window=5, factor=2.0)
