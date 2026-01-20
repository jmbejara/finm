"""
Tests for the fixedincome module.
"""

import numpy as np
import QuantLib as ql
import unittest

from datetime import datetime

from finm.fixedincome import (
    bond_price,
    convexity,
    duration,
    future_value,
    get_coupon_dates,
    modified_duration,
    present_value,
    yield_to_maturity,
)

from ql_test_functions import (
    ql_create_schedule,
    ql_extract_coupon_dates,
    ql_create_fixed_rate_bond,
    ql_create_zero_coupon_bond,
    ql_extract_cashflows,
    ql_extract_coupon_dates_cashflows,
    ql_calc_clean_price,
    ql_calc_dirty_price,
    ql_calc_accrued_interest,
    ql_calc_modified_duration,
    ql_calc_macaulay_duration,
    ql_calc_convexity,
    ql_calc_zero_coupon_bond_price,
    ql_calc_yield_to_maturity,
    ql_calc_dollar_duration,
    ql_create_forward_rate_agreement,
    ql_create_european_option,
    ql_calc_option_price,
    ql_extract_option_delta,
    ql_extract_option_gamma,
    ql_extract_option_vega,
    ql_extract_option_theta,
    ql_extract_option_rho,
    ql_calc_implied_volatility,
    ql_create_american_option,
    ql_calc_binomial_option_price,
    ql_is_business_day,
    ql_calc_business_days_between,
    ql_create_vanilla_swap,
    ql_calc_swap_npv,
    ql_calc_swap_fair_rate,
    ql_extract_swap_legs,
    ql_create_cds,
    ql_calc_cds_npv,
    ql_create_cds,
    ql_calc_cds_npv,
    ql_calc_cds_spread,
)



class TestPresentValue:
    """Tests for present_value function."""

    def test_discrete_compounding(self):
        """Test present value with discrete compounding."""
        pv = present_value(1000, 0.05, 2)
        expected = 1000 / (1.05**2)
        assert np.isclose(pv, expected)

    def test_continuous_compounding(self):
        """Test present value with continuous compounding."""
        pv = present_value(1000, 0.05, 2, compounding="continuous")
        expected = 1000 * np.exp(-0.05 * 2)
        assert np.isclose(pv, expected)

    def test_zero_rate(self):
        """Test present value with zero interest rate."""
        pv = present_value(1000, 0, 5)
        assert pv == 1000


class TestFutureValue:
    """Tests for future_value function."""

    def test_discrete_compounding(self):
        """Test future value with discrete compounding."""
        fv = future_value(1000, 0.05, 2)
        expected = 1000 * (1.05**2)
        assert np.isclose(fv, expected)

    def test_continuous_compounding(self):
        """Test future value with continuous compounding."""
        fv = future_value(1000, 0.05, 2, compounding="continuous")
        expected = 1000 * np.exp(0.05 * 2)
        assert np.isclose(fv, expected)


class TestBondPrice:
    """Tests for bond_price function."""

    def test_par_bond(self):
        """Test that a bond priced at par has price equal to face value."""
        # When coupon rate equals YTM, bond should trade at par
        price = bond_price(1000, 0.05, 0.05, 10, frequency=2)
        assert np.isclose(price, 1000, rtol=1e-6)

    def test_bond_price_ql(self):
        """Test that a bond priced with the python function matches that of the QuantLib function within 0.1%."""
        # When coupon rate equals YTM, bond should trade at par
        price = bond_price(1000, 0.05, 0.05, 10, frequency=2)
        price_ql = bond_price_ql(1000, 0.05, 0.05, 10, frequency=2)
        price_percent_delta = abs(price / price_ql)
        assert np.isclose(price_percent_delta, 1, rtol=1e-3)

    def test_premium_bond(self):
        """Test that coupon > YTM results in premium bond."""
        price = bond_price(1000, 0.06, 0.05, 10, frequency=2)
        assert price > 1000

    def test_discount_bond(self):
        """Test that coupon < YTM results in discount bond."""
        price = bond_price(1000, 0.04, 0.05, 10, frequency=2)
        assert price < 1000


