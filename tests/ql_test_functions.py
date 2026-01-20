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


def ql_extract_coupon_dates(
    schedule: ql.Schedule,
) -> pd.Series:
    """
    Extract coupon dates from a QuantLib Schedule object and 
    return a Series.

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

    # Remove the first date, which is the issue date
    dates = dates[1:]

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


def ql_extract_cashflows(
    bond: ql.FixedRateBond,
) -> pd.Series:
    """
    Extract bond cashflow amounts from a QuantLib bond and 
    return a Series.

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
    bond: ql.FixedRateBond | ql.ZeroCouponBond,
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


def ql_calc_yield_to_maturity(
    valuation_date: str,
    clean_price: float,
    bond: ql.FixedRateBond,
    accuracy: float = 1.0e-10,
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

    # Calculate yield to maturity
    ytm = ql.BondFunctions.bondYield(
        bond,
        clean_price,
        bond.dayCounter(),  # Use bond's day counter
        ql.Compounded,  # Use standard compounding
        bond.frequency(),  # Use bond's coupon frequency
        valuation_date,
        accuracy,
        max_evaluations,
    )

    return ytm


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
    clean_price = ql_calc_clean_price(
        valuation_date=valuation_date,
        ytm=ytm,
        bond=bond,
    )

    # Dollar duration = Modified Duration × Price × 0.0001 (for 1bp)
    # Price is expressed per 100 face value, so scale by (face_value / 100)
    dollar_duration = mod_duration * clean_price * 0.0001 * (face_value / 100.0)

    return dollar_duration


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


def ql_create_european_option(
    option_type: str,
    strike: float,
    maturity_date: str,
    underlying_price: float,
) -> ql.VanillaOption:
    """
    Create a QuantLib European option (call or put).

    A European option can only be exercised at maturity, unlike American options
    which can be exercised at any time before maturity.

    Parameters
    ----------
    option_type : str
        Either "call" or "put".
    strike : float
        The strike price of the option.
    maturity_date : str
        The option maturity/expiration date as a string "YYYY-MM-DD".
    underlying_price : float
        The current price of the underlying asset.

    Returns
    -------
    ql.VanillaOption
        The QuantLib VanillaOption object representing a European option.
    """

    # Convert to QuantLib date from string
    if isinstance(maturity_date, str):
        dt = datetime.strptime(maturity_date, "%Y-%m-%d")
        maturity_date = ql.Date(dt.day, dt.month, dt.year)

    # Set option type
    if option_type.lower() == "call":
        option_type_ql = ql.Option.Call
    elif option_type.lower() == "put":
        option_type_ql = ql.Option.Put
    else:
        raise ValueError("option_type must be either 'call' or 'put'")

    # Create the option
    option = ql.VanillaOption(
        ql.PlainVanillaPayoff(
            option_type_ql, strike
        ),  # Create payoff (vanilla payoff at strike)
        ql.EuropeanExercise(
            maturity_date
        ),  # Create European exercise (can only exercise at maturity)
    )

    return option


def ql_calc_option_price(
    valuation_date: str,
    option: ql.VanillaOption,
    spot_price: float,
    risk_free_rate: float,
    dividend_yield: float,
    volatility: float,
) -> float:
    """
    Calculate the Black-Scholes price of a European option.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    option : ql.VanillaOption
        The QuantLib VanillaOption object (European option).
    spot_price : float
        The current price of the underlying asset.
    risk_free_rate : float
        The risk-free interest rate (as a decimal, e.g., 0.05 for 5%).
    dividend_yield : float
        The continuous dividend yield (as a decimal, e.g., 0.02 for 2%).
    volatility : float
        The volatility of the underlying asset (as a decimal, e.g., 0.20 for 20%).

    Returns
    -------
    float
        The Black-Scholes price of the option.
    """

    # Convert to QuantLib date from string
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Set evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Create flat term structures for risk-free rate and dividend yield
    day_count = ql.Actual365Fixed()
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)

    # Create quote objects for spot price
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))

    # Create flat yield term structure
    risk_free_curve = ql.FlatForward(valuation_date, risk_free_rate, day_count)
    risk_free_handle = ql.YieldTermStructureHandle(risk_free_curve)

    # Create flat dividend yield term structure
    dividend_curve = ql.FlatForward(valuation_date, dividend_yield, day_count)
    dividend_handle = ql.YieldTermStructureHandle(dividend_curve)

    # Create flat volatility structure
    volatility_curve = ql.BlackConstantVol(
        valuation_date, calendar, volatility, day_count
    )
    volatility_handle = ql.BlackVolTermStructureHandle(volatility_curve)

    # Create Black-Scholes-Merton process
    bsm_process = ql.BlackScholesMertonProcess(
        spot_handle, dividend_handle, risk_free_handle, volatility_handle
    )

    # Set up the analytical (Black-Scholes) pricing engine
    engine = ql.AnalyticEuropeanEngine(bsm_process)
    option.setPricingEngine(engine)

    # Calculate and return the option price
    price = option.NPV()

    return price


