"""Constants for WRDS data module.

Data from Wharton Research Data Services (WRDS).

Website: https://wrds-www.wharton.upenn.edu/
"""

from typing import Final

DATASET_NAME: Final[str] = "wrds"
DISPLAY_NAME: Final[str] = "WRDS Financial Data"

# License and citation information
LICENSE_INFO: Final[dict] = {
    "license_type": "Subscription-based",
    "license_url": "https://wrds-www.wharton.upenn.edu/",
    "citation": (
        "Wharton Research Data Services (WRDS). "
        "https://wrds-www.wharton.upenn.edu/"
    ),
    "terms_url": "https://wrds-www.wharton.upenn.edu/",
    "disclaimer": (
        "This data requires a valid WRDS subscription. "
        "Usage is subject to WRDS terms of service. "
        "Not for redistribution without proper licensing."
    ),
}

# Parquet file names
PARQUET_TREASURY_DAILY: Final[str] = "CRSP_TFZ_DAILY.parquet"
PARQUET_TREASURY_INFO: Final[str] = "CRSP_TFZ_INFO.parquet"
PARQUET_TREASURY_CONSOLIDATED: Final[str] = "CRSP_TFZ_consolidated.parquet"
PARQUET_TREASURY_WITH_RUNNESS: Final[str] = "CRSP_TFZ_with_runness.parquet"
PARQUET_CORP_BOND: Final[str] = "WRDS_Corp_Bond_Monthly.parquet"
