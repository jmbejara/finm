"""Load functions for Fama-French factor data."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pandas as pd

from finm.data.fama_french._constants import BUNDLED_CSV, BUNDLED_DATA_DIR

if TYPE_CHECKING:
    from datetime import datetime


def load_data(
    data_dir: Path | str | None = None,
    start: str | datetime | None = None,
    end: str | datetime | None = None,
) -> pd.DataFrame:
    """Load Fama-French factors from bundled or cached data.

    This function loads pre-downloaded factor data, either from the package's
    bundled data or from a specified directory.

    Parameters
    ----------
    data_dir : Path or str, optional
        Directory containing the CSV file. If None, loads bundled data.
    start : str or datetime, optional
        Start date to filter data. Format: 'YYYY-MM-DD'.
    end : str or datetime, optional
        End date to filter data. Format: 'YYYY-MM-DD'.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the following columns (as decimals):
        - Mkt-RF: Excess return on the market
        - SMB: Small Minus Big (size factor)
        - HML: High Minus Low (value factor)
        - RF: Risk-free rate
    """
    if data_dir is None:
        # Load bundled data
        data_path = BUNDLED_DATA_DIR / BUNDLED_CSV
    else:
        # Load from specified directory
        data_path = Path(data_dir) / BUNDLED_CSV

    df = pd.read_csv(
        data_path,
        parse_dates=["Date"],
        index_col="Date",
        dtype={"Mkt-RF": float, "SMB": float, "HML": float, "RF": float},
    )

    # Filter by date range if specified
    if start is not None:
        df = df.loc[start:]
    if end is not None:
        df = df.loc[:end]

    return df
