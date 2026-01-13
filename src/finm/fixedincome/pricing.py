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


def ql_get_coupon_dates(
    quote_date,
    maturity_date,
    calendar=ql.UnitedStates(m=ql.UnitedStates.GovernmentBond),
    business_convention=ql.Following,
    end_of_month=False,
):
    """
    Calculate semiannual coupon payment dates using QuantLib.

    Parameters
    ----------
    quote_date : str or datetime
        Valuation / settlement date
    maturity_date : str or datetime
        Bond maturity date
    calendar : ql.Calendar
        Business calendar
    business_convention : ql.BusinessDayConvention
        Date adjustment rule
    end_of_month : bool
        Apply end-of-month rule

    Returns
    -------
    pd.Series
        Coupon dates strictly after quote_date
    """

    # Convert to QuantLib Dates
    ql_quote = ql.Date(
        pd.to_datetime(quote_date).day,
        pd.to_datetime(quote_date).month,
        pd.to_datetime(quote_date).year,
    )
    ql_maturity = ql.Date(
        pd.to_datetime(maturity_date).day,
        pd.to_datetime(maturity_date).month,
        pd.to_datetime(maturity_date).year,
    )

    schedule = ql.Schedule(
        ql_quote,
        ql_maturity,
        ql.Period(ql.Semiannual),
        calendar,
        business_convention,
        business_convention,
        ql.DateGeneration.Backward,
        end_of_month,
    )

    # Convert back to pandas and filter
    dates = [
        pd.Timestamp(d.year(), d.month(), d.dayOfMonth())
        for d in schedule
        if d > ql_quote
    ]

    return pd.Series(dates)


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