class TestYieldToMaturity:
    """Tests for yield_to_maturity function."""

    def test_ytm_roundtrip(self):
        """Test that YTM calculation is consistent with bond_price."""
        face = 1000
        coupon = 0.06
        ytm_expected = 0.05
        periods = 10
        freq = 2

        price = bond_price(face, coupon, ytm_expected, periods, freq)
        ytm_calculated = yield_to_maturity(price, face, coupon, periods, freq)

        assert np.isclose(ytm_calculated, ytm_expected, rtol=1e-4)

    def test_par_bond_ytm(self):
        """Test YTM equals coupon rate for par bond."""
        ytm = yield_to_maturity(1000, 1000, 0.05, 10, frequency=2)
        assert np.isclose(ytm, 0.05, rtol=1e-4)


class TestDuration:
    """Tests for duration functions."""

    def test_duration_positive(self):
        """Test that duration is positive."""
        dur = duration(1000, 0.05, 0.05, 10, frequency=2)
        assert dur > 0

    def test_duration_less_than_maturity(self):
        """Test that duration is less than or equal to maturity for coupon bonds."""
        dur = duration(1000, 0.05, 0.05, 10, frequency=2)
        maturity = 10 / 2  # years
        assert dur <= maturity

    def test_modified_duration_less_than_macaulay(self):
        """Test that modified duration is less than Macaulay duration."""
        mac_dur = duration(1000, 0.05, 0.05, 10, frequency=2)
        mod_dur = modified_duration(1000, 0.05, 0.05, 10, frequency=2)
        assert mod_dur < mac_dur


class TestConvexity:
    """Tests for convexity function."""

    def test_convexity_positive(self):
        """Test that convexity is positive for standard bonds."""
        conv = convexity(1000, 0.05, 0.05, 10, frequency=2)
        assert conv > 0

    def test_convexity_increases_with_maturity(self):
        """Test that convexity increases with maturity."""
        conv_short = convexity(1000, 0.05, 0.05, 4, frequency=2)
        conv_long = convexity(1000, 0.05, 0.05, 20, frequency=2)
        assert conv_long > conv_short


class TestCouponDates:
    """Tests for get_coupon_dates function."""

    def test_coupon_dates_count(self):
        """Test that the number of coupon dates is correct."""
        quote_date = "2020-01-01"
        maturity_date = "2025-01-01"
        coupon_dates = get_coupon_dates(quote_date, maturity_date)
        assert len(coupon_dates) == 10  # 5 years semiannual -> 10 payments

    def test_coupon_dates_count_ql(self):
        """Test that the number of coupon dates is correct based on the python function
        and the QuantLib function."""
        quote_date = "2020-01-02"
        maturity_date = "2025-01-01"
        coupon_dates = get_coupon_dates(quote_date, maturity_date)
        coupon_dates_ql = get_coupon_dates_ql(quote_date, maturity_date)
        assert len(coupon_dates) == len(
            coupon_dates_ql
        )  # 5 years semiannual -> 10 payments

    def test_coupon_date_gap(self):
        """Test that coupon dates are every six months."""
        quote_date = "2020-01-01"
        maturity_date = "2025-01-01"
        coupon_dates = get_coupon_dates(quote_date, maturity_date)

        # Check that each date is approximately 6 months apart
        for i in range(1, len(coupon_dates)):
            delta = (coupon_dates[i] - coupon_dates[i - 1]).days
            assert 170 <= delta <= 190  # Allow some leeway for month length variations

    def test_coupon_date_gap_ql(self):
        """Test that coupon dates are every six months and that the difference in date between
        python function and QuantLib function is less than 3 days (accounting for a weekend
        discrepancy)."""
        quote_date = "2020-01-02"
        maturity_date = "2025-01-01"
        coupon_dates = get_coupon_dates(quote_date, maturity_date)
        coupon_dates_ql = get_coupon_dates_ql(quote_date, maturity_date)

        # Check that each date is approximately 6 months apart
        for i in range(1, len(coupon_dates)):
            delta = (coupon_dates[i] - coupon_dates[i - 1]).days
            assert 170 <= delta <= 190  # Allow some leeway for month length variations

        # Check that each date is less than 3 days apart between the "coupon_dates" and "coupon_dates_ql"
        assert len(coupon_dates) == len(coupon_dates_ql)
        for i in range(1, len(coupon_dates)):
            delta = (coupon_dates[i] - coupon_dates_ql[i]).days
            assert delta <= 3  # Allow some leeway for month length variations