def ql_extract_option_delta(
    option: ql.VanillaOption,
) -> float:
    """
    Extract the delta of a QuantLib option.

    Delta measures the sensitivity of the option price to
    changes in the underlying asset price.

    Parameters
    ----------
    option : ql.VanillaOption
        The QuantLib VanillaOption object.

    Returns
    -------
    float
        The delta of the option.
    """

    # Extract and return the delta
    delta = option.delta()

    return delta


def ql_extract_option_gamma(
    option: ql.VanillaOption,
) -> float:
    """
    Extract the gamma of a QuantLib option.

    Gamma measures the sensitivity of delta to changes
    in the underlying asset price.

    Parameters
    ----------
    option : ql.VanillaOption
        The QuantLib VanillaOption object.

    Returns
    -------
    float
        The gamma of the option.
    """

    # Extract and return the gamma
    gamma = option.gamma()

    return gamma


def ql_extract_option_vega(
    option: ql.VanillaOption,
) -> float:
    """
    Extract the vega of a QuantLib option.

    Vega measures the sensitivity of the option price to
    changes in the volatility of the underlying asset.

    Parameters
    ----------
    option : ql.VanillaOption
        The QuantLib VanillaOption object.

    Returns
    -------
    float
        The vega of the option.
    """

    # Extract and return the vega
    vega = option.vega()

    return vega


def ql_extract_option_theta(
    option: ql.VanillaOption,
) -> float:
    """
    Extract the theta of a QuantLib option.

    Theta measures the sensitivity of the option price to
    the passage of time (time decay).

    Parameters
    ----------
    option : ql.VanillaOption
        The QuantLib VanillaOption object.

    Returns
    -------
    float
        The theta of the option.
    """

    # Extract and return the theta
    theta = option.theta()

    return theta


def ql_extract_option_rho(
    option: ql.VanillaOption,
) -> float:
    """
    Extract the rho of a QuantLib option.

    Rho measures the sensitivity of the option price to
    changes in the risk-free interest rate.

    Parameters
    ----------
    option : ql.VanillaOption
        The QuantLib VanillaOption object.

    Returns
    -------
    float
        The rho of the option.
    """

    # Extract and return the rho
    rho = option.rho()

    return rho


