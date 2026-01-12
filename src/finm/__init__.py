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

__version__ = "0.1.2"
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
    # Fixed income - bonds
    "present_value",
    "future_value",
    "yield_to_maturity",
    "duration",
    "modified_duration",
    "convexity",
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
    # Fixed income - pricing
    "get_coupon_dates_ql",
    "bond_price",
    "bond_price_ql",
]
