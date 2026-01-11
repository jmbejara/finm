"""Load functions for He-Kelly-Manela factor data."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pandas as pd

from finm.data.he_kelly_manela._constants import CSV_ALL, CSV_DAILY, CSV_MONTHLY

VariantType = Literal["factors_monthly", "factors_daily", "all"]


def load_data(
    data_dir: Path | str,
    variant: VariantType = "factors_monthly",
) -> pd.DataFrame:
    """Load He-Kelly-Manela factor data from CSV.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the CSV files.
    variant : {"factors_monthly", "factors_daily", "all"}, default "factors_monthly"
        Which dataset variant to load:
        - "factors_monthly": Monthly factor data
        - "factors_daily": Daily factor data
        - "all": Factors and test assets (monthly)

    Returns
    -------
    pd.DataFrame
        Factor data with parsed date column.
    """
    data_dir = Path(data_dir)

    if variant == "factors_monthly":
        path = data_dir / CSV_MONTHLY
        df = pd.read_csv(path)
        df["date"] = pd.to_datetime(df["yyyymm"], format="%Y%m")
    elif variant == "factors_daily":
        path = data_dir / CSV_DAILY
        df = pd.read_csv(path)
        df["date"] = pd.to_datetime(df["yyyymmdd"], format="%Y%m%d")
    elif variant == "all":
        path = data_dir / CSV_ALL
        df = pd.read_csv(path)
        df["date"] = pd.to_datetime(df["yyyymm"], format="%Y%m")
    else:
        raise ValueError(
            f"variant must be 'factors_monthly', 'factors_daily', or 'all', got '{variant}'"
        )

    return df
