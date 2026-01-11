"""Factor analysis and risk metrics.

This module provides asset-class-agnostic functions for:
- Beta calculations
- Sharpe ratio calculations
- Multi-factor exposure analysis (Fama-French 3-factor)
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_beta(returns: pd.Series, factor_returns: pd.Series) -> float:
    """Calculate beta with respect to any factor.

    Beta is computed as Cov(returns, factor) / Var(factor).

    Parameters
    ----------
    returns : pd.Series
        Asset or portfolio returns (should be excess returns if factor is excess).
    factor_returns : pd.Series
        Factor returns to regress against.

    Returns
    -------
    float
        The beta coefficient.

    Example
    -------
    >>> import pandas as pd
    >>> stock_returns = pd.Series([0.01, 0.02, -0.01, 0.03])
    >>> market_returns = pd.Series([0.005, 0.015, -0.005, 0.02])
    >>> beta = calculate_beta(stock_returns, market_returns)
    """
    # Use ddof=1 for both covariance and variance (sample statistics)
    cov = np.cov(returns, factor_returns, ddof=1)[0, 1]
    var = np.var(factor_returns, ddof=1)
    return float(cov / var)


def calculate_sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: pd.Series | float,
    annualization_factor: float = 252.0,
) -> float:
    """Calculate the annualized Sharpe ratio.

    Parameters
    ----------
    returns : pd.Series
        Asset or portfolio returns.
    risk_free_rate : pd.Series or float
        Risk-free rate. If Series, should align with returns index.
    annualization_factor : float, default 252.0
        Factor to annualize. Use 252 for daily, 12 for monthly, 1 for annual.

    Returns
    -------
    float
        Annualized Sharpe ratio.

    Example
    -------
    >>> import pandas as pd
    >>> returns = pd.Series([0.01, 0.02, -0.01, 0.03, 0.005])
    >>> rf = 0.0001  # daily risk-free rate
    >>> sharpe = calculate_sharpe_ratio(returns, rf)
    """
    excess_returns = returns - risk_free_rate
    return float(
        np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(annualization_factor)
    )


def calculate_factor_exposures(
    returns: pd.Series,
    factors: pd.DataFrame,
    annualization_factor: float = 252.0,
) -> dict[str, float]:
    """Calculate factor exposures (betas) and summary statistics.

    Computes betas for Fama-French 3 factors (Mkt-RF, SMB, HML) plus
    summary statistics including average return, volatility, and Sharpe ratio.

    Parameters
    ----------
    returns : pd.Series
        Asset or portfolio returns (raw returns, not excess).
    factors : pd.DataFrame
        DataFrame with columns: 'Mkt-RF', 'SMB', 'HML', 'RF'.
        Index should be dates aligning with returns.
    annualization_factor : float, default 252.0
        Factor to annualize statistics. Use 252 for daily, 12 for monthly.

    Returns
    -------
    dict[str, float]
        Dictionary containing:
        - 'average_return': Annualized average return
        - 'volatility': Annualized volatility (standard deviation)
        - 'sharpe_ratio': Annualized Sharpe ratio
        - 'market_beta': Beta with respect to market excess return
        - 'smb_beta': Beta with respect to SMB factor
        - 'hml_beta': Beta with respect to HML factor

    Example
    -------
    >>> import finm
    >>> factors = finm.load_fama_french_factors()
    >>> # Assume stock_returns is a pd.Series with matching dates
    >>> exposures = finm.calculate_factor_exposures(stock_returns, factors)
    >>> print(f"Market Beta: {exposures['market_beta']:.2f}")
    """
    # Align returns and factors on common dates
    common_dates = returns.index.intersection(factors.index)
    aligned_returns = returns.loc[common_dates]
    aligned_factors = factors.loc[common_dates]

    # Calculate excess returns
    excess_returns = aligned_returns - aligned_factors["RF"]
    market_excess = aligned_factors["Mkt-RF"]

    return {
        "average_return": float(aligned_returns.mean() * annualization_factor),
        "volatility": float(aligned_returns.std() * np.sqrt(annualization_factor)),
        "sharpe_ratio": calculate_sharpe_ratio(
            aligned_returns, aligned_factors["RF"], annualization_factor
        ),
        "market_beta": calculate_beta(excess_returns, market_excess),
        "smb_beta": calculate_beta(excess_returns, aligned_factors["SMB"]),
        "hml_beta": calculate_beta(excess_returns, aligned_factors["HML"]),
    }
