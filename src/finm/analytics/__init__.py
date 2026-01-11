"""Analytics Module.

This module provides asset-class-agnostic analytics functions including
factor analysis, risk metrics, and performance statistics.
"""

from finm.analytics.factor_analysis import (
    RegressionResult,
    calculate_beta,
    calculate_factor_exposures,
    calculate_sharpe_ratio,
    run_capm_regression,
    run_factor_regression,
    run_fama_french_regression,
)

__all__ = [
    "RegressionResult",
    "calculate_beta",
    "calculate_sharpe_ratio",
    "calculate_factor_exposures",
    "run_factor_regression",
    "run_capm_regression",
    "run_fama_french_regression",
]
