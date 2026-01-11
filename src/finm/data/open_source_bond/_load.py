"""Load functions for Open Source Bond data."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pandas as pd

from finm.data.open_source_bond._constants import DATA_INFO

VariantType = Literal["treasury", "corporate"]


def load_data(
    data_dir: Path | str,
    variant: VariantType = "treasury",
) -> pd.DataFrame:
    """Load Open Source Bond data from parquet.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet files.
    variant : {"treasury", "corporate"}, default "treasury"
        Which dataset to load:
        - "treasury": Treasury bond returns
        - "corporate": Corporate bond returns

    Returns
    -------
    pd.DataFrame
        Bond returns data.
    """
    data_dir = Path(data_dir)

    if variant not in DATA_INFO:
        raise ValueError(f"variant must be 'treasury' or 'corporate', got '{variant}'")

    parquet_file = DATA_INFO[variant]["parquet"]
    return pd.read_parquet(data_dir / parquet_file)
