"""
dynamic_watchlist_lib/utils.py

Utility functions: datetime conversion and caching.
"""

import time
from typing import Any, Callable
import functools
import datetime
import pytz

from .config import IST

# Timezone object for IST
TZ = pytz.timezone(IST)

def now_ist() -> datetime.datetime:
    """Return current datetime in IST timezone."""
    return datetime.datetime.now(tz=TZ)

def to_ist(dt: datetime.datetime) -> datetime.datetime:
    """Convert a datetime (naive or with tzinfo) to IST timezone."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.utc)
    return dt.astimezone(TZ)

def cache_ttl(ttl: int):
    """
    Decorator to cache function results for ttl seconds.
    """
    def decorator(func: Callable[..., Any]):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now_ts = time.time()
            if key in cache:
                ts, value = cache[key]
                if now_ts - ts < ttl:
                    return value
            result = func(*args, **kwargs)
            cache[key] = (now_ts, result)
            return result
        return wrapper
    return decorator
