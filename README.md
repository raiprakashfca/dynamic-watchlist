# dynamic-watchlist

A Python library and Streamlit app for building a **dynamic intraday watchlist** of Indian equities with real‑time metrics:

* **Support & Resistance** via pivot‑point calculations
* **VWAP** (Volume‑Weighted Average Price)
* **Volume Surges** detection
* **Sector Deviation** vs. NIFTY sector indices
* **Futures Open Interest** (live)
* **Timestamped News & Corporate Events** (FT News, dividends, results, ex‑dates)

---

## 🚀 Features

1. **Modular Library (`dynamic_watchlist_lib`)**

   * Clean wrappers for Zerodha Kite Connect and FT News API
   * Calculators for VWAP, pivots, volume surges, sector deviation
   * Configurable caching and timezone‑aware utilities

2. **Streamlit Dashboard (`streamlit_app/watchlist_dashboard.py`)**

   * Select or add tickers on the fly
   * Auto‑refreshing wide‑format table of live metrics
   * Sidebar controls for watchlist management and refresh info

3. **Extensible**

   * Easily add new metrics or data sources (e.g., technical indicators)
   * Plug‑and‑play sector mapping and news/event fetchers

4. **Test Coverage**

   * Unit tests under `tests/` to validate data fetchers and calculations

---

## 📋 Prerequisites

* **Python** ≥ 3.8
* **Zerodha Kite Connect** credentials: API Key, API Secret, Access Token
* **Financial Times News API** key (optional; for news/events)

---

## 🔧 Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/raiprakashfca/dynamic-watchlist.git
   cd dynamic-watchlist
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

3. Configure your API credentials in Streamlit secrets or environment variables:

   ```toml
   [secrets]
   Zerodha_API_Key = "<your_api_key>"
   Zerodha_API_Secret = "<your_api_secret>"
   Zerodha_Access_Token = "<your_access_token>"

   # (Optional) Financial Times News API
   FT_News_API_Key = "<your_ft_key>"
   ```

---

## ▶️ Usage

### As a Python Library

```python
from dynamic_watchlist_lib.data_fetcher import fetch_intraday_ohlc
from dynamic_watchlist_lib.metrics import calculate_vwap, calculate_pivot, detect_volume_surge

# Example:
token = 123456
df = fetch_intraday_ohlc(token)
vwap = calculate_vwap(df)
```

### Run the Streamlit Dashboard

```bash
streamlit run streamlit_app/watchlist_dashboard.py
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes
4. Run tests: `pytest`
5. Open a pull request

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
