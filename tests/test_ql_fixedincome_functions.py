"""
Functions from QuantLib examples to be used for fixed income tests.
"""

import pandas as pd
import QuantLib as ql

from datetime import datetime


def ql_calc_present_value(
    future_value: float,
    rate: float,
    periods: int,
    compounding: str = "discrete",
    frequency: int = 1,
) -> float:
    """
    Calculate the present value of a future cash flow using QuantLib.

    Parameters
    ----------
    future_value : float
        The future cash flow amount.
    rate : float
        The discount rate (as a decimal, e.g., 0.05 for 5%).
    periods : int
        The number of periods until the cash flow is received.
    compounding : str, optional
        The compounding method: 'discrete', 'continuous', 'simple'.
        Defaults to 'discrete'.
    frequency : int, optional
        Compounding frequency per period (only used for discrete compounding).
        1 = annual, 2 = semi-annual, 4 = quarterly, 12 = monthly.
        Defaults to 1 (annual).

    Returns
    -------
    float
        The present value of the future cash flow.
    """

    # Map compounding string to QuantLib compounding type
    if compounding == "continuous":
        comp_type = ql.Continuous
        freq = ql.NoFrequency  # Frequency doesn't matter for continuous
    elif compounding == "simple":
        comp_type = ql.Simple
        freq = ql.NoFrequency
    elif compounding == "discrete":
        comp_type = ql.Compounded
        # Map frequency to QuantLib frequency
        freq_map = {1: ql.Annual, 2: ql.Semiannual, 4: ql.Quarterly, 12: ql.Monthly}
        freq = freq_map.get(frequency, ql.Annual)
    else:
        raise ValueError("compounding must be 'discrete', 'continuous', or 'simple'")

    # Create an InterestRate object
    day_counter = ql.Actual365Fixed()
    interest_rate = ql.InterestRate(rate, day_counter, comp_type, freq)

    # Calculate discount factor
    discount_factor = interest_rate.discountFactor(periods)

    # Calculate present value
    present_value = future_value * discount_factor

    return present_value


def ql_calc_future_value(
    present_value: float,
    rate: float,
    periods: int,
    compounding: str = "discrete",
    frequency: int = 1,
) -> float:
    """
    Calculate the future value of a present cash flow using QuantLib.

    Parameters
    ----------
    present_value : float
        The present cash flow amount.
    rate : float
        The growth/interest rate (as a decimal, e.g., 0.05 for 5%).
    periods : int
        The number of periods until the future date.
    compounding : str, optional
        The compounding method: 'discrete', 'continuous', 'simple'.
        Defaults to 'discrete'.
    frequency : int, optional
        Compounding frequency per period (only used for discrete compounding).
        1 = annual, 2 = semi-annual, 4 = quarterly, 12 = monthly.
        Defaults to 1 (annual).

    Returns
    -------
    float
        The future value of the present cash flow.
    """

    # Map compounding string to QuantLib compounding type
    if compounding == "continuous":
        comp_type = ql.Continuous
        freq = ql.NoFrequency
    elif compounding == "simple":
        comp_type = ql.Simple
        freq = ql.NoFrequency
    elif compounding == "discrete":
        comp_type = ql.Compounded
        freq_map = {1: ql.Annual, 2: ql.Semiannual, 4: ql.Quarterly, 12: ql.Monthly}
        freq = freq_map.get(frequency, ql.Annual)
    else:
        raise ValueError("compounding must be 'discrete', 'continuous', or 'simple'")

    # Create an InterestRate object
    day_counter = ql.Actual365Fixed()
    interest_rate = ql.InterestRate(rate, day_counter, comp_type, freq)

    # Calculate compound factor
    compound_factor = interest_rate.compoundFactor(periods)

    # Calculate future value
    future_value = present_value * compound_factor

    return future_value


def ql_create_schedule(
    issue_date: str,  # "YYYY-MM-DD"
    maturity_date: str,
    frequency: int = 2,
    calendar: ql.Calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond),
) -> ql.Schedule:
    """
    Create a QuantLib Schedule object.

    Parameters
    ----------
    issue_date : str
        The issue date of the bond.
    maturity_date : str
        The maturity date of the bond.
    frequency : int, optional
        The number of coupon payments per year (default: 2
        for semi-annual).
    calendar : ql.Calendar, optional
        The business day calendar to use (default: US Government
        Bond calendar).

    Returns
    -------
    ql.Schedule
        The QuantLib Schedule object.
    """

    # Convert to QuantLib dates from strings
    if isinstance(issue_date, str):
        dt = datetime.strptime(issue_date, "%Y-%m-%d")
        issue_date = ql.Date(dt.day, dt.month, dt.year)
    if isinstance(maturity_date, str):
        dt = datetime.strptime(maturity_date, "%Y-%m-%d")
        maturity_date = ql.Date(dt.day, dt.month, dt.year)

    # Set frequency
    frequency_map = {
        1: ql.Annual,
        2: ql.Semiannual,
        4: ql.Quarterly,
        12: ql.Monthly,
    }
    frequency = frequency_map[frequency]

    # Create QuantLib schedule
    schedule = ql.Schedule(
        issue_date,  # Start date of the schedule
        maturity_date,  # End date of the schedule
        ql.Period(frequency),  # Time between coupon payments
        calendar,  # Business day calendar
        ql.Following,  # Business day convention for start date (what to do if coupon falls on a holiday/weekend)
        ql.Following,  # Business day convention for end date
        ql.DateGeneration.Backward,  # Date generation rule (Backward from maturity)
        False,  # End of month rule
    )

    return schedule


