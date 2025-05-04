"""
dynamic_watchlist_lib/data_fetcher.py

Fetches market data and futures open interest using KiteConnect and Google Sheets for dynamic tokens.
"""

from typing import Optional, Dict
import pandas as pd
from kiteconnect import KiteConnect
from .config import (
    KITE_API_KEY,
    get_kite_access_token,
)
from .utils import cache_ttl, now_ist

def get_kite_client() -> KiteConnect:
    """Initialize and return a KiteConnect client with dynamic access token."""
    client = KiteConnect(api_key=KITE_API_KEY)
    token = get_kite_access_token()
    client.set_access_token(token)
    return client

@cache_ttl(ttl=600)
def get_instrument_map() -> Dict[str, int]:
    client = get_kite_client()
    instruments = client.instruments("NSE")
    return {inst["tradingsymbol"]: inst["instrument_token"] for inst in instruments}

@cache_ttl(ttl=60)
def fetch_intraday_ohlc(symbol: str, interval: str = "5minute", duration_days: int = 1) -> pd.DataFrame:
    client = get_kite_client()
    token_map = get_instrument_map()
    instrument_token = token_map.get(symbol)
    if instrument_token is None:
        ltp_data = client.ltp(f"NSE:{symbol}").get(f"NSE:{symbol}", {})
        instrument_token = ltp_data.get("instrument_token")
        if instrument_token is None:
            raise ValueError(f"Symbol {symbol} not found for OHLC fetch")

    to_ts = now_ist()
    from_ts = to_ts - pd.Timedelta(days=duration_days)
    data = client.historical_data(instrument_token, from_ts, to_ts, interval)
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")
    df.index = df.index.tz_localize("UTC").tz_convert("Asia/Kolkata")
    return df[["open", "high", "low", "close", "volume"]]

@cache_ttl(ttl=600)
def fetch_daily_ohlc(symbol: str, duration_days: int = 5) -> pd.DataFrame:
    client = get_kite_client()
    token_map = get_instrument_map()
    instrument_token = token_map.get(symbol)
    if instrument_token is None:
        ltp_data = client.ltp(f"NSE:{symbol}").get(f"NSE:{symbol}", {})
        instrument_token = ltp_data.get("instrument_token")
        if instrument_token is None:
            raise ValueError(f"Symbol {symbol} not found for daily OHLC fetch")

    to_ts = now_ist()
    from_ts = to_ts - pd.Timedelta(days=duration_days)
    data = client.historical_data(instrument_token, from_ts, to_ts, "day")
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df = df.set_index("date")
    return df[["open", "high", "low", "close", "volume"]]

@cache_ttl(ttl=30)
def fetch_futures_oi(symbol: str) -> Optional[int]:
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
