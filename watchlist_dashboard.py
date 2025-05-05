import streamlit as st

# ─── FIRST STREAMLIT CALL ────────────────────────────────────────────────────────
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

# ─── Sidebar Inputs ────────────────────────────────────────────────────────────
st.sidebar.header("Watchlist Settings")
symbols = st.sidebar.text_area(
    "Enter NSE symbols (comma-separated)",
    value=(
        "ASIANPAINT,BAJAJ-AUTO,BANKBARODA,BPCL,...,TVSMOTOR"
    ),
    height=200,
)
symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]

st.sidebar.write("Last update (IST):", now_ist().strftime("%Y-%m-%d %H:%M:%S"))

# ─── Build & Display Metrics ────────────────────────────────────────────────────
rows = []
for sym in symbol_list:
    try:
        df = fetch_intraday_ohlc(sym)
        rows.append({
            "Symbol": sym,
            "VWAP": round(calculate_vwap(df), 2),
            **{k: round(v, 2) for k, v in calculate_pivots(df).items()},
            "Volume_Surge": detect_volume_surge(df),
            "Sector_Dev(%)": round(get_sector_deviation(sym), 2),
            "Futures_OI": fetch_futures_oi(sym) or "-",
        })
    except Exception as e:
        rows.append({"Symbol": sym, "Error": str(e)})

df_metrics = pd.DataFrame(rows)
display_metrics(df_metrics)