def ql_get_coupon_dates(
    schedule: ql.Schedule,
) -> list:
    """
    Get coupon payment dates from a QuantLib Schedule.

    Parameters
    ----------
    schedule : ql.Schedule
        The QuantLib Schedule object.

    Returns
    -------
    list
        List of coupon dates in "YYYY-MM-DD" format.
    """

    # Create a list
    coupon_dates = []

    # Get dates
    for i in range(1, len(schedule)):  # Skip the first date (issue date)
        date = schedule[i]
        coupon_dates.append(date.ISO())  # Convert to ISO format string

    return coupon_dates


def ql_create_fixed_rate_bond(
    schedule: ql.Schedule,
    face_value: float,
    coupon_rate: float,
    day_count: ql.DayCounter = ql.ActualActual(ql.ActualActual.ISDA),
) -> ql.FixedRateBond:
    """
    Create a QuantLib FixedRateBond object.

    Parameters
    ----------
    schedule : ql.Schedule
        The QuantLib Schedule object for the bond.
    face_value : float
        The face (par) value of the bond.
    coupon_rate : float
        The annual coupon rate (as a decimal, e.g., 0.05 for 5%).
    day_count : ql.DayCounter, optional
        The day count convention to use (default: Actual/Actual
        ISDA).

    Returns
    -------
    ql.FixedRateBond
        The QuantLib FixedRateBond object.
    """

    # Create QuantLib fixed-rate bond
    bond = ql.FixedRateBond(
        settlementDays=0,  # T+0 settlement
        faceAmount=face_value,
        schedule=schedule,
        coupons=[coupon_rate],
        paymentDayCounter=day_count,
    )

    return bond


def ql_create_zero_coupon_bond(
    issue_date: str,
    maturity_date: str,
    face_value: float,
    calendar: ql.Calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond),
) -> ql.ZeroCouponBond:
    """
    Create a QuantLib ZeroCouponBond object.

    Parameters
    ----------
    issue_date : str
        The issue date of the bond.
    maturity_date : str
        The maturity date of the bond.
    face_value : float
        The face (par) value of the bond.
    calendar : ql.Calendar, optional
        The business day calendar to use (default: US Government
        Bond calendar).

    Returns
    -------
    ql.ZeroCouponBond
        The QuantLib ZeroCouponBond object.
    """

    # Convert to QuantLib dates from strings
    if isinstance(issue_date, str):
        dt = datetime.strptime(issue_date, "%Y-%m-%d")
        issue_date = ql.Date(dt.day, dt.month, dt.year)
    if isinstance(maturity_date, str):
        dt = datetime.strptime(maturity_date, "%Y-%m-%d")
        maturity_date = ql.Date(dt.day, dt.month, dt.year)

    # Create QuantLib zero coupon bond
    bond = ql.ZeroCouponBond(
        settlementDays=0,  # T+0 settlement
        calendar=calendar,
        faceAmount=face_value,
        maturityDate=maturity_date,
        paymentConvention=ql.Following,
        redemption=100.0,  # Redemption value at maturity (usually 100% of face)
        issueDate=issue_date,
    )

    return bond


def ql_get_cashflows(
    bond: ql.FixedRateBond,
) -> pd.Series:
    """
    Get bond cashflow amounts from a QuantLib bond and
    return a Series.

    Parameters
    ----------
    bond : ql.FixedRateBond
        The QuantLib FixedRateBond object.

    Returns
    -------
    pd.Series
        Series with amounts as values.
    """

    # Get cashflows (contains both dates and cashflow amounts)
    cashflows = bond.cashflows()

    # create a list of amounts
    amounts = [cf.amount() for cf in cashflows]

    # Convert to a Series
    amounts = pd.Series(amounts)

    return amounts


