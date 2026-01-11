"""Transform functions for Fama-French factor data."""

from __future__ import annotations

import pandas as pd


def to_long_format(df: pd.DataFrame) -> pd.DataFrame:
    """Convert Fama-French factors from wide to long format.

    Parameters
    ----------
    df : pd.DataFrame
        Wide-format DataFrame with date index and factor columns.

    Returns
    -------
    pd.DataFrame
        Long-format DataFrame with columns:
        - unique_id: Factor name (e.g., "Mkt-RF", "SMB", "HML", "RF")
        - ds: Date
        - y: Factor value
    """
    # Reset index to make date a column
    df_reset = df.reset_index()
    date_col = df_reset.columns[0]  # First column is the date index

    # Melt from wide to long
    long_df = df_reset.melt(
        id_vars=[date_col],
        var_name="unique_id",
        value_name="y",
    )

    # Rename date column to ds
    long_df = long_df.rename(columns={date_col: "ds"})

    # Reorder columns
    long_df = long_df[["unique_id", "ds", "y"]]

    # Drop NaN values
    long_df = long_df.dropna(subset=["y"])

    return long_df.reset_index(drop=True)
