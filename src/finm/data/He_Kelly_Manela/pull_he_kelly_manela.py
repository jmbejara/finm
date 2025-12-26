import sys
import zipfile
from pathlib import Path
import urllib3

sys.path.insert(0, str(Path(__file__).parent.parent))

from io import BytesIO

import pandas as pd
import requests

# Suppress SSL warnings when verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# from settings import config

# DATA_DIR = config("DATA_DIR")
URL = "https://asaf.manela.org/papers/hkm/intermediarycapitalrisk/He_Kelly_Manela_Factors.zip"


def pull_he_kelly_manela(
    data_dir: Path | str,
) -> None:
    """
    Download the He-Kelly-Manela factors and test portfolios data as a zip file and then extract the data.

    Parameters
    ----------
    data_dir : Path
        The directory where the data will be stored.

    Returns
    -------
    None
    """

    data_dir = Path(data_dir)
    # DATA_DIR.mkdir(parents=True, exist_ok=True)
    response = requests.get(URL, verify=False)
    zip_file = BytesIO(response.content)
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(data_dir)


def load_he_kelly_manela_factors_monthly(
    data_dir: Path | str,
) -> pd.DataFrame:
    """
    Load CSV file of the He-Kelly-Manela monthly factors.
    
    Parameters
    ----------
    data_dir : Path
        The directory where the CSV file is stored.
        
    Returns
    -------
    pd.DataFrame
        The He-Kelly-Manela monthly factors data.
    """

    data_dir = Path(data_dir)
    path = data_dir / "He_Kelly_Manela_Factors_monthly.csv"
    _df = pd.read_csv(path)
    _df["date"] = pd.to_datetime(_df["yyyymm"], format="%Y%m")
    return _df


def load_he_kelly_manela_factors_daily(
    data_dir: Path | str,
) -> pd.DataFrame:
    """
    Load CSV file of the He-Kelly-Manela daily factors.
    
    Parameters
    ----------
    data_dir : Path
        The directory where the CSV file is stored.
        
    Returns
    -------
    pd.DataFrame
        The He-Kelly-Manela daily factors data.
    """
    
    data_dir = Path(data_dir)
    path = data_dir / "He_Kelly_Manela_Factors_daily.csv"
    _df = pd.read_csv(path)
    _df["date"] = pd.to_datetime(_df["yyyymmdd"], format="%Y%m%d")
    return _df


def load_he_kelly_manela_all(
    data_dir: Path | str,
) -> pd.DataFrame:
    """
    Load CSV file of the He-Kelly-Manela factors and test assets (monthly).

    Parameters
    ----------
    data_dir : Path
        The directory where the CSV file is stored.

    Returns
    -------
    pd.DataFrame
        The He-Kelly-Manela factors and test assets data.
    """

    data_dir = Path(data_dir)
    path = data_dir / "He_Kelly_Manela_Factors_And_Test_Assets_monthly.csv"
    _df = pd.read_csv(path)
    _df["date"] = pd.to_datetime(_df["yyyymm"], format="%Y%m")
    return _df


if __name__ == "__main__":

    # Get location of current file and parent folder
    current_file_path = Path(__file__).resolve()    
    current_dir = current_file_path.parent

    data_dir = current_dir
    pull_he_kelly_manela(data_dir=data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
