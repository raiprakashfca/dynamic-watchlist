"""
Configuration module for dynamic_watchlist_lib.
Reads API keys and endpoints from environment variables.
"""
import os

# Zerodha Kite Connect credentials
KITE_API_KEY = os.getenv("Zerodha_API_Key", "")
KITE_API_SECRET = os.getenv("Zerodha_API_Secret", "")
KITE_ACCESS_TOKEN = os.getenv("Zerodha_Access_Token", "")

# Financial Times API key
FT_NEWS_API_KEY = os.getenv("FT_News_API_Key", "")

# API endpoints
FT_NEWS_SEARCH_URL = "https://api.ft.com/content/search/v1"

# Timezone constant
timezone = "Asia/Kolkata"
