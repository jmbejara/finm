"""Constants for Federal Reserve yield curve data.

Data from the Federal Reserve Board of Governors.

Website: https://www.federalreserve.gov/data/yield-curve-tables.htm
Terms: https://www.federalreserve.gov/disclaimer.htm
"""

from typing import Final

DATASET_NAME: Final[str] = "federal_reserve"
DISPLAY_NAME: Final[str] = "Federal Reserve Yield Curve"

# License and citation information
LICENSE_INFO: Final[dict] = {
    "license_type": "Public Domain",
    "license_url": "https://www.federalreserve.gov/disclaimer.htm",
    "citation": (
        "Board of Governors of the Federal Reserve System. "
        "GSW Yield Curve Data. https://www.federalreserve.gov/data/yield-curve-tables.htm"
    ),
    "terms_url": "https://www.federalreserve.gov/disclaimer.htm",
    "disclaimer": (
        "This data is provided by the Federal Reserve Board of Governors and is in the "
        "public domain. Usage is subject to the Federal Reserve's terms. "
        "Please cite the Board as the source of the information."
    ),
}

# Data source URL
YIELD_CURVE_URL: Final[str] = (
    "https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv"
)

# Parquet file names
PARQUET_ALL: Final[str] = "fed_yield_curve_all.parquet"
PARQUET_STANDARD: Final[str] = "fed_yield_curve.parquet"

# Standard yield columns (SVENY01 through SVENY30)
YIELD_COLUMNS: Final[list[str]] = [f"SVENY{str(i).zfill(2)}" for i in range(1, 31)]
