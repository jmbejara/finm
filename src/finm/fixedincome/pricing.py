"""
Various functions related to bonds, including pricing, etc.
"""

import numpy as np
import pandas as pd
import QuantLib as ql


def get_coupon_dates(quote_date, maturity_date):
    """Calculate semiannual coupon payment dates between settlement and maturity."""
    quote_date = pd.to_datetime(quote_date)
    maturity_date = pd.to_datetime(maturity_date)

    # divide by 180 just to be safe
    temp = pd.date_range(
        end=maturity_date,
        periods=int(np.ceil((maturity_date - quote_date).days / 180)),
        freq=pd.DateOffset(months=6),
    )
    # filter out if one date too many
    temp = pd.DataFrame(data=temp[temp > quote_date])

    out = temp[0]
    return out


def bond_price(
    face_value: float, coupon_rate: float, ytm: float, periods: int, frequency: int = 2
) -> float:
    """
    Calculate the price of a bond.

    Parameters
    ----------
    face_value : float
        The face (par) value of the bond.
    coupon_rate : float
        The annual coupon rate (as a decimal, e.g., 0.05 for 5%).
    ytm : float
        The yield to maturity (as a decimal, e.g., 0.05 for 5%).
    periods : int
        The number of coupon periods remaining until maturity.
    frequency : int, optional
        The number of coupon payments per year (default: 2 for semi-annual).

    Returns
    -------
    float
        The price of the bond.

    Examples
    --------
    >>> bond_price(1000, 0.06, 0.05, 10, frequency=2)
    1038.8972918207702
    """
    coupon_payment = face_value * coupon_rate / frequency
    periodic_ytm = ytm / frequency

    # Present value of coupon payments (annuity)
    if periodic_ytm == 0:
        pv_coupons = coupon_payment * periods
    else:
        pv_coupons = (
            coupon_payment * (1 - (1 + periodic_ytm) ** (-periods)) / periodic_ytm
        )

    # Present value of face value
    pv_face = face_value / ((1 + periodic_ytm) ** periods)

    return pv_coupons + pv_face