class TestBondFunctions(unittest.TestCase):
    
    def setUp(self):
        """Set up common test fixtures"""
        # Common test parameters
        self.valuation_date = "2024-01-15"
        self.issue_date = "2024-01-15"
        self.maturity_date = "2029-01-15"
        self.frequency = 2
        self.face_value = 100.0
        self.coupon_rate = 0.05
        self.ytm = 0.045
        
        # Create a standard test bond
        self.schedule = ql_create_schedule(
            issue_date=self.issue_date,
            maturity_date=self.maturity_date,
            frequency=self.frequency,
        )
        
        # self.test_bond = ql_create_fixed_rate_bond(
        #     issue_date=self.issue_date,
        #     maturity_date=self.maturity_date,
        #     face_value=self.face_value,
        #     coupon_rate=self.coupon_rate,
        #     schedule=schedule
        # )

    def test_coupon_number(self):
        """Test number of coupon payments"""
        coupon_dates = ql_extract_coupon_dates(
            schedule=self.schedule,
        )
        
        # Expected number of coupon dates: 5 years semiannual = 10 payments
        expected_num_coupons = 10

        # Check assertion
        print(coupon_dates)
        assert len(coupon_dates) == expected_num_coupons

    # def test_coupon_dates(self):
    #     """Test coupon date extraction"""
    #     coupon_dates = ql_extract_coupon_dates(
    #         schedule=self.schedule,
    #     )
        
    #     # Expected number of coupon dates: 5 years semiannual = 10 payments
    #     expected_num_coupons = 10
    #     self.assertEqual(len(coupon_dates), expected_num_coupons,
    #                      msg=f"Should have {expected_num_coupons} coupon dates")
        
    #     # Check first and last coupon dates
    #     expected_first = datetime.strptime("2024-07-15", "%Y-%m-%d").date()
    #     expected_last = datetime.strptime("2029-01-15", "%Y-%m-%d").date()
        
    #     self.assertEqual(coupon_dates[0], expected_first,
    #                      msg="First coupon date should match expected")
    #     self.assertEqual(coupon_dates[-1], expected_last,
    #                      msg="Last coupon date should match expected")



    
    # def test_calc_clean_price(self):
    #     """Test clean price calculation"""
    #     price = ql_calc_clean_price(
    #         valuation_date=self.valuation_date,
    #         ytm=self.ytm,
    #         bond=self.test_bond
    #     )
        
    #     # Expected value (pre-calculated or from known result)
    #     expected_price = 102.41  # Approximate value
        
    #     self.assertAlmostEqual(price, expected_price, places=2,
    #                           msg=f"Clean price should be approximately {expected_price}")
        
    #     # Additional checks
    #     self.assertGreater(price, 0, "Price should be positive")
    #     self.assertLess(price, 200, "Price should be reasonable")
    
#     def test_calc_yield_to_maturity(self):
#         """Test YTM calculation (inverse of pricing)"""
#         # First calculate price at known YTM
#         clean_price = ql_calc_clean_price(
#             valuation_date=self.valuation_date,
#             ytm=self.ytm,
#             bond=self.test_bond
#         )
        
#         # Then calculate YTM from that price
#         calculated_ytm = ql_calc_yield_to_maturity(
#             valuation_date=self.valuation_date,
#             clean_price=clean_price,
#             bond=self.test_bond
#         )
        
#         # Should recover the original YTM
#         self.assertAlmostEqual(calculated_ytm, self.ytm, places=6,
#                               msg="YTM calculation should be inverse of pricing")
    
#     def test_calc_modified_duration(self):
#         """Test modified duration calculation"""
#         mod_duration = ql_calc_modified_duration(
#             valuation_date=self.valuation_date,
#             ytm=self.ytm,
#             bond=self.test_bond
#         )
        
#         # Duration should be positive and less than time to maturity
#         time_to_maturity = 5.0  # 5 years
        
