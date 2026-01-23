"""
Options pricing and greeks calculations for options.

This module provides basic functions for:

- Option price
- Option payoff
- Option delta
- Option gamma
- Option vega
- Option theta
- Option rho
- Implied volatility
- Binomial option price
"""

import math
import numpy as np
import pandas as pd

from datetime import datetime
from scipy.stats import norm

def calc_option_price(
    option_type: str,
    spot_price: float,
    strike: float,
    time_to_expiration: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float = 0.0
) -> float:
    """
    Calculate the Black-Scholes price of a European option.

    Parameters
    ----------
    option_type : str
        Either "call" or "put".
    spot_price : float
        The current price of the underlying asset.
    strike : float
        The strike price of the option.
    time_to_expiration : float
        Time to expiration in years.
    risk_free_rate : float
        The risk-free interest rate (as a decimal, e.g., 0.05 for 5%).
    volatility : float
        The volatility of the underlying asset (as a decimal, e.g., 0.20 for 20%).
    dividend_yield : float, optional
        The continuous dividend yield (as a decimal, e.g., 0.02 for 2%).
        Defaults to 0.0.

    Returns
    -------
    float
        The Black-Scholes price of the option.
    """

    # Calculate d1 and d2
    d1 = (math.log(spot_price / strike) + 
          (risk_free_rate - dividend_yield + 0.5 * volatility ** 2) * time_to_expiration) / \
         (volatility * math.sqrt(time_to_expiration))
    
    d2 = d1 - volatility * math.sqrt(time_to_expiration)
    
    # Calculate option price based on type
    if option_type.lower() == "call":
        # Call option: C = S*e^(-q*T)*N(d1) - K*e^(-r*T)*N(d2)
        price = (spot_price * math.exp(-dividend_yield * time_to_expiration) * norm.cdf(d1) -
                 strike * math.exp(-risk_free_rate * time_to_expiration) * norm.cdf(d2))
    elif option_type.lower() == "put":
        # Put option: P = K*e^(-r*T)*N(-d2) - S*e^(-q*T)*N(-d1)
        price = (strike * math.exp(-risk_free_rate * time_to_expiration) * norm.cdf(-d2) -
                 spot_price * math.exp(-dividend_yield * time_to_expiration) * norm.cdf(-d1))
    else:
        raise ValueError("option_type must be either 'call' or 'put'")
    
    return price

def calc_option_payoff(
    option_type: str,
    spot_price: float,
    strike: float
) -> float:
    """
    Calculate the payoff of a European option at expiration.
    
    The payoff is the intrinsic value of the option at expiration,
    before considering the premium paid.

    Parameters
    ----------
    option_type : str
        Either "call" or "put".
    spot_price : float
        The spot price of the underlying asset at expiration.
    strike : float
        The strike price of the option.

    Returns
    -------
    float
        The payoff of the option at expiration.
    """
    
    if option_type.lower() == "call":
        # Call payoff: max(S - K, 0)
        payoff = max(spot_price - strike, 0)
    elif option_type.lower() == "put":
        # Put payoff: max(K - S, 0)
        payoff = max(strike - spot_price, 0)
    else:
        raise ValueError("option_type must be either 'call' or 'put'")
    
    return payoff

def calc_option_delta(
    option_type: str,
    spot_price: float,
    strike: float,
    time_to_expiration: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float = 0.0
) -> float:
    """
    Calculate the delta of a European option.
    
    Delta measures the rate of change of option price with respect to 
    changes in the underlying asset's price.

    Parameters
    ----------
    option_type : str
        Either "call" or "put".
    spot_price : float
        The current price of the underlying asset.
    strike : float
        The strike price of the option.
    time_to_expiration : float
        Time to expiration in years.
    risk_free_rate : float
        The risk-free interest rate (as a decimal, e.g., 0.05 for 5%).
    volatility : float
        The volatility of the underlying asset (as a decimal, e.g., 0.20 for 20%).
    dividend_yield : float, optional
        The continuous dividend yield (as a decimal, e.g., 0.02 for 2%).
        Defaults to 0.0.

    Returns
    -------
    float
        The delta of the option.
    """
    
    # Calculate d1
    d1 = (math.log(spot_price / strike) + 
          (risk_free_rate - dividend_yield + 0.5 * volatility ** 2) * time_to_expiration) / \
         (volatility * math.sqrt(time_to_expiration))
    
    # Calculate delta based on option type
    if option_type.lower() == "call":
        # Call delta: e^(-qT) * N(d1)
        delta = math.exp(-dividend_yield * time_to_expiration) * norm.cdf(d1)
    elif option_type.lower() == "put":
        # Put delta: e^(-qT) * [N(d1) - 1]
        delta = math.exp(-dividend_yield * time_to_expiration) * (norm.cdf(d1) - 1)
    else:
        raise ValueError("option_type must be either 'call' or 'put'")
    
    return delta

