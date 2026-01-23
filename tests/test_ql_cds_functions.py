"""
Functions from QuantLib examples to be used for fixed income tests.
"""

import numpy as np
import pandas as pd
import QuantLib as ql

from datetime import datetime


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
        discount_curve,
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