#         self.assertGreater(mod_duration, 0, "Duration should be positive")
#         self.assertLess(mod_duration, time_to_maturity, 
#                        "Duration should be less than time to maturity")
        
#         # For a 5-year bond with 5% coupon, duration should be around 4.3-4.5 years
#         self.assertAlmostEqual(mod_duration, 4.4, places=0,
#                               msg="Duration should be approximately correct")
    
#     def test_duration_price_relationship(self):
#         """Test that duration correctly predicts price changes"""
#         # Calculate initial price and duration
#         price1 = ql_calc_clean_price(self.valuation_date, self.ytm, self.test_bond)
#         duration = ql_calc_modified_duration(self.valuation_date, self.ytm, self.test_bond)
        
#         # Calculate price at slightly different yield
#         delta_yield = 0.0001  # 1 basis point
#         ytm2 = self.ytm + delta_yield
#         price2 = ql_calc_clean_price(self.valuation_date, ytm2, self.test_bond)
        
#         # Predicted price change using duration
#         predicted_price_change = -duration * price1 * delta_yield
#         actual_price_change = price2 - price1
        
#         # Should be very close for small yield changes
#         self.assertAlmostEqual(predicted_price_change, actual_price_change, places=4,
#                               msg="Duration should predict price changes accurately")
    
#     def test_dollar_duration(self):
#         """Test dollar duration calculation"""
#         dv01 = ql_calc_dollar_duration(
#             valuation_date=self.valuation_date,
#             ytm=self.ytm,
#             bond=self.test_bond,
#             face_value=1_000_000  # $1M position
#         )
        
#         # DV01 should be positive
#         self.assertGreater(dv01, 0, "Dollar duration should be positive")
        
#         # For a $1M position with ~4.4 years duration at price ~102, 
#         # DV01 should be roughly $449
#         self.assertAlmostEqual(dv01, 449, places=-1,  # Round to nearest 10
#                               msg="Dollar duration should be approximately correct")
    
#     def test_convexity_positive(self):
#         """Test that convexity is positive"""
#         convexity = ql_calc_convexity(
#             valuation_date=self.valuation_date,
#             ytm=self.ytm,
#             bond=self.test_bond
#         )
        
#         # Convexity should always be positive for option-free bonds
#         self.assertGreater(convexity, 0, 
#                           "Convexity should be positive for vanilla bonds")


# class TestOptionFunctions(unittest.TestCase):
    
#     def setUp(self):
#         """Set up common test fixtures"""
#         self.valuation_date = "2024-01-15"
#         self.maturity_date = "2024-07-15"  # 6 months
#         self.strike = 100.0
#         self.spot = 100.0
#         self.risk_free_rate = 0.05
#         self.dividend_yield = 0.02
#         self.volatility = 0.25
        
#         # Create test option
#         self.call_option = ql_create_european_option(
#             option_type="call",
#             strike=self.strike,
#             maturity_date=self.maturity_date
#         )
    
#     def test_call_option_properties(self):
#         """Test basic call option properties"""
#         price = ql_calc_black_scholes_price(
#             valuation_date=self.valuation_date,
#             option=self.call_option,
#             spot_price=self.spot,
#             risk_free_rate=self.risk_free_rate,
#             dividend_yield=self.dividend_yield,
#             volatility=self.volatility
#         )
        
#         # ATM call should have positive value
#         self.assertGreater(price, 0, "ATM call should have positive value")
        
#         # Call value should be less than spot (no arbitrage)
#         self.assertLess(price, self.spot, "Call value should be less than spot")
    
#     def test_put_call_parity(self):
#         """Test put-call parity relationship"""
#         # Create call and put with same parameters
#         call = ql_create_european_option("call", self.strike, self.maturity_date)
#         put = ql_create_european_option("put", self.strike, self.maturity_date)
        
#         call_price = ql_calc_black_scholes_price(
#             self.valuation_date, call, self.spot, 
#             self.risk_free_rate, self.dividend_yield, self.volatility
#         )
        
#         put_price = ql_calc_black_scholes_price(
#             self.valuation_date, put, self.spot,
#             self.risk_free_rate, self.dividend_yield, self.volatility
#         )
        