def ql_calc_implied_volatility(
    valuation_date: str,
    option: ql.VanillaOption,
    market_price: float,
    spot_price: float,
    risk_free_rate: float,
    dividend_yield: float,
    initial_guess: float = 0.20,
    accuracy: float = 1.0e-6,
    max_evaluations: int = 100,
) -> float:
    """
    Calculate the implied volatility of a European option given its market price.
    
    Implied volatility is the volatility value that, when input into the 
    Black-Scholes model, produces the observed market price.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    option : ql.VanillaOption
        The QuantLib VanillaOption object (European option).
    market_price : float
        The observed market price of the option.
    spot_price : float
        The current price of the underlying asset.
    risk_free_rate : float
        The risk-free interest rate (as a decimal, e.g., 0.05 for 5%).
    dividend_yield : float
        The continuous dividend yield (as a decimal, e.g., 0.02 for 2%).
    initial_guess : float, optional
        Initial guess for the implied volatility (default: 0.20 for 20%).
    accuracy : float, optional
        Accuracy of the solver (default: 1.0e-6).
    max_evaluations : int, optional
        Maximum number of solver iterations (default: 100).

    Returns
    -------
    float
        The implied volatility as a decimal (e.g., 0.25 for 25%).
    """

    # Convert to QuantLib date from string
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Set evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Create quote objects for spot price
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))

    # Create flat term structures for risk-free rate and dividend yield
    day_count = ql.Actual365Fixed()
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)

    # Create flat yield term structure
    risk_free_curve = ql.FlatForward(
        valuation_date, risk_free_rate, day_count
    )
    risk_free_handle = ql.YieldTermStructureHandle(risk_free_curve)

    # Create flat dividend yield term structure
    dividend_curve = ql.FlatForward(
        valuation_date, dividend_yield, day_count
    )
    dividend_handle = ql.YieldTermStructureHandle(dividend_curve)

    # Calculate implied volatility using built-in solver
    implied_vol = option.impliedVolatility(
        market_price,
        ql.BlackScholesMertonProcess(
            spot_handle,
            dividend_handle,
            risk_free_handle,
            ql.BlackVolTermStructureHandle(
                ql.BlackConstantVol(valuation_date, calendar, initial_guess, day_count)
            )
        ),
        accuracy,
        max_evaluations,
        0.001,  # minVol (0.1%)
        4.0     # maxVol (400%)
    )

    return implied_vol


def ql_create_american_option(
    option_type: str,
    strike: float,
    maturity_date: str,
) -> ql.VanillaOption:
    """
    Create a QuantLib American option (call or put).
    
    An American option can be exercised at any time up to and including maturity,
    unlike European options which can only be exercised at maturity.

    Parameters
    ----------
    option_type : str
        Either "call" or "put".
    strike : float
        The strike price of the option.
    maturity_date : str
        The option maturity/expiration date as a string "YYYY-MM-DD".

    Returns
    -------
    ql.VanillaOption
        The QuantLib VanillaOption object representing an American option.
    """

    # Convert to QuantLib date from string
    if isinstance(maturity_date, str):
        dt = datetime.strptime(maturity_date, "%Y-%m-%d")
        maturity_date = ql.Date(dt.day, dt.month, dt.year)

    # Set option type
    if option_type.lower() == "call":
        option_type_ql = ql.Option.Call
    elif option_type.lower() == "put":
        option_type_ql = ql.Option.Put
    else:
        raise ValueError("option_type must be either 'call' or 'put'")

    # Create payoff (vanilla payoff at strike)
    payoff = ql.PlainVanillaPayoff(option_type_ql, strike)

    # Create American exercise (can exercise any time up to maturity)
    exercise = ql.AmericanExercise(None, maturity_date)

    # Create the option
    option = ql.VanillaOption(payoff, exercise)

    return option


def ql_calc_binomial_option_price(
    valuation_date: str,
    option: ql.VanillaOption,
    spot_price: float,
    risk_free_rate: float,
    dividend_yield: float,
    volatility: float,
    time_steps: int = 100,
) -> float:
    """
    Calculate the price of an option using the binomial tree method.
    
    The binomial tree method can price both European and American options.
    It's particularly necessary for American options since they don't have
    a closed-form Black-Scholes solution.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    option : ql.VanillaOption
        The QuantLib VanillaOption object (European or American).
    spot_price : float
        The current price of the underlying asset.
    risk_free_rate : float
        The risk-free interest rate (as a decimal, e.g., 0.05 for 5%).
    dividend_yield : float
        The continuous dividend yield (as a decimal, e.g., 0.02 for 2%).
    volatility : float
        The volatility of the underlying asset (as a decimal, e.g., 0.20 for 20%).
    time_steps : int, optional
        Number of time steps in the binomial tree (default: 100).
        More steps = more accurate but slower.

    Returns
    -------
    float
        The option price.
    """

    # Convert to QuantLib date from string
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Set evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Create quote objects for spot price
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))

    # Create flat term structures for risk-free rate and dividend yield
    day_count = ql.Actual365Fixed()
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)

    # Create flat yield term structure
    risk_free_curve = ql.FlatForward(
        valuation_date, risk_free_rate, day_count
    )
    risk_free_handle = ql.YieldTermStructureHandle(risk_free_curve)

    # Create flat dividend yield term structure
    dividend_curve = ql.FlatForward(
        valuation_date, dividend_yield, day_count
    )
    dividend_handle = ql.YieldTermStructureHandle(dividend_curve)

    # Create flat volatility structure
    volatility_curve = ql.BlackConstantVol(
        valuation_date, calendar, volatility, day_count
    )
    volatility_handle = ql.BlackVolTermStructureHandle(volatility_curve)

    # Create Black-Scholes-Merton process
    bsm_process = ql.BlackScholesMertonProcess(
        spot_handle,
        dividend_handle,
        risk_free_handle,
        volatility_handle
    )

    # Set up binomial pricing engine (Cox-Ross-Rubinstein method)
    engine = ql.BinomialVanillaEngine(bsm_process, "crr", time_steps)
    option.setPricingEngine(engine)

    # Calculate and return the option price
    price = option.NPV()

    return price


