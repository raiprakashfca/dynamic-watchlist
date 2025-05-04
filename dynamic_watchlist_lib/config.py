"""
dynamic_watchlist_lib/config.py

Centralized configuration for API keys, endpoints, and dynamic token loading.
"""

import os
import json
import gspread

# Kite Connect credentials
KITE_API_KEY = os.getenv("Zerodha_API_Key", "")
KITE_API_SECRET = os.getenv("Zerodha_API_Secret", "")

# FT News API configuration
FT_NEWS_API_KEY = os.getenv("FT_News_API_Key", "")
FT_NEWS_ENDPOINT = os.getenv("FT_News_Endpoint", "")

# Google Sheet settings for dynamic Zerodha Access Token
GSHEET_CREDENTIALS_JSON = os.getenv("GSHEET_CREDENTIALS_JSON", "")
ZERODHA_SHEET_ID = os.getenv("ZERODHA_SHEET_ID", "")

def get_kite_access_token() -> str:
    """
    Fetch the Zerodha Access Token from Google Sheet 'ZerodhaTokenStore'!C1,
    falling back to the environment variable if not configured.
    """
    if GSHEET_CREDENTIALS_JSON and ZERODHA_SHEET_ID:
        creds = json.loads(GSHEET_CREDENTIALS_JSON)
        client = gspread.service_account_from_dict(creds)
        sheet = client.open_by_key(ZERODHA_SHEET_ID).worksheet("ZerodhaTokenStore")
        return sheet.acell("C1").value
    return os.getenv("Zerodha_Access_Token", "")

# Timezone for all datetime operations
IST = "Asia/Kolkata"