#         # Put-Call Parity: C - P = S*e^(-q*T) - K*e^(-r*T)
#         # where q = dividend yield, r = risk-free rate
#         dt = datetime.strptime(self.valuation_date, "%Y-%m-%d")
#         mat_dt = datetime.strptime(self.maturity_date, "%Y-%m-%d")
#         T = (mat_dt - dt).days / 365.0
        
#         import math
#         lhs = call_price - put_price
#         rhs = self.spot * math.exp(-self.dividend_yield * T) - \
#               self.strike * math.exp(-self.risk_free_rate * T)
        
#         self.assertAlmostEqual(lhs, rhs, places=4,
#                               msg="Put-call parity should hold")
    
#     def test_delta_range(self):
#         """Test that delta is in valid range"""
#         # Price the option first
#         ql_calc_black_scholes_price(
#             self.valuation_date, self.call_option, self.spot,
#             self.risk_free_rate, self.dividend_yield, self.volatility
#         )
        
#         delta = ql_extract_option_delta(self.call_option)
        
#         # Call delta should be between 0 and 1
#         self.assertGreaterEqual(delta, 0, "Call delta should be >= 0")
#         self.assertLessEqual(delta, 1, "Call delta should be <= 1")
        
#         # ATM call delta should be around 0.5
#         self.assertAlmostEqual(delta, 0.5, places=1,
#                               msg="ATM call delta should be approximately 0.5")
    
#     def test_gamma_positive(self):
#         """Test that gamma is positive"""
#         # Price the option first
#         ql_calc_black_scholes_price(
#             self.valuation_date, self.call_option, self.spot,
#             self.risk_free_rate, self.dividend_yield, self.volatility
#         )
        
#         gamma = ql_extract_option_gamma(self.call_option)
        
#         # Gamma should always be positive for long options
#         self.assertGreater(gamma, 0, "Gamma should be positive for long options")
    
#     def test_vega_positive(self):
#         """Test that vega is positive"""
#         # Price the option first
#         ql_calc_black_scholes_price(
#             self.valuation_date, self.call_option, self.spot,
#             self.risk_free_rate, self.dividend_yield, self.volatility
#         )
        
#         vega = ql_extract_option_vega(self.call_option)
        
#         # Vega should be positive (option value increases with volatility)
#         self.assertGreater(vega, 0, "Vega should be positive")
    
#     def test_implied_volatility_recovery(self):
#         """Test that implied vol calculation recovers input volatility"""
#         # Calculate price with known volatility
#         price = ql_calc_black_scholes_price(
#             self.valuation_date, self.call_option, self.spot,
#             self.risk_free_rate, self.dividend_yield, self.volatility
#         )
        
#         # Calculate implied vol from that price
#         impl_vol = ql_calc_implied_volatility(
#             self.valuation_date, self.call_option, price, self.spot,
#             self.risk_free_rate, self.dividend_yield
#         )
        
#         # Should recover the original volatility
#         self.assertAlmostEqual(impl_vol, self.volatility, places=6,
#                               msg="Implied vol should match input volatility")
    
#     def test_american_vs_european_call(self):
#         """Test that American call >= European call"""
#         # European call
#         euro_call = ql_create_european_option("call", self.strike, self.maturity_date)
#         euro_price = ql_calc_black_scholes_price(
#             self.valuation_date, euro_call, self.spot,
#             self.risk_free_rate, self.dividend_yield, self.volatility
#         )
        
#         # American call
#         amer_call = ql_create_american_option("call", self.strike, self.maturity_date)
#         amer_price = ql_calc_binomial_option_price(
#             self.valuation_date, amer_call, self.spot,
#             self.risk_free_rate, self.dividend_yield, self.volatility
#         )
        
#         # American should be worth at least as much as European
#         self.assertGreaterEqual(amer_price, euro_price - 0.01,  # Small tolerance
#                                msg="American call should be >= European call")


# class TestSwapFunctions(unittest.TestCase):
    
#     def setUp(self):
#         """Set up common test fixtures"""
#         self.effective_date = "2024-01-15"
#         self.maturity_date = "2029-01-15"
#         self.notional = 10_000_000
#         self.fixed_rate = 0.04
        
