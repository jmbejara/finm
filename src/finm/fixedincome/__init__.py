"""
Fixed Income Module

This module provides functions for fixed income calculations including
bond pricing, yield calculations, and risk measures.
"""

from finm.fixedincome.bonds import (
    present_value,
    future_value,
    yield_to_maturity,
    bond_price,
    duration,
    modified_duration,
    convexity,
    get_coupon_dates,
)

__all__ = [
    "present_value",
    "future_value",
    "yield_to_maturity",
    "bond_price",
    "duration",
    "modified_duration",
    "convexity",
    "get_coupon_dates",
]

