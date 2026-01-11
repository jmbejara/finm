"""He-Kelly-Manela intermediary factor data module.

Provides access to intermediary capital risk factors from
He, Kelly, and Manela (2017).

Website: https://asaf.manela.org/papers/hkm/intermediarycapitalrisk/
Paper: https://doi.org/10.1016/j.jfineco.2017.08.002

Standard interface:
    - pull(data_dir, accept_license): Download data from source
    - load(data_dir, variant, format): Load cached data (returns polars)
    - to_long_format(df): Convert to long format

License:
    Academic (no explicit license). Please cite the paper.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal, Union

import pandas as pd
import polars as pl

from finm.data.he_kelly_manela._constants import (
    CSV_ALL,
    CSV_DAILY,
    CSV_MONTHLY,
    LICENSE_INFO,
)
from finm.data.he_kelly_manela._load import load_data
from finm.data.he_kelly_manela._pull import pull_data
from finm.data.he_kelly_manela._transform import to_long_format

FormatType = Literal["wide", "long"]
VariantType = Literal["factors_monthly", "factors_daily", "all"]

# Map variant to expected file
_VARIANT_FILES = {
    "factors_monthly": CSV_MONTHLY,
    "factors_daily": CSV_DAILY,
    "all": CSV_ALL,
}


def pull(data_dir: Path | str, accept_license: bool = False) -> None:
    """Download He-Kelly-Manela factors and test portfolios.

    Downloads a zip file containing the HKM factors and extracts it.

    Website: https://asaf.manela.org/papers/hkm/intermediarycapitalrisk/

    Parameters
    ----------
    data_dir : Path or str
        Directory to save extracted data.
    accept_license : bool, default False
        Must be set to True to acknowledge the data provider's terms.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If accept_license is False.
    """
    return pull_data(data_dir=data_dir, accept_license=accept_license)


def load(
    data_dir: Path | str,
    variant: VariantType = "factors_monthly",
    format: FormatType = "wide",
    pull_if_not_found: bool = False,
    accept_license: bool = False,
    lazy: bool = False,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    """Load He-Kelly-Manela factor data.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the CSV files.
    variant : {"factors_monthly", "factors_daily", "all"}, default "factors_monthly"
        Which dataset variant to load:
        - "factors_monthly": Monthly factor data
        - "factors_daily": Daily factor data
        - "all": Factors and test assets (monthly)
    format : {"wide", "long"}, default "wide"
        Output format:
        - "wide": Original format with factor columns
        - "long": Melted format with [unique_id, ds, y] columns
    pull_if_not_found : bool, default False
        If True and data doesn't exist locally, pull from source.
        Requires accept_license=True.
    accept_license : bool, default False
        Must be True when pull_if_not_found=True.
    lazy : bool, default False
        If True, return a polars LazyFrame instead of DataFrame.

    Returns
    -------
    pl.DataFrame or pl.LazyFrame
        Factor data as polars DataFrame (default) or LazyFrame.

    Raises
    ------
    ValueError
        If pull_if_not_found=True but accept_license=False.
    """
    from finm.data._utils import pandas_to_polars

    data_path = Path(data_dir)
    expected_file = _VARIANT_FILES[variant]

    # Handle pull_if_not_found
    if pull_if_not_found:
        if not accept_license:
            raise ValueError(
                "When pull_if_not_found=True, accept_license must also be True. "
                "This acknowledges the data provider's license terms."
            )
        if not (data_path / expected_file).exists():
            pull_data(data_dir=data_dir, accept_license=True)

    # Load data (internally uses pandas)
    df = load_data(data_dir=data_dir, variant=variant)

    if format == "long":
        df = to_long_format(df)

    # Convert to polars
    return pandas_to_polars(df, lazy=lazy)


__all__ = ["pull", "load", "to_long_format", "LICENSE_INFO"]
