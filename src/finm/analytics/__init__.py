"""Analytics Module.

This module provides asset-class-agnostic analytics functions including
factor analysis, risk metrics, and performance statistics.
"""

from finm.analytics.factor_analysis import (
    calculate_beta,
    calculate_factor_exposures,
    calculate_sharpe_ratio,
)

__all__ = [
    "calculate_beta",
    "calculate_sharpe_ratio",
    "calculate_factor_exposures",
]