def ql_get_coupon_dates_cashflows(
    bond: ql.FixedRateBond | ql.ZeroCouponBond,
) -> pd.DataFrame:
    """
    Get coupon dates and bond cashflow amounts from a QuantLib bond
    and return a DataFrame.

    Parameters
    ----------
    bond : ql.FixedRateBond
        The QuantLib FixedRateBond object.

    Returns
    -------
    pd.DataFrame
        DataFrame with cashflow dates and values.
    """

    # Get cashflows (contains both dates and cashflow amounts)
    cashflows = bond.cashflows()

    # Prepare data for DataFrame
    cashflows = {
        "date": [cf.date().ISO() for cf in cashflows],
        "amount": [cf.amount() for cf in cashflows],
    }

    # Convert to a DataFrame
    cashflows = pd.DataFrame(cashflows)

    return cashflows


def ql_calc_clean_bond_price(
    valuation_date: str,
    ytm: float,
    bond: ql.FixedRateBond,
) -> float:
    """
    Calculate the clean price of a QuantLib FixedRateBond.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    ytm : float
        The yield to maturity (as a decimal, e.g., 0.05 for 5%).
    bond : ql.FixedRateBond
        The QuantLib FixedRateBond object.

    Returns
    -------
    float
        The clean price of the bond.
    """

    # Convert to QuantLib dates from strings
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Calculate clean price for bond
    clean_price = bond.cleanPrice(
        ytm,
        bond.dayCounter(),  # Use bond's day counter
        ql.Compounded,  # Use standard compounding
        bond.frequency(),  # Use bond's coupon frequency
    )

    # Check if the face value is different from 100
    face_value = bond.notional()

    if face_value == 100.0:
        return clean_price
    else:
        # QuantLib prices are quoted per 100 face
        return clean_price * (face_value / 100.0)


def ql_calc_dirty_bond_price(
    valuation_date: str,
    ytm: float,
    bond: ql.FixedRateBond,
) -> float:
    """
    Calculate the dirty price of a QuantLib FixedRateBond.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    ytm : float
        The yield to maturity (as a decimal, e.g., 0.05 for 5%).
    bond : ql.FixedRateBond
        The QuantLib FixedRateBond object.

    Returns
    -------
    float
        The dirty price of the bond.
    """

    # Convert to QuantLib dates from strings
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Calculate dirty price for bond
    dirty_price = bond.dirtyPrice(
        ytm,
        bond.dayCounter(),  # Use bond's day counter
        ql.Compounded,  # Use standard compounding
        bond.frequency(),  # Use bond's coupon frequency
    )

    # Check if the face value is different from 100
    face_value = bond.notional()

    if face_value == 100.0:
        return dirty_price
    else:
        # QuantLib prices are quoted per 100 face
        return dirty_price * (face_value / 100.0)


def ql_calc_accrued_interest(
    valuation_date: str,
    bond: ql.FixedRateBond,
) -> float:
    """
    Calculate the accrued interest of a QuantLib FixedRateBond.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    bond : ql.FixedRateBond
        The QuantLib FixedRateBond object.

    Returns
    -------
    float
        The accrued interest of the bond.
    """

    # Convert to QuantLib dates from strings
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Calculate accrued interest for bond
    accrued_interest = bond.accruedAmount()

    # Check if the face value is different from 100
    face_value = bond.notional()

    if face_value == 100.0:
        return accrued_interest
    else:
        # QuantLib prices are quoted per 100 face
        return accrued_interest * (face_value / 100.0)


def ql_calc_yield_to_maturity(
    valuation_date: str,
    clean_price: float,
    bond: ql.FixedRateBond,
    accuracy: float = 1.0e-6,
    max_evaluations: int = 100,
) -> float:
    """
    Calculate the yield to maturity of a QuantLib FixedRateBond given its clean price.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    clean_price : float
        The clean price of the bond (as a percentage, e.g., 100.0 for par).
    bond : ql.FixedRateBond
        The QuantLib FixedRateBond object.
    accuracy : float, optional
        Accuracy of the solver (default: 1.0e-10).
    max_evaluations : int, optional
        Maximum number of solver iterations (default: 100).

    Returns
    -------
    float
        The yield to maturity as a decimal (e.g., 0.05 for 5%).
    """

    # Convert to QuantLib dates from strings
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Set evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Create BondPrice object
    bond_price = ql.BondPrice(clean_price, ql.BondPrice.Clean)

    # Calculate yield to maturity
    ytm = ql.BondFunctions.bondYield(
        bond,
        bond_price,
        bond.dayCounter(),  # Use bond's day counter
        ql.Compounded,  # Use standard compounding
        bond.frequency(),  # Use bond's coupon frequency
        valuation_date,
        accuracy,
        max_evaluations,
    )

    return ytm


