"""
Utility functions for dynamic_watchlist_lib.
Consistent timezone handling (IST) and common helpers.
"""
import os
import time
from functools import wraps
from datetime import datetime, timedelta
import pytz
from .config import timezone as TZ

# IST timezone object
IST = pytz.timezone(TZ)


def now_ist() -> datetime:
    """
    Returns the current datetime in IST timezone.
    """
    return datetime.now(IST)


def to_ist(dt: datetime) -> datetime:
    """
    Convert a UTC or naive datetime to IST timezone.
    """
    if dt.tzinfo is None:
        # assume dt is UTC if naive
        dt = dt.replace(tzinfo=pytz.utc)
    return dt.astimezone(IST)


def cache_ttl(ttl_seconds: int):
    """
    Decorator to cache function results for a given TTL (in seconds).
    """
    def decorator(fn):
        cache = {}

        @wraps(fn)
        def wrapped(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            result, timestamp = cache.get(key, (None, None))
            now = time.time()
            if result is None or (now - timestamp) > ttl_seconds:
                result = fn(*args, **kwargs)
                cache[key] = (result, now)
            return result

        return wrapped

    return decorator
