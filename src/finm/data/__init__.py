"""
Data module

This module provides functions for pulling, loading, and cleaning data from various data sources.
"""

from finm.data.Federal_Reserve import (
    pull_fed_yield_curve,
    load_fed_yield_curve_all,
    load_fed_yield_curve,
)

from finm.data.he_kelly_manela import (
    pull_he_kelly_manela,
    load_he_kelly_manela_factors_monthly,
    load_he_kelly_manela_factors_daily,
    load_he_kelly_manela_all,
)

from finm.data.Open_Source_Bond import (
    download_file,
    download_data,
    load_data_into_dataframe,
    load_treasury_returns,
    load_corporate_bond_returns,
)

from finm.data.WRDS import (
    pull_CRSP_treasury_daily,
    pull_CRSP_treasury_info,
    calc_runness,
    pull_CRSP_treasury_consolidated,
    load_CRSP_treasury_daily,
    load_CRSP_treasury_info,
    load_CRSP_treasury_consolidated,
)

__all__ = [
    "pull_fed_yield_curve",
    "load_fed_yield_curve_all",
    "load_fed_yield_curve",
    "pull_he_kelly_manela",
    "load_he_kelly_manela_factors_monthly",
    "load_he_kelly_manela_factors_daily",
    "load_he_kelly_manela_all",
    "download_file",
    "download_data",
    "load_data_into_dataframe",
    "load_treasury_returns",
    "load_corporate_bond_returns",
    "pull_CRSP_treasury_daily",
    "pull_CRSP_treasury_info",
    "calc_runness",
    "pull_CRSP_treasury_consolidated",
    "load_CRSP_treasury_daily",
    "load_CRSP_treasury_info",
    "load_CRSP_treasury_consolidated",
]