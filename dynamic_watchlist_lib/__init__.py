"""
dynamic_watchlist_lib/__init__.py

Package initialization.
"""

from .config import KITE_API_KEY, KITE_API_SECRET, KITE_ACCESS_TOKEN, IST
from .utils import cache_ttl, now_ist
from .data_fetcher import (
    get_kite_client,
    get_instrument_map,
    fetch_intraday_ohlc,
    fetch_daily_ohlc,
    fetch_futures_oi,
)
from .sector_mapping import get_sector_index, get_intraday_change, get_sector_deviation
from .metrics import calculate_vwap, calculate_pivots, detect_volume_surge

__version__ = "0.1.0"
