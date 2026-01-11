"""Bond pricing and risk calculations for fixed income securities.

This module provides basic functions for:

- Present and future value calculations
- Bond pricing
- Yield to maturity calculations
- Duration and convexity measures
- Calculate semiannual coupon payment dates for a bond
"""

from datetime import datetime

import numpy as np
import pandas as pd

import finm


def present_value(
    future_value: float, rate: float, periods: float, compounding: str = "discrete"
) -> float:
    """Calculate the present value of a future cash flow.

    :param future_value: The future cash flow amount.
    :param rate: The discount rate (as a decimal, e.g., 0.05 for 5%).
    :param periods: The number of periods until the cash flow is received.
    :param compounding: The compounding method: 'discrete' or 'continuous'.
        Defaults to 'discrete'.
    :returns: The present value of the future cash flow.

    Example:
        ```python
        >>> present_value(1000, 0.05, 2)
        907.0294784580498
        >>> present_value(1000, 0.05, 2, compounding='continuous')
        904.8374180359595
        ```
    """
    if compounding == "continuous":
        return future_value * np.exp(-rate * periods)
    else:
        return future_value / ((1 + rate) ** periods)


def future_value(
    present_value: float, rate: float, periods: float, compounding: str = "discrete"
) -> float:
    """Calculate the future value of a present cash flow.

    :param present_value: The present cash flow amount.
    :param rate: The interest rate (as a decimal, e.g., 0.05 for 5%).
    :param periods: The number of periods for compounding.
    :param compounding: The compounding method: 'discrete' or 'continuous'.
        Defaults to 'discrete'.
    :returns: The future value of the present cash flow.

    Example:
        ```python
        >>> future_value(1000, 0.05, 2)
        1102.5
        >>> future_value(1000, 0.05, 2, compounding='continuous')
        1105.1709180756477
        ```
    """
    if compounding == "continuous":
        return present_value * np.exp(rate * periods)
    else:
        return present_value * ((1 + rate) ** periods)


def yield_to_maturity(
    price: float,
    face_value: float,
    coupon_rate: float,
    periods: int,
    frequency: int = 2,
    tolerance: float = 1e-8,
    max_iterations: int = 100,
) -> float:
    """Calculate the yield to maturity of a bond using Newton-Raphson method.

    :param price: The current market price of the bond.
    :param face_value: The face (par) value of the bond.
    :param coupon_rate: The annual coupon rate (as a decimal, e.g., 0.05 for 5%).
    :param periods: The number of coupon periods remaining until maturity.
    :param frequency: The number of coupon payments per year. Defaults to 2.
    :param tolerance: The convergence tolerance. Defaults to 1e-8.
    :param max_iterations: Maximum number of iterations. Defaults to 100.
    :returns: The annualized yield to maturity.
    :raises ValueError: If YTM calculation does not converge.

    Example:
        ```python
        >>> ytm = yield_to_maturity(1038.90, 1000, 0.06, 10, frequency=2)
        >>> round(ytm, 4)
        0.05
        ```
    """
    coupon_payment = face_value * coupon_rate / frequency

    # Initial guess based on current yield
    ytm_guess = coupon_rate

    for _ in range(max_iterations):
        # Calculate bond price at current YTM guess
        periodic_ytm = ytm_guess / frequency

        if abs(periodic_ytm) < 1e-10:
            calculated_price = coupon_payment * periods + face_value
        else:
            pv_coupons = (
                coupon_payment * (1 - (1 + periodic_ytm) ** (-periods)) / periodic_ytm
            )
            pv_face = face_value / ((1 + periodic_ytm) ** periods)
            calculated_price = pv_coupons + pv_face

        # Price difference
        diff = calculated_price - price

        if abs(diff) < tolerance:
            return ytm_guess

        # Calculate derivative (dPrice/dYTM)
        if abs(periodic_ytm) < 1e-10:
            # Use approximation for very small yields
            derivative = (
                -sum((i + 1) * coupon_payment / frequency for i in range(periods))
                - periods * face_value / frequency
            )
        else:
            # Derivative of bond price with respect to YTM
            derivative = 0
            for i in range(1, periods + 1):
                derivative -= (
                    i * coupon_payment / (frequency * (1 + periodic_ytm) ** (i + 1))
                )
            derivative -= (
                periods * face_value / (frequency * (1 + periodic_ytm) ** (periods + 1))
            )

        # Newton-Raphson update
        ytm_guess = ytm_guess - diff / derivative

    raise ValueError(
        f"YTM calculation did not converge after {max_iterations} iterations"
    )


