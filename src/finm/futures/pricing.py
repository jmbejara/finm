"""
Pricing and related calculations for futures contracts.

This module provides basic functions for:

- Futures price from implied rate
- Implied rate from futures price
- Futures PNL
"""

import math
import numpy as np
import pandas as pd

from datetime import datetime
from scipy.stats import norm


def calc_futures_implied_rate(
    futures_price: float
) -> float:
    """
    Calculate the implied interest rate from a Eurodollar futures price.
    
    Eurodollar futures are quoted as 100 minus the implied 3-month LIBOR rate.
    For example, a price of 95.00 implies a rate of 5.00%.

    Parameters
    ----------
    futures_price : float
        The Eurodollar futures price (e.g., 95.00).

    Returns
    -------
    float
        The implied interest rate as a decimal (e.g., 0.05 for 5%).
    """
    
    # Implied rate = (100 - Futures Price) / 100
    implied_rate = (100 - futures_price) / 100
    
    return implied_rate

def calc_futures_price_from_rate(
    implied_rate: float
) -> float:
    """
    Calculate the Eurodollar futures price from an implied interest rate.
    
    Eurodollar futures are quoted as 100 minus the implied 3-month LIBOR rate.

    Parameters
    ----------
    implied_rate : float
        The implied interest rate as a decimal (e.g., 0.05 for 5%).

    Returns
    -------
    float
        The Eurodollar futures price (e.g., 95.00).
    """
    
    # Futures Price = 100 - (Implied Rate × 100)
    futures_price = 100 - (implied_rate * 100)
    
    return futures_price

def calc_futures_pnl(
    initial_price: float,
    final_price: float,
    num_contracts: int,
    position_type: str = "long"
) -> float:
    """
    Calculate the profit/loss on a Eurodollar futures position.
    
    Each basis point (0.01) move in price = $25 per contract.

    Parameters
    ----------
    initial_price : float
        The initial futures price (e.g., 95.00).
    final_price : float
        The final futures price (e.g., 95.50).
    num_contracts : int
        The number of contracts.
    position_type : str, optional
        Either "long" or "short". Default is "long".

    Returns
    -------
    float
        The profit/loss in dollars (positive = profit, negative = loss).
    """
    
    # Price change in basis points
    price_change = final_price - initial_price
    
    # Each basis point = $25 per contract
    # Total change = price_change × 100 (to get basis points) × $25 × num_contracts
    pnl = price_change * 100 * 25 * num_contracts
    
    # Adjust sign for short position
    if position_type.lower() == "long":
        return pnl
    elif position_type.lower() == "short":
        return -pnl
    else:
        raise ValueError("position_type must be either 'long' or 'short'")