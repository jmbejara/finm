"""
Functions from QuantLib examples to be used for fixed income tests.
"""

import numpy as np
import pandas as pd
import QuantLib as ql

from datetime import datetime


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
