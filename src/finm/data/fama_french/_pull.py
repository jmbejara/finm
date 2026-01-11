"""Pull functions for Fama-French factor data.

Website: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
"""

from __future__ import annotations

import logging
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Literal

import pandas as pd

from finm.data.fama_french._constants import (
    BUNDLED_CSV,
    BUNDLED_DATA_DIR,
    DATASET_DAILY,
    DATASET_MONTHLY,
    LICENSE_INFO,
)

if TYPE_CHECKING:
    from datetime import datetime

# Try to import pandas_datareader (optional dependency)
try:
    import pandas_datareader.data as web

    HAS_DATAREADER = True
except ModuleNotFoundError as e:
    if "No module named 'distutils'" in str(e):
        warnings.warn(
            "Could not import pandas_datareader due to missing distutils. "
            "Please install setuptools package.",
            stacklevel=2,
        )
    HAS_DATAREADER = False
    web = None

# Suppress FutureWarning about date_parser from pandas_datareader
warnings.filterwarnings("ignore", category=FutureWarning, message=".*date_parser.*")

FrequencyType = Literal["daily", "monthly"]


def _check_license_accepted(accept_license: bool) -> None:
    """Check if the user has accepted the license terms."""
    if not accept_license:
        msg = (
            f"\n{'='*70}\n"
            f"DATA LICENSE ACKNOWLEDGMENT REQUIRED\n"
            f"{'='*70}\n"
            f"Source: {LICENSE_INFO['terms_url']}\n"
            f"License: {LICENSE_INFO['license_type']}\n"
            f"\n{LICENSE_INFO['disclaimer']}\n"
            f"\nCitation:\n{LICENSE_INFO['citation']}\n"
            f"\nTo proceed, set accept_license=True\n"
            f"{'='*70}\n"
        )
        raise ValueError(msg)


def pull_data(
    data_dir: Path | str,
    start: str | datetime | None = None,
    end: str | datetime | None = None,
    frequency: FrequencyType = "daily",
    accept_license: bool = False,
) -> pd.DataFrame:
    """Download Fama-French factors from Ken French's Data Library.

    Requires pandas_datareader to be installed.

    Website: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

    Parameters
    ----------
    data_dir : Path or str
        Directory to save downloaded data.
    start : str or datetime, optional
        Start date of the data. Format: 'YYYY-MM-DD'.
    end : str or datetime, optional
        End date of the data. Format: 'YYYY-MM-DD'.
    frequency : {"daily", "monthly"}, default "daily"
        Data frequency.
    accept_license : bool, default False
        Must be set to True to acknowledge the data provider's terms.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the factors (as decimals, not percentages):
        - Mkt-RF: Excess return on the market
        - SMB: Small Minus Big (size factor)
        - HML: High Minus Low (value factor)
        - RF: Risk-free rate

    Raises
    ------
    ValueError
        If accept_license is False.
    ImportError
        If pandas_datareader is not installed.
    ValueError
        If frequency is not "daily" or "monthly".
    """
    _check_license_accepted(accept_license)

    if not HAS_DATAREADER or web is None:
        raise ImportError(
            "pandas_datareader is required to pull live Fama-French data. "
            "Install with: pip install pandas-datareader"
        )

    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    if frequency == "daily":
        dataset_name = DATASET_DAILY
    elif frequency == "monthly":
        dataset_name = DATASET_MONTHLY
    else:
        raise ValueError(f"frequency must be 'daily' or 'monthly', got '{frequency}'")

    logging.info(f"Downloading {dataset_name} from Ken French Data Library...")
    ff_factors = web.DataReader(dataset_name, "famafrench", start=start, end=end)

    # First table contains the factors; convert from percentage to decimal
    df = pd.DataFrame(ff_factors[0]).div(100)

    # Save to CSV (to match existing bundled format)
    output_path = data_dir / f"ff3factors_{frequency}.csv"
    df.to_csv(output_path)

    # Also update the bundled data if saving daily factors
    if frequency == "daily":
        bundled_path = BUNDLED_DATA_DIR / BUNDLED_CSV
        df.to_csv(bundled_path)

    return df
