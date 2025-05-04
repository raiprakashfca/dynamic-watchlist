import os
import pytest

from dynamic_watchlist_lib.sector_mapping import (
    get_sector_index,
    get_intraday_change,
    get_sector_deviation,
)

# Skip live tests if credentials are missing
@pytest.fixture(autouse=True)
def require_credentials():
    if not os.getenv("Zerodha_API_Key") or not os.getenv("Zerodha_API_Secret"):
        pytest.skip("Missing Zerodha_API_Key/Secret; skipping live sector mapping tests")

LIVE_SYMBOL = "RELIANCE"

def test_get_sector_index_known():
    assert get_sector_index("RELIANCE") == "NIFTY 50"

def test_get_intraday_change_live():
    change = get_intraday_change(LIVE_SYMBOL)
    assert isinstance(change, float)

def test_get_sector_deviation_live():
    dev = get_sector_deviation(LIVE_SYMBOL)
    assert isinstance(dev, float)
