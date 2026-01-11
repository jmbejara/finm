"""Constants for Open Source Bond data.

Data from the Open Source Bond Asset Pricing project.

Website: https://openbondassetpricing.com/
GitHub: https://github.com/Alexander-M-Dickerson/trace-data-pipeline
Data Dictionary: https://github.com/Alexander-M-Dickerson/trace-data-pipeline/blob/main/stage2/DATA_DICTIONARY.md
"""

from typing import Final

DATASET_NAME: Final[str] = "open_source_bond"
DISPLAY_NAME: Final[str] = "Open Source Bond Asset Pricing"

# License and citation information
LICENSE_INFO: Final[dict] = {
    "license_type": "MIT License",
    "license_url": "https://github.com/Alexander-M-Dickerson/trace-data-pipeline/blob/main/LICENSE",
    "citation": (
        "Dickerson, A., Robotti, C., & Rossetti, G. (2026). "
        "The Corporate Bond Factor Replication Crisis: A New Protocol. Working Paper."
    ),
    "terms_url": "https://openbondassetpricing.com/",
    "disclaimer": (
        "This data is provided by a third party. Usage is subject to the licensing terms "
        "and disclaimers of the original data provider, not the finm package maintainers."
    ),
}

# Documentation links
DOCUMENTATION: Final[dict] = {
    "website": "https://openbondassetpricing.com/",
    "data_dictionary": "https://github.com/Alexander-M-Dickerson/trace-data-pipeline/blob/main/stage2/DATA_DICTIONARY.md",
    "github": "https://github.com/Alexander-M-Dickerson/trace-data-pipeline",
}

# Minimum expected rows for data validation
MIN_N_ROWS_EXPECTED: Final[dict] = {
    "treasury": 500,
    "corporate_daily": 1_000_000,
    "corporate_monthly": 100_000,
}

# Data source information
DATA_INFO: Final[dict] = {
    "treasury": {
        "url": "https://openbondassetpricing.com/wp-content/uploads/2024/06/bondret_treasury.csv",
        "source_format": "csv",
        "csv": "bondret_treasury.csv",
        "parquet": "treasury_bond_returns.parquet",
        "readme_url": "https://openbondassetpricing.com/wp-content/uploads/2024/06/BNS_README.pdf",
        "readme_file": "treasury_bond_returns_README.pdf",
        "date_column": "date",
        "id_column": "cusip",
        "value_column": "bond_ret",
    },
    "corporate_daily": {
        "url": "https://openbondassetpricing.com/wp-content/uploads/2025/12/stage1_osbap_0k_volume_2025.zip",
        "source_format": "zip_parquet",
        "zip_contents": "stage1_osbap_0k_volume_2025.parquet",
        "parquet": "corporate_bond_prices_daily.parquet",
        "date_column": "trd_exctn_dt",
        "id_column": "cusip_id",
        "value_column": "pr",
    },
    "corporate_monthly": {
        "url": "https://openbondassetpricing.com/wp-content/uploads/2026/01/osbap_main_data_2025_public_beta.zip",
        "source_format": "zip_parquet",
        "zip_contents": "main_panel_2025.parquet",
        "readme_contents": "README.txt",
        "readme_file": "corporate_bond_returns_monthly_README.txt",
        "parquet": "corporate_bond_returns_monthly.parquet",
        "date_column": "date",
        "id_column": "cusip",
        "value_column": "ret_vw",
    },
}
