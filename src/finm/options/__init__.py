"""
Options Module

This module provides functions for option pricing 
calculations including Black-Scholes and the greeks.
"""

from finm.options.pricing import (
    calc_option_price,
    calc_option_payoff,
    calc_option_delta,
    calc_option_gamma,
    calc_option_vega,
    calc_option_theta,
    calc_option_rho,
    calc_implied_volatility,
    calc_binomial_option_price,
    calc_breakeven_price,
)

__all__ = [
    # from finm.options.pricing
    "calc_option_price",
    "calc_option_payoff",
    "calc_option_delta",
    "calc_option_gamma",
    "calc_option_vega",
    "calc_option_theta",
    "calc_option_rho",
    "calc_implied_volatility",
    "calc_binomial_option_price",
    "calc_breakeven_price",
]
