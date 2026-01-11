"""Constants for WRDS data module."""

from typing import Final

DATASET_NAME: Final[str] = "wrds"
DISPLAY_NAME: Final[str] = "WRDS Financial Data"

# Parquet file names
PARQUET_TREASURY_DAILY: Final[str] = "CRSP_TFZ_DAILY.parquet"
PARQUET_TREASURY_INFO: Final[str] = "CRSP_TFZ_INFO.parquet"
PARQUET_TREASURY_CONSOLIDATED: Final[str] = "CRSP_TFZ_consolidated.parquet"
PARQUET_TREASURY_WITH_RUNNESS: Final[str] = "CRSP_TFZ_with_runness.parquet"
PARQUET_CORP_BOND: Final[str] = "WRDS_Corp_Bond_Monthly.parquet"
