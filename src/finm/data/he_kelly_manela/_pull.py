"""Pull functions for He-Kelly-Manela factor data.

Website: https://asaf.manela.org/papers/hkm/intermediarycapitalrisk/
Paper: https://doi.org/10.1016/j.jfineco.2017.08.002
"""

from __future__ import annotations

import zipfile
from io import BytesIO
from pathlib import Path

import requests
import urllib3

from finm.data.he_kelly_manela._constants import DATA_URL, LICENSE_INFO

# Suppress SSL warnings when verify=False (required for this data source)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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


def pull_data(data_dir: Path | str, accept_license: bool = False) -> None:
    """Download He-Kelly-Manela factors and test portfolios.

    Downloads a zip file containing the HKM factors and extracts it
    to the specified directory.

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
    _check_license_accepted(accept_license)

    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    # Download zip file (SSL verification disabled due to certificate issues)
    response = requests.get(DATA_URL, verify=False)
    response.raise_for_status()

    # Extract zip contents
    zip_file = BytesIO(response.content)
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(data_dir)
