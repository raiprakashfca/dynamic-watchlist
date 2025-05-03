"""
News and corporate events fetchers for dynamic_watchlist_lib.
Provides combined news headlines and corporate actions for a given symbol.
"""
from typing import List, Dict
from .data_fetcher import fetch_latest_news, fetch_corporate_events
from .utils import cache_ttl, to_ist


@cache_ttl(300)
def get_recent_news(symbol: str, count: int = 5) -> List[Dict]:
    """
    Returns a list of recent news items for the given symbol.
    Each item contains: title, pubDate (IST), source URL.
    """
    raw = fetch_latest_news(symbol, count)
    news = []
    for item in raw:
        # Convert publication time to IST
        pub = item.get("pubDate")
        try:
            dt = to_ist(pd.to_datetime(pub))  # relying on pandas to parse
        except Exception:
            dt = None
        news.append({
            "title": item.get("title"),
            "pubDate": dt,
            "source": item.get("source"),
        })
    return news


@cache_ttl(3600)
def get_corporate_actions(symbol: str) -> List[Dict]:
    """
    Returns a list of upcoming corporate actions for the given symbol.
    Each item might include: type (Dividend, Result, Ex-Date), date, details.
    """
    raw = fetch_corporate_events(symbol)
    # Raw stub returns empty; this function formats real events when available
    events = []
    for ev in raw:
        # Expected keys: ev["type"], ev["date"], ev["details"]
        events.append({
            "type": ev.get("type"),
            "date": to_ist(pd.to_datetime(ev.get("date"))) if ev.get("date") else None,
            "details": ev.get("details"),
        })
    return events


@cache_ttl(300)
def get_news_and_events(symbol: str, count: int = 5) -> Dict[str, List[Dict]]:
    """
    Combined fetcher: returns both news and corporate actions.
    """
    return {
        "news": get_recent_news(symbol, count),
        "events": get_corporate_actions(symbol),
    }
