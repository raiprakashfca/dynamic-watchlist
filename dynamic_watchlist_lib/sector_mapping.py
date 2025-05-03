"""
Module to map stocks to their NIFTY sector indices and calculate intraday deviation.
"""
from typing import Dict
from .data_fetcher import fetch_intraday_ohlc
from .utils import cache_ttl

# Mapping of equity symbols to their NIFTY sector index symbols
SECTOR_INDEX_MAP: Dict[str, str] = {
    # Auto Sector
    "BAJAJ-AUTO": "NIFTY AUTO",
    "HEROMOTOCO": "NIFTY AUTO",
    "MARUTI": "NIFTY AUTO",
    "TVSMOTOR": "NIFTY AUTO",
    "BOSCHLTD": "NIFTY AUTO",
    "APLLTD": "NIFTY AUTO",  # Apollo Tyres

    # Banking Sector
    "ICICIBANK": "NIFTY BANK",
    "SBIN": "NIFTY BANK",
    "BANKBARODA": "NIFTY BANK",

    # Oil & Gas Sector
    "BPCL": "NIFTY OIL & GAS",
    "ONGC": "NIFTY OIL & GAS",

    # Pharma Sector
    "CIPLA": "NIFTY PHARMA",
    "SUNPHARMA": "NIFTY PHARMA",
    "DIVISLAB": "NIFTY PHARMA",
    "DRREDDY": "NIFTY PHARMA",
    "GLENMARK": "NIFTY PHARMA",

    # IT Sector
    "TCS": "NIFTY IT",
    "INFY": "NIFTY IT",
    "TECHM": "NIFTY IT",

    # FMCG Sector
    "ITC": "NIFTY FMCG",
    "HINDUNILVR": "NIFTY FMCG",
    "ASIANPAINT": "NIFTY FMCG",

    # Infrastructure & Capital Goods
    "LT": "NIFTY INFRASTRUCTURE",
    "GRASIM": "NIFTY INFRASTRUCTURE",
    "POWERGRID": "NIFTY INFRASTRUCTURE",
    "RELIANCE": "NIFTY 50",  # fallback to broad index
    "TITAN": "NIFTY 50",    # fallback

    # Others (fallback to NIFTY 50)
    "JSWSTEEL": "NIFTY METAL",
    "COALINDIA": "NIFTY METAL",
    "PFC": "NIFTY FINANCIAL SERVICES",
    "RECLTD": "NIFTY FINANCIAL SERVICES",
    "CDSL": "NIFTY FINANCIAL SERVICES",
    "JUBLFOOD": "NIFTY 50",
    "CIPLA": "NIFTY PHARMA",
    "DRREDDY": "NIFTY PHARMA",
    "DIVISLAB": "NIFTY PHARMA",
}

DEFAULT_SECTOR = "NIFTY 50"


@cache_ttl(60)
def get_sector_index(symbol: str) -> str:
    """
    Return the NIFTY sector index symbol for a given equity symbol.
    Defaults to 'NIFTY 50' if unmapped.
    """
    return SECTOR_INDEX_MAP.get(symbol, DEFAULT_SECTOR)


@cache_ttl(60)
def get_intraday_change(symbol: str) -> float:
    """
    Calculate percent change from first to last intraday close for a symbol.
    """
    df = fetch_intraday_ohlc(symbol)
    if df.empty:
        return 0.0
    first = df["close"].iloc[0]
    last = df["close"].iloc[-1]
    return (last - first) / first * 100


@cache_ttl(60)
def get_sector_deviation(symbol: str) -> float:
    """
    Compute relative intraday performance: equity change minus sector index change.
    Positive = outperforming; Negative = underperforming.
    """
    sector = get_sector_index(symbol)
    equity_change = get_intraday_change(symbol)
    sector_change = get_intraday_change(sector)
    return equity_change - sector_change
