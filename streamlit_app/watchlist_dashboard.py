import streamlit as st

# Set page config must be first Streamlit command
st.set_page_config(page_title="Dynamic Watchlist", layout="wide")
st.title("📊 Dynamic Watchlist Dashboard")

import pandas as pd
from utils_streamlit import display_metrics

from dynamic_watchlist_lib import (
    fetch_intraday_ohlc,
    fetch_futures_oi,
    calculate_vwap,
    calculate_pivots,
    detect_volume_surge,
    get_sector_deviation,
)
from dynamic_watchlist_lib.utils import now_ist

# Sidebar for ticker selection
st.sidebar.header("Watchlist Settings")
symbols = st.sidebar.text_area(
    "Enter NSE symbols (comma-separated)",
    value=(
        "ASIANPAINT,BAJAJ-AUTO,BANKBARODA,BPCL,CIPLA,COALINDIA,ICICIBANK,ITC,"
        "JSWSTEEL,LT,MARUTI,ONGC,RELIANCE,SBIN,TCS,INFY,CDSL,DRREDDY,JUBLFOOD,"
        "POWERGRID,SUNPHARMA,DIVISLAB,TECHM,HEROMOTOCO,HINDUNILVR,TATAPOWER,"
        "TITAN,BOSCHLTD,BHARATFORGE,GRASIM,APLAPOLLO,RECLTD,PFC,GLENMARK,TVSMOTOR"
    ),
    height=200
)
symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]

# Show last update time
st.sidebar.write("Last update (IST):", now_ist().strftime("%Y-%m-%d %H:%M:%S"))

# Build metrics table
rows = []
for sym in symbol_list:
    try:
        df = fetch_intraday_ohlc(sym)
        vwap = calculate_vwap(df)
        pivots = calculate_pivots(df)
        surge = detect_volume_surge(df)
        dev = get_sector_deviation(sym)
        oi = fetch_futures_oi(sym)

        rows.append({
            "Symbol": sym,
            "VWAP": round(vwap, 2),
            "Pivot": round(pivots["pivot"], 2),
            "R1": round(pivots["r1"], 2),
            "S1": round(pivots["s1"], 2),
            "Volume_Surge": surge,
            "Sector_Dev(%)": round(dev, 2),
            "Futures_OI": oi if oi is not None else "-",
        })
    except Exception as e:
        rows.append({"Symbol": sym, "Error": str(e)})

df_metrics = pd.DataFrame(rows)
display_metrics(df_metrics)
