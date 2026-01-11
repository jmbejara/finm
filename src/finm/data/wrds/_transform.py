"""Transform functions for WRDS data."""

from __future__ import annotations

import pandas as pd


def treasury_to_long_format(
    df: pd.DataFrame,
    value_column: str = "price",
) -> pd.DataFrame:
    """Convert Treasury data to long format.

    Parameters
    ----------
    df : pd.DataFrame
        Treasury DataFrame with date and identifier columns.
    value_column : str, default "price"
        Column containing the value to use.

    Returns
    -------
    pd.DataFrame
        Long-format DataFrame with columns:
        - unique_id: Treasury identifier (kycrspid)
        - ds: Date
        - y: Value
    """
    id_col = "kycrspid" if "kycrspid" in df.columns else "tcusip"
    date_col = "caldt" if "caldt" in df.columns else df.columns[0]

    if value_column not in df.columns:
        raise ValueError(f"Column '{value_column}' not found in DataFrame")

    long_df = df[[id_col, date_col, value_column]].copy()
    long_df.columns = ["unique_id", "ds", "y"]

    # Drop NaN values
    long_df = long_df.dropna(subset=["y"])

    return long_df.reset_index(drop=True)


def corp_bond_to_long_format(
    df: pd.DataFrame,
    value_column: str = "ret_eom",
) -> pd.DataFrame:
    """Convert corporate bond data to long format.

    Parameters
    ----------
    df : pd.DataFrame
        Corporate bond DataFrame.
    value_column : str, default "ret_eom"
        Column containing the return value.

    Returns
    -------
    pd.DataFrame
        Long-format DataFrame with columns:
        - unique_id: Bond CUSIP
        - ds: Date
        - y: Return value
    """
    id_col = "cusip" if "cusip" in df.columns else "CUSIP"
    date_col = "date" if "date" in df.columns else "DATE"

    if value_column not in df.columns:
        raise ValueError(f"Column '{value_column}' not found in DataFrame")

    long_df = df[[id_col, date_col, value_column]].copy()
    long_df.columns = ["unique_id", "ds", "y"]

    # Drop NaN values
    long_df = long_df.dropna(subset=["y"])

    return long_df.reset_index(drop=True)
