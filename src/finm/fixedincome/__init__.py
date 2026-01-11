"""
Fixed Income Module

This module provides functions for fixed income calculations including
bond pricing, yield calculations, and risk measures.
"""

from finm.fixedincome.bonds import (
    convexity,
    duration,
    future_value,
    modified_duration,
    present_value,
    yield_to_maturity,
)
from finm.fixedincome.calc_corp_bond_returns import (
    assign_cs_deciles,
    calc_corp_bond_returns,
    calc_value_weighted_decile_returns,
)
from finm.fixedincome.gsw2006_yield_curve import (
    calc_cashflows,
    compare_fit,
    discount,
    filter_treasury_cashflows,
    fit,
    get_coupon_dates,
    gurkaynak_sack_wright_filters,
    plot_spot_curve,
    predict_prices,
    spot,
)
from finm.fixedincome.pricing import (
    bond_price,
    bond_price_ql,
    get_coupon_dates,
    get_coupon_dates_ql,
)

__all__ = [
    # from finm.fixedincome.bonds
    "present_value",
    "future_value",
    "yield_to_maturity",
    "duration",
    "modified_duration",
    "convexity",
    # from finm.fixedincome.calc_corp_bond_returns
    "assign_cs_deciles",
    "calc_value_weighted_decile_returns",
    "calc_corp_bond_returns",
    # from finm.fixedincome.gsw2006_yield_curve
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
    # from finm.fixedincome.pricing import
    "get_coupon_dates",
    "get_coupon_dates_ql",
    "bond_price",
    "bond_price_ql",
]
