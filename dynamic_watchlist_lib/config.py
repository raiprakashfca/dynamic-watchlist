"""
dynamic_watchlist_lib/config.py

Centralized configuration for API keys and dynamic token loading.
Reads secrets lazily to avoid StreamlitSetPageConfigMustBeFirstCommandError.
"""

import os
import json

def _get_secret(name: str) -> str:
    """Retrieve secret from Streamlit secrets or environment variables."""
    try:
        import streamlit as _st
        val = _st.secrets.get(name)
        if val:
            return val
    except Exception:
        pass
    return os.getenv(name, "")

# Kite Connect credentials
KITE_API_KEY    = _get_secret("Zerodha_API_Key")
KITE_API_SECRET = _get_secret("Zerodha_API_Secret")

# Google Sheet settings for dynamic Zerodha Access Token
GSHEET_CREDENTIALS_JSON = _get_secret("GSHEET_CREDENTIALS_JSON")
ZERODHA_SHEET_ID        = _get_secret("ZERODHA_SHEET_ID")

# Timezone for datetime operations
IST = "Asia/Kolkata"

def get_kite_access_token() -> str:
    """
    Fetch the Zerodha Access Token from Google Sheet 'ZerodhaTokenStore'!C1,
    falling back to the 'Zerodha_Access_Token' secret or environment var.
    """
    if GSHEET_CREDENTIALS_JSON and ZERODHA_SHEET_ID:
        creds = json.loads(GSHEET_CREDENTIALS_JSON)
        import gspread
        client = gspread.service_account_from_dict(creds)
        sheet = client.open_by_key(ZERODHA_SHEET_ID).worksheet("ZerodhaTokenStore")
        return sheet.acell("C1").value
    # Fallback to direct secret/ENV
    return _get_secret("Zerodha_Access_Token")
