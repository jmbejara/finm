"""Federal Reserve yield curve data module.

Provides access to the GSW (Gurkaynak, Sack, Wright) yield curve model
published by the Federal Reserve.

Website: https://www.federalreserve.gov/data/yield-curve-tables.htm
Terms: https://www.federalreserve.gov/disclaimer.htm

Standard interface:
    - pull(data_dir, accept_license): Download data from source
    - load(data_dir, variant, format): Load cached data (returns polars)
    - to_long_format(df): Convert to long format

License:
    Public Domain. Please cite the Board as the source.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal, Union

import pandas as pd
import polars as pl

from finm.data.federal_reserve._constants import (
    LICENSE_INFO,
    PARQUET_ALL,
    PARQUET_STANDARD,
)
from finm.data.federal_reserve._load import load_data
from finm.data.federal_reserve._pull import pull_data
from finm.data.federal_reserve._transform import to_long_format

FormatType = Literal["wide", "long"]
VariantType = Literal["standard", "all"]


def pull(
    data_dir: Path | str,
    accept_license: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Download Federal Reserve yield curve data.

    Downloads the GSW (Gurkaynak, Sack, Wright) yield curve data from
    the Federal Reserve and saves to parquet files.

    Website: https://www.federalreserve.gov/data/yield-curve-tables.htm
    Terms: https://www.federalreserve.gov/disclaimer.htm

    Parameters
    ----------
    data_dir : Path or str
        Directory to save downloaded data.
    accept_license : bool, default False
        Must be set to True to acknowledge the data provider's terms.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        (df_all, df_standard) - Full dataset and filtered dataset.

    Raises
    ------
    ValueError
        If accept_license is False.
    """
    return pull_data(data_dir=data_dir, accept_license=accept_license)


def load(
    data_dir: Path | str,
    variant: VariantType = "standard",
    format: FormatType = "wide",
    pull_if_not_found: bool = False,
    accept_license: bool = False,
    lazy: bool = False,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    """Load Federal Reserve yield curve data.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet files.
    variant : {"standard", "all"}, default "standard"
        Which dataset variant to load:
        - "standard": Only SVENY01-SVENY30 columns
        - "all": Full dataset with all columns
    format : {"wide", "long"}, default "wide"
        Output format:
        - "wide": Original format with yield columns
        - "long": Melted format with [unique_id, ds, y] columns
    pull_if_not_found : bool, default False
        If True and data doesn't exist locally, pull from source.
        Requires accept_license=True.
    accept_license : bool, default False
        Must be True when pull_if_not_found=True.
    lazy : bool, default False
        If True, return a polars LazyFrame instead of DataFrame.

    Returns
    -------
    pl.DataFrame or pl.LazyFrame
        Yield curve data as polars DataFrame (default) or LazyFrame.

    Raises
    ------
    ValueError
        If pull_if_not_found=True but accept_license=False.
    FileNotFoundError
        If data doesn't exist and pull_if_not_found=False.
    """
    from finm.data._utils import pandas_to_polars

    data_path = Path(data_dir)
    expected_file = PARQUET_STANDARD if variant == "standard" else PARQUET_ALL

    # Handle pull_if_not_found
    if pull_if_not_found:
        if not accept_license:
            raise ValueError(
                "When pull_if_not_found=True, accept_license must also be True. "
                "This acknowledges the data provider's license terms."
            )
        if not (data_path / expected_file).exists():
            pull_data(data_dir=data_dir, accept_license=True)

    # Load data (internally uses pandas)
    df = load_data(data_dir=data_dir, variant=variant)

    if format == "long":
        df = to_long_format(df)

    # Convert to polars
    return pandas_to_polars(df, lazy=lazy)


__all__ = ["pull", "load", "to_long_format", "LICENSE_INFO"]
