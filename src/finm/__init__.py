"""
finm - Financial Mathematics Python Package

A student-led Python package for financial mathematics and quantitative finance
education, created by students and educators at the University of Chicago
Financial Mathematics program.

⚠️  DISCLAIMER: This package is for learning purposes only. There are likely
errors and this should NOT be used for any purposes beyond education and research.
"""

from finm.fixedincome import (
    present_value,
    future_value,
    yield_to_maturity,
    bond_price,
    duration,
    modified_duration,
    convexity,
    get_coupon_dates,
    filter_treasury_cashflows,
    calc_cashflows,
    plot_spot_curve,
    spot,
    discount,
    predict_prices,
    fit,
    gurkaynak_sack_wright_filters,
    compare_fit,
)

from finm.data import (
    pull_CRSP_treasury_daily,
    pull_CRSP_treasury_info,
    calc_runness,
    pull_CRSP_treasury_consolidated,
    load_CRSP_treasury_daily,
    load_CRSP_treasury_info,
    load_CRSP_treasury_consolidated,
    pull_fed_yield_curve,
    load_fed_yield_curve_all,
    load_fed_yield_curve,
)

__version__ = "0.1.0"
__author__ = "University of Chicago Financial Mathematics Program"

__all__ = [
    "present_value",
    "future_value",
    "yield_to_maturity",
    "bond_price",
    "duration",
    "modified_duration",
    "convexity",
    "get_coupon_dates",
    "filter_treasury_cashflows",
    "calc_cashflows",
    "plot_spot_curve",
    "spot",
    "discount",
    "predict_prices",
    "fit",
    "gurkaynak_sack_wright_filters",
    "compare_fit",
    "pull_CRSP_treasury_daily",
    "pull_CRSP_treasury_info",
    "calc_runness",
    "pull_CRSP_treasury_consolidated",
    "load_CRSP_treasury_daily",
    "load_CRSP_treasury_info",
    "load_CRSP_treasury_consolidated",
    "pull_fed_yield_curve",
    "load_fed_yield_curve_all",
    "load_fed_yield_curve",
]