def calc_option_gamma(
    spot_price: float,
    strike: float,
    time_to_expiration: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float = 0.0
) -> float:
    """
    Calculate the gamma of a European option.
    
    Gamma measures the rate of change of delta with respect to changes 
    in the underlying asset's price. It's the second derivative of the 
    option price with respect to the spot price.
    
    Note: Gamma is the same for both calls and puts with the same parameters.

    Parameters
    ----------
    spot_price : float
        The current price of the underlying asset.
    strike : float
        The strike price of the option.
    time_to_expiration : float
        Time to expiration in years.
    risk_free_rate : float
        The risk-free interest rate (as a decimal, e.g., 0.05 for 5%).
    volatility : float
        The volatility of the underlying asset (as a decimal, e.g., 0.20 for 20%).
    dividend_yield : float, optional
        The continuous dividend yield (as a decimal, e.g., 0.02 for 2%).
        Defaults to 0.0.

    Returns
    -------
    float
        The gamma of the option.
    """
    
    # Calculate d1
    d1 = (math.log(spot_price / strike) + 
          (risk_free_rate - dividend_yield + 0.5 * volatility ** 2) * time_to_expiration) / \
         (volatility * math.sqrt(time_to_expiration))
    
    # Calculate gamma: e^(-qT) * n(d1) / (S * σ * √T)
    # where n(d1) is the standard normal probability density function
    gamma = (math.exp(-dividend_yield * time_to_expiration) * norm.pdf(d1)) / \
            (spot_price * volatility * math.sqrt(time_to_expiration))
    
    return gamma

def calc_option_vega(
    spot_price: float,
    strike: float,
    time_to_expiration: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float = 0.0
) -> float:
    """
    Calculate the vega of a European option.
    
    Vega measures the rate of change of option price with respect to 
    changes in the volatility of the underlying asset. It represents 
    the change in option value for a 1% (0.01) change in volatility.
    
    Note: Vega is the same for both calls and puts with the same parameters.

    Parameters
    ----------
    spot_price : float
        The current price of the underlying asset.
    strike : float
        The strike price of the option.
    time_to_expiration : float
        Time to expiration in years.
    risk_free_rate : float
        The risk-free interest rate (as a decimal, e.g., 0.05 for 5%).
    volatility : float
        The volatility of the underlying asset (as a decimal, e.g., 0.20 for 20%).
    dividend_yield : float, optional
        The continuous dividend yield (as a decimal, e.g., 0.02 for 2%).
        Defaults to 0.0.

    Returns
    -------
    float
        The vega of the option (per 1% change in volatility).
    """
    import math
    from scipy.stats import norm
    
    # Calculate d1
    d1 = (math.log(spot_price / strike) + 
          (risk_free_rate - dividend_yield + 0.5 * volatility ** 2) * time_to_expiration) / \
         (volatility * math.sqrt(time_to_expiration))
    
    # Calculate vega: S * e^(-qT) * n(d1) * √T
    # NOTE: QuantLib returns vega per 1% (0.01) change, not per 100% (1.0) change
    # So we DON'T divide by 100
    vega = (spot_price * math.exp(-dividend_yield * time_to_expiration) * 
            norm.pdf(d1) * math.sqrt(time_to_expiration))
    
    return vega

