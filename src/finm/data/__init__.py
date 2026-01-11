"""Data module.

This module provides functions for pulling, loading, and transforming financial
data from various sources. All load functions return polars DataFrames by default.

Submodules:
    - federal_reserve: Federal Reserve yield curve data (GSW model)
    - fama_french: Fama-French 3 factors
    - he_kelly_manela: He-Kelly-Manela intermediary capital factors
    - open_source_bond: Open Source Bond Asset Pricing data
    - wrds: WRDS CRSP Treasury and corporate bond data

Each submodule follows a standard interface:
    - pull(data_dir, ...): Download data from source
    - load(data_dir, variant, format, pull_if_not_found, lazy): Load cached data (returns polars)
    - to_long_format(df): Convert to long format [unique_id, ds, y]

Example usage:
    from finm.data import federal_reserve

    # Load with auto-pull if data doesn't exist
    df = federal_reserve.load(
        data_dir="./data",
        pull_if_not_found=True,
        accept_license=True,
    )

    # Get a LazyFrame for deferred computation
    lf = federal_reserve.load(data_dir="./data", lazy=True)
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal, Union

import pandas as pd
import polars as pl

# Import submodules for direct access
from finm.data import (
    fama_french,
    federal_reserve,
    he_kelly_manela,
    open_source_bond,
    wrds,
)

if TYPE_CHECKING:
    from datetime import datetime

FormatType = Literal["wide", "long"]


# ==============================================================================
# Federal Reserve - Descriptive wrapper functions
# ==============================================================================


def pull_fed_yield_curve(data_dir: Path | str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Download Federal Reserve yield curve data.

    Parameters
    ----------
    data_dir : Path or str
        Directory to save downloaded data.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        (df_all, df_standard) - Full dataset and filtered dataset.
    """
    return federal_reserve.pull(data_dir=data_dir)


