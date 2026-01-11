"""Transform functions for Open Source Bond data."""

from __future__ import annotations

import pandas as pd


def to_long_format(
    df: pd.DataFrame,
    id_column: str = "cusip",
    date_column: str = "date",
    value_column: str = "bond_ret",
) -> pd.DataFrame:
    """Convert bond returns data to long format.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with bond returns data.
    id_column : str, default "cusip"
        Column to use as unique identifier.
    date_column : str, default "date"
        Column containing dates.
    value_column : str, default "bond_ret"
        Column containing return values.

    Returns
    -------
    pd.DataFrame
        Long-format DataFrame with columns:
        - unique_id: Bond identifier (e.g., CUSIP)
        - ds: Date
        - y: Return value
    """
    # Select relevant columns
    if id_column not in df.columns:
        raise ValueError(f"Column '{id_column}' not found in DataFrame")
    if date_column not in df.columns:
        raise ValueError(f"Column '{date_column}' not found in DataFrame")
    if value_column not in df.columns:
        raise ValueError(f"Column '{value_column}' not found in DataFrame")

    long_df = df[[id_column, date_column, value_column]].copy()
    long_df.columns = ["unique_id", "ds", "y"]

    # Drop NaN values
    long_df = long_df.dropna(subset=["y"])

    return long_df.reset_index(drop=True)


def portfolio_to_long_format(df: pd.DataFrame) -> pd.DataFrame:
    """Convert portfolio returns from wide to long format.

    Parameters
    ----------
    df : pd.DataFrame
        Wide-format DataFrame with date index and portfolio columns.

    Returns
    -------
    pd.DataFrame
        Long-format DataFrame with columns:
        - unique_id: Portfolio name
        - ds: Date
        - y: Return value
    """
    # Reset index to make date a column
    df_reset = df.reset_index()
    date_col = df_reset.columns[0]

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