def ql_calc_modified_duration(
    valuation_date: str,
    ytm: float,
    bond: ql.FixedRateBond,
) -> float:
    """
    Calculate the modified duration of a QuantLib FixedRateBond.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    ytm : float
        The yield to maturity (as a decimal, e.g., 0.05 for 5%).
    bond : ql.FixedRateBond
        The QuantLib FixedRateBond object.

    Returns
    -------
    float
        The modified duration of the bond.
    """

    # Convert to QuantLib dates from strings
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Calculate modified duration for bond
    mod_duration = ql.BondFunctions.duration(
        bond,
        ytm,
        bond.dayCounter(),  # Use bond's day counter
        ql.Compounded,  # Use standard compounding
        bond.frequency(),  # Use bond's coupon frequency
        ql.Duration.Modified,
    )

    return mod_duration


def ql_calc_macaulay_duration(
    valuation_date: str,
    ytm: float,
    bond: ql.FixedRateBond,
) -> float:
    """
    Calculate the Macaulay duration of a QuantLib FixedRateBond.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    ytm : float
        The yield to maturity (as a decimal, e.g., 0.05 for 5%).
    bond : ql.FixedRateBond
        The QuantLib FixedRateBond object.

    Returns
    -------
    float
        The Macaulay duration of the bond.
    """

    # Convert to QuantLib dates from strings
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Calculate Macaulay duration for bond
    mac_duration = ql.BondFunctions.duration(
        bond,
        ytm,
        bond.dayCounter(),  # Use bond's day counter
        ql.Compounded,  # Use standard compounding
        bond.frequency(),  # Use bond's coupon frequency
        ql.Duration.Macaulay,
    )

    return mac_duration


def ql_calc_convexity(
    valuation_date: str,
    ytm: float,
    bond: ql.FixedRateBond,
) -> float:
    """
    Calculate the convexity of a QuantLib FixedRateBond.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    ytm : float
        The yield to maturity (as a decimal, e.g., 0.05 for 5%).
    bond : ql.FixedRateBond
        The QuantLib FixedRateBond object.

    Returns
    -------
    float
        The convexity of the bond.
    """

    # Convert to QuantLib dates from strings
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Calculate convexity for bond
    convexity = ql.BondFunctions.convexity(
        bond,
        ytm,
        bond.dayCounter(),  # Use bond's day counter
        ql.Compounded,  # Use standard compounding
        bond.frequency(),  # Use bond's coupon frequency
    )

    return convexity


def ql_calc_zero_coupon_bond_price(
    valuation_date: str,
    ytm: float,
    bond: ql.ZeroCouponBond,
    day_counter: ql.DayCounter = ql.ActualActual(ql.ActualActual.ISDA),
) -> float:
    """
    Calculate the price of a QuantLib ZeroCouponBond.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    ytm : float
        The yield to maturity (as a decimal, e.g., 0.05 for 5%).
    zero_bond : ql.ZeroCouponBond
        The QuantLib ZeroCouponBond object.

    Returns
    -------
    float
        The price of the zero-coupon bond.
    """

    # Convert to QuantLib dates from strings
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Calculate price for zero coupon bond
    price = bond.cleanPrice(
        ytm,
        day_counter,
        ql.Compounded,  # Use standard compounding
        ql.Annual,  # Zero coupon bonds pay annually (at maturity)
    )

    # Check if the face value is different from 100
    face_value = bond.notional()

    if face_value == 100.0:
        return price
    else:
        # QuantLib prices are quoted per 100 face
        return price * (face_value / 100.0)


def ql_calc_dollar_duration(
    valuation_date: str,
    ytm: float,
    bond: ql.FixedRateBond,
    face_value: float = 100.0,
) -> float:
    """
    Calculate the dollar duration (DV01) of a QuantLib FixedRateBond.

    Dollar duration measures the change in bond price for a 1 basis point (0.01%)
    change in yield. It's also known as DV01 (dollar value of a basis point).

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    ytm : float
        The yield to maturity (as a decimal, e.g., 0.05 for 5%).
    bond : ql.FixedRateBond
        The QuantLib FixedRateBond object.
    face_value : float, optional
        The face value of the bond position (default: 100.0).

    Returns
    -------
    float
        The dollar duration (change in dollar value for 1bp yield change).
    """

    # Convert to QuantLib dates from strings
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Set evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Calculate modified duration
    mod_duration = ql_calc_modified_duration(
        valuation_date=valuation_date,
        ytm=ytm,
        bond=bond,
    )

    # Calculate current clean price
    clean_price = ql_calc_clean_bond_price(
        valuation_date=valuation_date,
        ytm=ytm,
        bond=bond,
    )

    # Dollar duration = Modified Duration × Price × 0.0001 (for 1bp)
    # Price is expressed per 100 face value, so scale by (face_value / 100)
    dollar_duration = mod_duration * clean_price * 0.0001 * (face_value / 100.0)

    return dollar_duration
