"""
dynamic_watchlist_lib/data_fetcher.py

Fetches market data, futures open interest, and FT News headlines using KiteConnect and Google Sheets for dynamic tokens.
"""

from typing import Optional, Dict
import json
import gspread
import requests
import pandas as pd
from kiteconnect import KiteConnect
from .config import (
    KITE_API_KEY,
    KITE_API_SECRET,
    KITE_ACCESS_TOKEN,
    FT_NEWS_API_KEY,
    FT_NEWS_ENDPOINT,
    GSHEET_CREDENTIALS_JSON,
    ZERODHA_SHEET_ID,
)
from .utils import cache_ttl, now_ist


def get_kite_client() -> KiteConnect:
    """Initialize and return a KiteConnect client with dynamic access token."""
    client = KiteConnect(api_key=KITE_API_KEY)
    client.set_access_token(KITE_ACCESS_TOKEN)
    return client


@cache_ttl(ttl=600)
def get_instrument_map() -> Dict[str, int]:
    """
    Fetch and return a mapping from NSE trading symbols to instrument tokens.
    """
    client = get_kite_client()
    instruments = client.instruments("NSE")
    return {inst["tradingsymbol"]: inst["instrument_token"] for inst in instruments}


@cache_ttl(ttl=60)
def fetch_intraday_ohlc(symbol: str, interval: str = "5minute", duration_days: int = 1) -> pd.DataFrame:
    """
    Fetch intraday OHLC for a given symbol.
    Returns a DataFrame indexed by IST datetime with columns ['open', 'high', 'low', 'close', 'volume'].
    """
    token_map = get_instrument_map()
    instrument_token = token_map.get(symbol)
    if instrument_token is None:
        raise ValueError(f"Symbol {symbol} not found in instrument map")
    to_ts = now_ist()
    from_ts = to_ts - pd.Timedelta(days=duration_days)
    data = get_kite_client().historical_data(instrument_token, from_ts, to_ts, interval)
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")
    df.index = df.index.tz_localize("UTC").tz_convert("Asia/Kolkata")
    return df[["open", "high", "low", "close", "volume"]]


@cache_ttl(ttl=600)
def fetch_daily_ohlc(symbol: str, duration_days: int = 5) -> pd.DataFrame:
    """
    Fetch daily OHLC for a given symbol for the past duration_days.
    """
    token_map = get_instrument_map()
    instrument_token = token_map.get(symbol)
    if instrument_token is None:
        raise ValueError(f"Symbol {symbol} not found in instrument map")
    to_ts = now_ist()
    from_ts = to_ts - pd.Timedelta(days=duration_days)
    data = get_kite_client().historical_data(instrument_token, from_ts, to_ts, "day")
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df = df.set_index("date")
    return df[["open", "high", "low", "close", "volume"]]


@cache_ttl(ttl=30)
def fetch_futures_oi(symbol: str) -> Optional[int]:
    """
    Fetch the current open interest for the nearest futures contract of the given symbol.
    Returns None if not available.
    """
    client = get_kite_client()
    instruments = client.instruments("NSE")
    futures = [
        inst for inst in instruments
        if inst.get("tradingsymbol", "").startswith(symbol) and inst.get("segment") == "NFO-FUT"
    ]
    if not futures:
        return None
    futures.sort(key=lambda x: pd.to_datetime(x.get("expiry")))
    nearest = futures[0]
    ltp = client.ltp(f"NSE:{nearest['tradingsymbol']}").get(f"NSE:{nearest['tradingsymbol']}", {})
    return ltp.get("oi")


@cache_ttl(ttl=300)
def fetch_latest_news(count: int = 5) -> list[dict]:
    """
    Fetch the latest FT News headlines.
    """
    if not FT_NEWS_API_KEY or not FT_NEWS_ENDPOINT:
        return []
    response = requests.get(
        FT_NEWS_ENDPOINT,
        params={"apiKey": FT_NEWS_API_KEY, "count": count},
        timeout=10,
    )
    if response.status_code != 200:
        return []
    data = response.json()
    return data.get("articles", [])


@cache_ttl(ttl=300)
def fetch_corporate_events(symbol: str) -> list[dict]:
    """
    Stub - fetch corporate actions for symbol.
    """
    # Placeholder for future FT endpoint integration
    return []
