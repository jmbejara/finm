"""Load functions for Federal Reserve yield curve data."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pandas as pd

from finm.data.federal_reserve._constants import PARQUET_ALL, PARQUET_STANDARD

VariantType = Literal["standard", "all"]


def load_data(
    data_dir: Path | str,
    variant: VariantType = "standard",
) -> pd.DataFrame:
    """Load Federal Reserve yield curve data from parquet.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet files.
    variant : {"standard", "all"}, default "standard"
        Which dataset variant to load:
        - "standard": Only SVENY01-SVENY30 columns (30 yield columns)
        - "all": Full dataset with all columns

    Returns
    -------
    pd.DataFrame
        Yield curve data with date index.
    """
    data_dir = Path(data_dir)

    if variant == "all":
        path = data_dir / PARQUET_ALL
    else:
        path = data_dir / PARQUET_STANDARD

    return pd.read_parquet(path)
