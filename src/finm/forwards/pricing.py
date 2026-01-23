"""
Pricing and related calculations for forward rate agreements.

This module provides basic functions for:

- 
"""

import math
import numpy as np
import pandas as pd

from datetime import datetime
from scipy.stats import norm


def calc_fra_settlement(
    notional: float,
    strike_rate: float,
    reference_rate: float,
    value_date: str,
    maturity_date: str,
    position_type: str = "long"
) -> float:
    """
    Calculate the settlement payment for a Forward Rate Agreement.
    
    The settlement occurs at the value date and is the present value
    of the interest rate differential over the FRA period.

    Parameters
    ----------
    notional : float
        The notional amount of the FRA.
    strike_rate : float
        The locked-in forward rate (as a decimal, e.g., 0.05 for 5%).
    reference_rate : float
        The market reference rate at fixing (as a decimal, e.g., 0.055 for 5.5%).
    value_date : str
        The FRA value/fixing date as a string "YYYY-MM-DD".
    maturity_date : str
        The FRA maturity date as a string "YYYY-MM-DD".
    position_type : str, optional
        Either "long" (receiver if rates rise) or "short" (payer if rates rise).
        Default is "long".

    Returns
    -------
    float
        The settlement payment (positive = receive, negative = pay).
    """
    
    # Calculate day count fraction using Actual/360
    val_dt = datetime.strptime(value_date, "%Y-%m-%d")
    mat_dt = datetime.strptime(maturity_date, "%Y-%m-%d")
    days = (mat_dt - val_dt).days
    day_count_fraction = days / 360.0
    
    # Calculate the interest rate differential
    rate_diff = reference_rate - strike_rate
    
    # Calculate settlement (discounted to value date)
    # Settlement = Notional × (Reference - Strike) × DCF / (1 + Reference × DCF)
    settlement = (notional * rate_diff * day_count_fraction) / \
                 (1 + reference_rate * day_count_fraction)
    
    # Adjust sign based on position
    if position_type.lower() == "long":
        return settlement
    elif position_type.lower() == "short":
        return -settlement
    else:
        raise ValueError("position_type must be either 'long' or 'short'")
