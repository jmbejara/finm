import pandas as pd
import requests

from io import BytesIO
from pathlib import Path

# from settings import config
# DATA_DIR = config('DATA_DIR')


def pull_fed_yield_curve() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Download the latest yield curve from the Federal Reserve.
    
    This is the published data using Gurkaynak, Sack, and Wright (2007) model.

    Parameters
    ----------
    None

    Returns
    -------
    pd.DataFrame
        The full yield curve data from the Federal Reserve.
    pd.DataFrame
        The yield curve data from the Federal Reserve, with only the relevant columns.
    """
    
    url = "https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv"
    response = requests.get(url)
    pdf_stream = BytesIO(response.content)
    df_all = pd.read_csv(pdf_stream, skiprows=9, index_col=0, parse_dates=True)

    cols = ['SVENY' + str(i).zfill(2) for i in range(1, 31)]
    df = df_all[cols]
    return df_all, df

def load_fed_yield_curve_all(
    data_dir: str | Path, # DATA_DIR
) -> pd.DataFrame:
    """
    Load parquet file of the full yield curve data from the Federal Reserve.

    Parameters
    ----------
    data_dir : str | Path
        The directory where the parquet file is stored.

    Returns
    -------
    pd.DataFrame
        The full yield curve data from the Federal Reserve.
    """
    
    data_dir = Path(data_dir)
    path = data_dir / "fed_yield_curve_all.parquet"
    _df = pd.read_parquet(path)
    return _df

def load_fed_yield_curve(
    data_dir: str | Path, # DATA_DIR
) -> pd.DataFrame:
    """
    Load parquet file of the yield curve data from the Federal Reserve.

    Parameters
    ----------
    data_dir : str | Path
        The directory where the parquet file is stored.

    Returns
    -------
    pd.DataFrame
        The yield curve data from the Federal Reserve.
    """
    
    data_dir = Path(data_dir)
    path = data_dir / "fed_yield_curve.parquet"
    _df = pd.read_parquet(path)
    return _df

# def _demo():
#     _df = load_fed_yield_curve(data_dir=DATA_DIR)
    

if __name__ == "__main__":

    # Get location of current file and parent folder
    current_file_path = Path(__file__).resolve()    
    current_dir = current_file_path.parent

    # Download and save the yield curve data
    df_all, df = pull_fed_yield_curve()

    path = Path(current_dir) / "fed_yield_curve_all.parquet"
    df_all.to_parquet(path)
    
    path = Path(current_dir) / "fed_yield_curve.parquet"
    df.to_parquet(path)