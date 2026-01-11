"""Pull functions for Open Source Bond data."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

import pandas as pd
import requests

from finm.data.open_source_bond._constants import DATA_INFO, MIN_N_ROWS_EXPECTED

VariantType = Literal["treasury", "corporate", "all"]


def _download_file(url: str, output_path: Path) -> Path:
    """Download a file from URL.

    Parameters
    ----------
    url : str
        URL to download from.
    output_path : Path
        Path to save the file.

    Returns
    -------
    Path
        Path to downloaded file.
    """
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path


def _load_and_validate_csv(csv_path: Path, check_n_rows: bool = True) -> pd.DataFrame:
    """Load CSV and validate row count.

    Parameters
    ----------
    csv_path : Path
        Path to CSV file.
    check_n_rows : bool, default True
        Whether to validate minimum row count.

    Returns
    -------
    pd.DataFrame
        Loaded DataFrame.
    """
    df = pd.read_csv(csv_path)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    if check_n_rows and len(df) < MIN_N_ROWS_EXPECTED:
        raise ValueError(
            f"Expected at least {MIN_N_ROWS_EXPECTED} rows, but found {len(df)}. "
            "Validate the csv file or set 'check_n_rows=False'."
        )

    return df


def pull_data(
    data_dir: Path | str,
    variant: VariantType = "all",
    download_readme: bool = True,
) -> None:
    """Download Open Source Bond data.

    Parameters
    ----------
    data_dir : Path or str
        Directory to save downloaded data.
    variant : {"treasury", "corporate", "all"}, default "all"
        Which dataset(s) to download:
        - "treasury": Treasury bond returns only
        - "corporate": Corporate bond returns only
        - "all": Both datasets
    download_readme : bool, default True
        Whether to also download the README PDF files.

    Returns
    -------
    None
    """
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    # Determine which datasets to download
    if variant == "all":
        datasets = ["treasury", "corporate"]
    else:
        datasets = [variant]

    for dataset_name in datasets:
        info = DATA_INFO[dataset_name]

        # Download CSV
        csv_path = data_dir / info["csv"]
        _download_file(info["url"], csv_path)

        # Load, validate, and convert to parquet
        df = _load_and_validate_csv(csv_path)
        df.to_parquet(data_dir / info["parquet"])

        # Remove CSV after conversion
        os.remove(csv_path)

        # Download README if requested
        if download_readme:
            readme_filename = info["parquet"].replace(".parquet", "_README.pdf")
            _download_file(info["readme"], data_dir / readme_filename)
