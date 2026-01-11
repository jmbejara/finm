"""Constants for He-Kelly-Manela factor data.

Data from He, Kelly, and Manela (2017) Intermediary Asset Pricing.

Website: https://asaf.manela.org/papers/hkm/intermediarycapitalrisk/
Paper: https://doi.org/10.1016/j.jfineco.2017.08.002
"""

from typing import Final

DATASET_NAME: Final[str] = "he_kelly_manela"
DISPLAY_NAME: Final[str] = "He-Kelly-Manela Intermediary Factors"

# License and citation information
LICENSE_INFO: Final[dict] = {
    "license_type": "Academic (no explicit license)",
    "license_url": "https://asaf.manela.org/papers/hkm/intermediarycapitalrisk/",
    "citation": (
        "He, Z., Kelly, B., and Manela, A. (2017). Intermediary Asset Pricing: "
        "New Evidence from Many Asset Classes. Journal of Financial Economics 126(1): 1-35."
    ),
    "terms_url": "https://asaf.manela.org/papers/hkm/intermediarycapitalrisk/",
    "disclaimer": (
        "This data is provided by the authors for academic research. "
        "Please cite the paper when using this data."
    ),
}

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
