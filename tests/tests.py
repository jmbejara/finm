"""
Functions from QuantLib examples to be used in tests.
"""

import numpy as np
import pandas as pd
import QuantLib as ql

from datetime import datetime


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
        The number of coupon payments per year (default: 2 for semi-annual).
    calendar : ql.Calendar, optional
        The business day calendar to use (default: US Government Bond calendar).

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


def ql_extract_coupon_dates(
    schedule: ql.Schedule,
) -> pd.Series:
    """
    Extract coupon dates from a QuantLib Schedule object and return a Series.

    Parameters
    ----------
    schedule : ql.Schedule
        The QuantLib Schedule object.

    Returns
    -------
    pd.Series
        Series with cashflow dates.
    """

    # Create a list of dates
    dates = [date for date in schedule]

    # Convert to a Series
    dates = pd.Series(dates)

    return dates


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
        The day count convention to use (default: Actual/Actual ISDA).

    Returns
    -------
    ql.FixedRateBond
        The QuantLib FixedRateBond object.
    """

    # Create QuantLib fixed-rate bond
    bond = ql.FixedRateBond(
        settlementDays=1,  # T+1 settlement
        faceAmount=face_value,
        schedule=schedule,
        coupons=[coupon_rate],
        paymentDayCounter=day_count,
    )

    return bond


def ql_extract_cashflows(
    bond: ql.FixedRateBond,
) -> pd.Series:
    """
    Extract bond cashflow amounts from a QuantLib bond and return a Series.

    Parameters
    ----------
    bond : ql.FixedRateBond
        The QuantLib FixedRateBond object.

    Returns
    -------
    pd.Series
        Series with cashflow dates as index and amounts as values.
    """

    # Extract cashflows (contains both dates and cashflow amounts)
    cashflows = bond.cashflows()

    # create a list of amounts
    amounts = [cf.amount() for cf in cashflows]

    # Convert to a Series
    amounts = pd.Series(amounts)

    return amounts


def ql_extract_coupon_dates_cashflows(
    bond: ql.FixedRateBond,
) -> pd.DataFrame:
    """
    Extract coupon dates and bond cashflow amounts from a QuantLib bond
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

    # Extract cashflows (contains both dates and cashflow amounts)
    cashflows = bond.cashflows()

    # Prepare data for DataFrame
    cashflows = {
        "date": [cf.date() for cf in cashflows],
        "amount": [cf.amount() for cf in cashflows],
    }

    # Conver to a DataFrame
    cashflows = pd.DataFrame(cashflows)

    return cashflows


