"""Constants for He-Kelly-Manela factor data."""

from typing import Final

DATASET_NAME: Final[str] = "he_kelly_manela"
DISPLAY_NAME: Final[str] = "He-Kelly-Manela Intermediary Factors"

# Data source URL
DATA_URL: Final[str] = (
    "https://asaf.manela.org/papers/hkm/intermediarycapitalrisk/He_Kelly_Manela_Factors.zip"
)

# CSV file names (extracted from zip)
CSV_MONTHLY: Final[str] = "He_Kelly_Manela_Factors_monthly.csv"
CSV_DAILY: Final[str] = "He_Kelly_Manela_Factors_daily.csv"
CSV_ALL: Final[str] = "He_Kelly_Manela_Factors_And_Test_Assets_monthly.csv"

# Factor columns for long format conversion
FACTOR_COLUMNS: Final[list[str]] = [
    "intermediary_capital_ratio",
    "intermediary_capital_risk_factor",
    "intermediary_value_weighted_investment_return",
    "intermediary_leverage_ratio_squared",
]