def duration(
    face_value: float, coupon_rate: float, ytm: float, periods: int, frequency: int = 2
) -> float:
    """Calculate the Macaulay duration of a bond.

    :param face_value: The face (par) value of the bond.
    :param coupon_rate: The annual coupon rate (as a decimal, e.g., 0.05 for 5%).
    :param ytm: The yield to maturity (as a decimal, e.g., 0.05 for 5%).
    :param periods: The number of coupon periods remaining until maturity.
    :param frequency: The number of coupon payments per year. Defaults to 2.
    :returns: The Macaulay duration in years.

    Example:
        ```python
        >>> dur = duration(1000, 0.06, 0.05, 10, frequency=2)
        >>> round(dur, 4)
        4.3295
        ```
    """
    coupon_payment = face_value * coupon_rate / frequency
    periodic_ytm = ytm / frequency

    price = finm.bond_price(face_value, coupon_rate, ytm, periods, frequency)

    # Calculate weighted average time
    weighted_sum = 0
    for t in range(1, periods + 1):
        # Present value of coupon at time t
        pv_coupon = coupon_payment / ((1 + periodic_ytm) ** t)
        # Weight by time (in years)
        weighted_sum += (t / frequency) * pv_coupon

    # Add the present value of face value at maturity
    pv_face = face_value / ((1 + periodic_ytm) ** periods)
    weighted_sum += (periods / frequency) * pv_face

    return weighted_sum / price


def modified_duration(
    face_value: float, coupon_rate: float, ytm: float, periods: int, frequency: int = 2
) -> float:
    """Calculate the modified duration of a bond.

    Modified duration measures the percentage change in bond price
    for a 1% change in yield.

    :param face_value: The face (par) value of the bond.
    :param coupon_rate: The annual coupon rate (as a decimal, e.g., 0.05 for 5%).
    :param ytm: The yield to maturity (as a decimal, e.g., 0.05 for 5%).
    :param periods: The number of coupon periods remaining until maturity.
    :param frequency: The number of coupon payments per year. Defaults to 2.
    :returns: The modified duration.

    Example:
        ```python
        >>> mod_dur = modified_duration(1000, 0.06, 0.05, 10, frequency=2)
        >>> round(mod_dur, 4)
        4.2239
        ```
    """
    mac_duration = duration(face_value, coupon_rate, ytm, periods, frequency)
    periodic_ytm = ytm / frequency

    return mac_duration / (1 + periodic_ytm)


def convexity(
    face_value: float, coupon_rate: float, ytm: float, periods: int, frequency: int = 2
) -> float:
    """Calculate the convexity of a bond.

    Convexity measures the curvature of the bond price-yield relationship
    and is used to improve duration-based price change estimates.

    :param face_value: The face (par) value of the bond.
    :param coupon_rate: The annual coupon rate (as a decimal, e.g., 0.05 for 5%).
    :param ytm: The yield to maturity (as a decimal, e.g., 0.05 for 5%).
    :param periods: The number of coupon periods remaining until maturity.
    :param frequency: The number of coupon payments per year. Defaults to 2.
    :returns: The convexity of the bond.

    Example:
        ```python
        >>> conv = convexity(1000, 0.06, 0.05, 10, frequency=2)
        >>> round(conv, 2)
        21.74
        ```
    """
    coupon_payment = face_value * coupon_rate / frequency
    periodic_ytm = ytm / frequency

    price = finm.bond_price(face_value, coupon_rate, ytm, periods, frequency)

    # Calculate convexity
    convexity_sum = 0
    for t in range(1, periods + 1):
        # Present value of coupon at time t
        pv_coupon = coupon_payment / ((1 + periodic_ytm) ** t)
        # Add t * (t + 1) * PV(CF) / (1 + y)^2
        convexity_sum += t * (t + 1) * pv_coupon

    # Add the face value at maturity
    pv_face = face_value / ((1 + periodic_ytm) ** periods)
    convexity_sum += periods * (periods + 1) * pv_face

    # Adjust for compounding frequency
    convexity_value = convexity_sum / (price * (1 + periodic_ytm) ** 2 * frequency**2)

    return convexity_value


def get_coupon_dates(quote_date, maturity_date):
    """Calculate semiannual coupon payment dates for a bond.

    :param quote_date: The quote date of the bond (str or datetime).
    :param maturity_date: The maturity date of the bond (str or datetime).
    :returns: List of semiannual coupon payment dates after the quote date.
    :raises ValueError: If quote date is not earlier than maturity date.
    """
    # Convert input to datetime if needed
    if isinstance(quote_date, str):
        quote_date = datetime.strptime(quote_date, "%Y-%m-%d")
    if isinstance(maturity_date, str):
        maturity_date = datetime.strptime(maturity_date, "%Y-%m-%d")

    # Ensure dates are valid
    if quote_date >= maturity_date:
        raise ValueError("Quote date must be earlier than maturity date.")

    # Generate coupon dates
    semiannual_offset = pd.DateOffset(months=6)
    dates = []
    current_date = maturity_date

    while current_date > quote_date:
        dates.append(current_date)
        current_date -= semiannual_offset

    # Return sorted dates in ascending order
    return sorted(dates)
