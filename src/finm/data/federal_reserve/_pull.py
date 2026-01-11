"""Pull functions for Federal Reserve yield curve data."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pandas as pd
import requests

from finm.data.federal_reserve._constants import (
    PARQUET_ALL,
    PARQUET_STANDARD,
    YIELD_COLUMNS,
    YIELD_CURVE_URL,
)


def pull_data(data_dir: Path | str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Download Federal Reserve yield curve data and save to parquet.

    Downloads the GSW (Gurkaynak, Sack, Wright) yield curve data from
    the Federal Reserve and saves both the full dataset and a filtered
    version with only the standard yield columns (SVENY01-SVENY30).

    Parameters
    ----------
    data_dir : Path or str
        Directory to save the parquet files.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        (df_all, df_standard) - Full dataset and filtered dataset.
    """
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    # Download data
    response = requests.get(YIELD_CURVE_URL)
    response.raise_for_status()
    pdf_stream = BytesIO(response.content)

    # Parse CSV (skip header rows)
    df_all = pd.read_csv(pdf_stream, skiprows=9, index_col=0, parse_dates=True)

    # Filter to standard yield columns
    df_standard = df_all[YIELD_COLUMNS]

    # Save to parquet
    df_all.to_parquet(data_dir / PARQUET_ALL)
    df_standard.to_parquet(data_dir / PARQUET_STANDARD)

    return df_all, df_standard