#         # Create test swap
#         self.swap = ql_create_vanilla_swap(
#             effective_date=self.effective_date,
#             maturity_date=self.maturity_date,
#             notional=self.notional,
#             fixed_rate=self.fixed_rate,
#             swap_type="payer"
#         )
        
#         # Create discount curve
#         dt = datetime.strptime(self.effective_date, "%Y-%m-%d")
#         val_date = ql.Date(dt.day, dt.month, dt.year)
#         self.discount_curve = ql.YieldTermStructureHandle(
#             ql.FlatForward(val_date, 0.045, ql.Actual365Fixed())
#         )
    
#     def test_fair_rate_gives_zero_npv(self):
#         """Test that fair rate produces zero NPV"""
#         # Calculate fair rate
#         fair_rate = ql_calc_swap_fair_rate(
#             self.effective_date, self.swap, self.discount_curve
#         )
        
#         # Create new swap at fair rate
#         fair_swap = ql_create_vanilla_swap(
#             effective_date=self.effective_date,
#             maturity_date=self.maturity_date,
#             notional=self.notional,
#             fixed_rate=fair_rate,
#             swap_type="payer"
#         )
        
#         # Calculate NPV
#         npv = ql_calc_swap_npv(
#             self.effective_date, fair_swap, self.discount_curve
#         )
        
#         # NPV should be essentially zero
#         self.assertAlmostEqual(npv, 0.0, places=2,
#                               msg="Swap at fair rate should have zero NPV")
    
#     def test_payer_receiver_symmetry(self):
#         """Test that payer and receiver swaps have opposite values"""
#         # Payer swap
#         payer = ql_create_vanilla_swap(
#             self.effective_date, self.maturity_date,
#             self.notional, self.fixed_rate, swap_type="payer"
#         )
#         payer_npv = ql_calc_swap_npv(
#             self.effective_date, payer, self.discount_curve
#         )
        
#         # Receiver swap
#         receiver = ql_create_vanilla_swap(
#             self.effective_date, self.maturity_date,
#             self.notional, self.fixed_rate, swap_type="receiver"
#         )
#         receiver_npv = ql_calc_swap_npv(
#             self.effective_date, receiver, self.discount_curve
#         )
        
#         # Should be opposite signs and equal magnitude
#         self.assertAlmostEqual(payer_npv, -receiver_npv, places=2,
#                               msg="Payer and receiver NPVs should be opposites")
    
#     def test_swap_legs_count(self):
#         """Test that swap has correct number of cashflows"""
#         legs = ql_extract_swap_legs(
#             self.effective_date, self.swap, self.discount_curve
#         )
        
#         # 5-year swap with semi-annual fixed = 10 payments
#         self.assertEqual(len(legs['fixed_leg']), 10,
#                         msg="5-year semi-annual swap should have 10 fixed payments")
        
#         # 5-year swap with quarterly floating = 20 payments
#         self.assertEqual(len(legs['floating_leg']), 20,
#                         msg="5-year quarterly swap should have 20 floating payments")


# class TestCDSFunctions(unittest.TestCase):
    
#     def setUp(self):
#         """Set up common test fixtures"""
#         self.effective_date = "2024-01-15"
#         self.maturity_date = "2029-01-15"
#         self.notional = 10_000_000
#         self.spread = 0.0150  # 150 bps
#         self.recovery_rate = 0.40
        
#         # Create test CDS
#         self.cds = ql_create_cds(
#             effective_date=self.effective_date,
#             maturity_date=self.maturity_date,
#             notional=self.notional,
#             spread=self.spread,
#             recovery_rate=self.recovery_rate
#         )
        
#         # Create curves
#         dt = datetime.strptime(self.effective_date, "%Y-%m-%d")
#         val_date = ql.Date(dt.day, dt.month, dt.year)
        
#         self.discount_curve = ql.YieldTermStructureHandle(
#             ql.FlatForward(val_date, 0.05, ql.Actual365Fixed())
#         )
        
#         self.default_curve = ql.DefaultProbabilityTermStructureHandle(
#             ql.FlatHazardRate(val_date, 0.01, ql.Actual365Fixed())
#         )
    
