"""Factor analysis and risk metrics.

This module provides asset-class-agnostic functions for:
- Beta calculations
- Sharpe ratio calculations
- Multi-factor exposure analysis (Fama-French 3-factor)
- OLS regression with full statistics (alpha, beta, t-stats, R-squared)
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats


@dataclass
class RegressionResult:
    """Results from OLS regression of asset returns on factor(s).

    This dataclass holds all standard OLS statistics commonly used
    in asset pricing analysis, including Jensen's alpha.

    Attributes
    ----------
    alpha : float
        Intercept (Jensen's alpha) from the regression.
    alpha_tstat : float
        t-statistic for alpha.
    alpha_pvalue : float
        Two-sided p-value for alpha.
    alpha_se : float
        Standard error of alpha.
    betas : dict[str, float]
        Factor betas, keyed by factor name.
    beta_tstats : dict[str, float]
        t-statistics for betas, keyed by factor name.
    beta_pvalues : dict[str, float]
        Two-sided p-values for betas, keyed by factor name.
    beta_ses : dict[str, float]
        Standard errors of betas, keyed by factor name.
    r_squared : float
        R-squared (coefficient of determination).
    adj_r_squared : float
        Adjusted R-squared.
    n_observations : int
        Number of observations used in regression.
    residual_std : float
        Standard deviation of residuals.
    alpha_annualized : float or None
        Annualized alpha (if annualization_factor was provided).
    annualization_factor : float or None
        Factor used to annualize alpha.
    """

    alpha: float
    alpha_tstat: float
    alpha_pvalue: float
    alpha_se: float
    betas: dict[str, float]
    beta_tstats: dict[str, float]
    beta_pvalues: dict[str, float]
    beta_ses: dict[str, float]
    r_squared: float
    adj_r_squared: float
    n_observations: int
    residual_std: float
    alpha_annualized: float | None = None
    annualization_factor: float | None = None


def _ols_regression(
    y: np.ndarray, X: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float, float, int, float]:
    """Perform OLS regression and return coefficients and statistics.

    Parameters
    ----------
    y : np.ndarray
        Dependent variable (n,).
    X : np.ndarray
        Independent variables without constant (n, k).

    Returns
    -------
    tuple
        (coefficients, standard_errors, t_stats, p_values,
         r_squared, adj_r_squared, degrees_of_freedom, residual_std)
        where coefficients[0] is the intercept.
    """
    # Add constant column for intercept
    n = len(y)
    X_with_const = np.column_stack([np.ones(n), X])
    k = X_with_const.shape[1]  # number of parameters including intercept

    # OLS: beta = (X'X)^(-1) X'y
    XtX = X_with_const.T @ X_with_const
    XtX_inv = np.linalg.inv(XtX)
    coefficients = XtX_inv @ X_with_const.T @ y

    # Residuals and variance
    residuals = y - X_with_const @ coefficients
    dof = n - k
    residual_var = (residuals @ residuals) / dof
    residual_std = np.sqrt(residual_var)

    # Standard errors
    se = np.sqrt(np.diag(XtX_inv) * residual_var)

    # t-statistics and p-values (two-sided)
    with np.errstate(divide='ignore', invalid='ignore'):
        t_stats = coefficients / se
    p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), dof))

    # R-squared
    ss_res = residuals @ residuals
    ss_tot = np.sum((y - y.mean()) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    adj_r_squared = 1 - (1 - r_squared) * (n - 1) / dof if dof > 0 else 0.0

    return coefficients, se, t_stats, p_values, r_squared, adj_r_squared, dof, residual_std


def run_factor_regression(
    returns: pd.Series,
    factors: pd.DataFrame | pd.Series,
    annualization_factor: float | None = None,
) -> RegressionResult:
    """Run OLS regression of returns on factor(s) with full statistics.

    This function performs OLS regression and returns Jensen's alpha,
    factor betas, t-statistics, p-values, and R-squared. It handles
    both single-factor (CAPM) and multi-factor (Fama-French) regressions.

    Parameters
    ----------
    returns : pd.Series
        Asset or portfolio excess returns. Index should be dates.
        These should be excess returns (returns minus risk-free rate).
    factors : pd.DataFrame or pd.Series
        Factor returns to regress against. If Series, treated as single
        factor. If DataFrame, each column is a factor.
        Index should be dates aligning with returns.
    annualization_factor : float, optional
        Factor to annualize alpha. Use 12 for monthly data, 252 for daily.
        If None, alpha_annualized will be None.

    Returns
    -------
    RegressionResult
        Dataclass containing alpha, betas, t-stats, p-values, R-squared.

    Example
    -------
    >>> import pandas as pd
    >>> import finm
    >>> # CAPM regression (single factor)
    >>> portfolio_excess = pd.Series([0.01, -0.02, 0.015], index=dates)
    >>> market_excess = pd.Series([0.005, -0.01, 0.01], index=dates)
    >>> result = finm.run_factor_regression(portfolio_excess, market_excess)
    >>> print(f"Alpha: {result.alpha:.4f} (t={result.alpha_tstat:.2f})")
    >>> print(f"Beta: {result.betas['factor']:.2f}")

    >>> # Fama-French 3-factor regression
    >>> factors = pd.DataFrame({
    ...     'Mkt-RF': mkt_rf, 'SMB': smb, 'HML': hml
    ... })
    >>> result = finm.run_factor_regression(
    ...     portfolio_excess, factors, annualization_factor=12
    ... )
    >>> print(f"Alpha: {result.alpha_annualized:.2%} annualized")
    """
    # Convert Series to DataFrame if needed
    if isinstance(factors, pd.Series):
        factor_names = [factors.name if factors.name else "factor"]
        factors = factors.to_frame(name=factor_names[0])
    else:
        factor_names = list(factors.columns)

    # Align returns and factors on common dates
    common_idx = returns.index.intersection(factors.index)
    y = returns.loc[common_idx].values
    X = factors.loc[common_idx].values

    # Run OLS regression
    coeffs, se, t_stats, p_values, r_sq, adj_r_sq, dof, resid_std = _ols_regression(y, X)

    # Extract alpha (intercept) and betas
    alpha = coeffs[0]
    alpha_se = se[0]
    alpha_tstat = t_stats[0]
    alpha_pvalue = p_values[0]

    betas = {name: coeffs[i + 1] for i, name in enumerate(factor_names)}
    beta_ses = {name: se[i + 1] for i, name in enumerate(factor_names)}
    beta_tstats = {name: t_stats[i + 1] for i, name in enumerate(factor_names)}
    beta_pvalues = {name: p_values[i + 1] for i, name in enumerate(factor_names)}

    # Annualize alpha if requested
    alpha_ann = alpha * annualization_factor if annualization_factor else None

    return RegressionResult(
        alpha=float(alpha),
        alpha_tstat=float(alpha_tstat),
        alpha_pvalue=float(alpha_pvalue),
        alpha_se=float(alpha_se),
        betas=betas,
        beta_tstats=beta_tstats,
        beta_pvalues=beta_pvalues,
        beta_ses=beta_ses,
        r_squared=float(r_sq),
        adj_r_squared=float(adj_r_sq),
        n_observations=len(common_idx),
        residual_std=float(resid_std),
        alpha_annualized=float(alpha_ann) if alpha_ann is not None else None,
        annualization_factor=annualization_factor,
    )


def run_capm_regression(
    excess_returns: pd.Series,
    market_excess_returns: pd.Series,
    annualization_factor: float | None = None,
) -> RegressionResult:
    """Run CAPM regression (single-factor model).

    Convenience wrapper around run_factor_regression for CAPM.
    Regresses portfolio excess returns on market excess returns.

    Parameters
    ----------
    excess_returns : pd.Series
        Portfolio or asset excess returns (returns - risk-free rate).
    market_excess_returns : pd.Series
        Market excess returns (market return - risk-free rate).
    annualization_factor : float, optional
        Factor to annualize alpha. Use 12 for monthly, 252 for daily.

    Returns
    -------
    RegressionResult
        Regression results with alpha, market beta, and statistics.

    Example
    -------
    >>> result = finm.run_capm_regression(
    ...     portfolio_excess_ret, market_excess_ret, annualization_factor=12
    ... )
    >>> print(f"Alpha: {result.alpha:.4f}")
    >>> print(f"Market Beta: {result.betas['Mkt-RF']:.2f}")
    """
    factors = market_excess_returns.to_frame(name="Mkt-RF")
    return run_factor_regression(excess_returns, factors, annualization_factor)


def run_fama_french_regression(
    returns: pd.Series,
    factors: pd.DataFrame,
    annualization_factor: float | None = None,
) -> RegressionResult:
    """Run Fama-French 3-factor regression.

    Computes excess returns internally and regresses on Mkt-RF, SMB, HML.

    Parameters
    ----------
    returns : pd.Series
        Asset or portfolio returns (raw returns, not excess).
    factors : pd.DataFrame
        Must contain columns: 'Mkt-RF', 'SMB', 'HML', 'RF'.
    annualization_factor : float, optional
        Factor to annualize alpha. Use 12 for monthly, 252 for daily.

    Returns
    -------
    RegressionResult
        Regression results with alpha and betas for all three factors.

    Example
    -------
    >>> factors = finm.load_fama_french_factors()
    >>> result = finm.run_fama_french_regression(
    ...     portfolio_returns, factors, annualization_factor=12
    ... )
    >>> print(f"Alpha: {result.alpha_annualized:.2%} annualized")
    >>> print(f"Market Beta: {result.betas['Mkt-RF']:.2f}")
    >>> print(f"SMB Beta: {result.betas['SMB']:.2f}")
    >>> print(f"HML Beta: {result.betas['HML']:.2f}")
    """
    # Compute excess returns
    common_idx = returns.index.intersection(factors.index)
    excess_ret = returns.loc[common_idx] - factors.loc[common_idx, "RF"]
    ff_factors = factors.loc[common_idx, ["Mkt-RF", "SMB", "HML"]]

    return run_factor_regression(excess_ret, ff_factors, annualization_factor)


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
