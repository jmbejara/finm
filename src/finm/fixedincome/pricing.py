"""
Bond pricing and risk calculations for fixed income securities.

This module provides basic functions for:

- Present value
- Future value
- Coupon dates
- Cashflows
- Clean price
- Dirty price
- Accrued interest
- Yield to maturity
- Macaulay duration
- Modified duration
- Convexity
- Zero coupon bond price
- Dollar duration
"""

import numpy as np
import pandas as pd

from datetime import datetime


def present_value(
    future_value: float,
    rate: float,
    periods: int,
    compounding: str = "discrete",
) -> float:
    """
    Calculate the present value of a future cash flow.

    Parameters
    ----------
    future_value : float
        The future cash flow amount.
    rate : float
        The discount rate (as a decimal, e.g., 0.05 for 5%).
    periods : int
        The number of periods until the cash flow is received.
    compounding : str
        The compounding method: 'discrete' or 'continuous'.
        Defaults to 'discrete'.

    Returns
    -------
    float
        The present value of the future cash flow.

    Example:
        ```python
        >>> present_value(1000, 0.05, 2)
        907.0294784580498
        >>> present_value(1000, 0.05, 2, compounding='continuous')
        904.8374180359595
        ```
    """

    # YOUR CODE HERE

    if compounding == "continuous":
        return future_value * np.exp(-rate * periods)
    else:
        return future_value / ((1 + rate) ** periods)


def future_value(
    present_value: float,
    rate: float,
    periods: int,
    compounding: str = "discrete",
) -> float:
    """
    Calculate the future value of a present cash flow.

    Parameters
    ----------
    present_value : float
        The present cash flow amount.
    rate : float
        The interest rate (as a decimal, e.g., 0.05 for 5%).
    periods : int
        The number of periods for compounding.
    compounding : str
        The compounding method: 'discrete' or 'continuous'.
        Defaults to 'discrete'.

    Returns
    -------
    float
        The future value of the present cash flow.

    Example:
        ```python
        >>> future_value(1000, 0.05, 2)
        1102.5
        >>> future_value(1000, 0.05, 2, compounding='continuous')
        1105.1709180756477
        ```
    """

    # YOUR CODE HERE

    if compounding == "continuous":
        return present_value * np.exp(rate * periods)
    else:
        return present_value * ((1 + rate) ** periods)


def get_coupon_dates(
    issue_date: str | datetime,
    maturity_date: str | datetime,
    frequency: int = 2,
) -> list[str]:
    """
    Calculate coupon payment dates for a bond.

    Parameters
    ----------
    issue_date : str or datetime
        The issue date of the bond.
    maturity_date : str or datetime
        The maturity date of the bond.
    frequency : int, optional
        Payment frequency (1=annual, 2=semi-annual, 4=quarterly, 12=monthly).
        Defaults to 2 (semi-annual).

    Returns
    -------
    list[str]
        List of coupon payment dates in "YYYY-MM-DD" format.

    Raises
    ------
    ValueError
        If issue date is not earlier than maturity date.
    """

    # YOUR CODE HERE

    # Convert input to datetime if needed
    if isinstance(issue_date, str):
        issue_date = datetime.strptime(issue_date, "%Y-%m-%d")
    if isinstance(maturity_date, str):
        maturity_date = datetime.strptime(maturity_date, "%Y-%m-%d")

    # Ensure dates are valid
    if issue_date >= maturity_date:
        raise ValueError("Issue date must be earlier than maturity date.")

    # Calculate months between payments
    months_between_payments = 12 // frequency

    # Generate coupon dates working forward from issue date
    offset = pd.DateOffset(months=months_between_payments)
    dates = []
    current_date = issue_date + offset

    while current_date <= maturity_date:
        dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += offset

    return dates


