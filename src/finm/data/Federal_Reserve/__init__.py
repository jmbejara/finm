"""
Data module - Federal Reserve

This module provides functions for pulling, loading, and cleaning data.
"""

from finm.data.Federal_Reserve.pull_yield_curve_data import (
    pull_fed_yield_curve,
    load_fed_yield_curve_all,
    load_fed_yield_curve,
)

__all__ = [
    "pull_fed_yield_curve",
    "load_fed_yield_curve_all",
    "load_fed_yield_curve",
]
