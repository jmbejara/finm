"""Open Source Bond Asset Pricing data module.

Provides access to treasury and corporate bond data from the Open Bond Asset
Pricing project.

Website: https://openbondassetpricing.com/
GitHub: https://github.com/Alexander-M-Dickerson/trace-data-pipeline
Data Dictionary: https://github.com/Alexander-M-Dickerson/trace-data-pipeline/blob/main/stage2/DATA_DICTIONARY.md

Available datasets:
    - treasury: Treasury bond returns (daily)
    - corporate_daily: Corporate bond PRICES from TRACE Stage 1 (~29.8M rows)
    - corporate_monthly: Corporate bond RETURNS with 108 factor signals (~1.86M rows)

Standard interface:
    - pull(data_dir, variant, accept_license): Download data from source
    - load(data_dir, variant, format): Load cached data (returns polars)
    - to_long_format(df, variant): Convert to long format

License:
    MIT License. See LICENSE_INFO for citation requirements.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal, Union

import pandas as pd
import polars as pl

from finm.data.open_source_bond._constants import (
    DATA_INFO,
    DOCUMENTATION,
    LICENSE_INFO,
)
from finm.data.open_source_bond._load import load_data
from finm.data.open_source_bond._pull import pull_data
from finm.data.open_source_bond._transform import (
    portfolio_to_long_format,
    to_long_format,
)

FormatType = Literal["wide", "long"]
VariantType = Literal["treasury", "corporate_daily", "corporate_monthly"]
PullVariantType = Literal[
    "treasury", "corporate_daily", "corporate_monthly", "corporate_all", "all"
]


def pull(
    data_dir: Path | str,
    variant: PullVariantType = "all",
    accept_license: bool = False,
    download_readme: bool = True,
) -> None:
    """Download Open Source Bond data.

    Downloads data from the Open Source Bond Asset Pricing project.

    Website: https://openbondassetpricing.com/
    Data Dictionary: https://github.com/Alexander-M-Dickerson/trace-data-pipeline/blob/main/stage2/DATA_DICTIONARY.md

    Parameters
    ----------
    data_dir : Path or str
        Directory to save downloaded data.
    variant : str
        Which dataset(s) to download. One of:
        - "treasury": Treasury bond returns (CSV, ~120MB)
        - "corporate_daily": Daily corporate bond PRICES (~1.8GB ZIP)
        - "corporate_monthly": Monthly RETURNS with 108 factor signals (~1.2GB)
        - "corporate_all": Both corporate datasets
        - "all": All datasets
    accept_license : bool, default False
        Must be set to True to acknowledge the data provider's license terms.
        The data is provided under the MIT License. Citation is required.
    download_readme : bool, default True
        Whether to save README files when available.

    Raises
    ------
    ValueError
        If accept_license is False.

    Notes
    -----
    - corporate_daily contains PRICES (not returns)
    - corporate_monthly contains RETURNS (ready to use)
    - corporate_monthly includes 108 factor signals for asset pricing research

    Citation:
        Dickerson, A., Robotti, C., & Rossetti, G. (2026).
        The Corporate Bond Factor Replication Crisis: A New Protocol.
    """
    return pull_data(
        data_dir=data_dir,
        variant=variant,
        accept_license=accept_license,
        download_readme=download_readme,
    )


def load(
    data_dir: Path | str,
    variant: VariantType = "treasury",
    format: FormatType = "wide",
    pull_if_not_found: bool = False,
    accept_license: bool = False,
    lazy: bool = False,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    """Load Open Source Bond data.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet files.
    variant : {"treasury", "corporate_daily", "corporate_monthly"}
        Which dataset to load:
        - "treasury": Treasury bond returns
        - "corporate_daily": Daily corporate bond PRICES (not returns)
        - "corporate_monthly": Monthly corporate bond RETURNS with factor signals
    format : {"wide", "long"}, default "wide"
        Output format:
        - "wide": Original format with all columns
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
        Bond data as polars DataFrame (default) or LazyFrame.

    Notes
    -----
    - treasury and corporate_monthly contain RETURNS
    - corporate_daily contains PRICES (columns: pr, prc_vw_par, etc.)
    - corporate_monthly has return column 'ret_vw' (volume-weighted)

    Key columns by variant:
        treasury: cusip, date, bond_ret
        corporate_daily: cusip_id, trd_exctn_dt, pr
        corporate_monthly: cusip, date, ret_vw, rfret, tret, + 108 factor signals

    Raises
    ------
    ValueError
        If pull_if_not_found=True but accept_license=False.

    See Also
    --------
    https://openbondassetpricing.com/ : Official website
    """
    from finm.data._utils import pandas_to_polars

    data_path = Path(data_dir)
    expected_file = DATA_INFO[variant]["parquet"]

    # Handle pull_if_not_found
    if pull_if_not_found:
        if not accept_license:
            raise ValueError(
                "When pull_if_not_found=True, accept_license must also be True. "
                "This acknowledges the data provider's license terms."
            )
        if not (data_path / expected_file).exists():
            pull_data(data_dir=data_dir, variant=variant, accept_license=True)

    # Load data (internally uses pandas)
    df = load_data(data_dir=data_dir, variant=variant)

    if format == "long":
        df = to_long_format(df, variant=variant)

    # Convert to polars
    return pandas_to_polars(df, lazy=lazy)


__all__ = [
    "pull",
    "load",
    "to_long_format",
    "portfolio_to_long_format",
    "DATA_INFO",
    "DOCUMENTATION",
    "LICENSE_INFO",
]
