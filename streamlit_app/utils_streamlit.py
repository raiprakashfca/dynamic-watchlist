"""
Streamlit UI helper functions for styling and displaying tables in the watchlist dashboard.
"""
import pandas as pd
import streamlit as st

def style_metrics(df):
    """
    Apply styling to the metrics DataFrame:
    - Highlight volume surge rows
    - Color-code sector deviation (green for outperform, red for underperform)
    - Format numeric columns to 2 decimal places
    """
    # Highlight volume surge in yellow background
    def highlight_surge(val):
        return 'background-color: yellow' if val else ''

    # Color code sector deviation
    def color_sector(val):
        try:
            return 'color: green' if val > 0 else 'color: red'
        except:
            return ''

    # Define formatting for numeric columns
    fmt = {col: '{:.2f}' for col in df.select_dtypes(include=['float']).columns}

    styler = df.style.format(fmt)
    if 'Volume_Surge' in df.columns:
        styler = styler.applymap(highlight_surge, subset=['Volume_Surge'])
    if 'Sector_Dev(%)' in df.columns:
        styler = styler.applymap(color_sector, subset=['Sector_Dev(%)'])

    return styler

def display_metrics(df):
    """
    Render the styled metrics DataFrame in Streamlit.
    """
    styled = style_metrics(df)
    st.dataframe(styled, use_container_width=True)
