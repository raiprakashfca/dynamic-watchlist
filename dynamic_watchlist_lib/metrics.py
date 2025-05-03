"""
Metric calculation functions for dynamic_watchlist_lib.
Includes VWAP, pivot points, and volume surge detection.
"""
from typing import Tuple
import pandas as pd


def calculate_vwap(df: pd.DataFrame) -> float:
    """
    Calculate Volume-Weighted Average Price (VWAP) for the given DataFrame.
    Assumes df has columns: ['high', 'low', 'close', 'volume'] indexed by timestamp.
    """
    if df.empty or 'volume' not in df or df['volume'].sum() == 0:
        return 0.0
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    vwap = (typical_price * df['volume']).sum() / df['volume'].sum()
    return float(vwap)


def calculate_pivots(df: pd.DataFrame) -> Tuple[float, float, float, float, float]:
    """
    Calculate standard pivot point and support/resistance levels.

    Returns:
        pivot: (High + Low + Close) / 3
        r1: 2*pivot - Low
        r2: pivot + (High - Low)
        s1: 2*pivot - High
        s2: pivot - (High - Low)
    """
    if df.empty:
        return (0.0, 0.0, 0.0, 0.0, 0.0)
    high = df['high'].iloc[-1]
    low = df['low'].iloc[-1]
    close = df['close'].iloc[-1]
    pivot = (high + low + close) / 3.0
    r1 = 2 * pivot - low
    r2 = pivot + (high - low)
    s1 = 2 * pivot - high
    s2 = pivot - (high - low)
    return float(pivot), float(r1), float(r2), float(s1), float(s2)


def detect_volume_surge(df: pd.DataFrame, window: int = 6, factor: float = 2.0) -> bool:
    """
    Detects if latest volume is greater than a factor * average volume over a window.

    Args:
        df: intraday OHLC DataFrame with 'volume' column.
        window: rolling window (number of periods) to compute average volume.
        factor: multiplier threshold for surge detection.

    Returns:
        True if latest volume > factor * rolling average volume, else False.
    """
    if df.empty or 'volume' not in df or len(df['volume']) < window + 1:
        return False
    rolling_avg = df['volume'].rolling(window=window).mean().iloc[-2]
    latest_vol = df['volume'].iloc[-1]
    return latest_vol > factor * rolling_avg
