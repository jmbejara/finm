"""
Tests for the fixedincome module.
"""

import numpy as np
import pandas as pd

from datetime import datetime

from finm.options import (
    calc_option_price,
    calc_option_payoff,
    calc_option_delta,
    calc_option_gamma,
    calc_option_vega,
    calc_option_theta,
    calc_option_rho,
    calc_implied_volatility,
    calc_binomial_option_price,
)

from tests.test_ql_options_functions import (
    ql_create_european_option,
    ql_calc_option_price,
    ql_calc_option_delta,
    ql_calc_option_gamma,
    ql_calc_option_vega,
    ql_calc_option_theta,
    ql_calc_option_rho,
    ql_calc_implied_volatility,
    ql_create_american_option,
    ql_calc_binomial_option_price,
)

class TestOptionFunctions:
    """Tests for option pricing and Greeks functions."""
    
    def setup_method(self):
        """Set up QuantLib parameters for option tests."""
        # Common test parameters
        self.valuation_date = "2024-01-15"
        self.expiration_date = "2024-07-15"  # 6 months out
        self.strike = 100.0
        self.spot_price = 100.0  # At-the-money
        self.risk_free_rate = 0.05  # 5%
        self.dividend_yield = 0.02  # 2%
        self.volatility = 0.25  # 25%
        
        # Create European options
        self.call_option = ql_create_european_option(
            option_type="call",
            strike=self.strike,
            expiration_date=self.expiration_date,
            spot_price=self.spot_price
        )
        
        self.put_option = ql_create_european_option(
            option_type="put",
            strike=self.strike,
            expiration_date=self.expiration_date,
            spot_price=self.spot_price
        )
        
        # Price the European options
        self.call_price = ql_calc_option_price(
            valuation_date=self.valuation_date,
            option=self.call_option,
            spot_price=self.spot_price,
            risk_free_rate=self.risk_free_rate,
            dividend_yield=self.dividend_yield,
            volatility=self.volatility
        )
        
        self.put_price = ql_calc_option_price(
            valuation_date=self.valuation_date,
            option=self.put_option,
            spot_price=self.spot_price,
            risk_free_rate=self.risk_free_rate,
            dividend_yield=self.dividend_yield,
            volatility=self.volatility
        )
        
        # Create American options
        self.american_call = ql_create_american_option(
            option_type="call",
            strike=self.strike,
            maturity_date=self.expiration_date
        )
        
        self.american_put = ql_create_american_option(
            option_type="put",
            strike=self.strike,
            maturity_date=self.expiration_date
        )
        
        # Price the American options using binomial tree
        self.american_call_price = ql_calc_binomial_option_price(
            valuation_date=self.valuation_date,
            option=self.american_call,
            spot_price=self.spot_price,
            risk_free_rate=self.risk_free_rate,
            dividend_yield=self.dividend_yield,
            volatility=self.volatility,
            time_steps=100
        )
        
        self.american_put_price = ql_calc_binomial_option_price(
            valuation_date=self.valuation_date,
            option=self.american_put,
            spot_price=self.spot_price,
            risk_free_rate=self.risk_free_rate,
            dividend_yield=self.dividend_yield,
            volatility=self.volatility,
            time_steps=100
        )

    def test_calc_option_price(self):
        """Test that Black-Scholes option price is calculated correctly."""
        
        # Calculate time to expiration in years
        val_dt = datetime.strptime(self.valuation_date, "%Y-%m-%d")
        exp_dt = datetime.strptime(self.expiration_date, "%Y-%m-%d")
        time_to_expiration = (exp_dt - val_dt).days / 365.0
        
        # Calculate call option price using student function
        student_call_price = calc_option_price(
            option_type="call",
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield
        )
        
        # Compare with QuantLib price
        ql_call_price = self.call_price
        
        # Test: Check that prices match within tolerance
        tolerance = 0.01  # 1 cent tolerance
        diff = abs(student_call_price - ql_call_price)
        
        assert diff < tolerance, \
            f"Call price mismatch: student={student_call_price:.4f}, ql={ql_call_price:.4f}, diff={diff:.4f}"
        
        # Test put option as well
        student_put_price = calc_option_price(
            option_type="put",
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield
        )
        
        ql_put_price = self.put_price
        
        diff_put = abs(student_put_price - ql_put_price)
        
        assert diff_put < tolerance, \
            f"Put price mismatch: student={student_put_price:.4f}, ql={ql_put_price:.4f}, diff={diff_put:.4f}"
        
        # Additional sanity checks
        assert student_call_price > 0, "Call option price should be positive"
        assert student_put_price > 0, "Put option price should be positive"

    def test_calc_option_payoff(self):
        """Test that option payoff is calculated correctly."""
        
        # Test call option payoff at various spot prices
        
        # ITM call (spot > strike)
        call_payoff_itm = calc_option_payoff(
            option_type="call",
            spot_price=110.0,
            strike=self.strike
        )
        assert call_payoff_itm == 10.0, \
            f"ITM call payoff should be 10.0, got {call_payoff_itm:.2f}"
        
        # ATM call (spot = strike)
        call_payoff_atm = calc_option_payoff(
            option_type="call",
            spot_price=100.0,
            strike=self.strike
        )
        assert call_payoff_atm == 0.0, \
            f"ATM call payoff should be 0.0, got {call_payoff_atm:.2f}"
        
        # OTM call (spot < strike)
        call_payoff_otm = calc_option_payoff(
            option_type="call",
            spot_price=90.0,
            strike=self.strike
        )
        assert call_payoff_otm == 0.0, \
            f"OTM call payoff should be 0.0, got {call_payoff_otm:.2f}"
        
        # Test put option payoff at various spot prices
        
        # ITM put (spot < strike)
        put_payoff_itm = calc_option_payoff(
            option_type="put",
            spot_price=90.0,
            strike=self.strike
        )
        assert put_payoff_itm == 10.0, \
            f"ITM put payoff should be 10.0, got {put_payoff_itm:.2f}"
        
        # ATM put (spot = strike)
        put_payoff_atm = calc_option_payoff(
            option_type="put",
            spot_price=100.0,
            strike=self.strike
        )
        assert put_payoff_atm == 0.0, \
            f"ATM put payoff should be 0.0, got {put_payoff_atm:.2f}"
        
        # OTM put (spot > strike)
        put_payoff_otm = calc_option_payoff(
            option_type="put",
            spot_price=110.0,
            strike=self.strike
        )
        assert put_payoff_otm == 0.0, \
            f"OTM put payoff should be 0.0, got {put_payoff_otm:.2f}"
        
        # Additional sanity checks
        # Payoffs should never be negative
        assert call_payoff_itm >= 0, "Call payoff should never be negative"
        assert put_payoff_itm >= 0, "Put payoff should never be negative"


    def test_calc_option_delta(self):
        """Test that option delta is calculated correctly."""
        
        # Calculate time to expiration in years
        val_dt = datetime.strptime(self.valuation_date, "%Y-%m-%d")
        exp_dt = datetime.strptime(self.expiration_date, "%Y-%m-%d")
        time_to_expiration = (exp_dt - val_dt).days / 365.0
        
        # Calculate call delta using student function
        student_call_delta = calc_option_delta(
            option_type="call",
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield
        )
        
        # Get QuantLib delta
        ql_call_delta = ql_calc_option_delta(self.call_option)
        
        # Test: Check that deltas match within tolerance
        tolerance = 0.01
        diff = abs(student_call_delta - ql_call_delta)
        
        assert diff < tolerance, \
            f"Call delta mismatch: student={student_call_delta:.4f}, ql={ql_call_delta:.4f}, diff={diff:.4f}"
        
        # Test put delta as well
        student_put_delta = calc_option_delta(
            option_type="put",
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield
        )
        
        ql_put_delta = ql_calc_option_delta(self.put_option)
        
        diff_put = abs(student_put_delta - ql_put_delta)
        
        assert diff_put < tolerance, \
            f"Put delta mismatch: student={student_put_delta:.4f}, ql={ql_put_delta:.4f}, diff={diff_put:.4f}"
        
        # Additional sanity checks
        # Call delta should be between 0 and 1
        assert 0 <= student_call_delta <= 1, \
            f"Call delta should be between 0 and 1, got {student_call_delta:.4f}"
        
        # Put delta should be between -1 and 0
        assert -1 <= student_put_delta <= 0, \
            f"Put delta should be between -1 and 0, got {student_put_delta:.4f}"

    def test_calc_option_gamma(self):
        """Test that option gamma is calculated correctly."""
        
        # Calculate time to expiration in years
        val_dt = datetime.strptime(self.valuation_date, "%Y-%m-%d")
        exp_dt = datetime.strptime(self.expiration_date, "%Y-%m-%d")
        time_to_expiration = (exp_dt - val_dt).days / 365.0
        
        # Calculate call gamma using student function
        student_call_gamma = calc_option_gamma(
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield
        )
        
        # Get QuantLib gamma
        ql_call_gamma = ql_calc_option_gamma(self.call_option)
        
        # Test: Check that gammas match within tolerance
        tolerance = 0.001  # Gamma is typically a small number
        diff = abs(student_call_gamma - ql_call_gamma)
        
        assert diff < tolerance, \
            f"Call gamma mismatch: student={student_call_gamma:.6f}, ql={ql_call_gamma:.6f}, diff={diff:.6f}"
        
        # Test put gamma as well (should be same as call gamma)
        student_put_gamma = calc_option_gamma(
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield
        )
        
        ql_put_gamma = ql_calc_option_gamma(self.put_option)
        
        diff_put = abs(student_put_gamma - ql_put_gamma)
        
        assert diff_put < tolerance, \
            f"Put gamma mismatch: student={student_put_gamma:.6f}, ql={ql_put_gamma:.6f}, diff={diff_put:.6f}"
        
        # Additional sanity checks
        # Gamma should be positive for both calls and puts
        assert student_call_gamma > 0, "Gamma should be positive for long options"
        assert student_put_gamma > 0, "Gamma should be positive for long options"

    def test_calc_option_vega(self):
        """Test that option vega is calculated correctly."""
        
        # Calculate time to expiration in years
        val_dt = datetime.strptime(self.valuation_date, "%Y-%m-%d")
        exp_dt = datetime.strptime(self.expiration_date, "%Y-%m-%d")
        time_to_expiration = (exp_dt - val_dt).days / 365.0
        
        # Calculate call vega using student function
        student_call_vega = calc_option_vega(
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield
        )
        
        # Get QuantLib vega
        ql_call_vega = ql_calc_option_vega(self.call_option)
        
        # Test: Check that vegas match within tolerance
        tolerance = 0.01
        diff = abs(student_call_vega - ql_call_vega)
        
        assert diff < tolerance, \
            f"Call vega mismatch: student={student_call_vega:.4f}, ql={ql_call_vega:.4f}, diff={diff:.4f}"
        
        # Test put vega as well (should be same as call vega)
        student_put_vega = calc_option_vega(
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield
        )
        
        ql_put_vega = ql_calc_option_vega(self.put_option)
        
        diff_put = abs(student_put_vega - ql_put_vega)
        
        assert diff_put < tolerance, \
            f"Put vega mismatch: student={student_put_vega:.4f}, ql={ql_put_vega:.4f}, diff={diff_put:.4f}"
        
        # Additional sanity checks
        # Vega should be positive for both calls and puts
        assert student_call_vega > 0, "Vega should be positive for long options"
        assert student_put_vega > 0, "Vega should be positive for long options"

    def test_calc_option_theta(self):
        """Test that option theta is calculated correctly."""
        
        # Calculate time to expiration in years
        val_dt = datetime.strptime(self.valuation_date, "%Y-%m-%d")
        exp_dt = datetime.strptime(self.expiration_date, "%Y-%m-%d")
        time_to_expiration = (exp_dt - val_dt).days / 365.0
        
        # Calculate call theta using student function
        student_call_theta = calc_option_theta(
            option_type="call",
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield
        )
        
        # Get QuantLib theta
        ql_call_theta = ql_calc_option_theta(self.call_option)
        
        # Test: Check that thetas match within tolerance
        tolerance = 0.01
        diff = abs(student_call_theta - ql_call_theta)
        
        assert diff < tolerance, \
            f"Call theta mismatch: student={student_call_theta:.4f}, ql={ql_call_theta:.4f}, diff={diff:.4f}"
        
        # Test put theta as well
        student_put_theta = calc_option_theta(
            option_type="put",
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield
        )
        
        ql_put_theta = ql_calc_option_theta(self.put_option)
        
        diff_put = abs(student_put_theta - ql_put_theta)
        
        assert diff_put < tolerance, \
            f"Put theta mismatch: student={student_put_theta:.4f}, ql={ql_put_theta:.4f}, diff={diff_put:.4f}"
        
        # Additional sanity checks
        # Theta is typically negative for long options (time decay)
        assert student_call_theta < 0, "Call theta should be negative (time decay)"

    def test_calc_option_rho(self):
        """Test that option rho is calculated correctly."""
        
        # Calculate time to expiration in years
        val_dt = datetime.strptime(self.valuation_date, "%Y-%m-%d")
        exp_dt = datetime.strptime(self.expiration_date, "%Y-%m-%d")
        time_to_expiration = (exp_dt - val_dt).days / 365.0
        
        # Calculate call rho using student function
        student_call_rho = calc_option_rho(
            option_type="call",
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield
        )
        
        # Get QuantLib rho
        ql_call_rho = ql_calc_option_rho(self.call_option)
        
        # Test: Check that rhos match within tolerance
        tolerance = 0.01
        diff = abs(student_call_rho - ql_call_rho)
        
        assert diff < tolerance, \
            f"Call rho mismatch: student={student_call_rho:.4f}, ql={ql_call_rho:.4f}, diff={diff:.4f}"
        
        # Test put rho as well
        student_put_rho = calc_option_rho(
            option_type="put",
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield
        )
        
        ql_put_rho = ql_calc_option_rho(self.put_option)
        
        diff_put = abs(student_put_rho - ql_put_rho)
        
        assert diff_put < tolerance, \
            f"Put rho mismatch: student={student_put_rho:.4f}, ql={ql_put_rho:.4f}, diff={diff_put:.4f}"
        
        # Additional sanity checks
        # Call rho should be positive (calls benefit from higher rates)
        assert student_call_rho > 0, \
            f"Call rho should be positive, got {student_call_rho:.4f}"
        
        # Put rho should be negative (puts hurt by higher rates)
        assert student_put_rho < 0, \
            f"Put rho should be negative, got {student_put_rho:.4f}"

    def test_calc_implied_volatility(self):
        """Test that implied volatility is calculated correctly."""
        
        # Calculate time to expiration in years
        val_dt = datetime.strptime(self.valuation_date, "%Y-%m-%d")
        exp_dt = datetime.strptime(self.expiration_date, "%Y-%m-%d")
        time_to_expiration = (exp_dt - val_dt).days / 365.0
        
        # First, calculate option price at known volatility
        known_volatility = self.volatility  # 0.25
        
        market_call_price = calc_option_price(
            option_type="call",
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=known_volatility,
            dividend_yield=self.dividend_yield
        )
        
        # Now calculate implied vol from that price (should recover original vol)
        student_implied_vol = calc_implied_volatility(
            option_type="call",
            market_price=market_call_price,
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            dividend_yield=self.dividend_yield
        )
        
        # Get QuantLib implied vol
        ql_implied_vol = ql_calc_implied_volatility(
            valuation_date=self.valuation_date,
            option=self.call_option,
            market_price=market_call_price,
            spot_price=self.spot_price,
            risk_free_rate=self.risk_free_rate,
            dividend_yield=self.dividend_yield
        )
        
        # Test: Check that implied vols match within tolerance
        tolerance = 0.02  # 2% tolerance
        diff = abs(student_implied_vol - ql_implied_vol)
        
        assert diff < tolerance, \
            f"Implied vol mismatch: student={student_implied_vol:.6f}, ql={ql_implied_vol:.6f}, diff={diff:.6f}"
        
        # Should recover the original volatility
        assert abs(student_implied_vol - known_volatility) < tolerance, \
            f"Should recover original volatility: student={student_implied_vol:.6f}, original={known_volatility:.6f}"
        
        # Test with put option as well
        market_put_price = calc_option_price(
            option_type="put",
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=known_volatility,
            dividend_yield=self.dividend_yield
        )
        
        student_put_implied_vol = calc_implied_volatility(
            option_type="put",
            market_price=market_put_price,
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            dividend_yield=self.dividend_yield
        )
        
        assert abs(student_put_implied_vol - known_volatility) < tolerance, \
            f"Put: Should recover original volatility: {student_put_implied_vol:.6f} vs {known_volatility:.6f}"
        
        # Additional sanity checks
        assert student_implied_vol > 0, "Implied volatility should be positive"
        assert student_implied_vol < 2.0, "Implied volatility should be reasonable (< 200%)"

    def test_calc_binomial_option_price(self):
        """Test that binomial tree option pricing works correctly."""
        
        # Calculate time to expiration in years
        val_dt = datetime.strptime(self.valuation_date, "%Y-%m-%d")
        exp_dt = datetime.strptime(self.expiration_date, "%Y-%m-%d")
        time_to_expiration = (exp_dt - val_dt).days / 365.0
        
        # Calculate American put price using student function
        student_put_price = calc_binomial_option_price(
            option_type="put",
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield,
            time_steps=100
        )
        
        # Compare with QuantLib price
        ql_put_price = self.american_put_price
        
        # Test: Check that prices match within tolerance
        tolerance = 0.10  # Larger tolerance for binomial approximation
        diff = abs(student_put_price - ql_put_price)
        
        assert diff < tolerance, \
            f"American put price mismatch: student={student_put_price:.4f}, ql={ql_put_price:.4f}, diff={diff:.4f}"
        
        # Test American call as well
        student_call_price = calc_binomial_option_price(
            option_type="call",
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield,
            time_steps=100
        )
        
        ql_call_price = self.american_call_price
        
        diff_call = abs(student_call_price - ql_call_price)
        
        assert diff_call < tolerance, \
            f"American call price mismatch: student={student_call_price:.4f}, ql={ql_call_price:.4f}, diff={diff_call:.4f}"
        
        # Additional sanity checks
        assert student_put_price > 0, "American put price should be positive"
        assert student_call_price > 0, "American call price should be positive"
        
        # American option should be worth at least as much as European
        european_put = calc_option_price(
            option_type="put",
            spot_price=self.spot_price,
            strike=self.strike,
            time_to_expiration=time_to_expiration,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield
        )
        
        assert student_put_price >= european_put - 0.01, \
            f"American put ({student_put_price:.4f}) should be >= European put ({european_put:.4f})"