#     def test_fair_spread_gives_zero_npv(self):
#         """Test that fair spread produces zero NPV"""
#         # Calculate fair spread
#         fair_spread = ql_calc_cds_spread(
#             self.effective_date, self.cds,
#             self.discount_curve, self.default_curve,
#             self.recovery_rate
#         )
        
#         # Create new CDS at fair spread
#         fair_cds = ql_create_cds(
#             self.effective_date, self.maturity_date,
#             self.notional, fair_spread, self.recovery_rate
#         )
        
#         # Calculate NPV
#         npv = ql_calc_cds_npv(
#             self.effective_date, fair_cds,
#             self.discount_curve, self.default_curve,
#             self.recovery_rate
#         )
        
#         # NPV should be essentially zero
#         self.assertAlmostEqual(npv, 0.0, places=0,
#                               msg="CDS at fair spread should have zero NPV")
    
#     def test_spread_positive(self):
#         """Test that CDS spread is positive"""
#         spread = ql_calc_cds_spread(
#             self.effective_date, self.cds,
#             self.discount_curve, self.default_curve,
#             self.recovery_rate
#         )
        
#         self.assertGreater(spread, 0, "CDS spread should be positive")
    
#     def test_higher_hazard_rate_higher_spread(self):
#         """Test that higher default probability leads to higher spread"""
#         # Low hazard rate
#         low_hazard = ql.DefaultProbabilityTermStructureHandle(
#             ql.FlatHazardRate(
#                 ql.Date(15, 1, 2024), 0.005, ql.Actual365Fixed()
#             )
#         )
#         spread_low = ql_calc_cds_spread(
#             self.effective_date, self.cds,
#             self.discount_curve, low_hazard, self.recovery_rate
#         )
        
#         # High hazard rate
#         high_hazard = ql.DefaultProbabilityTermStructureHandle(
#             ql.FlatHazardRate(
#                 ql.Date(15, 1, 2024), 0.020, ql.Actual365Fixed()
#             )
#         )
#         spread_high = ql_calc_cds_spread(
#             self.effective_date, self.cds,
#             self.discount_curve, high_hazard, self.recovery_rate
#         )
        
#         self.assertGreater(spread_high, spread_low,
#                           msg="Higher default probability should lead to higher spread")


# class TestUtilityFunctions(unittest.TestCase):
    
#     def test_is_business_day_weekend(self):
#         """Test that weekends are not business days"""
#         # Saturday, January 20, 2024
#         is_bday = ql_is_business_day("2024-01-20")
#         self.assertFalse(is_bday, "Saturday should not be a business day")
        
#         # Sunday, January 21, 2024
#         is_bday = ql_is_business_day("2024-01-21")
#         self.assertFalse(is_bday, "Sunday should not be a business day")
    
#     def test_is_business_day_holiday(self):
#         """Test that Independence Day is not a business day"""
#         # July 4, 2024
#         is_bday = ql_is_business_day("2024-07-04")
#         self.assertFalse(is_bday, "Independence Day should not be a business day")
    
#     def test_is_business_day_weekday(self):
#         """Test that normal weekdays are business days"""
#         # Monday, January 15, 2024 (MLK Day - but checking normal weekday)
#         # Let's use Tuesday, January 16, 2024
#         is_bday = ql_is_business_day("2024-01-16")
#         self.assertTrue(is_bday, "Normal Tuesday should be a business day")
    
#     def test_business_days_between(self):
#         """Test business days calculation"""
#         # Monday Jan 15 to Friday Jan 19 (inclusive of start) = 5 days
#         bdays = ql_calc_business_days_between(
#             "2024-01-15", "2024-01-19",
#             include_first=True, include_last=True
#         )
#         self.assertEqual(bdays, 5, "Should be 5 business days Mon-Fri inclusive")
    
#     def test_business_days_with_weekend(self):
#         """Test business days calculation over weekend"""
#         # Friday Jan 19 to Monday Jan 22 (exclude both ends) = 0 days
#         bdays = ql_calc_business_days_between(
#             "2024-01-19", "2024-01-22",
#             include_first=False, include_last=False
#         )
#         self.assertEqual(bdays, 0, 
#                         "Should be 0 business days between Fri and Mon (exclusive)")


if __name__ == '__main__':
    unittest.main()
