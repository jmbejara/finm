"""Pull functions for Open Source Bond data.

Downloads data from the Open Source Bond Asset Pricing project.

Website: https://openbondassetpricing.com/
GitHub: https://github.com/Alexander-M-Dickerson/trace-data-pipeline
"""

from __future__ import annotations

import os
import warnings
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Literal

import pandas as pd
import requests

from finm.data.open_source_bond._constants import (
    DATA_INFO,
    LICENSE_INFO,
    MIN_N_ROWS_EXPECTED,
)

VariantType = Literal["treasury", "corporate_daily", "corporate_monthly"]
PullVariantType = Literal[
    "treasury", "corporate_daily", "corporate_monthly", "corporate_all", "all"
]


def _check_license_accepted(accept_license: bool) -> None:
    """Check if the user has accepted the license terms.

    Parameters
    ----------
    accept_license : bool
        Whether the user has accepted the license terms.

    Raises
    ------
    ValueError
        If accept_license is False.
    """
    if not accept_license:
        msg = (
            f"\n{'='*70}\n"
            f"DATA LICENSE ACKNOWLEDGMENT REQUIRED\n"
            f"{'='*70}\n"
            f"Source: {LICENSE_INFO['terms_url']}\n"
            f"License: {LICENSE_INFO['license_type']}\n"
            f"License URL: {LICENSE_INFO['license_url']}\n"
            f"\n{LICENSE_INFO['disclaimer']}\n"
            f"\nCitation:\n{LICENSE_INFO['citation']}\n"
            f"\nTo proceed, set accept_license=True\n"
            f"{'='*70}\n"
        )
        raise ValueError(msg)


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
    response = requests.get(url, timeout=300)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path


def _download_and_extract_zip_parquet(
    url: str,
    output_dir: Path,
    expected_parquet: str,
    expected_readme: str | None = None,
) -> tuple[Path, Path | None]:
    """Download ZIP file and extract parquet (and optionally README).

    Parameters
    ----------
    url : str
        URL to download from.
    output_dir : Path
        Directory to extract files to.
    expected_parquet : str
        Expected parquet filename inside ZIP.
    expected_readme : str, optional
        Expected README filename inside ZIP.

    Returns
    -------
    tuple[Path, Path | None]
        (parquet_path, readme_path) - paths to extracted files.
    """
    print(f"Downloading from {url}...")
    response = requests.get(url, timeout=600)
    response.raise_for_status()

    print("Extracting ZIP contents...")
    zip_file = BytesIO(response.content)
    readme_path = None

    with zipfile.ZipFile(zip_file, "r") as zf:
        if expected_parquet not in zf.namelist():
            available = ", ".join(zf.namelist())
            raise ValueError(
                f"Expected {expected_parquet} not found in ZIP. "
                f"Available files: {available}"
            )
        zf.extract(expected_parquet, output_dir)
        parquet_path = output_dir / expected_parquet

        if expected_readme and expected_readme in zf.namelist():
            zf.extract(expected_readme, output_dir)
            readme_path = output_dir / expected_readme

    return parquet_path, readme_path


