"""
Dynamic Watchlist Library

Exposes core modules for data fetching, metrics calculations, sector mapping, and news/events.
"""
__version__ = "0.1.0"

from .config import KITE_API_KEY, KITE_API_SECRET, KITE_ACCESS_TOKEN, FT_NEWS_API_KEY
from .data_fetcher import (
    get_kite_client,
    get_instrument_map,
    fetch_intraday_ohlc,
    fetch_daily_ohlc,
    fetch_futures_oi,
    fetch_latest_news,
    fetch_corporate_events,
)
from .metrics import calculate_vwap, calculate_pivots, detect_volume_surge
from .sector_mapping import get_sector_index, get_intraday_change, get_sector_deviation
from .news_events import get_recent_news, get_corporate_actions, get_news_and_events
from .utils import now_ist, to_ist, cache_ttl
