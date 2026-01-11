"""Load functions for Open Source Bond data.

Loads cached parquet files from the Open Source Bond Asset Pricing project.

Website: https://openbondassetpricing.com/
Data Dictionary: https://github.com/Alexander-M-Dickerson/trace-data-pipeline/blob/main/stage2/DATA_DICTIONARY.md
"""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Literal

import pandas as pd

from finm.data.open_source_bond._constants import DATA_INFO

VariantType = Literal["treasury", "corporate_daily", "corporate_monthly"]


def load_data(
    data_dir: Path | str,
    variant: VariantType = "treasury",
) -> pd.DataFrame:
    """Load Open Source Bond data from parquet.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet files.
    variant : {"treasury", "corporate_daily", "corporate_monthly"}
        Which dataset to load:
        - "treasury": Treasury bond returns
        - "corporate_daily": Daily corporate bond PRICES (not returns)
        - "corporate_monthly": Monthly corporate bond RETURNS with factor signals

    Returns
    -------
    pd.DataFrame
        Bond data.

    Notes
    -----
    - treasury and corporate_monthly contain RETURNS
    - corporate_daily contains PRICES (use price columns like 'pr', 'prc_vw_par')
    - corporate_monthly includes 108 factor signals for asset pricing research

    See Also
    --------
    https://openbondassetpricing.com/ : Official website
    https://github.com/Alexander-M-Dickerson/trace-data-pipeline : GitHub repo
    """
    data_dir = Path(data_dir)

    # Handle deprecated "corporate" variant
    if variant == "corporate":
        warnings.warn(
            "variant='corporate' is deprecated. Use 'corporate_monthly' for returns "
            "or 'corporate_daily' for prices. Defaulting to 'corporate_monthly'.",
            DeprecationWarning,
            stacklevel=2,
        )
        variant = "corporate_monthly"

    if variant not in DATA_INFO:
        valid_variants = list(DATA_INFO.keys())
        raise ValueError(
            f"variant must be one of {valid_variants}, got '{variant}'"
        )

    parquet_file = DATA_INFO[variant]["parquet"]
    parquet_path = data_dir / parquet_file

    if not parquet_path.exists():
        raise FileNotFoundError(
            f"Data file not found: {parquet_path}. "
            f"Run pull(data_dir, variant='{variant}', accept_license=True) first."
        )

    return pd.read_parquet(parquet_path)
