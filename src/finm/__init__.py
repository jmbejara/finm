"""
finm - Financial Mathematics Python Package

A student-led Python package for financial mathematics and quantitative finance
education, created by students and educators at the University of Chicago
Financial Mathematics program.

DISCLAIMER: This package is for learning purposes only. There are likely
errors and this should NOT be used for any purposes beyond education and research.
"""

from finm.analytics.factor_analysis import (
    RegressionResult,
    calculate_beta,
    calculate_factor_exposures,
    calculate_sharpe_ratio,
    run_capm_regression,
    run_factor_regression,
    run_fama_french_regression,
)
from finm.data import (
    # WRDS
    calc_treasury_runness,
    # Submodules
    fama_french,
    federal_reserve,
    he_kelly_manela,
    # Open Source Bond
    load_corporate_bond_returns,
    # Fama-French
    load_fama_french_factors,
    # Federal Reserve
    load_fed_yield_curve,
    load_fed_yield_curve_all,
    # He-Kelly-Manela
    load_he_kelly_manela_all,
    load_he_kelly_manela_factors_daily,
    load_he_kelly_manela_factors_monthly,
    load_treasury_returns,
    load_wrds_corp_bond,
    load_wrds_treasury,
    open_source_bond,
    pull_fama_french_factors,
    pull_fed_yield_curve,
    pull_he_kelly_manela,
    pull_open_source_bond,
    pull_wrds_corp_bond,
    pull_wrds_treasury,
    wrds,
)
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
from finm.options import (
    calc_option_price,
    calc_option_payoff,
    calc_option_delta,
    calc_option_gamma,
    calc_option_vega,
    calc_option_theta,
    calc_option_rho,
    calc_implied_volatility,
    calc_binomial_option_price,
    calc_breakeven_price,
)
from finm.forwards import (
    calc_fra_settlement,
)
from finm.futures import (
    calc_futures_implied_rate,
    calc_futures_price_from_rate,
    calc_futures_pnl,
)
__version__ = "0.1.3"
__author__ = "University of Chicago Financial Mathematics Program"

__all__ = [
    # Data submodules
    "fama_french",
    "federal_reserve",
    "he_kelly_manela",
    "open_source_bond",
    "wrds",
    # Analytics
    "RegressionResult",
    "calculate_beta",
    "calculate_sharpe_ratio",
    "calculate_factor_exposures",
    "run_factor_regression",
    "run_capm_regression",
    "run_fama_french_regression",
    # Federal Reserve data
    "pull_fed_yield_curve",
    "load_fed_yield_curve_all",
    "load_fed_yield_curve",
    # Fama-French data
    "pull_fama_french_factors",
    "load_fama_french_factors",
    # He-Kelly-Manela data
    "pull_he_kelly_manela",
    "load_he_kelly_manela_factors_monthly",
    "load_he_kelly_manela_factors_daily",
    "load_he_kelly_manela_all",
    # Open Source Bond data
    "pull_open_source_bond",
    "load_treasury_returns",
    "load_corporate_bond_returns",
    # WRDS data
    "pull_wrds_treasury",
    "load_wrds_treasury",
    "pull_wrds_corp_bond",
    "load_wrds_corp_bond",
    "calc_treasury_runness",
    # Fixed income - pricing
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
    # Fixed income - corporate bond returns
    "assign_cs_deciles",
    "calc_value_weighted_decile_returns",
    "calc_corp_bond_returns",
    # Fixed income - GSW yield curve
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
    # Options
    "calc_option_price",
    "calc_option_payoff",
    "calc_option_delta",
    "calc_option_gamma",
    "calc_option_vega",
    "calc_option_theta",
    "calc_option_rho",
    "calc_implied_volatility",
    "calc_binomial_option_price",
    "calc_breakeven_price",
    # Forwards
    "calc_fra_settlement",
    # Futures
    "calc_futures_implied_rate",
    "calc_futures_price_from_rate",
    "calc_futures_pnl",
]