def ql_is_business_day(
    date: str,
    calendar: ql.Calendar = None,
) -> bool:
    """
    Check if a date is a business day according to a specified calendar.

    Parameters
    ----------
    date : str
        The date to check as a string "YYYY-MM-DD".
    calendar : ql.Calendar, optional
        The calendar to use for business day determination.
        If None, uses US Government Bond calendar (default).

    Note
    ----
    Calendar options include:
    - ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    - ql.UnitedStates(ql.UnitedStates.NYSE)
    - ql.UnitedKingdom(ql.UnitedKingdom.LSE)
    - ql.TARGET()
    - ql.EuropeanCentralBank()
    - ql.SouthAfrica()
    - ql.Japan()
    - ql.China()
    - ql.Switzerland()
    etc.

    Returns
    -------
    bool
        True if the date is a business day, False otherwise.
    """

    # Convert to QuantLib date from string
    if isinstance(date, str):
        dt = datetime.strptime(date, "%Y-%m-%d")
        date = ql.Date(dt.day, dt.month, dt.year)

    # Use US Government Bond calendar if not specified
    if calendar is None:
        calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)

    # Check if business day
    is_business_day = calendar.isBusinessDay(date)

    return is_business_day


def ql_calc_business_days_between(
    start_date: str,
    end_date: str,
    calendar: ql.Calendar = None,
    include_first: bool = True,
    include_last: bool = False,
) -> int:
    """
    Calculate the number of business days between two dates.

    Parameters
    ----------
    start_date : str
        The start date as a string "YYYY-MM-DD".
    end_date : str
        The end date as a string "YYYY-MM-DD".
    calendar : ql.Calendar, optional
        The calendar to use for business day determination.
        If None, uses US Government Bond calendar (default).
    include_first : bool, optional
        Whether to include the start date in the count (default: True).
    include_last : bool, optional
        Whether to include the end date in the count (default: False).

    Returns
    -------
    int
        The number of business days between the two dates.
    """

    # Convert to QuantLib dates from strings
    if isinstance(start_date, str):
        dt = datetime.strptime(start_date, "%Y-%m-%d")
        start_date = ql.Date(dt.day, dt.month, dt.year)

    if isinstance(end_date, str):
        dt = datetime.strptime(end_date, "%Y-%m-%d")
        end_date = ql.Date(dt.day, dt.month, dt.year)

    # Use US Government Bond calendar if not specified
    if calendar is None:
        calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)

    # Calculate business days between dates
    business_days = calendar.businessDaysBetween(
        start_date,
        end_date,
        include_first,
        include_last
    )

    return business_days


