"""Data module - Federal Reserve.

This module provides functions for pulling, loading, and cleaning Federal Reserve data.
"""

from finm.data.federal_reserve.pull_yield_curve_data import (
    load_fed_yield_curve,
    load_fed_yield_curve_all,
    pull_fed_yield_curve,
)

__all__ = [
    "pull_fed_yield_curve",
    "load_fed_yield_curve_all",
    "load_fed_yield_curve",
]
