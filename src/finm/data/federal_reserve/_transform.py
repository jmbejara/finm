"""Transform functions for Federal Reserve yield curve data."""

from __future__ import annotations

import pandas as pd


def to_long_format(df: pd.DataFrame) -> pd.DataFrame:
    """Convert yield curve data from wide to long format.

    Transforms the wide-format yield curve data (columns for each maturity)
    into long format suitable for time series analysis.

    Parameters
    ----------
    df : pd.DataFrame
        Wide-format DataFrame with date index and yield columns (e.g., SVENY01-SVENY30).

    Returns
    -------
    pd.DataFrame
        Long-format DataFrame with columns:
        - unique_id: Yield column name (e.g., "SVENY01")
        - ds: Date
        - y: Yield value
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
