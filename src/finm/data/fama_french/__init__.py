"""Fama-French factor data module.

Provides access to Fama-French 3 factors from Ken French's Data Library.

Website: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

Standard interface:
    - pull(data_dir, accept_license): Download data from source
    - load(data_dir, format): Load cached or bundled data
    - to_long_format(df): Convert to long format

License:
    Copyright Fama & French. Please cite the papers when using this data.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal

import pandas as pd

from finm.data.fama_french._constants import LICENSE_INFO
from finm.data.fama_french._load import load_data
from finm.data.fama_french._pull import pull_data
from finm.data.fama_french._transform import to_long_format

if TYPE_CHECKING:
    from datetime import datetime

FormatType = Literal["wide", "long"]
FrequencyType = Literal["daily", "monthly"]


def pull(
    data_dir: Path | str,
    start: str | datetime | None = None,
    end: str | datetime | None = None,
    frequency: FrequencyType = "daily",
    accept_license: bool = False,
) -> pd.DataFrame:
    """Download Fama-French factors from Ken French's Data Library.

    Requires pandas_datareader to be installed.

    Website: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

    Parameters
    ----------
    data_dir : Path or str
        Directory to save downloaded data.
    start : str or datetime, optional
        Start date of the data. Format: 'YYYY-MM-DD'.
    end : str or datetime, optional
        End date of the data. Format: 'YYYY-MM-DD'.
    frequency : {"daily", "monthly"}, default "daily"
        Data frequency.
    accept_license : bool, default False
        Must be set to True to acknowledge the data provider's terms.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the factors (as decimals):
        - Mkt-RF: Excess return on the market
        - SMB: Small Minus Big (size factor)
        - HML: High Minus Low (value factor)
        - RF: Risk-free rate

    Raises
    ------
    ValueError
        If accept_license is False.
    """
    return pull_data(
        data_dir=data_dir,
        start=start,
        end=end,
        frequency=frequency,
        accept_license=accept_license,
    )


def load(
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
        Start date to filter data. Format: 'YYYY-MM-DD'.
    end : str or datetime, optional
        End date to filter data. Format: 'YYYY-MM-DD'.
    format : {"wide", "long"}, default "wide"
        Output format:
        - "wide": Original format with factor columns
        - "long": Melted format with [unique_id, ds, y] columns

    Returns
    -------
    pd.DataFrame
        Factor data.
    """
    df = load_data(data_dir=data_dir, start=start, end=end)

    if format == "long":
        df = to_long_format(df)

    return df


__all__ = ["pull", "load", "to_long_format", "LICENSE_INFO"]
