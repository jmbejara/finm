"""Constants for Fama-French factor data."""

from pathlib import Path
from typing import Final

DATASET_NAME: Final[str] = "fama_french"
DISPLAY_NAME: Final[str] = "Fama-French Factors"

# Bundled data location (within package)
BUNDLED_DATA_DIR: Final[Path] = Path(__file__).parent / "data"
BUNDLED_CSV: Final[str] = "ff3factors.csv"

# Ken French Data Library dataset names
DATASET_DAILY: Final[str] = "F-F_Research_Data_Factors_Daily"
DATASET_MONTHLY: Final[str] = "F-F_Research_Data_Factors"
