"""Constants for Open Source Bond data."""

from typing import Final

DATASET_NAME: Final[str] = "open_source_bond"
DISPLAY_NAME: Final[str] = "Open Source Bond Asset Pricing"

# Minimum expected rows for data validation
MIN_N_ROWS_EXPECTED: Final[int] = 500

# Data source information
DATA_INFO: Final[dict] = {
    "treasury": {
        "url": "https://openbondassetpricing.com/wp-content/uploads/2024/06/bondret_treasury.csv",
        "csv": "bondret_treasury.csv",
        "parquet": "treasury_bond_returns.parquet",
        "readme": "https://openbondassetpricing.com/wp-content/uploads/2024/06/BNS_README.pdf",
    },
    "corporate": {
        "url": "https://openbondassetpricing.com/wp-content/uploads/2024/07/WRDS_MMN_Corrected_Data_2024_July.csv",
        "csv": "WRDS_MMN_Corrected_Data.csv",
        "parquet": "corporate_bond_returns.parquet",
        "readme": "https://openbondassetpricing.com/wp-content/uploads/2024/07/DRR-README.pdf",
    },
}
