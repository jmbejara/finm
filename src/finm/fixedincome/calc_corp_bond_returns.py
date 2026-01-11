from pathlib import Path

import pandas as pd

import finm

# warnings.filterwarnings("ignore", category=DeprecationWarning)


def assign_cs_deciles(
    df: pd.DataFrame,
    cs_col: str = "cs",
) -> pd.DataFrame:
    """
    Assign deciles based on the credit spread column within each date.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing at least 'date' and credit spread columns.
    cs_col : str, default "cs"
        Name of the credit spread column. Supports both old format ("CS")
        and new format ("cs").

    Returns
    -------
    pd.DataFrame
        DataFrame with an additional 'cs_decile' column.
    """

    def assign_deciles(group):
        group = group.copy()
        # Skip groups with too few observations or all NaN values
        valid_cs = group[cs_col].dropna()
        if len(valid_cs) < 10:
            group["cs_decile"] = pd.NA
            return group
        try:
            group["cs_decile"] = (
                pd.qcut(group[cs_col], 10, labels=False, duplicates="drop") + 1
            )
        except ValueError:
            # Handle case where there aren't enough unique values
            group["cs_decile"] = pd.NA
        return group

    return df.groupby("date", group_keys=False).apply(assign_deciles)


def calc_value_weighted_decile_returns(
    df: pd.DataFrame,
    value_col: str = "sze",
    ret_col: str = "ret_vw",
) -> pd.DataFrame:
    """
    Calculate value-weighted bond returns by date and cs_decile.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with cs_decile, date, return, and value columns.
    value_col : str, default "sze"
        Name of the value/size column for weighting. Supports both old format
        ("BOND_VALUE") and new format ("sze" for market cap).
    ret_col : str, default "ret_vw"
        Name of the return column. Supports both old format ("bond_ret")
        and new format ("ret_vw").

    Returns
    -------
    pd.DataFrame
        Pivoted DataFrame with dates as index and deciles as columns.
    """
    # Drop rows with missing decile assignments
    df = df.dropna(subset=["cs_decile"])

    def weighted_return(x):
        weights = x[value_col]
        returns = x[ret_col]
        # Handle missing values
        mask = weights.notna() & returns.notna()
        if mask.sum() == 0:
            return pd.NA
        return (returns[mask] * weights[mask]).sum() / weights[mask].sum()

    agg = (
        df.groupby(["date", "cs_decile"])
        .apply(weighted_return, include_groups=False)
        .reset_index(name="weighted_bond_ret")
    )
    pivoted = agg.pivot(index="date", columns="cs_decile", values="weighted_bond_ret")
    pivoted = pivoted.sort_index(axis=1)
    return pivoted


def calc_corp_bond_returns(
    data_dir: Path,
) -> pd.DataFrame:
    """
    Calculate value-weighted decile portfolio returns from corporate bond data.

    This function loads corporate bond returns, assigns bonds to deciles based
    on credit spread, and calculates value-weighted returns for each decile.

    Parameters
    ----------
    data_dir : Path
        Directory containing the corporate bond data.

    Returns
    -------
    pd.DataFrame
        DataFrame with dates as index and decile portfolios (1-10) as columns.
        Each value is the value-weighted return for that decile-month.

    Notes
    -----
    This function supports both the old data format (with columns CS, BOND_VALUE,
    bond_ret) and the new Open Source Bond format (with columns cs, sze, ret_vw).
    """
    bond_returns = finm.load_corporate_bond_returns(data_dir=data_dir).to_pandas()

    # Detect column format (old vs new)
    if "CS" in bond_returns.columns:
        # Old format
        cs_col = "CS"
        value_col = "BOND_VALUE"
        ret_col = "bond_ret"
    elif "cs" in bond_returns.columns:
        # New Open Source Bond format
        cs_col = "cs"
        value_col = "sze"  # Market cap in millions
        ret_col = "ret_vw"  # Volume-weighted return
    else:
        raise ValueError(
            "Could not detect data format. Expected either 'CS' (old format) "
            "or 'cs' (new Open Source Bond format) column."
        )

    deciled_bond_returns = assign_cs_deciles(bond_returns, cs_col=cs_col)
    # Value-weighted returns
    value_weighted = calc_value_weighted_decile_returns(
        deciled_bond_returns,
        value_col=value_col,
        ret_col=ret_col,
    )
    return value_weighted


# if __name__ == "__main__":
#     bond_returns = finm.load_corporate_bond_returns(data_dir=DATA_DIR)
#     deciled_bond_returns = assign_cs_deciles(bond_returns)
#     # Value-weighted returns
#     value_weighted = calc_value_weighted_decile_returns(
#         deciled_bond_returns, value_col="BOND_VALUE"
#     )
#     value_weighted.to_parquet(DATA_DIR / "corp_bond_portfolio_returns.parquet")