def ql_create_vanilla_swap(
    effective_date: str,
    maturity_date: str,
    notional: float,
    fixed_rate: float,
    floating_index: ql.IborIndex = None,
    swap_type: str = "payer",
    fixed_frequency: ql.Period = None,
    floating_frequency: ql.Period = None,
) -> ql.VanillaSwap:
    """
    Create a QuantLib vanilla interest rate swap.
    
    A vanilla swap exchanges fixed rate payments for floating rate payments.
    A payer swap means you pay fixed and receive floating.
    A receiver swap means you receive fixed and pay floating.

    Parameters
    ----------
    effective_date : str
        The swap effective/start date as a string "YYYY-MM-DD".
    maturity_date : str
        The swap maturity/end date as a string "YYYY-MM-DD".
    notional : float
        The notional amount of the swap.
    fixed_rate : float
        The fixed rate (as a decimal, e.g., 0.05 for 5%).
    floating_index : ql.IborIndex, optional
        The floating rate index. If None, uses 3-month USD LIBOR.
    swap_type : str, optional
        Either "payer" (pay fixed, receive floating) or 
        "receiver" (receive fixed, pay floating). Default is "payer".
    fixed_frequency : ql.Period, optional
        Payment frequency for fixed leg. If None, uses semi-annual.
    floating_frequency : ql.Period, optional
        Payment frequency for floating leg. If None, uses quarterly.

    Returns
    -------
    ql.VanillaSwap
        The QuantLib VanillaSwap object.
    """

    # Convert to QuantLib dates from strings
    if isinstance(effective_date, str):
        dt = datetime.strptime(effective_date, "%Y-%m-%d")
        effective_date = ql.Date(dt.day, dt.month, dt.year)

    if isinstance(maturity_date, str):
        dt = datetime.strptime(maturity_date, "%Y-%m-%d")
        maturity_date = ql.Date(dt.day, dt.month, dt.year)

    # Set default floating index (3M USD LIBOR)
    if floating_index is None:
        floating_index = ql.USDLibor(ql.Period(3, ql.Months))

    # Set default frequencies
    if fixed_frequency is None:
        fixed_frequency = ql.Period(6, ql.Months)  # Semi-annual
    if floating_frequency is None:
        floating_frequency = ql.Period(3, ql.Months)  # Quarterly

    # Determine swap type
    if swap_type.lower() == "payer":
        swap_type_ql = ql.VanillaSwap.Payer
    elif swap_type.lower() == "receiver":
        swap_type_ql = ql.VanillaSwap.Receiver
    else:
        raise ValueError("swap_type must be either 'payer' or 'receiver'")

    # Set calendar and conventions
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    business_convention = ql.ModifiedFollowing
    day_count = ql.Thirty360(ql.Thirty360.BondBasis)

    # Create fixed leg schedule
    fixed_schedule = ql.Schedule(
        effective_date,
        maturity_date,
        fixed_frequency,
        calendar,
        business_convention,
        business_convention,
        ql.DateGeneration.Forward,
        False
    )

    # Create floating leg schedule
    floating_schedule = ql.Schedule(
        effective_date,
        maturity_date,
        floating_frequency,
        calendar,
        business_convention,
        business_convention,
        ql.DateGeneration.Forward,
        False
    )

    # Create the vanilla swap
    swap = ql.VanillaSwap(
        swap_type_ql,
        notional,
        fixed_schedule,
        fixed_rate,
        day_count,
        floating_schedule,
        floating_index,
        0.0,  # Floating spread
        floating_index.dayCounter()
    )

    return swap


def ql_calc_swap_npv(
    valuation_date: str,
    swap: ql.VanillaSwap,
    discount_curve: ql.YieldTermStructureHandle,
    forecast_curve: ql.YieldTermStructureHandle = None,
) -> float:
    """
    Calculate the net present value (NPV) of an interest rate swap.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    swap : ql.VanillaSwap
        The QuantLib VanillaSwap object.
    discount_curve : ql.YieldTermStructureHandle
        The yield curve used for discounting cash flows.
    forecast_curve : ql.YieldTermStructureHandle, optional
        The yield curve used for forecasting floating rates.
        If None, uses the discount_curve for both.

    Returns
    -------
    float
        The net present value of the swap.
    """

    # Convert to QuantLib date from string
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Set evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Use discount curve for forecasting if not provided
    if forecast_curve is None:
        forecast_curve = discount_curve

    # Set up pricing engine
    engine = ql.DiscountingSwapEngine(discount_curve)
    swap.setPricingEngine(engine)

    # Calculate NPV
    npv = swap.NPV()

    return npv


