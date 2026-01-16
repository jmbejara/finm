"""
Tests for the fixedincome module.
"""

import numpy as np

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

from tests import (
    ql_create_schedule,
    ql_extract_coupon_dates,
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


class TestBond