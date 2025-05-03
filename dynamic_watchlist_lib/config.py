"""
Configuration module for dynamic_watchlist_lib.
Reads static API keys and dynamically fetches Zerodha Access Token from Google Sheet.
"""
import os
import json
import gspread

# Static Zerodha credentials (API Key & Secret)
KITE_API_KEY = os.getenv("Zerodha_API_Key", "")
KITE_API_SECRET = os.getenv("Zerodha_API_Secret", "")

# Google Sheet settings for dynamic Access Token
# GSHEET_CREDENTIALS_JSON: JSON string of service account creds
# ZERODHA_SHEET_ID: Google Sheet ID for 'ZerodhaTokenStore'
GSHEET_CREDENTIALS_JSON = os.getenv("GSHEET_CREDENTIALS_JSON", "")
ZERODHA_SHEET_ID = os.getenv("ZERODHA_SHEET_ID", "")


def get_kite_access_token() -> str:
    """
    Fetch the Zerodha Access Token from Google Sheet 'ZerodhaTokenStore'!C1,
    falling back to the environment variable if not configured.
    """
    # Try Google Sheets first
    if GSHEET_CREDENTIALS_JSON and ZERODHA_SHEET_ID:
        creds_dict = json.loads(GSHEET_CREDENTIALS_JSON)
        client = gspread.service_account_from_dict(creds_dict)
        sheet = client.open_by_key(ZERODHA_SHEET_ID).worksheet("ZerodhaTokenStore")
        token = sheet.acell("C1").value
        if token:
            return token.strip()
    # Fallback to env var
    return os.getenv("Zerodha_Access_Token", "")

# Use dynamic fetch
KITE_ACCESS_TOKEN = get_kite_access_token()

# Financial Times API key
FT_NEWS_API_KEY = os.getenv("FT_News_API_Key", "")

# API endpoints
FT_NEWS_SEARCH_URL = "https://api.ft.com/content/search/v1"

# Timezone constant
timezone = "Asia/Kolkata"