def _load_and_validate_csv(
    csv_path: Path, min_rows: int = 500, check_n_rows: bool = True
) -> pd.DataFrame:
    """Load CSV and validate row count.

    Parameters
    ----------
    csv_path : Path
        Path to CSV file.
    min_rows : int, default 500
        Minimum expected row count.
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

    if check_n_rows and len(df) < min_rows:
        raise ValueError(
            f"Expected at least {min_rows} rows, but found {len(df)}. "
            "Validate the csv file or set 'check_n_rows=False'."
        )

    return df


def _validate_parquet(parquet_path: Path, min_rows: int) -> None:
    """Validate parquet file has minimum expected rows.

    Parameters
    ----------
    parquet_path : Path
        Path to parquet file.
    min_rows : int
        Minimum expected row count.

    Raises
    ------
    ValueError
        If row count is below minimum.
    """
    df = pd.read_parquet(parquet_path)
    if len(df) < min_rows:
        raise ValueError(
            f"Expected at least {min_rows} rows, but found {len(df)}. "
            "Data file may be corrupted or incomplete."
        )


def _pull_csv_dataset(
    data_dir: Path,
    info: dict,
    download_readme: bool = True,
) -> None:
    """Pull a CSV-based dataset (treasury).

    Parameters
    ----------
    data_dir : Path
        Directory to save data.
    info : dict
        Dataset info from DATA_INFO.
    download_readme : bool, default True
        Whether to download README.
    """
    print(f"Downloading {info['csv']}...")
    csv_path = data_dir / info["csv"]
    _download_file(info["url"], csv_path)

    min_rows = MIN_N_ROWS_EXPECTED.get("treasury", 500)
    df = _load_and_validate_csv(csv_path, min_rows=min_rows)

    parquet_path = data_dir / info["parquet"]
    df.to_parquet(parquet_path)
    print(f"Saved to {parquet_path}")

    os.remove(csv_path)

    if download_readme and "readme_url" in info:
        readme_path = data_dir / info["readme_file"]
        print(f"Downloading README to {readme_path}...")
        _download_file(info["readme_url"], readme_path)


def _pull_zip_parquet_dataset(
    data_dir: Path,
    variant_name: str,
    info: dict,
    download_readme: bool = True,
) -> None:
    """Pull a ZIP-containing-parquet dataset (corporate).

    Parameters
    ----------
    data_dir : Path
        Directory to save data.
    variant_name : str
        Name of the variant (for min_rows lookup).
    info : dict
        Dataset info from DATA_INFO.
    download_readme : bool, default True
        Whether to save README if present in ZIP.
    """
    extracted_parquet, extracted_readme = _download_and_extract_zip_parquet(
        url=info["url"],
        output_dir=data_dir,
        expected_parquet=info["zip_contents"],
        expected_readme=info.get("readme_contents") if download_readme else None,
    )

    min_rows = MIN_N_ROWS_EXPECTED.get(variant_name, 500)
    _validate_parquet(extracted_parquet, min_rows)

    final_parquet_path = data_dir / info["parquet"]
    if extracted_parquet != final_parquet_path:
        extracted_parquet.rename(final_parquet_path)
    print(f"Saved to {final_parquet_path}")

    if extracted_readme and "readme_file" in info:
        final_readme_path = data_dir / info["readme_file"]
        if extracted_readme != final_readme_path:
            extracted_readme.rename(final_readme_path)
        print(f"Saved README to {final_readme_path}")


def pull_data(
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
        - "corporate_daily": Daily corporate bond prices, TRACE Stage 1 (~1.8GB)
        - "corporate_monthly": Monthly returns with 108 factor signals (~1.2GB)
        - "corporate_all": Both corporate datasets
        - "all": All datasets (treasury + corporate_daily + corporate_monthly)
    accept_license : bool, default False
        Must be set to True to acknowledge the data provider's license terms.
        The data is provided under the MIT License. See LICENSE_INFO for details.
    download_readme : bool, default True
        Whether to save README files when available.

    Returns
    -------
    None

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
        The Corporate Bond Factor Replication Crisis: A New Protocol. Working Paper.
    """
    _check_license_accepted(accept_license)

    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    # Handle deprecated "corporate" variant
    if variant == "corporate":
        warnings.warn(
            "variant='corporate' is deprecated. Use 'corporate_monthly' for returns "
            "or 'corporate_daily' for prices. Defaulting to 'corporate_monthly'.",
            DeprecationWarning,
            stacklevel=2,
        )
        variant = "corporate_monthly"

    # Determine which datasets to download
    if variant == "all":
        datasets = ["treasury", "corporate_daily", "corporate_monthly"]
    elif variant == "corporate_all":
        datasets = ["corporate_daily", "corporate_monthly"]
    else:
        datasets = [variant]

    for dataset_name in datasets:
        if dataset_name not in DATA_INFO:
            valid_variants = list(DATA_INFO.keys())
            raise ValueError(
                f"Unknown variant '{dataset_name}'. Valid variants: {valid_variants}"
            )

        info = DATA_INFO[dataset_name]
        source_format = info.get("source_format", "csv")

        print(f"\n--- Pulling {dataset_name} ---")

        if source_format == "csv":
            _pull_csv_dataset(data_dir, info, download_readme)
        elif source_format == "zip_parquet":
            _pull_zip_parquet_dataset(data_dir, dataset_name, info, download_readme)
        else:
            raise ValueError(f"Unknown source_format: {source_format}")

    print("\nDone!")
