import streamlit as st
import pandas as pd

# Import our UI helper from the same folder
from utils_streamlit import display_metrics

# Core library imports
from dynamic_watchlist_lib import (
    fetch_intraday_ohlc,
    fetch_futures_oi,
    calculate_vwap,
    calculate_pivots,
    detect_volume_surge,
    get_sector_deviation,
)
from dynamic_watchlist_lib.utils import now_ist

# Page config
st.set_page_config(page_title="Dynamic Watchlist", layout="wide")
st.title("📊 Dynamic Watchlist Dashboard")

# Sidebar: ticker input
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

# Show last update time
st.sidebar.write("Last update (IST):", now_ist().strftime("%Y-%m-%d %H:%M:%S"))

# Build the metrics table
data = []
for sym in symbol_list:
    try:
        df = fetch_intraday_ohlc(sym)
        vwap = calculate_vwap(df)
        pivots = calculate_pivots(df)
        surge = detect_volume_surge(df)
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

# Display with our styled helper
display_metrics(df_metrics)