def calc_bond_cashflows(
    issue_date: str | datetime,
    maturity_date: str | datetime,
    face_value: float,
    coupon_rate: float,
    frequency: int = 2,
) -> pd.Series:
    """
    Calculate the cashflows (coupons and principal) payments
    for a bond.

    Parameters
    ----------
    issue_date : str or datetime
        The issue date of the bond.
    maturity_date : str or datetime
        The maturity date of the bond.
    face_value : float
        The face (par) value of the bond.
    coupon_rate : float
        The annual coupon rate (as a decimal, e.g., 0.05 for 5%).
    frequency : int, optional
        Payment frequency (1=annual, 2=semi-annual, 4=quarterly, 12=monthly).
        Defaults to 2 (semi-annual).

    Returns
    -------
    pd.Series
        A list of cashflows as a pandas Series.
    """

    # YOUR CODE HERE

    # Get the coupon payment dates
    coupon_dates = get_coupon_dates(issue_date, maturity_date, frequency)

    # Calculate the periodic coupon payment
    coupon_payment = face_value * coupon_rate / frequency

    # Create a list of cashflows (all coupons)
    cashflows = [coupon_payment] * len(coupon_dates)

    # Add the principal as the final cashflow
    cashflows.append(face_value)

    # Convert to pandas Series
    return pd.Series(cashflows)