def ql_calc_swap_fair_rate(
    valuation_date: str,
    swap: ql.VanillaSwap,
    discount_curve: ql.YieldTermStructureHandle,
    forecast_curve: ql.YieldTermStructureHandle = None,
) -> float:
    """
    Calculate the fair fixed rate for an interest rate swap.
    
    The fair rate is the fixed rate that makes the swap have zero NPV.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    swap : ql.VanillaSwap
        The QuantLib VanillaSwap object.
    discount_curve : ql.YieldTermStructureHandle
        The yield curve used for discounting cash flows.
    forecast_curve : ql.YieldTermStructureHandle, optional
        The yield curve used for forecasting floating rates.
        If None, uses the discount_curve for both.

    Returns
    -------
    float
        The fair fixed rate (as a decimal, e.g., 0.05 for 5%).
    """

    # Convert to QuantLib date from string
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Set evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Use discount curve for forecasting if not provided
    if forecast_curve is None:
        forecast_curve = discount_curve

    # Set up pricing engine
    engine = ql.DiscountingSwapEngine(discount_curve)
    swap.setPricingEngine(engine)

    # Calculate fair rate
    fair_rate = swap.fairRate()

    return fair_rate


def ql_extract_swap_legs(
    valuation_date: str,
    swap: ql.VanillaSwap,
    discount_curve: ql.YieldTermStructureHandle = None,
) -> dict:
    """
    Extract cashflow information from both legs of an interest rate swap.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    swap : ql.VanillaSwap
        The QuantLib VanillaSwap object.
    discount_curve : ql.YieldTermStructureHandle, optional
        The yield curve used for forecasting floating rates.
        If None, floating rates will not be forecasted.

    Returns
    -------
    dict
        Dictionary with 'fixed_leg' and 'floating_leg' keys, each containing
        lists of cashflow information (dates and amounts).
    """

    # Convert to QuantLib date from string
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Set evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Extract fixed leg cashflows
    fixed_leg = []
    for cf in swap.fixedLeg():
        if cf.date() > valuation_date:
            fixed_leg.append({
                'date': cf.date().ISO(),
                'amount': cf.amount()
            })

    # Extract floating leg cashflows
    floating_leg = []
    for cf in swap.floatingLeg():
        if cf.date() > valuation_date:
            floating_leg.append({
                'date': cf.date().ISO(),
                'amount': cf.amount()
            })

    return {
        'fixed_leg': fixed_leg,
        'floating_leg': floating_leg
    }


def ql_create_cds(
    effective_date: str,
    maturity_date: str,
    notional: float,
    spread: float,
    recovery_rate: float = 0.40,
    payment_frequency: ql.Period = None,
) -> ql.CreditDefaultSwap:
    """
    Create a QuantLib Credit Default Swap (CDS).
    
    A CDS is a contract that provides protection against default of a reference entity.
    The protection buyer pays a periodic spread and receives compensation if default occurs.

    Parameters
    ----------
    effective_date : str
        The CDS effective/start date as a string "YYYY-MM-DD".
    maturity_date : str
        The CDS maturity/end date as a string "YYYY-MM-DD".
    notional : float
        The notional amount of protection.
    spread : float
        The CDS spread in basis points per annum (as a decimal, e.g., 0.01 for 100 bps).
    recovery_rate : float, optional
        The assumed recovery rate in case of default (default: 0.40 for 40%).
    payment_frequency : ql.Period, optional
        Premium payment frequency. If None, uses quarterly (standard for CDS).

    Returns
    -------
    ql.CreditDefaultSwap
        The QuantLib CreditDefaultSwap object.
    """

    # Convert to QuantLib dates from strings
    if isinstance(effective_date, str):
        dt = datetime.strptime(effective_date, "%Y-%m-%d")
        effective_date = ql.Date(dt.day, dt.month, dt.year)

    if isinstance(maturity_date, str):
        dt = datetime.strptime(maturity_date, "%Y-%m-%d")
        maturity_date = ql.Date(dt.day, dt.month, dt.year)

    # Set default payment frequency (quarterly is standard)
    if payment_frequency is None:
        payment_frequency = ql.Period(3, ql.Months)

    # Set calendar and conventions (standard CDS conventions)
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    business_convention = ql.Following
    day_count = ql.Actual360()
    date_generation = ql.DateGeneration.CDS  # Special CDS date generation rule

    # Create premium payment schedule
    schedule = ql.Schedule(
        effective_date,
        maturity_date,
        payment_frequency,
        calendar,
        business_convention,
        business_convention,
        date_generation,
        False  # End of month
    )

    # Create the CDS
    # Protection side = buyer's perspective (pay spread, receive protection)
    cds = ql.CreditDefaultSwap(
        ql.Protection.Buyer,  # Protection buyer
        notional,
        spread,
        schedule,
        business_convention,
        day_count,
        True,  # Settles accrual
        True,  # Pays at default time
        effective_date,
        ql.Actual360(),  # Last period day counter
        True,  # Rebates accrual
        ql.CreditDefaultSwap.ISDA  # ISDA pricing convention
    )

    return cds


