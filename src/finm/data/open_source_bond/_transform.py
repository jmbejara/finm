"""Transform functions for Open Source Bond data.

Website: https://openbondassetpricing.com/
Data Dictionary: https://github.com/Alexander-M-Dickerson/trace-data-pipeline/blob/main/stage2/DATA_DICTIONARY.md
"""

from __future__ import annotations

from typing import Literal

import pandas as pd

from finm.data.open_source_bond._constants import DATA_INFO

VariantType = Literal["treasury", "corporate_daily", "corporate_monthly"]


def to_long_format(
    df: pd.DataFrame,
    id_column: str | None = None,
    date_column: str | None = None,
    value_column: str | None = None,
    variant: VariantType | None = None,
) -> pd.DataFrame:
    """Convert bond data to long format.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with bond data.
    id_column : str, optional
        Column to use as unique identifier. Auto-detected if variant provided.
    date_column : str, optional
        Column containing dates. Auto-detected if variant provided.
    value_column : str, optional
        Column containing values (returns or prices). Auto-detected if variant.
    variant : {"treasury", "corporate_daily", "corporate_monthly"}, optional
        Dataset variant for auto-detection of columns. If provided, column
        parameters are inferred from DATA_INFO.

    Returns
    -------
    pd.DataFrame
        Long-format DataFrame with columns:
        - unique_id: Bond identifier (e.g., CUSIP)
        - ds: Date
        - y: Value (return or price)

    Notes
    -----
    Column defaults by variant:
    - treasury: cusip, date, bond_ret
    - corporate_daily: cusip_id, trd_exctn_dt, pr
    - corporate_monthly: cusip, date, ret_vw

    Examples
    --------
    >>> df = load(data_dir, variant="corporate_monthly")
    >>> long_df = to_long_format(df, variant="corporate_monthly")
    """
    # Auto-detect columns based on variant
    if variant and variant in DATA_INFO:
        info = DATA_INFO[variant]
        id_column = id_column or info.get("id_column", "cusip")
        date_column = date_column or info.get("date_column", "date")
        value_column = value_column or info.get("value_column", "bond_ret")
    else:
        # Defaults for backward compatibility
        id_column = id_column or "cusip"
        date_column = date_column or "date"
        value_column = value_column or "bond_ret"

    # Validation
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
