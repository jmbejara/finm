"""
finm - Financial Mathematics Python Package

A student-led Python package for financial mathematics and quantitative finance
education, created by students and educators at the University of Chicago
Financial Mathematics program.

⚠️  DISCLAIMER: This package is for learning purposes only. There are likely
errors and this should NOT be used for any purposes beyond education and research.
"""

from finm.data.federal_reserve.pull_yield_curve_data import (
    load_fed_yield_curve,
    load_fed_yield_curve_all,
    pull_fed_yield_curve,
)
from finm.data.he_kelly_manela.pull_he_kelly_manela import (
    load_he_kelly_manela_all,
    load_he_kelly_manela_factors_daily,
    load_he_kelly_manela_factors_monthly,
    pull_he_kelly_manela,
)
from finm.data.open_source_bond.pull_open_source_bond import (
    download_data,
    download_file,
    load_corporate_bond_returns,
    load_data_into_dataframe,
    load_treasury_returns,
)
from finm.data.wrds_data.pull_CRSP_treasury import (
    calc_runness,
    load_CRSP_treasury_consolidated,
    load_CRSP_treasury_daily,
    load_CRSP_treasury_info,
    pull_CRSP_treasury_consolidated,
    pull_CRSP_treasury_daily,
    pull_CRSP_treasury_info,
)
from finm.data.wrds_data.pull_WRDS_corp_bond import (
    load_WRDS_corp_bond_monthly,
    pull_WRDS_corp_bond_monthly,
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

__version__ = "0.1.0"
__author__ = "University of Chicago Financial Mathematics Program"

__all__ = [
    # from finm.data.federal_reserve.pull_yield_curve_data
    "pull_fed_yield_curve",
    "load_fed_yield_curve_all",
    "load_fed_yield_curve",
    # from finm.data.he_kelly_manela.pull_he_kelly_manela
    "pull_he_kelly_manela",
    "load_he_kelly_manela_factors_monthly",
    "load_he_kelly_manela_factors_daily",
    "load_he_kelly_manela_all",
    # from finm.data.open_source_bond.pull_open_source_bond
    "download_file",
    "download_data",
    "load_data_into_dataframe",
    "load_treasury_returns",
    "load_corporate_bond_returns",
    # from finm.data.wrds_data.pull_CRSP_treasury
    "pull_CRSP_treasury_daily",
    "pull_CRSP_treasury_info",
    "calc_runness",
    "pull_CRSP_treasury_consolidated",
    "load_CRSP_treasury_daily",
    "load_CRSP_treasury_info",
    "load_CRSP_treasury_consolidated",
    # from finm.data.wrds_data.pull_WRDS_corp_bond
    "pull_WRDS_corp_bond_monthly",
    "load_WRDS_corp_bond_monthly",
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
