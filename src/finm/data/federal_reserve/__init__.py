"""Federal Reserve yield curve data module.

Provides access to the GSW (Gurkaynak, Sack, Wright) yield curve model
published by the Federal Reserve.

Website: https://www.federalreserve.gov/data/yield-curve-tables.htm
Terms: https://www.federalreserve.gov/disclaimer.htm

Standard interface:
    - pull(data_dir, accept_license): Download data from source
    - load(data_dir, variant, format): Load cached data
    - to_long_format(df): Convert to long format

License:
    Public Domain. Please cite the Board as the source.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pandas as pd

from finm.data.federal_reserve._constants import LICENSE_INFO
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
) -> pd.DataFrame:
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

    Returns
    -------
    pd.DataFrame
        Yield curve data.
    """
    df = load_data(data_dir=data_dir, variant=variant)

    if format == "long":
        df = to_long_format(df)

    return df


__all__ = ["pull", "load", "to_long_format", "LICENSE_INFO"]