def calc_clean_bond_price(
    face_value: float,
    coupon_rate: float,
    ytm: float,
    periods: int,
    frequency: int = 2,
) -> float:
    """
    Calculate the price of a bond.

    Parameters
    ----------
    issue_date : str
        The issue date of the bond.
    valuation_date : str
        The valuation date for pricing the bond.
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

    # YOUR CODE HERE

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


def calc_dirty_bond_price(
    clean_price: float,
    accrued_interest: float,
) -> float:
    """
    Calculate the dirty price of a bond.

    Parameters
    ----------
    clean_price : float
        The clean price of the bond.
    accrued_interest : float
        The accrued interest of the bond.

    Returns
    -------
    float
        The dirty price of the bond.
    """

    # YOUR CODE HERE

    # Dirty price = Clean price + Accrued interest
    dirty_price = clean_price + accrued_interest

    return dirty_price


def calc_accrued_interest(
    last_coupon_date: str,
    next_coupon_date: str,
    valuation_date: str,
    face_value: float,
    coupon_rate: float,
    frequency: int = 2,
) -> float:
    """
    Calculate the accrued interest on a bond.

    Parameters
    ----------
    last_coupon_date : str
        The last coupon payment date of the bond.
    next_coupon_date : str
        The next coupon payment date of the bond.
    valuation_date : str
        The valuation date for calculating accrued interest.
    face_value : float
        The face (par) value of the bond.
    coupon_rate : float
        The annual coupon rate (as a decimal, e.g., 0.05 for 5%).
    frequency : int, optional
        The number of coupon payments per year (default: 2 for semi-annual).

    Returns
    -------
    float
        The accrued interest amount.
    """

    # YOUR CODE HERE

    # Convert dates to datetime objects
    last_coupon_dt = datetime.strptime(last_coupon_date, "%Y-%m-%d")
    next_coupon_dt = datetime.strptime(next_coupon_date, "%Y-%m-%d")
    valuation_dt = datetime.strptime(valuation_date, "%Y-%m-%d")

    # Calculate days in the coupon period
    days_in_period = (next_coupon_dt - last_coupon_dt).days

    # Calculate days accrued (from last coupon to valuation)
    days_accrued = (valuation_dt - last_coupon_dt).days

    # Calculate the full coupon payment
    full_coupon = face_value * coupon_rate / frequency

    # Calculate accrued interest (proportional to days elapsed)
    accrued_interest = full_coupon * (days_accrued / days_in_period)

    return accrued_interest


def calc_yield_to_maturity(
    clean_price: float,
    face_value: float,
    coupon_rate: float,
    periods: int,
    frequency: int = 2,
    initial_guess: float = 0.05,
    tolerance: float = 1e-6,
    max_iterations: int = 100,
) -> float:
    """
    Calculate the yield to maturity of a bond given its clean price.

    Uses Newton-Raphson method to find the YTM that produces the given price.

    Parameters
    ----------
    clean_price : float
        The clean price of the bond.
    face_value : float
        The face (par) value of the bond.
    coupon_rate : float
        The annual coupon rate (as a decimal, e.g., 0.05 for 5%).
    periods : int
        The number of coupon periods remaining until maturity.
    frequency : int, optional
        The number of coupon payments per year (default: 2 for semi-annual).
    initial_guess : float, optional
        Initial guess for YTM (default: 0.05 for 5%).
    tolerance : float, optional
        Convergence tolerance (default: 1e-6).
    max_iterations : int, optional
        Maximum number of iterations (default: 100).

    Returns
    -------
    float
        The yield to maturity as a decimal (e.g., 0.05 for 5%).
    """

    ytm = initial_guess

    for iteration in range(max_iterations):
        # Calculate price at current YTM guess
        calculated_price = calc_clean_bond_price(
            face_value=face_value,
            coupon_rate=coupon_rate,
            ytm=ytm,
            periods=periods,
            frequency=frequency,
        )

        # Check if we're close enough
        price_diff = calculated_price - clean_price
        if abs(price_diff) < tolerance:
            return ytm

        # Calculate derivative (price change for small YTM change)
        delta_ytm = 0.0001  # 1 basis point
        price_up = calc_clean_bond_price(
            face_value=face_value,
            coupon_rate=coupon_rate,
            ytm=ytm + delta_ytm,
            periods=periods,
            frequency=frequency,
        )

        # Derivative of price with respect to YTM
        dprice_dytm = (price_up - calculated_price) / delta_ytm

        # Newton-Raphson update: ytm_new = ytm_old - f(ytm) / f'(ytm)
        if abs(dprice_dytm) > 1e-10:  # Avoid division by zero
            ytm = ytm - price_diff / dprice_dytm
        else:
            # If derivative is too small, use bisection step
            ytm = ytm - 0.01 * (1 if price_diff > 0 else -1)

        # Keep YTM in reasonable bounds
        ytm = max(0.0001, min(ytm, 0.5))  # Between 0.01% and 50%

    # If we didn't converge, return the best estimate
    return ytm


def calc_macaulay_duration(
    face_value: float, coupon_rate: float, ytm: float, periods: int, frequency: int = 2
) -> float:
    """
    Calculate the Macaulay duration of a bond.

    Macaulay duration is the weighted average time to receive the bond's cash flows,
    where weights are the present values of each cash flow.

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
        The Macaulay duration in years.
    """

    # Calculate periodic values
    coupon_payment = face_value * coupon_rate / frequency
    periodic_ytm = ytm / frequency

    # Calculate weighted average time to cash flows
    weighted_time_sum = 0.0
    total_pv = 0.0

    # Process each coupon payment
    for t in range(1, periods + 1):
        # Present value of this cash flow
        if t < periods:
            # Regular coupon payment
            cash_flow = coupon_payment
        else:
            # Final payment includes coupon + principal
            cash_flow = coupon_payment + face_value

        # Discount the cash flow
        pv_cash_flow = cash_flow / ((1 + periodic_ytm) ** t)

        # Time in periods
        time_in_periods = t

        # Add to weighted sum (PV × time)
        weighted_time_sum += pv_cash_flow * time_in_periods
        total_pv += pv_cash_flow

    # Macaulay duration in periods
    duration_in_periods = weighted_time_sum / total_pv

    # Convert to years
    duration_in_years = duration_in_periods / frequency

    return duration_in_years


def calc_modified_duration(
    face_value: float, coupon_rate: float, ytm: float, periods: int, frequency: int = 2
) -> float:
    """
    Calculate the modified duration of a bond.

    Modified duration measures the percentage change in bond price for a
    1% change in yield. It's related to Macaulay duration by:
    Modified Duration = Macaulay Duration / (1 + ytm/frequency)

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
        The modified duration in years.
    """

    # First calculate Macaulay duration
    macaulay_duration = calc_macaulay_duration(
        face_value=face_value,
        coupon_rate=coupon_rate,
        ytm=ytm,
        periods=periods,
        frequency=frequency,
    )

    # Convert to modified duration
    periodic_ytm = ytm / frequency
    modified_duration = macaulay_duration / (1 + periodic_ytm)

    return modified_duration


def calc_convexity(
    face_value: float, coupon_rate: float, ytm: float, periods: int, frequency: int = 2
) -> float:
    """
    Calculate the convexity of a bond.

    Convexity measures the curvature of the price-yield relationship.
    It's used to improve duration-based price estimates for larger yield changes.

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
        The convexity of the bond.
    """

    # Calculate periodic values
    coupon_payment = face_value * coupon_rate / frequency
    periodic_ytm = ytm / frequency

    # Calculate bond price
    bond_price = calc_clean_bond_price(
        face_value=face_value,
        coupon_rate=coupon_rate,
        ytm=ytm,
        periods=periods,
        frequency=frequency,
    )

    # Calculate sum of (t × (t+1) × PV of cash flow)
    weighted_pv_sum = 0.0

    for t in range(1, periods + 1):
        # Determine cash flow
        if t < periods:
            cash_flow = coupon_payment
        else:
            cash_flow = coupon_payment + face_value

        # PV of cash flow
        pv_cash_flow = cash_flow / ((1 + periodic_ytm) ** t)

        # Weight by t × (t + 1)
        weighted_pv_sum += t * (t + 1) * pv_cash_flow

    # Convexity formula: Σ[t(t+1) × PV(CF_t)] / [P × (1+y)^2]
    convexity_periods = weighted_pv_sum / (bond_price * (1 + periodic_ytm) ** 2)

    # Convert from periods to years (divide by frequency^2)
    convexity = convexity_periods / (frequency**2)

    return convexity


def calc_zero_bond_price(
    face_value: float, ytm: float, years_to_maturity: float, frequency: int = 2
) -> float:
    """
    Calculate the price of a zero coupon bond.

    A zero coupon bond makes no periodic interest payments. It only pays
    the face value at maturity, so its price is simply the present value
    of that single future payment.

    Parameters
    ----------
    face_value : float
        The face (par) value of the bond.
    ytm : float
        The yield to maturity (as a decimal, e.g., 0.05 for 5%).
    years_to_maturity : float
        The number of years until maturity.
    frequency : int, optional
        The compounding frequency per year (default: 2 for semi-annual).

    Returns
    -------
    float
        The price of the zero coupon bond.
    """

    # Calculate periodic yield
    periodic_ytm = ytm / frequency

    # Calculate total number of compounding periods
    total_periods = years_to_maturity * frequency

    # Present value of face value
    price = face_value / ((1 + periodic_ytm) ** total_periods)

    return price


def calc_dollar_duration(
    face_value: float, coupon_rate: float, ytm: float, periods: int, frequency: int = 2
) -> float:
    """
    Calculate the dollar duration (DV01) of a bond.

    Dollar duration measures the change in bond price (in dollars) for a
    1 basis point (0.01%) change in yield. It's also known as DV01
    (dollar value of a 01, i.e., one basis point).

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
        The dollar duration (change in dollar value for 1bp yield change).
    """

    # Calculate modified duration
    modified_duration = calc_modified_duration(
        face_value=face_value,
        coupon_rate=coupon_rate,
        ytm=ytm,
        periods=periods,
        frequency=frequency,
    )

    # Calculate current clean price
    clean_price = calc_clean_bond_price(
        face_value=face_value,
        coupon_rate=coupon_rate,
        ytm=ytm,
        periods=periods,
        frequency=frequency,
    )

    # Dollar duration = Modified Duration × Price × 0.0001 (for 1bp)
    # 0.0001 = 1 basis point as a decimal (0.01% = 0.0001)
    dollar_duration = modified_duration * clean_price * 0.0001

    return dollar_duration
