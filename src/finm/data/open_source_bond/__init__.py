"""Open Source Bond Asset Pricing data module.

Provides access to treasury and corporate bond returns from
the Open Bond Asset Pricing project.

Standard interface:
    - pull(data_dir, variant): Download data from source
    - load(data_dir, variant, format): Load cached data
    - to_long_format(df): Convert to long format
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pandas as pd

from finm.data.open_source_bond._load import load_data
from finm.data.open_source_bond._pull import pull_data
from finm.data.open_source_bond._transform import (
    portfolio_to_long_format,
    to_long_format,
)

FormatType = Literal["wide", "long"]
VariantType = Literal["treasury", "corporate"]
PullVariantType = Literal["treasury", "corporate", "all"]


def pull(
    data_dir: Path | str,
    variant: PullVariantType = "all",
    download_readme: bool = True,
) -> None:
    """Download Open Source Bond data.

    Parameters
    ----------
    data_dir : Path or str
        Directory to save downloaded data.
    variant : {"treasury", "corporate", "all"}, default "all"
        Which dataset(s) to download.
    download_readme : bool, default True
        Whether to also download the README PDF files.

    Returns
    -------
    None
    """
    return pull_data(
        data_dir=data_dir,
        variant=variant,
        download_readme=download_readme,
    )


def load(
    data_dir: Path | str,
    variant: VariantType = "treasury",
    format: FormatType = "wide",
) -> pd.DataFrame:
    """Load Open Source Bond data.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet files.
    variant : {"treasury", "corporate"}, default "treasury"
        Which dataset to load.
    format : {"wide", "long"}, default "wide"
        Output format:
        - "wide": Original format
        - "long": Melted format with [unique_id, ds, y] columns

    Returns
    -------
    pd.DataFrame
        Bond returns data.
    """
    df = load_data(data_dir=data_dir, variant=variant)

    if format == "long":
        # Use appropriate columns based on variant
        if variant == "corporate":
            df = to_long_format(df, id_column="cusip", value_column="bond_ret")
        else:
            # Treasury data may have different column structure
            df = to_long_format(df)

    return df


__all__ = ["pull", "load", "to_long_format", "portfolio_to_long_format"]
