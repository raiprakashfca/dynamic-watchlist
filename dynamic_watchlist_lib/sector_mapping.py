"""
dynamic_watchlist_lib/sector_mapping.py

Map equities to NIFTY sector indices and compute relative performance.
"""

from typing import Optional
import pandas as pd
from .data_fetcher import fetch_intraday_ohlc, fetch_daily_ohlc
from .utils import cache_ttl

# Static map of equity symbol to its NIFTY sector index
SECTOR_INDEX_MAP = {
    "ASIANPAINT": "NIFTY AUTO",
    "BAJAJ-AUTO": "NIFTY AUTO",
    "BANKBARODA": "NIFTY BANK",
    "BPCL": "NIFTY ENERGY",
    "CIPLA": "NIFTY PHARMA",
    "COALINDIA": "NIFTY METAL",
    "ICICIBANK": "NIFTY BANK",
    "ITC": "NIFTY FMCG",
    "JSWSTEEL": "NIFTY METAL",
    "LT": "NIFTY METAL",
    "MARUTI": "NIFTY AUTO",
    "ONGC": "NIFTY ENERGY",
    "RELIANCE": "NIFTY 50",
    "SBIN": "NIFTY BANK",
    "TCS": "NIFTY IT",
    "INFY": "NIFTY IT",
    "CDSL": "NIFTY 50",
    "DRREDDY": "NIFTY PHARMA",
    "JUBLFOOD": "NIFTY FMCG",
    "POWERGRID": "NIFTY PSU BANK",
    "SUNPHARMA": "NIFTY PHARMA",
    "DIVISLAB": "NIFTY PHARMA",
    "TECHM": "NIFTY IT",
    "HEROMOTOCO": "NIFTY AUTO",
    "HINDUNILVR": "NIFTY FMCG",
    "TATAPOWER": "NIFTY POWER",
    "TITAN": "NIFTY 50",
    "BOSCHLTD": "NIFTY AUTO",
    "BHARATFORGE": "NIFTY METAL",
    "GRASIM": "NIFTY METAL",
    "APLAPOLLO": "NIFTY 50",
    "RECLTD": "NIFTY PSU BANK",
    "PFC": "NIFTY PSU BANK",
    "GLENMARK": "NIFTY PHARMA",
    "TVSMOTOR": "NIFTY AUTO",
}

@cache_ttl(ttl=60)
def get_sector_index(symbol: str) -> str:
    """
    Return the NIFTY sector index for a given equity symbol.
    Defaults to 'NIFTY 50' if unknown.
    """
    return SECTOR_INDEX_MAP.get(symbol, "NIFTY 50")


@cache_ttl(ttl=60)
def get_intraday_change(symbol: str) -> float:
    """
    Compute intraday % change: (last_close - open_price)/open_price * 100.
    Falls back to daily % change if intraday data is unavailable or market is closed.
    """
    # Try intraday OHLC first
    try:
        df = fetch_intraday_ohlc(symbol)
        if not df.empty:
            open_price = df['open'].iloc[0]
            last_close = df['close'].iloc[-1]
            return float((last_close - open_price) / open_price * 100)
    except Exception:
        pass

    # Fallback: use last two daily closes
    try:
        daily = fetch_daily_ohlc(symbol, duration_days=2)
        if len(daily) >= 2:
            closes = daily['close']
            prev_close, last_close = closes.iloc[-2], closes.iloc[-1]
            return float((last_close - prev_close) / prev_close * 100)
    except Exception:
        pass

    return 0.0


@cache_ttl(ttl=60)
def get_sector_deviation(symbol: str) -> float:
    """
    Equity deviation from its sector index: equity_change - sector_change.
    """
    sec_idx = get_sector_index(symbol)
    equity_chg = get_intraday_change(symbol)
    sector_chg = get_intraday_change(sec_idx)
    return float(equity_chg - sector_chg)
