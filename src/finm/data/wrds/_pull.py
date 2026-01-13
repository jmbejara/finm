"""Pull functions for WRDS data."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pandas as pd
import wrds

from finm.data.wrds._constants import (
    PARQUET_CORP_BOND,
    PARQUET_TREASURY_CONSOLIDATED,
    PARQUET_TREASURY_DAILY,
    PARQUET_TREASURY_INFO,
    PARQUET_TREASURY_WITH_RUNNESS,
)

TreasuryVariantType = Literal["daily", "info", "consolidated"]


def _pull_treasury_daily(
    start_date: str,
    end_date: str,
    wrds_username: str,
) -> pd.DataFrame:
    """Pull daily CRSP Treasury data from WRDS.

    Parameters
    ----------
    start_date : str
        Start date in 'YYYY-MM-DD' format.
    end_date : str
        End date in 'YYYY-MM-DD' format.
    wrds_username : str
        WRDS username.

    Returns
    -------
    pd.DataFrame
        Daily Treasury data.
    """
    query = f"""
    SELECT
        kytreasno, kycrspid, caldt, tdbid, tdask, tdaccint, tdyld,
        ((tdbid + tdask) / 2.0 + tdaccint) AS price,
        tdduratn,
        tdretnua,
        tdpubout,
        tdtotout,
        tdpdint
    FROM
        crspm.tfz_dly
    WHERE
        caldt BETWEEN '{start_date}' AND '{end_date}'
    """

    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(query, date_cols=["caldt"])
    db.close()
    return df


def _pull_treasury_info(wrds_username: str) -> pd.DataFrame:
    """Pull Treasury issue information from WRDS.

    Parameters
    ----------
    wrds_username : str
        WRDS username.

    Returns
    -------
    pd.DataFrame
        Treasury issue information.
    """
    query = """
        SELECT
            kytreasno, kycrspid, tcusip, tdatdt, tmatdt, tcouprt, itype,
            ROUND((tmatdt - tdatdt) / 365.0) AS original_maturity
        FROM
            crspm.tfz_iss AS iss
        WHERE
            iss.itype IN (1, 2)
    """

    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(query, date_cols=["tdatdt", "tmatdt"])
    db.close()
    return df


def _pull_treasury_consolidated(
    start_date: str,
    end_date: str,
    wrds_username: str,
) -> pd.DataFrame:
    """Pull consolidated CRSP Treasury data from WRDS.

    Parameters
    ----------
    start_date : str
        Start date in 'YYYY-MM-DD' format.
    end_date : str
        End date in 'YYYY-MM-DD' format.
    wrds_username : str
        WRDS username.

    Returns
    -------
    pd.DataFrame
        Consolidated Treasury data with daily quotes and issue info.
    """
    query = f"""
    SELECT
        tfz.kytreasno, tfz.kycrspid, iss.tcusip,
        tfz.caldt,
        iss.tdatdt,
        iss.tmatdt,
        iss.tfcaldt,
        tfz.tdbid,
        tfz.tdask,
        tfz.tdaccint,
        tfz.tdyld,
        ((tfz.tdbid + tfz.tdask) / 2.0 + tfz.tdaccint) AS price,
        tfz.tdpubout,
        tfz.tdtotout,
        tfz.tdpdint,
        iss.tcouprt,
        iss.itype,
        ROUND((iss.tmatdt - iss.tdatdt) / 365.0) AS original_maturity,
        ROUND((iss.tmatdt - tfz.caldt) / 365.0) AS years_to_maturity,
        tfz.tdduratn,
        tfz.tdretnua
    FROM
        crspm.tfz_dly AS tfz
    LEFT JOIN
        crspm.tfz_iss AS iss
    ON
        tfz.kytreasno = iss.kytreasno AND
        tfz.kycrspid = iss.kycrspid
    WHERE
        tfz.caldt BETWEEN '{start_date}' AND '{end_date}' AND
        iss.itype IN (1, 2)
    """

    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(query, date_cols=["caldt", "tdatdt", "tmatdt", "tfcaldt"])
    df["days_to_maturity"] = (df["tmatdt"] - df["caldt"]).dt.days
    df["tfcaldt"] = pd.to_datetime(df["tfcaldt"]).fillna(pd.Timestamp(0))
    df["callable"] = df["tfcaldt"] != pd.Timestamp(0)
    db.close()
    df = df.reset_index(drop=True)
    return df


def _pull_corp_bond(
    start_date: str,
    end_date: str,
    wrds_username: str,
) -> pd.DataFrame:
    """Pull monthly corporate bond data from WRDS.

    Parameters
    ----------
    start_date : str
        Start date in 'YYYY-MM-DD' format.
    end_date : str
        End date in 'YYYY-MM-DD' format.
    wrds_username : str
        WRDS username.

    Returns
    -------
    pd.DataFrame
        Monthly corporate bond data.
    """
    query = f"""
        SELECT
            DATE,
            CUSIP,
            COMPANY_SYMBOL,
            BOND_TYPE,
            coupon,
            amount_outstanding,
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


