"""WRDS financial data module.

Provides access to CRSP Treasury and corporate bond data from WRDS.

Standard interface:
    - pull(data_dir, variant, ...): Download data from WRDS
    - load(data_dir, variant, format): Load cached data
    - to_long_format(df): Convert to long format

Requires WRDS credentials (username).
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pandas as pd

from finm.data.wrds._load import load_corp_bond, load_treasury
from finm.data.wrds._pull import calc_runness, pull_corp_bond, pull_treasury
from finm.data.wrds._transform import corp_bond_to_long_format, treasury_to_long_format

FormatType = Literal["wide", "long"]
DatasetType = Literal["treasury", "corp_bond"]
TreasuryVariantType = Literal["daily", "info", "consolidated"]


def pull(
    data_dir: Path | str,
    variant: DatasetType,
    wrds_username: str,
    start_date: str | None = None,
    end_date: str | None = None,
    treasury_variant: TreasuryVariantType = "consolidated",
    with_runness: bool = True,
) -> pd.DataFrame:
    """Pull data from WRDS.

    Parameters
    ----------
    data_dir : Path or str
        Directory to save the data.
    variant : {"treasury", "corp_bond"}
        Which dataset to pull.
    wrds_username : str
        WRDS username.
    start_date : str, optional
        Start date in 'YYYY-MM-DD' format. Required for pulling data.
    end_date : str, optional
        End date in 'YYYY-MM-DD' format. Required for pulling data.
    treasury_variant : {"daily", "info", "consolidated"}, default "consolidated"
        For treasury data, which variant to pull.
    with_runness : bool, default True
        For consolidated treasury, whether to calculate runness.

    Returns
    -------
    pd.DataFrame
        Downloaded data.
    """
    if variant == "treasury":
        if treasury_variant != "info" and (not start_date or not end_date):
            raise ValueError("start_date and end_date required for treasury data")
        return pull_treasury(
            data_dir=data_dir,
            wrds_username=wrds_username,
            start_date=start_date or "",
            end_date=end_date or "",
            variant=treasury_variant,
            with_runness=with_runness,
        )
    elif variant == "corp_bond":
        if not start_date or not end_date:
            raise ValueError("start_date and end_date required for corp_bond data")
        return pull_corp_bond(
            data_dir=data_dir,
            wrds_username=wrds_username,
            start_date=start_date,
            end_date=end_date,
        )
    else:
        raise ValueError(f"variant must be 'treasury' or 'corp_bond', got '{variant}'")


def load(
    data_dir: Path | str,
    variant: DatasetType,
    format: FormatType = "wide",
    treasury_variant: TreasuryVariantType = "consolidated",
    with_runness: bool = True,
) -> pd.DataFrame:
    """Load WRDS data from local cache.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet files.
    variant : {"treasury", "corp_bond"}
        Which dataset to load.
    format : {"wide", "long"}, default "wide"
        Output format.
    treasury_variant : {"daily", "info", "consolidated"}, default "consolidated"
        For treasury data, which variant to load.
    with_runness : bool, default True
        For consolidated treasury, whether to load version with runness.

    Returns
    -------
    pd.DataFrame
        Loaded data.
    """
    if variant == "treasury":
        df = load_treasury(
            data_dir=data_dir,
            variant=treasury_variant,
            with_runness=with_runness,
        )
        if format == "long":
            df = treasury_to_long_format(df)
    elif variant == "corp_bond":
        df = load_corp_bond(data_dir=data_dir)
        if format == "long":
            df = corp_bond_to_long_format(df)
    else:
        raise ValueError(f"variant must be 'treasury' or 'corp_bond', got '{variant}'")

    return df


__all__ = [
    "pull",
    "load",
    "calc_runness",
    "treasury_to_long_format",
    "corp_bond_to_long_format",
]