def ql_bond_price(
    face_value: float,
    coupon_rate: float,
    ytm: float,
    periods: int,
    frequency: int = 2,
) -> float:
    """
    QuantLib equivalent of simple bond pricing formula.
    """

    # Evaluation date (arbitrary, since we're matching formula math)
    today = ql.Date.todaysDate()
    ql.Settings.instance().evaluationDate = today

    # Map frequency
    freq_map = {
        1: ql.Annual,
        2: ql.Semiannual,
        4: ql.Quarterly,
    }

    schedule = ql.Schedule(
        today,
        today + ql.Period(periods * (12 // frequency), ql.Months),
        ql.Period(freq_map[frequency]),
        ql.NullCalendar(),
        ql.Unadjusted,
        ql.Unadjusted,
        ql.DateGeneration.Forward,
        False,
    )

    bond = ql.FixedRateBond(
        settlementDays=0,
        faceAmount=face_value,
        schedule=schedule,
        coupons=[coupon_rate],
        paymentDayCounter=ql.Actual365Fixed(),
    )

    price = bond.cleanPrice(
        ytm,
        ql.Actual365Fixed(),
        ql.Compounded,
        freq_map[frequency],
    )

    # QuantLib prices are quoted per 100 face
    return price * (face_value / 100.0)


def ql_create_bond(
    issue_date: ql.Date,
    maturity_date: ql.Date,
    face_value: float,
    coupon_rate: float,
    frequency: int = 2,
) -> ql.FixedRateBond:
    """
    Create a QuantLib FixedRateBond object.
    
    Parameters
    ----------
    issue_date : ql.Date
        The issue date of the bond.
    maturity_date : ql.Date
        The maturity date of the bond.
    face_value : float
        The face (par) value of the bond.
    coupon_rate : float
        The annual coupon rate (as a decimal, e.g., 0.05 for 5%).
    frequency : int, optional
        The number of coupon payments per year (default: 2 for semi-annual).
    
    Returns
    -------
    ql.FixedRateBond
        The QuantLib FixedRateBond object.
    """
    
    # -----------------------------
    # Global evaluation date
    # -----------------------------
    valuation_date = ql.Date(15, 1, 2025)
    ql.Settings.instance().evaluationDate = valuation_date

    # -----------------------------
    # Bond specification
    # -----------------------------
    issue_date = issue_date
    maturity_date = maturity_date
    face_value = face_value
    coupon_rate = coupon_rate

    if frequency == 2:
        frequency = ql.Semiannual
    else:
        raise ValueError("Only semiannual frequency supported in this example.")

    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    day_count = ql.ActualActual(ql.ActualActual.ISDA)

    # -----------------------------
    # Coupon schedule
    # -----------------------------
    schedule = ql.Schedule(
        issue_date,
        maturity_date,
        ql.Period(frequency),
        calendar,
        ql.Following,
        ql.Following,
        ql.DateGeneration.Backward,
        False,
    )

    # -----------------------------
    # Fixed-rate bond
    # -----------------------------
    bond = ql.FixedRateBond(
        settlementDays=1,
        faceAmount=face_value,
        schedule=schedule,
        coupons=[coupon_rate],
        paymentDayCounter=day_count,
    )

    return bond


def ql_bond_dates_cashflows(
    bond: ql.FixedRateBond,
) -> pd.DataFrame:
    """
    Extract bond cashflow dates and amounts and return a DataFrame.
    """

    cashflows = bond.cashflows()
    data = {
        "date": [cf.date() for cf in cashflows],
        "amount": [cf.amount() for cf in cashflows],
    }

    df = pd.DataFrame(data).set_index("date")
    return df


def ql_clean_price(
    bond: ql.FixedRateBond,
    ytm: float,
    frequency: int = 2,
) -> float:
    """
    Calculate the clean price of a QuantLib FixedRateBond given a YTM.
    """

    if frequency == 2:
        frequency = ql.Semiannual
    else:
        raise ValueError("Only semiannual frequency supported in this example.")

    # Need to extact the day_count
    day_count = ql.ActualActual(ql.ActualActual.ISDA)

    clean_price = bond.cleanPrice(
        ytm,
        day_count,
        ql.Compounded,
        frequency,
    )

    return clean_price


def ql_dirty_price(
    bond: ql.FixedRateBond,
    ytm: float,
    frequency: int = 2,
) -> float:
    """
    Calculate the dirty price of a QuantLib FixedRateBond given a YTM.
    """

    if frequency == 2:
        frequency = ql.Semiannual
    else:
        raise ValueError("Only semiannual frequency supported in this example.")

    # Need to extact the day_count
    day_count = ql.ActualActual(ql.ActualActual.ISDA)

    dirty_price = bond.dirtyPrice(
        ytm,
        day_count,
        ql.Compounded,
        frequency,
    )

    return dirty_price

def ql_accrued_interest(
    bond: ql.FixedRateBond,
) -> float:
    """
    Calculate the accrued interest of a QuantLib FixedRateBond.
    """

    accrued_interest = bond.accruedAmount()
    return accrued_interest



if __name__ == "__main__":
    quote_date = "2020-01-02"
    maturity_date = "2025-01-01"

    coupon_dates = get_coupon_dates(
        quote_date=quote_date,
        maturity_date=maturity_date,
    )

    print(coupon_dates)

    coupon_dates_ql = ql_get_coupon_dates(
        quote_date=quote_date,
        maturity_date=maturity_date,
    )

    print(coupon_dates_ql)

    price = bond_price(
        face_value=1000,
        coupon_rate=0.06,
        ytm=0.05,
        periods=10,
        frequency=2,
    )

    print(price)

    price_ql = ql_bond_price(
        face_value=1000,
        coupon_rate=0.06,
        ytm=0.05,
        periods=10,
        frequency=2,
    )

    print(price_ql)

    print(price / price_ql + 1e-3)

    day_count = ql.ActualActual(ql.ActualActual.ISDA)
    frequency = ql.Semiannual
    ytm = 0.05

    bond = ql_create_bond(
        issue_date=ql.Date(15, 1, 2025),
        maturity_date=ql.Date(15, 1, 2055),
        face_value=1000.0,
        coupon_rate=0.04,
        frequency=2,
    )

    df = ql_bond_dates_cashflows(bond)
    print(df)

    clean_price = ql_clean_price(
        bond=bond,
        ytm=ytm,
        frequency=2,
    )

    print(clean_price)

    dirty_price = ql_dirty_price(
        bond=bond,
        ytm=0.05,
        frequency=2,
    )

    print(dirty_price)

    accrued_interest = ql_accrued_interest(bond)
    print(accrued_interest)

    

    mod_duration = ql.BondFunctions.duration(
        bond,
        ytm,
        day_count,
        ql.Compounded,
        frequency,
        ql.Duration.Modified,
    )

    print(mod_duration)

    mac_duration = ql.BondFunctions.duration(
        bond,
        ytm,
        day_count,
        ql.Compounded,
        frequency,
        ql.Duration.Macaulay,
    )

    convexity = ql.BondFunctions.convexity(
        bond,
        ytm,
        day_count,
        ql.Compounded,
        frequency,
    )

 