def calc_runness(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate on-the-run/off-the-run status for Treasury securities.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame with Treasury data including 'caldt', 'original_maturity',
        and 'tdatdt' columns.

    Returns
    -------
    pd.DataFrame
        Input DataFrame with additional 'run' column.
    """

    def _calc_runness(df: pd.DataFrame) -> pd.Series:
        temp = df.sort_values(by=["caldt", "original_maturity", "tdatdt"])
        next_temp = (
            temp.groupby(["caldt", "original_maturity"])["tdatdt"].rank(
                method="first", ascending=False
            )
            - 1
        )
        return next_temp

    data_run_ = data[data["caldt"] >= "1980"]
    runs = _calc_runness(data_run_)
    data["run"] = 0
    data.loc[data_run_.index, "run"] = runs
    return data


def pull_treasury(
    data_dir: Path | str,
    wrds_username: str,
    start_date: str,
    end_date: str,
    variant: TreasuryVariantType = "consolidated",
    with_runness: bool = True,
) -> pd.DataFrame:
    """Pull CRSP Treasury data from WRDS.

    Parameters
    ----------
    data_dir : Path or str
        Directory to save the data.
    wrds_username : str
        WRDS username.
    start_date : str
        Start date in 'YYYY-MM-DD' format.
    end_date : str
        End date in 'YYYY-MM-DD' format.
    variant : {"daily", "info", "consolidated"}, default "consolidated"
        Which data variant to pull.
    with_runness : bool, default True
        Whether to calculate runness for consolidated data.

    Returns
    -------
    pd.DataFrame
        Treasury data.
    """
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    if variant == "daily":
        df = _pull_treasury_daily(start_date, end_date, wrds_username)
        df.to_parquet(data_dir / PARQUET_TREASURY_DAILY)

    elif variant == "info":
        df = _pull_treasury_info(wrds_username)
        df.to_parquet(data_dir / PARQUET_TREASURY_INFO)

    elif variant == "consolidated":
        df = _pull_treasury_consolidated(start_date, end_date, wrds_username)
        df.to_parquet(data_dir / PARQUET_TREASURY_CONSOLIDATED)

        if with_runness:
            df = calc_runness(df)
            df.to_parquet(data_dir / PARQUET_TREASURY_WITH_RUNNESS)

    return df


def pull_corp_bond(
    data_dir: Path | str,
    wrds_username: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """Pull corporate bond data from WRDS.

    Parameters
    ----------
    data_dir : Path or str
        Directory to save the data.
    wrds_username : str
        WRDS username.
    start_date : str
        Start date in 'YYYY-MM-DD' format.
    end_date : str
        End date in 'YYYY-MM-DD' format.

    Returns
    -------
    pd.DataFrame
        Corporate bond data.
    """
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    df = _pull_corp_bond(start_date, end_date, wrds_username)
    df.to_parquet(data_dir / PARQUET_CORP_BOND)

    return df
