"""
Futures Module

This module provides functions for pricing and related 
calculations for futures contracts.
"""

from finm.futures.pricing import (
    calc_futures_implied_rate,
    calc_futures_price_from_rate,
    calc_futures_pnl,
)

__all__ = [
    # from finm.futures.pricing
    "calc_futures_implied_rate",
    "calc_futures_price_from_rate",
    "calc_futures_pnl",
]
