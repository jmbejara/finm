"""Transform functions for He-Kelly-Manela factor data."""

from __future__ import annotations

import pandas as pd

from finm.data.he_kelly_manela._constants import FACTOR_COLUMNS


def to_long_format(df: pd.DataFrame) -> pd.DataFrame:
    """Convert He-Kelly-Manela factors from wide to long format.

    Parameters
    ----------
    df : pd.DataFrame
        Wide-format DataFrame with date column and factor columns.

    Returns
    -------
    pd.DataFrame
        Long-format DataFrame with columns:
        - unique_id: Factor name
        - ds: Date
        - y: Factor value
    """
    # Determine which factor columns are present
    available_columns = [col for col in FACTOR_COLUMNS if col in df.columns]

    if not available_columns:
        raise ValueError(f"No factor columns found. Expected one of: {FACTOR_COLUMNS}")

    # Melt from wide to long
    long_df = df.melt(
        id_vars=["date"],
        value_vars=available_columns,
        var_name="unique_id",
        value_name="y",
    )

    # Rename date column to ds
    long_df = long_df.rename(columns={"date": "ds"})

    # Reorder columns
    long_df = long_df[["unique_id", "ds", "y"]]

    # Drop NaN values
    long_df = long_df.dropna(subset=["y"])

    return long_df.reset_index(drop=True)