def ql_calc_cds_npv(
    valuation_date: str,
    cds: ql.CreditDefaultSwap,
    discount_curve: ql.YieldTermStructureHandle,
    default_probability_curve: ql.DefaultProbabilityTermStructureHandle,
    recovery_rate: float = 0.40,
) -> float:
    """
    Calculate the net present value (NPV) of a Credit Default Swap.
    
    The NPV represents the value of the protection leg minus the premium leg.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    cds : ql.CreditDefaultSwap
        The QuantLib CreditDefaultSwap object.
    discount_curve : ql.YieldTermStructureHandle
        The yield curve used for discounting cash flows.
    default_probability_curve : ql.DefaultProbabilityTermStructureHandle
        The hazard rate/default probability curve.
    recovery_rate : float, optional
        The assumed recovery rate in case of default (default: 0.40 for 40%).

    Returns
    -------
    float
        The net present value of the CDS.
    """

    # Convert to QuantLib date from string
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Set evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Set up pricing engine
    engine = ql.MidPointCdsEngine(
        default_probability_curve,
        recovery_rate,
        discount_curve
    )
    cds.setPricingEngine(engine)

    # Calculate NPV
    npv = cds.NPV()

    return npv


def ql_create_cds(
    effective_date: str,
    maturity_date: str,
    notional: float,
    spread: float,
    recovery_rate: float = 0.40,
    payment_frequency: ql.Period = None,
) -> ql.CreditDefaultSwap:
    """
    Create a QuantLib Credit Default Swap (CDS).
    
    A CDS is a contract that provides protection against default of a reference entity.
    The protection buyer pays a periodic spread and receives compensation if default occurs.

    Parameters
    ----------
    effective_date : str
        The CDS effective/start date as a string "YYYY-MM-DD".
    maturity_date : str
        The CDS maturity/end date as a string "YYYY-MM-DD".
    notional : float
        The notional amount of protection.
    spread : float
        The CDS spread in basis points per annum (as a decimal, e.g., 0.01 for 100 bps).
    recovery_rate : float, optional
        The assumed recovery rate in case of default (default: 0.40 for 40%).
    payment_frequency : ql.Period, optional
        Premium payment frequency. If None, uses quarterly (standard for CDS).

    Returns
    -------
    ql.CreditDefaultSwap
        The QuantLib CreditDefaultSwap object.
    """

    # Convert to QuantLib dates from strings
    if isinstance(effective_date, str):
        dt = datetime.strptime(effective_date, "%Y-%m-%d")
        effective_date = ql.Date(dt.day, dt.month, dt.year)

    if isinstance(maturity_date, str):
        dt = datetime.strptime(maturity_date, "%Y-%m-%d")
        maturity_date = ql.Date(dt.day, dt.month, dt.year)

    # Set default payment frequency (quarterly is standard)
    if payment_frequency is None:
        payment_frequency = ql.Period(3, ql.Months)

    # Set calendar and conventions (standard CDS conventions)
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    business_convention = ql.Following
    day_count = ql.Actual360()
    date_generation = ql.DateGeneration.CDS  # Special CDS date generation rule

    # Create premium payment schedule
    schedule = ql.Schedule(
        effective_date,
        maturity_date,
        payment_frequency,
        calendar,
        business_convention,
        business_convention,
        date_generation,
        False  # End of month
    )

    # Create the CDS
    # Protection side = buyer's perspective (pay spread, receive protection)
    cds = ql.CreditDefaultSwap(
        ql.Protection.Buyer,  # Protection buyer
        notional,
        spread,
        schedule,
        business_convention,
        day_count,
        True,  # Settles accrual
        True,  # Pays at default time
        effective_date,
        ql.Actual360(),  # Last period day counter
        True,  # Rebates accrual
        ql.CreditDefaultSwap.ISDA  # ISDA pricing convention
    )

    return cds


