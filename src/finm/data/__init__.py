"""Data module.

This module provides functions for pulling, loading, and cleaning data from various data sources.
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
]
