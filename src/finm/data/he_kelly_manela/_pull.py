"""Pull functions for He-Kelly-Manela factor data."""

from __future__ import annotations

import zipfile
from io import BytesIO
from pathlib import Path

import requests
import urllib3

from finm.data.he_kelly_manela._constants import DATA_URL

# Suppress SSL warnings when verify=False (required for this data source)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def pull_data(data_dir: Path | str) -> None:
    """Download He-Kelly-Manela factors and test portfolios.

    Downloads a zip file containing the HKM factors and extracts it
    to the specified directory.

    Parameters
    ----------
    data_dir : Path or str
        Directory to save extracted data.

    Returns
    -------
    None
    """
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    # Download zip file (SSL verification disabled due to certificate issues)
    response = requests.get(DATA_URL, verify=False)
    response.raise_for_status()

    # Extract zip contents
    zip_file = BytesIO(response.content)
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(data_dir)
