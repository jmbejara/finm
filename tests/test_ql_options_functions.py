"""
Functions from QuantLib examples to be used for options tests.
"""

import numpy as np
import pandas as pd
import QuantLib as ql

from datetime import datetime


def ql_create_european_option(
    option_type: str,
    strike: float,
    expiration_date: str,
    spot_price: float,
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
    expiration_date : str
        The option maturity/expiration date as a string "YYYY-MM-DD".
    spot_price : float
        The current price of the underlying asset.

    Returns
    -------
    ql.VanillaOption
        The QuantLib VanillaOption object representing a European option.
    """

    # Convert to QuantLib date from string
    if isinstance(expiration_date, str):
        dt = datetime.strptime(expiration_date, "%Y-%m-%d")
        expiration_date = ql.Date(dt.day, dt.month, dt.year)

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
            expiration_date
        ),  # Create European exercise (can only exercise at expiration)
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


def ql_calc_option_delta(
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


def ql_calc_option_gamma(
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


def ql_calc_option_vega(
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


def ql_calc_option_theta(
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


def ql_calc_option_rho(
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

    # Create American exercise (can exercise any time from today to maturity)
    # Use the current evaluation date as the earliest exercise date
    earliest_exercise = ql.Settings.instance().evaluationDate
    exercise = ql.AmericanExercise(earliest_exercise, maturity_date)

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
