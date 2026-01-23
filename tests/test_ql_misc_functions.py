"""
Functions from QuantLib examples to be used for fixed income tests.
"""

import numpy as np
import pandas as pd
import QuantLib as ql

from datetime import datetime


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
