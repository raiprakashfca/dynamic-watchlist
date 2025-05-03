import streamlit as st
import pandas as pd
from dynamic_watchlist_lib.data_fetcher import (
    get_instrument_map,
    fetch_intraday_ohlc,
    fetch_daily_ohlc,
    fetch_futures_oi,
)
from dynamic_watchlist_lib.metrics import (
    calculate_vwap,
    calculate_pivots,
    detect_volume_surge,
)
from dynamic_watchlist_lib.sector_mapping import get_sector_deviation
from dynamic_watchlist_lib.news_events import get_recent_news, get_corporate_actions
from dynamic_watchlist_lib.utils import now_ist
from streamlit_app.utils_streamlit import display_metrics

# Page config
st.set_page_config(page_title="Dynamic Watchlist", layout="wide")
st.title("📊 Dynamic Intraday Watchlist")

# Sidebar: Watchlist control
st.sidebar.header("Watchlist Settings")
instrument_map = get_instrument_map()
all_symbols = sorted(instrument_map.keys())

# Default symbols
default_symbols = [
    "ASIANPAINT", "BAJAJ-AUTO", "BANKBARODA", "BPCL", "CIPLA",
    "COALINDIA", "ICICIBANK", "ITC", "JSWSTEEL", "LT", "MARUTI",
    "ONGC", "RELIANCE", "SBIN", "TCS", "INFY", "CDSL", "DRREDDY",
    "JUBLFOOD", "POWERGRID", "SUNPHARMA", "DIVISLAB", "TECHM",
    "HEROMOTOCO", "HINDUNILVR", "TATAPOWER", "TITAN", "BOSCHLTD",
    "BHARATFORGE", "GRASIM", "APLLTD", "RECLTD", "PFC", "GLENMARK",
    "TVSMOTOR"
]

# Multi-select widget for watchlist
selected = [s for s in default_symbols if s in all_symbols]
watchlist = st.sidebar.multiselect(
    "Select stocks to monitor", all_symbols, default=selected
)
new_sym = st.sidebar.text_input("Add new symbol (exact)")
if st.sidebar.button("Add to Watchlist"):
    sym = new_sym.strip().upper()
    if sym and sym in all_symbols and sym not in watchlist:
        watchlist.append(sym)
        st.sidebar.success(f"{sym} added!")
    elif sym and sym not in all_symbols:
        st.sidebar.error(f"{sym} not found in instrument map")

# Last update timestamp
st.sidebar.markdown(f"**Last update:** {now_ist().strftime('%d-%b-%Y %H:%M:%S')} IST")

# Build metrics rows
data_rows = []
for sym in watchlist:
    try:
        df_intra = fetch_intraday_ohlc(sym)
        df_day = fetch_daily_ohlc(sym)
        vwap = calculate_vwap(df_intra)
        pivot, r1, r2, s1, s2 = calculate_pivots(df_day)
        surge = detect_volume_surge(df_intra)
        sect_dev = get_sector_deviation(sym)
        fut_oi = fetch_futures_oi(sym)
        ltp = float(df_intra['close'].iloc[-1]) if not df_intra.empty else None
        data_rows.append({
            'Symbol': sym,
            'LTP': ltp,
            'VWAP': vwap,
            'Pivot': pivot,
            'S1': s1,
            'S2': s2,
            'R1': r1,
            'R2': r2,
            'Vol Surge': surge,
            'Sector Dev (%)': sect_dev,
            'Fut OI': fut_oi,
        })
    except Exception as e:
        data_rows.append({'Symbol': sym, 'Error': str(e)})

# Display metrics table with consistent styling
metrics_df = pd.DataFrame(data_rows).set_index('Symbol')
display_metrics(metrics_df)

# News & Corporate Events section
news_count = st.sidebar.slider(
    "Number of news headlines", min_value=1, max_value=10, value=5
)
st.markdown("---")
st.header("News & Corporate Events")
for sym in watchlist:
    with st.expander(f"{sym}"):
        news = get_recent_news(sym, count=news_count)
        if news:
            st.subheader("News")
            dfn = pd.DataFrame(news)
            dfn['pubDate'] = dfn['pubDate'].dt.strftime('%d-%b-%Y %H:%M:%S')
            st.table(dfn.rename(columns={'pubDate':'Published'}))
        else:
            st.write("No recent news.")

        events = get_corporate_actions(sym)
        if events:
            st.subheader("Corporate Actions")
            dfe = pd.DataFrame(events)
            dfe['date'] = dfe['date'].dt.strftime('%d-%b-%Y')
            st.table(dfe)
        else:
            st.write("No upcoming corporate events.")
