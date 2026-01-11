"""Data module.

This module provides functions for pulling, loading, and transforming financial
data from various sources.

Submodules:
    - federal_reserve: Federal Reserve yield curve data (GSW model)
    - fama_french: Fama-French 3 factors
    - he_kelly_manela: He-Kelly-Manela intermediary capital factors
    - open_source_bond: Open Source Bond Asset Pricing data
    - wrds: WRDS CRSP Treasury and corporate bond data

Each submodule follows a standard interface:
    - pull(data_dir, ...): Download data from source
    - load(data_dir, variant, format): Load cached data
    - to_long_format(df): Convert to long format [unique_id, ds, y]

Example usage:
    from finm.data import federal_reserve
    federal_reserve.pull(data_dir="./data")
    df = federal_reserve.load(data_dir="./data", format="long")
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal

import pandas as pd

# Import submodules for direct access
from finm.data import fama_french
from finm.data import federal_reserve
from finm.data import he_kelly_manela
from finm.data import open_source_bond
from finm.data import wrds

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
) -> pd.DataFrame:
    """Load Federal Reserve yield curve data (SVENY01-30).

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet files.
    format : {"wide", "long"}, default "wide"
        Output format.

    Returns
    -------
    pd.DataFrame
        Yield curve data.
    """
    return federal_reserve.load(data_dir=data_dir, variant="standard", format=format)


def load_fed_yield_curve_all(
    data_dir: Path | str,
    format: FormatType = "wide",
) -> pd.DataFrame:
    """Load full Federal Reserve yield curve data.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet files.
    format : {"wide", "long"}, default "wide"
        Output format.

    Returns
    -------
    pd.DataFrame
        Full yield curve data.
    """
    return federal_reserve.load(data_dir=data_dir, variant="all", format=format)


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
    return fama_french.pull(data_dir=data_dir, start=start, end=end, frequency=frequency)


def load_fama_french_factors(
    data_dir: Path | str | None = None,
    start: str | datetime | None = None,
    end: str | datetime | None = None,
    format: FormatType = "wide",
) -> pd.DataFrame:
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

    Returns
    -------
    pd.DataFrame
        Factor data.
    """
    return fama_french.load(data_dir=data_dir, start=start, end=end, format=format)


# ==============================================================================
# He-Kelly-Manela - Descriptive wrapper functions
# ==============================================================================


def pull_he_kelly_manela(data_dir: Path | str) -> None:
    """Download He-Kelly-Manela factors.

    Parameters
    ----------
    data_dir : Path or str
        Directory to save downloaded data.
    """
    return he_kelly_manela.pull(data_dir=data_dir)


def load_he_kelly_manela_factors_monthly(
    data_dir: Path | str,
    format: FormatType = "wide",
) -> pd.DataFrame:
    """Load He-Kelly-Manela monthly factors.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the data.
    format : {"wide", "long"}, default "wide"
        Output format.

    Returns
    -------
    pd.DataFrame
        Monthly factor data.
    """
    return he_kelly_manela.load(data_dir=data_dir, variant="factors_monthly", format=format)


def load_he_kelly_manela_factors_daily(
    data_dir: Path | str,
    format: FormatType = "wide",
) -> pd.DataFrame:
    """Load He-Kelly-Manela daily factors.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the data.
    format : {"wide", "long"}, default "wide"
        Output format.

    Returns
    -------
    pd.DataFrame
        Daily factor data.
    """
    return he_kelly_manela.load(data_dir=data_dir, variant="factors_daily", format=format)


def load_he_kelly_manela_all(
    data_dir: Path | str,
    format: FormatType = "wide",
) -> pd.DataFrame:
    """Load He-Kelly-Manela factors and test assets.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the data.
    format : {"wide", "long"}, default "wide"
        Output format.

    Returns
    -------
    pd.DataFrame
        Factors and test assets data.
    """
    return he_kelly_manela.load(data_dir=data_dir, variant="all", format=format)


# ==============================================================================
# Open Source Bond - Descriptive wrapper functions
# ==============================================================================


def pull_open_source_bond(
    data_dir: Path | str,
    variant: Literal["treasury", "corporate", "all"] = "all",
) -> None:
    """Download Open Source Bond data.

    Parameters
    ----------
    data_dir : Path or str
        Directory to save downloaded data.
    variant : {"treasury", "corporate", "all"}, default "all"
        Which dataset(s) to download.
    """
    return open_source_bond.pull(data_dir=data_dir, variant=variant)


def load_treasury_returns(
    data_dir: Path | str,
    format: FormatType = "wide",
) -> pd.DataFrame:
    """Load treasury bond returns.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the data.
    format : {"wide", "long"}, default "wide"
        Output format.

    Returns
    -------
    pd.DataFrame
        Treasury bond returns.
    """
    return open_source_bond.load(data_dir=data_dir, variant="treasury", format=format)


def load_corporate_bond_returns(
    data_dir: Path | str,
    format: FormatType = "wide",
) -> pd.DataFrame:
    """Load corporate bond returns.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the data.
    format : {"wide", "long"}, default "wide"
        Output format.

    Returns
    -------
    pd.DataFrame
        Corporate bond returns.
    """
    return open_source_bond.load(data_dir=data_dir, variant="corporate", format=format)


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
) -> pd.DataFrame:
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

    Returns
    -------
    pd.DataFrame
        Treasury data.
    """
    return wrds.load(
        data_dir=data_dir,
        variant="treasury",
        format=format,
        treasury_variant=variant,
        with_runness=with_runness,
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
) -> pd.DataFrame:
    """Load corporate bond data from local cache.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet file.
    format : {"wide", "long"}, default "wide"
        Output format.

    Returns
    -------
    pd.DataFrame
        Corporate bond data.
    """
    return wrds.load(data_dir=data_dir, variant="corp_bond", format=format)


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
    # WRDS
    "pull_wrds_treasury",
    "load_wrds_treasury",
    "pull_wrds_corp_bond",
    "load_wrds_corp_bond",
    "calc_treasury_runness",
]
