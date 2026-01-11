"""Load functions for WRDS data."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pandas as pd

from finm.data.wrds._constants import (
    PARQUET_CORP_BOND,
    PARQUET_TREASURY_CONSOLIDATED,
    PARQUET_TREASURY_DAILY,
    PARQUET_TREASURY_INFO,
    PARQUET_TREASURY_WITH_RUNNESS,
)

TreasuryVariantType = Literal["daily", "info", "consolidated"]


def load_treasury(
    data_dir: Path | str,
    variant: TreasuryVariantType = "consolidated",
    with_runness: bool = True,
) -> pd.DataFrame:
    """Load CRSP Treasury data from parquet.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet files.
    variant : {"daily", "info", "consolidated"}, default "consolidated"
        Which data variant to load.
    with_runness : bool, default True
        For consolidated variant, whether to load the version with runness.

    Returns
    -------
    pd.DataFrame
        Treasury data.
    """
    data_dir = Path(data_dir)

    if variant == "daily":
        return pd.read_parquet(data_dir / PARQUET_TREASURY_DAILY)
    elif variant == "info":
        return pd.read_parquet(data_dir / PARQUET_TREASURY_INFO)
    elif variant == "consolidated":
        if with_runness:
            return pd.read_parquet(data_dir / PARQUET_TREASURY_WITH_RUNNESS)
        else:
            return pd.read_parquet(data_dir / PARQUET_TREASURY_CONSOLIDATED)
    else:
        raise ValueError(
            f"variant must be 'daily', 'info', or 'consolidated', got '{variant}'"
        )


def load_corp_bond(data_dir: Path | str) -> pd.DataFrame:
    """Load corporate bond data from parquet.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet file.

    Returns
    -------
    pd.DataFrame
        Corporate bond data.
    """
    data_dir = Path(data_dir)
    return pd.read_parquet(data_dir / PARQUET_CORP_BOND)
