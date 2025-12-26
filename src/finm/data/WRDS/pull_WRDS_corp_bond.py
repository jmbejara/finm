"""
Pull and load WRDS corporate bond return data from WRDS.

Reference:
    WRDS Bond Returns
    https://wrds-www.wharton.upenn.edu/documents/248/WRDS_Corporate_Bond_Database_Manual.pdf

Data Description:
    Identifying information:
        (DATE) DATE
        (CUSIP) CUSIP ID
        (COMPANY_SYMBOL) Company Symbol (issuer stock ticker)
        (BOND_TYPE) Corporate Bond Types: Convertible, Debenture, Medium Term Note, MTN Zero
        # (CONV) Flag Convertible
        # (PREF) Flag preferred
    Offering and Coupon Characteristics:
        # (offering_date) Offering Date
        # (offering_amt) Offering Amount
        # (offering_price) Offering Price
        # (principal_amt) The face or par value of a single bond (i.e., the sum that is to be paid at maturity, usually $1000).
        # (maturity) Maturity Date
        # (treasury_maturity) Treasuary Maturity
        # (ncoups) No of Coupons Per Year
    Time Series Data Prices and Returns:
        (price_eom) Price-End of Month
        (price_ldm) Price-Last Trading Day of Month
        (price_l5m) Price-EOM(Last 5D)
        (ret_eom) Return-End of Month
        (ret_ldm) Return-Last Trading Day of Month
        (ret_l5m) Return-End of Month (Last 5 Days)
        # (tmt) Time to Maturity (Years)
        # (duration) Duration
    Credit Rating:
        (r_sp) S&P Bond Issue Credit Rating
        (r_mr) Moody Issue Credit Rating
        (r_fr) Fitch IBCA Issue Credit Rating
        (n_sp) Numerical Rating S&P: 1=AAA
        (n_mr) Numerical Rating Moody: 1=AAA
        (n_fr) Numerical Rating Fitch: 1=AAA
        (rating_num) Combined Numerical Rating: 1=AAA
        (rating_cat) Combined Credit Rating
        (rating_class) Combined Rating Class: 0.IG or 1.HY
    Default Information:
        # (defaulted) Flag Default
        # (default_date) Default Date
        # (default_type) Default Type
        # (default_type) Default Type
        # (reinstated_date) Reinstated Date

Note: For any field above, it is not included below if preceded by #.
"""

import pandas as pd
import wrds

from datetime import datetime
from pathlib import Path

def pull_WRDS_corp_bond_monthly(
    start_date: str, # "2002-07-31"
    end_date: str, # "2024-08-31"
    wrds_username: str, # "WRDS_USERNAME"
) -> pd.DataFrame:
    """
    Pull monthly WRDS corporate bond data from WRDS within the specified date range.

    Parameters
    ----------
    start_date : str
        Start date for the query in 'YYYY-MM-DD' format.
    end_date : str
        End date for the query in 'YYYY-MM-DD' format.
    wrds_username : str
        WRDS username to use for the connection.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the monthly WRDS corporate bond data with the following columns:

        - (DATE) DATE
        - (CUSIP) CUSIP ID
        - (COMPANY_SYMBOL) Company Symbol (issuer stock ticker)
        - (BOND_TYPE) Corporate Bond Types: Convertible, Debenture, Medium Term Note, MTN Zero
        - (price_eom) Price-End of Month
        - (price_ldm) Price-Last Trading Day of Month
        - (price_l5m) Price-EOM(Last 5D)
        - (ret_eom) Return-End of Month
        - (ret_ldm) Return-Last Trading Day of Month
        - (ret_l5m) Return-End of Month (Last 5 Days)
        - (r_sp) S&P Bond Issue Credit Rating
        - (r_mr) Moody Issue Credit Rating
        - (r_fr) Fitch IBCA Issue Credit Rating
        - (n_sp) Numerical Rating S&P: 1=AAA
        - (n_mr) Numerical Rating Moody: 1=AAA
        - (n_fr) Numerical Rating Fitch: 1=AAA
        - (rating_num) Combined Numerical Rating: 1=AAA
        - (rating_cat) Combined Credit Rating
        - (rating_class) Combined Rating Class: 0.IG or 1.HY

    Notes
    -----
    Field Details:
    - TBD
    """

    query = f"""
        SELECT 
            DATE,
            CUSIP,
            COMPANY_SYMBOL,
            BOND_TYPE,
            price_eom,
            price_ldm,
            price_l5m,
            ret_eom,
            ret_ldm,
            ret_l5m,
            r_sp,
            r_mr,
            r_fr,
            n_sp,
            n_mr,
            n_fr,
            rating_num,
            rating_cat,
            rating_class
        FROM 
            wrdsapps.bondret
        WHERE 
            DATE BETWEEN '{start_date}' AND '{end_date}'
    """

    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(query, date_cols=["DATE"])
    db.close()
    return df

def load_WRDS_corp_bond_monthly(
    data_dir: Path | str, # DATA_DIR
) -> pd.DataFrame:
    """Load monthly WRDS corporate bond data from a Parquet file.

    Parameters
    ----------
    data_dir : Path or str
        Directory where the Parquet file is stored.

    Returns
    -------
    pd.DataFrame
        DataFrame containing monthly WRDS corporate bond data. See docstring for details on the columns.
    """

    data_dir = Path(data_dir)
    path = data_dir / "WRDS_Corp_Bond_Monthly.parquet"
    df = pd.read_parquet(path)
    return df


if __name__ == "__main__":

    # Get location of current file and parent folder
    current_file_path = Path(__file__).resolve()    
    current_dir = current_file_path.parent

    WRDS_USERNAME = "jszajkowski"  # Replace with your WRDS username

    # Download and save the corporate bond data
    df = pull_WRDS_corp_bond_monthly(
        start_date="2020-01-01",
        end_date="2020-12-31",
        wrds_username=WRDS_USERNAME,
    )

    path = Path(current_dir) / "WRDS_Corp_Bond_Monthly.parquet"
    df.to_parquet(path)
