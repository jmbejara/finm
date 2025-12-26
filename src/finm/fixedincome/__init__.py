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
    # get_coupon_dates,
)

from finm.fixedincome.calc_corp_bond_returns import (
    assign_cs_deciles,
    calc_value_weighted_decile_returns,
    calc_corp_bond_returns,
)

from finm.fixedincome.gsw2006_yield_curve import (
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

__all__ = [
    "present_value",
    "future_value",
    "yield_to_maturity",
    "bond_price",
    "duration",
    "modified_duration",
    "convexity",
    "assign_cs_deciles",
    "calc_value_weighted_decile_returns",
    "calc_corp_bond_returns",
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
]

