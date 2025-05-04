[![Python Tests](https://github.com/raiprakashfca/dynamic-watchlist/actions/workflows/python-tests.yml/badge.svg)](https://github.com/raiprakashfca/dynamic-watchlist/actions/workflows/python-tests.yml)

# Dynamic Watchlist

A Python library and Streamlit app for live intraday watchlists with support/resistance, VWAP, volume surges, sector deviations, and futures Open Interest.

## Features
- Monitor Support & Resistance levels via pivot points
- Intraday VWAP calculation
- Volume surge detection
- Sector deviation analysis against NIFTY indices
- Real-time Futures Open Interest
- Live FT News headlines and corporate events

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

### Library

```python
from dynamic_watchlist_lib import data_fetcher, metrics, sector_mapping, news_events
```

### Streamlit App

```bash
streamlit run streamlit_app/watchlist_dashboard.py
```

Ensure your `st.secrets` or environment variables contain:
```toml
Zerodha_API_Key = "YOUR_API_KEY"
Zerodha_API_Secret = "YOUR_API_SECRET"
GSHEET_CREDENTIALS_JSON = "YOUR_GOOGLE_SERVICE_ACCOUNT_JSON"
ZERODHA_SHEET_ID = "YOUR_SHEET_ID"
FT_News_API_Key = "YOUR_FT_NEWS_KEY"
FT_News_Endpoint = "YOUR_FT_NEWS_ENDPOINT"
```

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

MIT © 2025 Prakash Rai
