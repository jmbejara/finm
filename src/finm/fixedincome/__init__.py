"""
Fixed Income Module

This module provides functions for fixed income calculations including
bond pricing, yield calculations, and risk measures.
"""

from finm.fixedincome.pricing import (
    present_value,
    future_value,
    get_coupon_dates,
    calc_bond_cashflows,
    calc_clean_bond_price,
    calc_dirty_bond_price,
    calc_accrued_interest,
    calc_yield_to_maturity,
    calc_macaulay_duration,
    calc_modified_duration,
    calc_dollar_duration,
    calc_convexity,
    calc_zero_bond_price,
    calc_zero_bond_yield,
    calc_zero_bond_duration,
    calc_zero_bond_convexity,
    calc_zero_bond_discount_factor,
    calc_current_yield,
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

__all__ = [
    # from finm.fixedincome.pricing
    "present_value",
    "future_value",
    "get_coupon_dates",
    "calc_bond_cashflows",
    "calc_clean_bond_price",
    "calc_dirty_bond_price",
    "calc_accrued_interest",
    "calc_yield_to_maturity",
    "calc_macaulay_duration",
    "calc_modified_duration",
    "calc_dollar_duration",
    "calc_convexity",
    "calc_zero_bond_price",
    "calc_zero_bond_yield",
    "calc_zero_bond_duration",
    "calc_zero_bond_convexity",
    "calc_zero_bond_discount_factor",
    "calc_current_yield",
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
]
