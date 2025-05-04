"""
dynamic_watchlist_lib/metrics.py

Functions to compute VWAP, Pivot Points, and detect volume surges.
"""

import pandas as pd

def calculate_vwap(df: pd.DataFrame) -> float:
    """
    Calculate Volume Weighted Average Price (VWAP) for the given DataFrame.
    Expects columns: ['open', 'high', 'low', 'close', 'volume'].
    """
    if df.empty or df['volume'].sum() == 0:
        return 0.0
    # Typical price
    tp = (df['high'] + df['low'] + df['close']) / 3
    vwap = (tp * df['volume']).sum() / df['volume'].sum()
    return float(vwap)

def calculate_pivots(df: pd.DataFrame) -> dict:
    """
    Calculate pivot point, support and resistance levels for the last row in df.
    Expects columns: ['open', 'high', 'low', 'close'].
    
    Returns a dict with keys: pivot, r1, r2, s1, s2.
    """
    if df.empty:
        return {'pivot': 0, 'r1': 0, 'r2': 0, 's1': 0, 's2': 0}
    last = df.iloc[-1]
    high = last['high']
    low = last['low']
    close = last['close']
    pivot = (high + low + close) / 3
    r1 = (2 * pivot) - low
    s1 = (2 * pivot) - high
    r2 = pivot + (high - low)
    s2 = pivot - (high - low)
    return {
        'pivot': float(pivot),
        'r1': float(r1),
        'r2': float(r2),
        's1': float(s1),
        's2': float(s2),
    }

def detect_volume_surge(df: pd.DataFrame, window: int = 5, factor: float = 2.0) -> bool:
    """
    Detect a volume surge: if the latest volume exceeds (factor * average volume over the prior window).
    """
    if df.empty or len(df) <= window:
        return False
    vols = df['volume'].iloc[-(window+1):-1]
    avg_vol = vols.mean()
    latest_vol = df['volume'].iloc[-1]
    return latest_vol > (factor * avg_vol)