def calc_option_theta(
    option_type: str,
    spot_price: float,
    strike: float,
    time_to_expiration: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float = 0.0
) -> float:
    """
    Calculate the theta of a European option.
    
    Theta measures the rate of change of option price with respect to 
    the passage of time (time decay). It represents the change in option 
    value for one calendar day passing.

    Parameters
    ----------
    option_type : str
        Either "call" or "put".
    spot_price : float
        The current price of the underlying asset.
    strike : float
        The strike price of the option.
    time_to_expiration : float
        Time to expiration in years.
    risk_free_rate : float
        The risk-free interest rate (as a decimal, e.g., 0.05 for 5%).
    volatility : float
        The volatility of the underlying asset (as a decimal, e.g., 0.20 for 20%).
    dividend_yield : float, optional
        The continuous dividend yield (as a decimal, e.g., 0.02 for 2%).
        Defaults to 0.0.

    Returns
    -------
    float
        The theta of the option (per calendar day).
    """
    
    # Calculate d1 and d2
    d1 = (math.log(spot_price / strike) + 
          (risk_free_rate - dividend_yield + 0.5 * volatility ** 2) * time_to_expiration) / \
         (volatility * math.sqrt(time_to_expiration))
    
    d2 = d1 - volatility * math.sqrt(time_to_expiration)
    
    # Common term for both call and put
    term1 = -(spot_price * math.exp(-dividend_yield * time_to_expiration) * 
              norm.pdf(d1) * volatility) / (2 * math.sqrt(time_to_expiration))
    
    if option_type.lower() == "call":
        # Call theta
        term2 = dividend_yield * spot_price * math.exp(-dividend_yield * time_to_expiration) * norm.cdf(d1)
        term3 = -risk_free_rate * strike * math.exp(-risk_free_rate * time_to_expiration) * norm.cdf(d2)
        theta = term1 + term2 + term3
    elif option_type.lower() == "put":
        # Put theta
        term2 = -dividend_yield * spot_price * math.exp(-dividend_yield * time_to_expiration) * norm.cdf(-d1)
        term3 = risk_free_rate * strike * math.exp(-risk_free_rate * time_to_expiration) * norm.cdf(-d2)
        theta = term1 + term2 + term3
    else:
        raise ValueError("option_type must be either 'call' or 'put'")
    
    # NOTE: QuantLib returns theta per calendar day, not per year
    # So we DON'T divide by 365
    return theta

def calc_option_rho(
    option_type: str,
    spot_price: float,
    strike: float,
    time_to_expiration: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float = 0.0
) -> float:
    """
    Calculate the rho of a European option.
    
    Rho measures the rate of change of option price with respect to 
    changes in the risk-free interest rate. It represents the change 
    in option value for a 1% (0.01) change in interest rates.

    Parameters
    ----------
    option_type : str
        Either "call" or "put".
    spot_price : float
        The current price of the underlying asset.
    strike : float
        The strike price of the option.
    time_to_expiration : float
        Time to expiration in years.
    risk_free_rate : float
        The risk-free interest rate (as a decimal, e.g., 0.05 for 5%).
    volatility : float
        The volatility of the underlying asset (as a decimal, e.g., 0.20 for 20%).
    dividend_yield : float, optional
        The continuous dividend yield (as a decimal, e.g., 0.02 for 2%).
        Defaults to 0.0.

    Returns
    -------
    float
        The rho of the option (per 1% change in interest rate).
    """
    import math
    from scipy.stats import norm
    
    # Calculate d1 and d2
    d1 = (math.log(spot_price / strike) + 
          (risk_free_rate - dividend_yield + 0.5 * volatility ** 2) * time_to_expiration) / \
         (volatility * math.sqrt(time_to_expiration))
    
    d2 = d1 - volatility * math.sqrt(time_to_expiration)
    
    if option_type.lower() == "call":
        # Call rho: K * T * e^(-rT) * N(d2)
        # NOTE: QuantLib returns rho per 1% (0.01) change, not per 100% (1.0)
        # So we DON'T divide by 100
        rho = (strike * time_to_expiration * 
               math.exp(-risk_free_rate * time_to_expiration) * 
               norm.cdf(d2))
    elif option_type.lower() == "put":
        # Put rho: -K * T * e^(-rT) * N(-d2)
        rho = -(strike * time_to_expiration * 
                math.exp(-risk_free_rate * time_to_expiration) * 
                norm.cdf(-d2))
    else:
        raise ValueError("option_type must be either 'call' or 'put'")
    
    return rho