def load_fed_yield_curve(
    data_dir: Path | str,
    format: FormatType = "wide",
    pull_if_not_found: bool = False,
    accept_license: bool = False,
    lazy: bool = False,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    """Load Federal Reserve yield curve data (SVENY01-30).

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet files.
    format : {"wide", "long"}, default "wide"
        Output format.
    pull_if_not_found : bool, default False
        If True and data doesn't exist locally, pull from source.
    accept_license : bool, default False
        Must be True when pull_if_not_found=True.
    lazy : bool, default False
        If True, return a polars LazyFrame instead of DataFrame.

    Returns
    -------
    pl.DataFrame or pl.LazyFrame
        Yield curve data.
    """
    return federal_reserve.load(
        data_dir=data_dir,
        variant="standard",
        format=format,
        pull_if_not_found=pull_if_not_found,
        accept_license=accept_license,
        lazy=lazy,
    )


def load_fed_yield_curve_all(
    data_dir: Path | str,
    format: FormatType = "wide",
    pull_if_not_found: bool = False,
    accept_license: bool = False,
    lazy: bool = False,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    """Load full Federal Reserve yield curve data.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet files.
    format : {"wide", "long"}, default "wide"
        Output format.
    pull_if_not_found : bool, default False
        If True and data doesn't exist locally, pull from source.
    accept_license : bool, default False
        Must be True when pull_if_not_found=True.
    lazy : bool, default False
        If True, return a polars LazyFrame instead of DataFrame.

    Returns
    -------
    pl.DataFrame or pl.LazyFrame
        Full yield curve data.
    """
    return federal_reserve.load(
        data_dir=data_dir,
        variant="all",
        format=format,
        pull_if_not_found=pull_if_not_found,
        accept_license=accept_license,
        lazy=lazy,
    )


# ==============================================================================
# Fama-French - Descriptive wrapper functions
# ==============================================================================


def pull_fama_french_factors(
    data_dir: Path | str,
    start: str | datetime | None = None,
    end: str | datetime | None = None,
    frequency: Literal["daily", "monthly"] = "daily",
) -> pd.DataFrame:
    """Download Fama-French factors from Ken French's Data Library.

    Parameters
    ----------
    data_dir : Path or str
        Directory to save downloaded data.
    start : str or datetime, optional
        Start date.
    end : str or datetime, optional
        End date.
    frequency : {"daily", "monthly"}, default "daily"
        Data frequency.

    Returns
    -------
    pd.DataFrame
        Factor data.
    """
    return fama_french.pull(
        data_dir=data_dir, start=start, end=end, frequency=frequency
    )


def load_fama_french_factors(
    data_dir: Path | str | None = None,
    start: str | datetime | None = None,
    end: str | datetime | None = None,
    format: FormatType = "wide",
    frequency: Literal["daily", "monthly"] = "daily",
    pull_if_not_found: bool = False,
    accept_license: bool = False,
    lazy: bool = False,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    """Load Fama-French factors from bundled or cached data.

    Parameters
    ----------
    data_dir : Path or str, optional
        Directory containing the data. If None, loads bundled data.
    start : str or datetime, optional
        Start date to filter.
    end : str or datetime, optional
        End date to filter.
    format : {"wide", "long"}, default "wide"
        Output format.
    frequency : {"daily", "monthly"}, default "daily"
        Data frequency to pull if pull_if_not_found=True.
    pull_if_not_found : bool, default False
        If True and data doesn't exist locally, pull from source.
    accept_license : bool, default False
        Must be True when pull_if_not_found=True.
    lazy : bool, default False
        If True, return a polars LazyFrame instead of DataFrame.

    Returns
    -------
    pl.DataFrame or pl.LazyFrame
        Factor data.
    """
    return fama_french.load(
        data_dir=data_dir,
        start=start,
        end=end,
        format=format,
        frequency=frequency,
        pull_if_not_found=pull_if_not_found,
        accept_license=accept_license,
        lazy=lazy,
    )


# ==============================================================================
# He-Kelly-Manela - Descriptive wrapper functions
# ==============================================================================


def pull_he_kelly_manela(
    data_dir: Path | str,
    accept_license: bool = False,
) -> None:
    """Download He-Kelly-Manela factors.

    Parameters
    ----------
    data_dir : Path or str
        Directory to save downloaded data.
    accept_license : bool, default False
        Must be set to True to acknowledge the data provider's terms.
    """
    return he_kelly_manela.pull(data_dir=data_dir, accept_license=accept_license)


def load_he_kelly_manela_factors_monthly(
    data_dir: Path | str,
    format: FormatType = "wide",
    pull_if_not_found: bool = False,
    accept_license: bool = False,
    lazy: bool = False,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    """Load He-Kelly-Manela monthly factors.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the data.
    format : {"wide", "long"}, default "wide"
        Output format.
    pull_if_not_found : bool, default False
        If True and data doesn't exist locally, pull from source.
    accept_license : bool, default False
        Must be True when pull_if_not_found=True.
    lazy : bool, default False
        If True, return a polars LazyFrame instead of DataFrame.

    Returns
    -------
    pl.DataFrame or pl.LazyFrame
        Monthly factor data.
    """
    return he_kelly_manela.load(
        data_dir=data_dir,
        variant="factors_monthly",
        format=format,
        pull_if_not_found=pull_if_not_found,
        accept_license=accept_license,
        lazy=lazy,
    )


def load_he_kelly_manela_factors_daily(
    data_dir: Path | str,
    format: FormatType = "wide",
    pull_if_not_found: bool = False,
    accept_license: bool = False,
    lazy: bool = False,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    """Load He-Kelly-Manela daily factors.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the data.
    format : {"wide", "long"}, default "wide"
        Output format.
    pull_if_not_found : bool, default False
        If True and data doesn't exist locally, pull from source.
    accept_license : bool, default False
        Must be True when pull_if_not_found=True.
    lazy : bool, default False
        If True, return a polars LazyFrame instead of DataFrame.

    Returns
    -------
    pl.DataFrame or pl.LazyFrame
        Daily factor data.
    """
    return he_kelly_manela.load(
        data_dir=data_dir,
        variant="factors_daily",
        format=format,
        pull_if_not_found=pull_if_not_found,
        accept_license=accept_license,
        lazy=lazy,
    )


def load_he_kelly_manela_all(
    data_dir: Path | str,
    format: FormatType = "wide",
    pull_if_not_found: bool = False,
    accept_license: bool = False,
    lazy: bool = False,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    """Load He-Kelly-Manela factors and test assets.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the data.
    format : {"wide", "long"}, default "wide"
        Output format.
    pull_if_not_found : bool, default False
        If True and data doesn't exist locally, pull from source.
    accept_license : bool, default False
        Must be True when pull_if_not_found=True.
    lazy : bool, default False
        If True, return a polars LazyFrame instead of DataFrame.

    Returns
    -------
    pl.DataFrame or pl.LazyFrame
        Factors and test assets data.
    """
    return he_kelly_manela.load(
        data_dir=data_dir,
        variant="all",
        format=format,
        pull_if_not_found=pull_if_not_found,
        accept_license=accept_license,
        lazy=lazy,
    )


# ==============================================================================
# Open Source Bond - Descriptive wrapper functions
# ==============================================================================


def pull_open_source_bond(
    data_dir: Path | str,
    variant: Literal[
        "treasury", "corporate_daily", "corporate_monthly", "corporate_all", "all"
    ] = "all",
    accept_license: bool = False,
) -> None:
    """Download Open Source Bond data.

    Website: https://openbondassetpricing.com/
    License: MIT License (citation required)

    Parameters
    ----------
    data_dir : Path or str
        Directory to save downloaded data.
    variant : str, default "all"
        Which dataset(s) to download:
        - "treasury": Treasury bond returns
        - "corporate_daily": Daily corporate bond PRICES
        - "corporate_monthly": Monthly corporate bond RETURNS with factor signals
        - "corporate_all": Both corporate datasets
        - "all": All datasets
    accept_license : bool, default False
        Must be True to acknowledge the data provider's license terms.
    """
    return open_source_bond.pull(
        data_dir=data_dir, variant=variant, accept_license=accept_license
    )


def load_treasury_returns(
    data_dir: Path | str,
    format: FormatType = "wide",
    pull_if_not_found: bool = False,
    accept_license: bool = False,
    lazy: bool = False,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    """Load treasury bond returns.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the data.
    format : {"wide", "long"}, default "wide"
        Output format.
    pull_if_not_found : bool, default False
        If True and data doesn't exist locally, pull from source.
    accept_license : bool, default False
        Must be True when pull_if_not_found=True.
    lazy : bool, default False
        If True, return a polars LazyFrame instead of DataFrame.

    Returns
    -------
    pl.DataFrame or pl.LazyFrame
        Treasury bond returns.
    """
    return open_source_bond.load(
        data_dir=data_dir,
        variant="treasury",
        format=format,
        pull_if_not_found=pull_if_not_found,
        accept_license=accept_license,
        lazy=lazy,
    )


def load_corporate_bond_returns(
    data_dir: Path | str,
    format: FormatType = "wide",
    pull_if_not_found: bool = False,
    accept_license: bool = False,
    lazy: bool = False,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    """Load corporate bond returns (monthly).

    This loads the monthly corporate bond returns with 108 factor signals.
    For daily prices, use load_corporate_bond_prices_daily().

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the data.
    format : {"wide", "long"}, default "wide"
        Output format.
    pull_if_not_found : bool, default False
        If True and data doesn't exist locally, pull from source.
    accept_license : bool, default False
        Must be True when pull_if_not_found=True.
    lazy : bool, default False
        If True, return a polars LazyFrame instead of DataFrame.

    Returns
    -------
    pl.DataFrame or pl.LazyFrame
        Corporate bond returns (monthly). Key columns:
        - cusip: Bond identifier
        - date: Month-end date
        - ret_vw: Volume-weighted total return
        - rfret: Risk-free rate
        - tret: Duration-matched Treasury return
    """
    return open_source_bond.load(
        data_dir=data_dir,
        variant="corporate_monthly",
        format=format,
        pull_if_not_found=pull_if_not_found,
        accept_license=accept_license,
        lazy=lazy,
    )


def load_corporate_bond_prices_daily(
    data_dir: Path | str,
    format: FormatType = "wide",
    pull_if_not_found: bool = False,
    accept_license: bool = False,
    lazy: bool = False,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    """Load daily corporate bond prices (TRACE Stage 1).

    This is PRICE data, not returns. For returns, use load_corporate_bond_returns().

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the data.
    format : {"wide", "long"}, default "wide"
        Output format.
    pull_if_not_found : bool, default False
        If True and data doesn't exist locally, pull from source.
    accept_license : bool, default False
        Must be True when pull_if_not_found=True.
    lazy : bool, default False
        If True, return a polars LazyFrame instead of DataFrame.

    Returns
    -------
    pl.DataFrame or pl.LazyFrame
        Daily corporate bond prices. Key columns:
        - cusip_id: Bond identifier
        - trd_exctn_dt: Trade execution date
        - pr: Price
        - mod_dur: Modified duration
        - ytm: Yield to maturity
    """
    return open_source_bond.load(
        data_dir=data_dir,
        variant="corporate_daily",
        format=format,
        pull_if_not_found=pull_if_not_found,
        accept_license=accept_license,
        lazy=lazy,
    )


def load_corporate_bond_returns_monthly(
    data_dir: Path | str,
    format: FormatType = "wide",
    pull_if_not_found: bool = False,
    accept_license: bool = False,
    lazy: bool = False,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    """Load monthly corporate bond returns with factor signals.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the data.
    format : {"wide", "long"}, default "wide"
        Output format.
    pull_if_not_found : bool, default False
        If True and data doesn't exist locally, pull from source.
    accept_license : bool, default False
        Must be True when pull_if_not_found=True.
    lazy : bool, default False
        If True, return a polars LazyFrame instead of DataFrame.

    Returns
    -------
    pl.DataFrame or pl.LazyFrame
        Corporate bond returns (monthly) with 108 factor signals.
    """
    return open_source_bond.load(
        data_dir=data_dir,
        variant="corporate_monthly",
        format=format,
        pull_if_not_found=pull_if_not_found,
        accept_license=accept_license,
        lazy=lazy,
    )


# ==============================================================================
# WRDS - Descriptive wrapper functions
# ==============================================================================


def pull_wrds_treasury(
    data_dir: Path | str,
    wrds_username: str,
    start_date: str,
    end_date: str,
    variant: Literal["daily", "info", "consolidated"] = "consolidated",
    with_runness: bool = True,
) -> pd.DataFrame:
    """Pull CRSP Treasury data from WRDS.

    Parameters
    ----------
    data_dir : Path or str
        Directory to save the data.
    wrds_username : str
        WRDS username.
    start_date : str
        Start date in 'YYYY-MM-DD' format.
    end_date : str
        End date in 'YYYY-MM-DD' format.
    variant : {"daily", "info", "consolidated"}, default "consolidated"
        Which data variant to pull.
    with_runness : bool, default True
        Whether to calculate runness for consolidated data.

    Returns
    -------
    pd.DataFrame
        Treasury data.
    """
    return wrds.pull(
        data_dir=data_dir,
        variant="treasury",
        wrds_username=wrds_username,
        start_date=start_date,
        end_date=end_date,
        treasury_variant=variant,
        with_runness=with_runness,
    )


def load_wrds_treasury(
    data_dir: Path | str,
    variant: Literal["daily", "info", "consolidated"] = "consolidated",
    with_runness: bool = True,
    format: FormatType = "wide",
    pull_if_not_found: bool = False,
    wrds_username: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    lazy: bool = False,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    """Load CRSP Treasury data from local cache.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet files.
    variant : {"daily", "info", "consolidated"}, default "consolidated"
        Which data variant to load.
    with_runness : bool, default True
        For consolidated variant, whether to load version with runness.
    format : {"wide", "long"}, default "wide"
        Output format.
    pull_if_not_found : bool, default False
        If True and data doesn't exist locally, pull from WRDS.
    wrds_username : str, optional
        WRDS username. Required when pull_if_not_found=True.
    start_date : str, optional
        Start date ('YYYY-MM-DD'). Required when pull_if_not_found=True.
    end_date : str, optional
        End date ('YYYY-MM-DD'). Required when pull_if_not_found=True.
    lazy : bool, default False
        If True, return a polars LazyFrame instead of DataFrame.

    Returns
    -------
    pl.DataFrame or pl.LazyFrame
        Treasury data.
    """
    return wrds.load(
        data_dir=data_dir,
        variant="treasury",
        format=format,
        treasury_variant=variant,
        with_runness=with_runness,
        pull_if_not_found=pull_if_not_found,
        wrds_username=wrds_username,
        start_date=start_date,
        end_date=end_date,
        lazy=lazy,
    )


def pull_wrds_corp_bond(
    data_dir: Path | str,
    wrds_username: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """Pull corporate bond data from WRDS.

    Parameters
    ----------
    data_dir : Path or str
        Directory to save the data.
    wrds_username : str
        WRDS username.
    start_date : str
        Start date in 'YYYY-MM-DD' format.
    end_date : str
        End date in 'YYYY-MM-DD' format.

    Returns
    -------
    pd.DataFrame
        Corporate bond data.
    """
    return wrds.pull(
        data_dir=data_dir,
        variant="corp_bond",
        wrds_username=wrds_username,
        start_date=start_date,
        end_date=end_date,
    )


def load_wrds_corp_bond(
    data_dir: Path | str,
    format: FormatType = "wide",
    pull_if_not_found: bool = False,
    wrds_username: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    lazy: bool = False,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    """Load corporate bond data from local cache.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet file.
    format : {"wide", "long"}, default "wide"
        Output format.
    pull_if_not_found : bool, default False
        If True and data doesn't exist locally, pull from WRDS.
    wrds_username : str, optional
        WRDS username. Required when pull_if_not_found=True.
    start_date : str, optional
        Start date ('YYYY-MM-DD'). Required when pull_if_not_found=True.
    end_date : str, optional
        End date ('YYYY-MM-DD'). Required when pull_if_not_found=True.
    lazy : bool, default False
        If True, return a polars LazyFrame instead of DataFrame.

    Returns
    -------
    pl.DataFrame or pl.LazyFrame
        Corporate bond data.
    """
    return wrds.load(
        data_dir=data_dir,
        variant="corp_bond",
        format=format,
        pull_if_not_found=pull_if_not_found,
        wrds_username=wrds_username,
        start_date=start_date,
        end_date=end_date,
        lazy=lazy,
    )


def calc_treasury_runness(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate on-the-run/off-the-run status for Treasury securities.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame with Treasury data.

    Returns
    -------
    pd.DataFrame
        Data with 'run' column added.
    """
    return wrds.calc_runness(data)


__all__ = [
    # Submodules
    "federal_reserve",
    "fama_french",
    "he_kelly_manela",
    "open_source_bond",
    "wrds",
    # Federal Reserve
    "pull_fed_yield_curve",
    "load_fed_yield_curve",
    "load_fed_yield_curve_all",
    # Fama-French
    "pull_fama_french_factors",
    "load_fama_french_factors",
    # He-Kelly-Manela
    "pull_he_kelly_manela",
    "load_he_kelly_manela_factors_monthly",
    "load_he_kelly_manela_factors_daily",
    "load_he_kelly_manela_all",
    # Open Source Bond
    "pull_open_source_bond",
    "load_treasury_returns",
    "load_corporate_bond_returns",
    "load_corporate_bond_prices_daily",
    "load_corporate_bond_returns_monthly",
    # WRDS
    "pull_wrds_treasury",
    "load_wrds_treasury",
    "pull_wrds_corp_bond",
    "load_wrds_corp_bond",
    "calc_treasury_runness",
]