def ql_calc_cds_npv(
    valuation_date: str,
    cds: ql.CreditDefaultSwap,
    discount_curve: ql.YieldTermStructureHandle,
    default_probability_curve: ql.DefaultProbabilityTermStructureHandle,
    recovery_rate: float = 0.40,
) -> float:
    """
    Calculate the net present value (NPV) of a Credit Default Swap.
    
    The NPV represents the value of the protection leg minus the premium leg.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    cds : ql.CreditDefaultSwap
        The QuantLib CreditDefaultSwap object.
    discount_curve : ql.YieldTermStructureHandle
        The yield curve used for discounting cash flows.
    default_probability_curve : ql.DefaultProbabilityTermStructureHandle
        The hazard rate/default probability curve.
    recovery_rate : float, optional
        The assumed recovery rate in case of default (default: 0.40 for 40%).

    Returns
    -------
    float
        The net present value of the CDS.
    """

    # Convert to QuantLib date from string
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Set evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Set up pricing engine
    engine = ql.MidPointCdsEngine(
        default_probability_curve,
        recovery_rate,
        discount_curve
    )
    cds.setPricingEngine(engine)

    # Calculate NPV
    npv = cds.NPV()

    return npv


def ql_calc_cds_spread(
    valuation_date: str,
    cds: ql.CreditDefaultSwap,
    discount_curve: ql.YieldTermStructureHandle,
    default_probability_curve: ql.DefaultProbabilityTermStructureHandle,
    recovery_rate: float = 0.40,
) -> float:
    """
    Calculate the fair spread of a Credit Default Swap.
    
    The fair spread is the CDS spread that makes the contract have zero NPV.
    This is also known as the par spread.

    Parameters
    ----------
    valuation_date : str
        The valuation date as a string "YYYY-MM-DD".
    cds : ql.CreditDefaultSwap
        The QuantLib CreditDefaultSwap object.
    discount_curve : ql.YieldTermStructureHandle
        The yield curve used for discounting cash flows.
    default_probability_curve : ql.DefaultProbabilityTermStructureHandle
        The hazard rate/default probability curve.
    recovery_rate : float, optional
        The assumed recovery rate in case of default (default: 0.40 for 40%).

    Returns
    -------
    float
        The fair CDS spread (as a decimal, e.g., 0.01 for 100 bps).
    """

    # Convert to QuantLib date from string
    if isinstance(valuation_date, str):
        dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        valuation_date = ql.Date(dt.day, dt.month, dt.year)

    # Set evaluation date
    ql.Settings.instance().evaluationDate = valuation_date

    # Set up pricing engine
    engine = ql.MidPointCdsEngine(
        default_probability_curve,
        recovery_rate,
        discount_curve
    )
    cds.setPricingEngine(engine)

    # Calculate fair spread
    fair_spread = cds.fairSpread()

    return fair_spread

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

    macaulay_duration = ql_calc_macaulay_duration(
        valuation_date=valuation_date,
        ytm=0.06,
        bond=bond,
    )

    print(macaulay_duration)

    convexity = ql_calc_convexity(
        valuation_date=valuation_date,
        ytm=0.06,
        bond=bond,
    )

    print(convexity)

    zero_coupon_bond = ql_create_zero_coupon_bond(
        issue_date=quote_date,
        maturity_date=maturity_date,
        face_value=1000,
    )

    dates_cashflows = ql_extract_coupon_dates_cashflows(zero_coupon_bond)
    print(dates_cashflows)

    current_price = ql_calc_zero_coupon_bond_price(
        valuation_date=valuation_date,
        ytm=0.06,
        bond=zero_coupon_bond,
    )

    print(current_price)

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