def calc_implied_volatility(
    option_type: str,
    market_price: float,
    spot_price: float,
    strike: float,
    time_to_expiration: float,
    risk_free_rate: float,
    dividend_yield: float = 0.0,
    initial_guess: float = 0.20,
    tolerance: float = 1e-6,
    max_iterations: int = 100
) -> float:
    """
    Calculate the implied volatility of a European option given its market price.
    
    Uses Newton-Raphson method to find the volatility that produces the 
    observed market price.

    Parameters
    ----------
    option_type : str
        Either "call" or "put".
    market_price : float
        The observed market price of the option.
    spot_price : float
        The current price of the underlying asset.
    strike : float
        The strike price of the option.
    time_to_expiration : float
        Time to expiration in years.
    risk_free_rate : float
        The risk-free interest rate (as a decimal, e.g., 0.05 for 5%).
    dividend_yield : float, optional
        The continuous dividend yield (as a decimal, e.g., 0.02 for 2%).
        Defaults to 0.0.
    initial_guess : float, optional
        Initial guess for implied volatility (default: 0.20 for 20%).
    tolerance : float, optional
        Convergence tolerance (default: 1e-6).
    max_iterations : int, optional
        Maximum number of iterations (default: 100).

    Returns
    -------
    float
        The implied volatility as a decimal (e.g., 0.25 for 25%).
    """
    
    volatility = initial_guess
    
    for iteration in range(max_iterations):
        # Calculate option price at current volatility guess
        calculated_price = calc_option_price(
            option_type=option_type,
            spot_price=spot_price,
            strike=strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=risk_free_rate,
            volatility=volatility,
            dividend_yield=dividend_yield
        )
        
        # Check if we're close enough
        price_diff = calculated_price - market_price
        if abs(price_diff) < tolerance:
            return volatility
        
        # Calculate vega (derivative of price with respect to volatility)
        vega = calc_option_vega(
            spot_price=spot_price,
            strike=strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=risk_free_rate,
            volatility=volatility,
            dividend_yield=dividend_yield
        )
        
        # Vega is expressed per 1% change, so multiply by 100 for per-unit change
        vega_per_unit = vega * 100
        
        # Newton-Raphson update: vol_new = vol_old - f(vol) / f'(vol)
        if abs(vega_per_unit) > 1e-10:  # Avoid division by zero
            volatility = volatility - price_diff / vega_per_unit
        else:
            # If vega is too small, use bisection step
            volatility = volatility - 0.01 * (1 if price_diff > 0 else -1)
        
        # Keep volatility in reasonable bounds
        volatility = max(0.001, min(volatility, 5.0))  # Between 0.1% and 500%
    
    # If we didn't converge, return the best estimate
    return volatility

def calc_binomial_option_price(
    option_type: str,
    spot_price: float,
    strike: float,
    time_to_expiration: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float = 0.0,
    time_steps: int = 100
) -> float:
    """
    Calculate the price of an American option using the binomial tree method.
    
    The binomial tree method builds a discrete-time model of possible stock 
    price movements and works backward from expiration to find the option value.

    Parameters
    ----------
    option_type : str
        Either "call" or "put".
    spot_price : float
        The current price of the underlying asset.
    strike : float
        The strike price of the option.
    time_to_expiration : float
        Time to expiration in years.
    risk_free_rate : float
        The risk-free interest rate (as a decimal, e.g., 0.05 for 5%).
    volatility : float
        The volatility of the underlying asset (as a decimal, e.g., 0.20 for 20%).
    dividend_yield : float, optional
        The continuous dividend yield (as a decimal, e.g., 0.02 for 2%).
        Defaults to 0.0.
    time_steps : int, optional
        Number of time steps in the binomial tree (default: 100).
        More steps = more accurate but slower.

    Returns
    -------
    float
        The American option price.
    """
        
    # Calculate parameters
    dt = time_to_expiration / time_steps  # Time per step
    
    # Cox-Ross-Rubinstein (CRR) parameters
    u = math.exp(volatility * math.sqrt(dt))  # Up factor
    d = 1 / u  # Down factor
    
    # Risk-neutral probability (adjusted for dividends)
    a = math.exp((risk_free_rate - dividend_yield) * dt)
    p = (a - d) / (u - d)  # Risk-neutral probability of up move
    
    # Discount factor
    discount = math.exp(-risk_free_rate * dt)
    
    # Initialize asset prices at maturity (final nodes)
    asset_prices = np.zeros(time_steps + 1)
    for i in range(time_steps + 1):
        asset_prices[i] = spot_price * (u ** (time_steps - i)) * (d ** i)
    
    # Initialize option values at maturity
    option_values = np.zeros(time_steps + 1)
    
    if option_type.lower() == "call":
        for i in range(time_steps + 1):
            option_values[i] = max(0, asset_prices[i] - strike)
    elif option_type.lower() == "put":
        for i in range(time_steps + 1):
            option_values[i] = max(0, strike - asset_prices[i])
    else:
        raise ValueError("option_type must be either 'call' or 'put'")
    
    # Work backwards through the tree
    for step in range(time_steps - 1, -1, -1):
        for i in range(step + 1):
            # Asset price at this node
            asset_price = spot_price * (u ** (step - i)) * (d ** i)
            
            # Intrinsic value (value if exercised now)
            if option_type.lower() == "call":
                intrinsic_value = max(0, asset_price - strike)
            else:  # put
                intrinsic_value = max(0, strike - asset_price)
            
            # Continuation value (expected value if held)
            continuation_value = discount * (p * option_values[i] + (1 - p) * option_values[i + 1])
            
            # American option: take max of exercise vs. continuation
            option_values[i] = max(intrinsic_value, continuation_value)
    
    return option_values[0]