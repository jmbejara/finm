"""
Tests for the fixedincome module.
"""

import pytest
import numpy as np
from finm.fixedincome import (
    present_value,
    future_value,
    bond_price,
    yield_to_maturity,
    duration,
    modified_duration,
    convexity,
)


class TestPresentValue:
    """Tests for present_value function."""

    def test_discrete_compounding(self):
        """Test present value with discrete compounding."""
        pv = present_value(1000, 0.05, 2)
        expected = 1000 / (1.05 ** 2)
        assert np.isclose(pv, expected)

    def test_continuous_compounding(self):
        """Test present value with continuous compounding."""
        pv = present_value(1000, 0.05, 2, compounding='continuous')
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
        expected = 1000 * (1.05 ** 2)
        assert np.isclose(fv, expected)

    def test_continuous_compounding(self):
        """Test future value with continuous compounding."""
        fv = future_value(1000, 0.05, 2, compounding='continuous')
        expected = 1000 * np.exp(0.05 * 2)
        assert np.isclose(fv, expected)


class TestBondPrice:
    """Tests for bond_price function."""

    def test_par_bond(self):
        """Test that a bond priced at par has price equal to face value."""
        # When coupon rate equals YTM, bond should trade at par
        price = bond_price(1000, 0.05, 0.05, 10, frequency=2)
        assert np.isclose(price, 1000, rtol=1e-6)

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

