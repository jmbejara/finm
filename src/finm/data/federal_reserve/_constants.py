"""Constants for Federal Reserve yield curve data."""

from typing import Final

DATASET_NAME: Final[str] = "federal_reserve"
DISPLAY_NAME: Final[str] = "Federal Reserve Yield Curve"

# Data source URL
YIELD_CURVE_URL: Final[str] = (
    "https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv"
)

# Parquet file names
PARQUET_ALL: Final[str] = "fed_yield_curve_all.parquet"
PARQUET_STANDARD: Final[str] = "fed_yield_curve.parquet"

# Standard yield columns (SVENY01 through SVENY30)
YIELD_COLUMNS: Final[list[str]] = [f"SVENY{str(i).zfill(2)}" for i in range(1, 31)]
