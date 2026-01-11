"""He-Kelly-Manela intermediary factor data module.

Provides access to intermediary capital risk factors from
He, Kelly, and Manela (2017).

Website: https://asaf.manela.org/papers/hkm/intermediarycapitalrisk/
Paper: https://doi.org/10.1016/j.jfineco.2017.08.002

Standard interface:
    - pull(data_dir, accept_license): Download data from source
    - load(data_dir, variant, format): Load cached data
    - to_long_format(df): Convert to long format

License:
    Academic (no explicit license). Please cite the paper.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pandas as pd

from finm.data.he_kelly_manela._constants import LICENSE_INFO
from finm.data.he_kelly_manela._load import load_data
from finm.data.he_kelly_manela._pull import pull_data
from finm.data.he_kelly_manela._transform import to_long_format

FormatType = Literal["wide", "long"]
VariantType = Literal["factors_monthly", "factors_daily", "all"]


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
) -> pd.DataFrame:
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

    Returns
    -------
    pd.DataFrame
        Factor data.
    """
    df = load_data(data_dir=data_dir, variant=variant)

    if format == "long":
        df = to_long_format(df)

    return df


__all__ = ["pull", "load", "to_long_format"]
