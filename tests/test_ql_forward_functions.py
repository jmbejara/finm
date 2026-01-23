"""
Functions from QuantLib examples to be used for forward tests.
"""

import numpy as np
import pandas as pd
import QuantLib as ql

from datetime import datetime

def ql_create_forward_rate_agreement(
    quote_date: str,
    value_date: str,
    maturity_date: str,
    notional: float,
    strike_rate: float,
    position_type: str = "long",
) -> ql.ForwardRateAgreement:
    """
    Create a QuantLib Forward Rate Agreement (FRA).

    An FRA is a contract to lock in an interest rate for a future period.
    The buyer (long position) receives if the reference rate > strike rate.

    Parameters
    ----------
    value_date : str
        The FRA value/fixing date as a string "YYYY-MM-DD".
        This is when the reference rate is observed.
    maturity_date : str
        The FRA maturity date as a string "YYYY-MM-DD".
        This defines the end of the interest rate period.
    notional : float
        The notional amount of the FRA.
    strike_rate : float
        The locked-in forward rate (as a decimal, e.g., 0.05 for 5%).
    index : ql.IborIndex
        The reference interest rate index (e.g., ql.USDLibor with appropriate term).
    position_type : str, optional
        Either "long" (receiver if rates rise) or "short" (payer if rates rise).
        Default is "long".

    Returns
    -------
    ql.ForwardRateAgreement
        The QuantLib ForwardRateAgreement object.
    """

    # Convert to QuantLib dates from strings
    if isinstance(quote_date, str):
        dt = datetime.strptime(value_date, "%Y-%m-%d")
        quote_date = ql.Date(dt.day, dt.month, dt.year)

    if isinstance(value_date, str):
        dt = datetime.strptime(value_date, "%Y-%m-%d")
        value_date = ql.Date(dt.day, dt.month, dt.year)

    if isinstance(maturity_date, str):
        dt = datetime.strptime(maturity_date, "%Y-%m-%d")
        maturity_date = ql.Date(dt.day, dt.month, dt.year)

    # Set evaluation date
    ql.Settings.instance().evaluationDate = quote_date

    # Calculate the tenor (period between value_date and maturity_date)
    # This determines which LIBOR/SOFR index to use
    day_count = ql.Actual360()
    tenor_years = day_count.yearFraction(value_date, maturity_date)

    # Convert to months (rounded)
    tenor_months = int(round(tenor_years * 12))

    # Create appropriate USD LIBOR index based on tenor
    index = ql.USDLibor(ql.Period(tenor_months, ql.Months))

    # Determine position type
    if position_type.lower() == "long":
        position = ql.Position.Long
    elif position_type.lower() == "short":
        position = ql.Position.Short
    else:
        raise ValueError("position_type must be either 'long' or 'short'")

    # Create the FRA
    fra = ql.ForwardRateAgreement(
        value_date,
        maturity_date,
        position,
        strike_rate,
        notional,
        index,
    )

    return fra