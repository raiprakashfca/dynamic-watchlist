import os
import sys
from dynamic_watchlist_lib.config import KITE_API_KEY, KITE_ACCESS_TOKEN
st.sidebar.write("🔑 API key loaded?", bool(KITE_API_KEY))
st.sidebar.write("🗝️ Access token loaded?", bool(KITE_ACCESS_TOKEN))

# Ensure the streamlit_app directory is on the path so we can import utils_streamlit
sys.path.append(os.path.dirname(__file__))

import streamlit as st
import pandas as pd

from dynamic_watchlist_lib import (
    fetch_intraday_ohlc,
    fetch_futures_oi,
    calculate_vwap,
    calculate_pivots,
    detect_volume_surge,
    get_sector_deviation,
)
from dynamic_watchlist_lib.utils import now_ist
from utils_streamlit import display_metrics

st.set_page_config(page_title="Dynamic Watchlist", layout="wide")
st.title("📊 Dynamic Watchlist Dashboard")

# Sidebar for ticker selection
st.sidebar.header("Watchlist Settings")
symbols = st.sidebar.text_area(
    "Enter NSE symbols (comma-separated)",
    value="ASIANPAINT,BAJAJ-AUTO,BANKBARODA,BPCL,CIPLA,COALINDIA,ICICIBANK,ITC,JSWSTEEL,"
          "LT,MARUTI,ONGC,RELIANCE,SBIN,TCS,INFY,CDSL,DRREDDY,JUBLFOOD,POWERGRID,"
          "SUNPHARMA,DIVISLAB,TECHM,HEROMOTOCO,HINDUNILVR,TATAPOWER,TITAN,BOSCHLTD,"
          "BHARATFORGE,GRASIM,APLAPOLLO,RECLTD,PFC,GLENMARK,TVSMOTOR",
    height=200
)
symbol_list = [sym.strip().upper() for sym in symbols.split(",") if sym.strip()]

st.sidebar.write("Last update (IST):", now_ist().strftime("%Y-%m-%d %H:%M:%S"))

# Build DataFrame of metrics
data = []
for sym in symbol_list:
    try:
        df_intraday = fetch_intraday_ohlc(sym)
        vwap = calculate_vwap(df_intraday)
        pivots = calculate_pivots(df_intraday)
        surge = detect_volume_surge(df_intraday)
        deviation = get_sector_deviation(sym)
        oi = fetch_futures_oi(sym)

        data.append({
            "Symbol": sym,
            "VWAP": round(vwap, 2),
            "Pivot": round(pivots["pivot"], 2),
            "R1": round(pivots["r1"], 2),
            "S1": round(pivots["s1"], 2),
            "Volume_Surge": surge,
            "Sector_Dev(%)": round(deviation, 2),
            "Futures_OI": oi if oi is not None else "-",
        })
    except Exception as e:
        data.append({
            "Symbol": sym,
            "Error": str(e)
        })

df_metrics = pd.DataFrame(data)

# Display the styled table
display_metrics(df_metrics)
