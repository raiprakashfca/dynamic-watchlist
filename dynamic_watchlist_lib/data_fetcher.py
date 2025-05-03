"""
Data fetchers for market data and news for dynamic_watchlist_lib.
"""
import pandas as pd
import requests
from kiteconnect import KiteConnect
from datetime import datetime

from .config import (
    KITE_API_KEY,
    KITE_API_SECRET,
    KITE_ACCESS_TOKEN,
    FT_NEWS_API_KEY,
    FT_NEWS_SEARCH_URL,
)
from .utils import cache_ttl, now_ist


def get_kite_client() -> KiteConnect:
    """
    Initialize and return a KiteConnect client using configured credentials.
    """
    kite = KiteConnect(api_key=KITE_API_KEY)
    kite.set_access_token(KITE_ACCESS_TOKEN)
    return kite


@cache_ttl(24 * 3600)
def get_instrument_map() -> dict[str, int]:
    """
    Fetch and cache mapping of NSE tradingsymbol to instrument_token.
    """
    kite = get_kite_client()
    instruments = kite.instruments(exchange="NSE")
    return {inst["tradingsymbol"]: inst["instrument_token"] for inst in instruments}


@cache_ttl(60)
def fetch_intraday_ohlc(symbol: str, interval: str = "5minute") -> pd.DataFrame:
    """
    Fetch recent intraday OHLC data for a given symbol.
    Returns a DataFrame indexed by timestamp (IST).
    """
    inst_map = get_instrument_map()
    token = inst_map.get(symbol)
    if not token:
        raise ValueError(f"Symbol {symbol} not found in instrument map")

    kite = get_kite_client()
    start = now_ist().replace(hour=9, minute=15, second=0, microsecond=0)
    end = now_ist()
    data = kite.historical(token, from_date=start, to_date=end, interval=interval)
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
    df.set_index("date", inplace=True)
    return df


@cache_ttl(86400)
def fetch_daily_ohlc(symbol: str) -> pd.DataFrame:
    """
    Fetch previous day OHLC data for a given symbol.
    """
    inst_map = get_instrument_map()
    token = inst_map.get(symbol)
    if not token:
        raise ValueError(f"Symbol {symbol} not found in instrument map")

    kite = get_kite_client()
    today = now_ist().date()
    yesterday = today - pd.Timedelta(days=1)
    data = kite.historical(token, from_date=yesterday, to_date=today, interval="day")
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
    df.set_index("date", inplace=True)
    return df


@cache_ttl(60)
def fetch_futures_oi(symbol: str) -> int | None:
    """
    Fetch real-time Futures Open Interest for the nearest futures contract of a given symbol.
    """
    inst_map = get_instrument_map()
    # Assumes symbol itself refers to a futures contract tradingsymbol
    token = inst_map.get(symbol)
    if not token:
        raise ValueError(f"Symbol {symbol} not found in instrument map")

    kite = get_kite_client()
    ltp_data = kite.ltp([token])
    token_data = ltp_data.get(str(token), {})
    return token_data.get("oi")


@cache_ttl(300)
def fetch_latest_news(query: str, count: int = 5) -> list[dict]:
    """
    Fetch latest news headlines from FT News API matching the query string.
    Returns a list of result dicts containing title, source, and timestamp.
    """
    if not FT_NEWS_API_KEY:
        return []

    headers = {"X-Api-Key": FT_NEWS_API_KEY, "Content-Type": "application/json"}
    payload = {
        "queryString": query,
        "resultContext": {"maxResults": count},
    }
    resp = requests.post(FT_NEWS_SEARCH_URL, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    # Extract and return simplified news items
    items = []
    for r in data.get("results", []):
        items.append({
            "title": r.get("title", {}).get("title"),
            "pubDate": r.get("lifecycle", {}).get("firstPublishedDateTime"),
            "source": r.get("location", {}).get("uri"),
        })
    return items


@cache_ttl(300)
def fetch_corporate_events(symbol: str) -> list[dict]:
    """
    Placeholder for corporate actions (dividends, results, ex-dates).
    FT API corporate endpoint can be integrated here.
    """
    # TODO: Integrate FT corporate actions API
    return []
