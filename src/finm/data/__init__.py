"""
Data module

This module provides functions for pulling, loading, and cleaning data from various data sources.
"""

from finm.data.Federal_Reserve.pull_yield_curve_data import (
    pull_fed_yield_curve,
    load_fed_yield_curve_all,
    load_fed_yield_curve,
)

from finm.data.He_Kelly_Manela.pull_he_kelly_manela import (
    pull_he_kelly_manela,
    load_he_kelly_manela_factors_monthly,
    load_he_kelly_manela_factors_daily,
    load_he_kelly_manela_all,
)

from finm.data.Open_Source_Bond.pull_open_source_bond import (
    download_file,
    download_data,
    load_data_into_dataframe,
    load_treasury_returns,
    load_corporate_bond_returns,
)

from finm.data.WRDS.pull_CRSP_treasury import (
    pull_CRSP_treasury_daily,
    pull_CRSP_treasury_info,
    calc_runness,
    pull_CRSP_treasury_consolidated,
    load_CRSP_treasury_daily,
    load_CRSP_treasury_info,
    load_CRSP_treasury_consolidated,
)

from finm.data.WRDS.pull_WRDS_corp_bond import (
    pull_WRDS_corp_bond_monthly,
    load_WRDS_corp_bond_monthly,
)

__all__ = [
    # from finm.data.Federal_Reserve.pull_yield_curve_data
    "pull_fed_yield_curve",
    "load_fed_yield_curve_all",
    "load_fed_yield_curve",

    # from finm.data.He_Kelly_Manela.pull_he_kelly_manela
    "pull_he_kelly_manela",
    "load_he_kelly_manela_factors_monthly",
    "load_he_kelly_manela_factors_daily",
    "load_he_kelly_manela_all",

    # from finm.data.Open_Source_Bond.pull_open_source_bond
    "download_file",
    "download_data",
    "load_data_into_dataframe",
    "load_treasury_returns",
    "load_corporate_bond_returns",

    # from finm.data.WRDS.pull_CRSP_treasury
    "pull_CRSP_treasury_daily",
    "pull_CRSP_treasury_info",
    "calc_runness",
    "pull_CRSP_treasury_consolidated",
    "load_CRSP_treasury_daily",
    "load_CRSP_treasury_info",
    "load_CRSP_treasury_consolidated",

    # from from finm.data.WRDS.pull_WRDS_corp_bond
    "pull_WRDS_corp_bond_monthly",
    "load_WRDS_corp_bond_monthly",
]