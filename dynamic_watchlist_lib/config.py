"""
dynamic_watchlist_lib/config.py

Centralized configuration for API keys and dynamic token loading.
Reads first from Streamlit secrets, then environment variables.
"""

import os
import json

# Try to import Streamlit secrets (in Cloud); otherwise use an empty dict
try:
    import streamlit as _st
    _SECRETS = _st.secrets
except ImportError:
    _SECRETS = {}

def _get_secret(name: str) -> str:
    """Look up a secret in st.secrets first, then environment variables."""
    return _SECRETS.get(name) or os.getenv(name, "")

# Kite Connect credentials
KITE_API_KEY    = _get_secret("Zerodha_API_Key")
KITE_API_SECRET = _get_secret("Zerodha_API_Secret")

# Google Sheet settings for dynamic Zerodha Access Token
GSHEET_CREDENTIALS_JSON = _get_secret("GSHEET_CREDENTIALS_JSON")
ZERODHA_SHEET_ID        = _get_secret("ZERODHA_SHEET_ID")

def get_kite_access_token() -> str:
    """
    Fetch the Zerodha Access Token from Google Sheet 'ZerodhaTokenStore'!C1,
    falling back to the environment variable if not configured.
    """
    creds_json = GSHEET_CREDENTIALS_JSON
    sheet_id = ZERODHA_SHEET_ID
    if creds_json and sheet_id:
        creds = json.loads(creds_json)
        import gspread
        client = gspread.service_account_from_dict(creds)
        sheet = client.open_by_key(sheet_id).worksheet("ZerodhaTokenStore")
        return sheet.acell("C1").value
    # Fallback to environment or secrets
    return _get_secret("Zerodha_Access_Token")

# Alias for easy import
KITE_ACCESS_TOKEN = get_kite_access_token()

# Timezone for all datetime operations
IST = "Asia/Kolkata"