def ql_calc_clean_price(
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


def ql_calc_dirty_price(
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


if __name__ == "__main__":
    quote_date = "2020-01-01"
    maturity_date = "2025-12-24"
    valuation_date = "2020-02-01"

    schedule = ql_create_schedule(
        issue_date=quote_date,
        maturity_date=maturity_date,
        frequency=2,
    )

    coupon_dates = ql_extract_coupon_dates(schedule)
    print(coupon_dates)

    bond = ql_create_fixed_rate_bond(
        schedule=schedule,
        face_value=1000,
        coupon_rate=0.05,
    )

    cashflows = ql_extract_cashflows(bond)
    print(cashflows)

    coupon_dates_cashflows = ql_extract_coupon_dates_cashflows(bond)
    print(coupon_dates_cashflows)

    clean_price = ql_calc_clean_price(
        valuation_date=valuation_date,
        ytm=0.06,
        bond=bond,
    )

    print(clean_price)

    dirty_price = ql_calc_dirty_price(
        valuation_date=valuation_date,
        ytm=0.06,
        bond=bond,
    )

    print(dirty_price)

    accrued_interest = ql_calc_accrued_interest(
        valuation_date=valuation_date,
        bond=bond,
    )

    print(accrued_interest)

    print(dirty_price - clean_price)

    modified_duration = ql_calc_modified_duration(
        valuation_date=valuation_date,
        ytm=0.06,
        bond=bond,
    )

    print(modified_duration)

    # mac_duration = ql.BondFunctions.duration(
    #     bond,
    #     ytm,
    #     day_count,
    #     ql.Compounded,
    #     frequency,
    #     ql.Duration.Macaulay,
    # )

    # print(mac_duration)

    # convexity = ql.BondFunctions.convexity(
    #     bond,
    #     ytm,
    #     day_count,
    #     ql.Compounded,
    #     frequency,
    # )

    # print(convexity)

    # valuation_date = ql.Date(15, 1, 2025)

    # curve = ql.FlatForward(
    #     valuation_date,
    #     ql.QuoteHandle(ql.SimpleQuote(0.045)),
    #     day_count,
    #     ql.Compounded,
    #     ql.Semiannual,
    # )

    # curve_handle = ql.YieldTermStructureHandle(curve)

    # engine = ql.DiscountingBondEngine(curve_handle)

    # bond.setPricingEngine(engine)

    # pv = bond.NPV()
    # print(pv)

    # clean_price = pv - bond.accruedAmount()
    # print(clean_price)

    # # Create complete yield curve
    # treasury_data = [
    #     # maturity (years), coupon, clean price
    #     (2, 0.030, 99.50),
    #     (5, 0.035, 100.20),
    #     (10, 0.040, 101.80),
    #     (30, 0.045, 103.10),
    # ]

    # valuation_date = ql.Date(15, 1, 2025)
    # ql.Settings.instance().evaluationDate = valuation_date

    # calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    # day_count = ql.ActualActual(ql.ActualActual.ISDA)
    # frequency = ql.Semiannual
    # settlement_days = 1

    # helpers = []

    # for maturity_years, coupon, clean_price in treasury_data:
    #     maturity_date = valuation_date + ql.Period(maturity_years, ql.Years)

    #     schedule = ql.Schedule(
    #         valuation_date,
    #         maturity_date,
    #         ql.Period(frequency),
    #         calendar,
    #         ql.Following,
    #         ql.Following,
    #         ql.DateGeneration.Backward,
    #         False,
    #     )

    #     bond_helper = ql.FixedRateBondHelper(
    #         ql.QuoteHandle(ql.SimpleQuote(clean_price)),
    #         settlement_days,
    #         100.0,  # par = 100 for curve building
    #         schedule,
    #         [coupon],
    #         day_count,
    #     )

    #     helpers.append(bond_helper)

    # curve = ql.PiecewiseLogLinearDiscount(
    #     valuation_date,
    #     helpers,
    #     day_count,
    # )

    # curve_handle = ql.YieldTermStructureHandle(curve)

    # for y in [1, 2, 5, 10, 30]:
    #     date = valuation_date + ql.Period(y, ql.Years)
    #     print(y, curve.discount(date))

    # for y in [1, 2, 5, 10, 30]:
    #     date = valuation_date + ql.Period(y, ql.Years)
    #     zero = curve.zeroRate(
    #         date,
    #         day_count,
    #         ql.Compounded,
    #         frequency,
    #     ).rate()
    #     print(y, zero)

    # engine = ql.DiscountingBondEngine(curve_handle)

    # test_bond = ql.FixedRateBond(
    #     settlement_days,
    #     100.0,
    #     schedule,
    #     [coupon],
    #     day_count,
    # )

    # test_bond.setPricingEngine(engine)

    # model_price = test_bond.cleanPrice()

    # # Create zero coupon bond
    # import QuantLib as ql

    # valuation_date = ql.Date(15, 1, 2025)
    # ql.Settings.instance().evaluationDate = valuation_date

    # calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    # day_count = ql.ActualActual(ql.ActualActual.ISDA)

    # settlement_days = 1
    # face_value = 100.0

    # issue_date = valuation_date
    # maturity_date = valuation_date + ql.Period(10, ql.Years)

    # # ZeroCouponBond(
    # #     settlementDays,   # T+ settlement
    # #     calendar,         # business-day calendar
    # #     faceAmount,       # notional
    # #     maturityDate,     # when principal is paid
    # #     paymentConvention,# adjust maturity date
    # #     redemption,       # usually = faceAmount
    # #     issueDate,        # optional, but good practice
    # # )

    # zero_bond = ql.ZeroCouponBond(
    #     settlement_days,
    #     calendar,
    #     face_value,
    #     maturity_date,
    #     ql.Following,
    #     face_value,  # redemption
    #     issue_date,
    # )

    # for cf in zero_bond.cashflows():
    #     print(cf.date(), cf.amount())
