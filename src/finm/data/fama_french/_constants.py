"""Constants for Fama-French factor data.

Data from Ken French's Data Library.

Website: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
"""

from pathlib import Path
from typing import Final

DATASET_NAME: Final[str] = "fama_french"
DISPLAY_NAME: Final[str] = "Fama-French Factors"

# License and citation information
LICENSE_INFO: Final[dict] = {
    "license_type": "Copyright Fama & French",
    "license_url": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html",
    "citation": (
        "Fama, E.F. and French, K.R. (1993). Common Risk Factors in the Returns "
        "on Stocks and Bonds. Journal of Financial Economics 33(1): 3-56."
    ),
    "terms_url": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html",
    "disclaimer": (
        "This data is provided by Ken French's Data Library. "
        "Usage is subject to the data provider's terms. "
        "Please cite the Fama-French papers when using this data."
    ),
}

# Bundled data location (within package)
BUNDLED_DATA_DIR: Final[Path] = Path(__file__).parent / "data"
BUNDLED_CSV: Final[str] = "ff3factors.csv"

# Ken French Data Library dataset names
DATASET_DAILY: Final[str] = "F-F_Research_Data_Factors_Daily"
DATASET_MONTHLY: Final[str] = "F-F_Research_Data_Factors"
