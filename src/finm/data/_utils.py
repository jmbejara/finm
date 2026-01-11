"""Shared utilities for data module."""

from __future__ import annotations

from typing import Union

import pandas as pd
import polars as pl


def pandas_to_polars(
    df: pd.DataFrame,
    lazy: bool = False,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    """Convert pandas DataFrame to polars DataFrame or LazyFrame.

    Handles DatetimeIndex by resetting it to a column.

    Parameters
    ----------
    df : pd.DataFrame
        Input pandas DataFrame.
    lazy : bool, default False
        If True, return a LazyFrame instead of DataFrame.

    Returns
    -------
    pl.DataFrame or pl.LazyFrame
        Polars DataFrame (default) or LazyFrame.
    """
    if isinstance(df.index, pd.DatetimeIndex):
        df = df.reset_index()
    elif df.index.name is not None:
        df = df.reset_index()

    result = pl.from_pandas(df)

    if lazy:
        return result.lazy()
    return result
