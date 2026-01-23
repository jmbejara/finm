"""
Tests for the fixedincome module.
"""

import numpy as np
import pandas as pd

from finm.fixedincome import (
    present_value,
    future_value,
    get_coupon_dates,
    calc_bond_cashflows,
    calc_clean_bond_price,
    calc_dirty_bond_price,
    calc_accrued_interest,
    calc_yield_to_maturity,
    calc_macaulay_duration,
    calc_modified_duration,
    calc_dollar_duration,
    calc_convexity,
    calc_zero_bond_price,
    calc_zero_bond_yield,
    calc_zero_bond_duration,
    calc_zero_bond_convexity,
    calc_zero_bond_discount_factor,
    calc_current_yield,
)

from tests.test_ql_fixedincome_functions import (
    ql_calc_present_value,
    ql_calc_future_value,
    ql_create_schedule,
    ql_get_coupon_dates,
    ql_create_fixed_rate_bond,
    ql_get_cashflows,
    ql_create_zero_coupon_bond,
    # ql_extract_coupon_dates_cashflows,
    ql_calc_clean_bond_price,
    ql_calc_dirty_bond_price,
    ql_calc_accrued_interest,
    ql_calc_yield_to_maturity,
    ql_calc_modified_duration,
    ql_calc_macaulay_duration,
    ql_calc_dollar_duration,
    ql_calc_convexity,
    ql_calc_zero_coupon_bond_price,
    ql_calc_zero_bond_yield,
    ql_calc_zero_bond_duration,
    ql_calc_zero_bond_convexity,
    ql_calc_zero_bond_discount_factor,
    ql_calc_current_yield,
)


class TestPresentValue:
    """Tests for present_value function."""

    def test_discrete_compounding(self):
        """Test present value with discrete compounding."""
        student_pv = present_value(1000, 0.05, 2)
        ql_pv = ql_calc_present_value(1000, 0.05, 2, "discrete", 1)
        assert np.isclose(student_pv, ql_pv)

    def test_continuous_compounding(self):
        """Test present value with continuous compounding."""
        student_pv = present_value(1000, 0.05, 2, compounding="continuous")
        ql_pv = ql_calc_present_value(1000, 0.05, 2, "continuous", 1)
        assert np.isclose(student_pv, ql_pv)

    def test_zero_rate(self):
        """Test present value with zero interest rate."""
        student_pv = present_value(1000, 0, 5)
        assert student_pv == 1000


class TestFutureValue:
    """Tests for future_value function."""

    def test_discrete_compounding(self):
        """Test future value with discrete compounding."""
        student_fv = future_value(1000, 0.05, 2)
        ql_fv = ql_calc_future_value(1000, 0.05, 2, "discrete", 1)
        assert np.isclose(student_fv, ql_fv)

    def test_continuous_compounding(self):
        """Test future value with continuous compounding."""
        student_fv = future_value(1000, 0.05, 2, compounding="continuous")
        ql_fv = ql_calc_future_value(1000, 0.05, 2, "continuous", 1)
        assert np.isclose(student_fv, ql_fv)


class TestCouponDates:
    """Tests for get_coupon_dates function."""

    def setup_method(self):
        """Set up QuantLib parameters."""
        # Common test parameters
        self.valuation_date = "2020-01-01"
        self.issue_date = "2020-01-01"
        self.maturity_date = "2025-01-01"
        self.frequency = 2  # Semi-annual

        # Create a standard test schedule
        self.schedule = ql_create_schedule(
            issue_date=self.issue_date,
            maturity_date=self.maturity_date,
            frequency=2,  # Semi-annual
        )

    def test_coupon_dates_count(self):
        """Test that the number of coupon dates is correct."""
        student_coupon_dates = get_coupon_dates(self.issue_date, self.maturity_date)
        ql_coupon_dates = ql_get_coupon_dates(self.schedule)

        assert len(student_coupon_dates) == len(
            ql_coupon_dates
        ), f"Expected {len(ql_coupon_dates)} dates, got {len(student_coupon_dates)}"

    def test_coupon_dates_values(self):
        """Test that coupon dates match within ±3 days."""
        from datetime import datetime, timedelta

        student_coupon_dates = get_coupon_dates(self.issue_date, self.maturity_date)
        ql_coupon_dates = ql_get_coupon_dates(self.schedule)

        for i, (student_date, ql_date) in enumerate(
            zip(student_coupon_dates, ql_coupon_dates)
        ):
            # Convert both to datetime for comparison
            student_dt = datetime.strptime(student_date, "%Y-%m-%d")
            ql_dt = datetime.strptime(ql_date, "%Y-%m-%d")

            # Calculate difference in days
            diff_days = abs((student_dt - ql_dt).days)

            assert (
                diff_days <= 3
            ), f"Date mismatch at index {i}: {student_date} vs {ql_date} ({diff_days} days apart, max 3 allowed)"


class TestBondFunctions:
    """Tests for bond pricing and related functions."""

    def setup_method(self):
        """Set up QuantLib parameters."""
        # Common test parameters
        self.valuation_date = "2020-01-15"
        self.issue_date = "2020-01-01"
        self.maturity_date = "2025-01-01"
        self.frequency = 2  # Semi-annual
        self.face_value = 100.0
        self.coupon_rate = 0.05
        self.ytm = 0.045

        # Create a standard test schedule
        self.schedule = ql_create_schedule(
            issue_date=self.issue_date,
            maturity_date=self.maturity_date,
            frequency=2,  # Semi-annual
        )

        # Create a fixed rate bond
        self.fixed_bond = ql_create_fixed_rate_bond(
            schedule=self.schedule,
            face_value=self.face_value,
            coupon_rate=self.coupon_rate,
        )

        # Create a zero coupon bond
        self.zero_bond = ql_create_zero_coupon_bond(
            issue_date=self.issue_date,
            maturity_date=self.maturity_date,
            face_value=self.face_value,
        )

    def test_calc_fixed_bond_cashflows(self):
        """Test that cashflows are calculated correctly."""

        # Get cashflows from student function
        student_cashflows = calc_bond_cashflows(
            issue_date=self.issue_date,
            maturity_date=self.maturity_date,
            face_value=self.face_value,
            coupon_rate=self.coupon_rate,
        )

        # Get cashflows from QuantLib function
        ql_cashflows = ql_get_cashflows(self.fixed_bond)

        # Test 1: Check that result is a pandas Series
        assert isinstance(
            student_cashflows, pd.Series
        ), "Cashflows should be returned as a pandas Series"

        # Test 2: Check length matches
        assert len(student_cashflows) == len(
            ql_cashflows
        ), f"Expected {len(ql_cashflows)} cashflows, got {len(student_cashflows)}"

        # Test 3: Check each cashflow amount matches (within tolerance)
        tolerance = 0.1  # 10 cents tolerance
        for i, (student_cf, ql_cf) in enumerate(zip(student_cashflows, ql_cashflows)):
            diff = abs(student_cf - ql_cf)
            assert diff < tolerance, (
                f"Cashflow mismatch at index {i}: student={student_cf:.4f}, "
                f"ql={ql_cf:.4f}, diff={diff:.4f}"
            )

        # Test 4: Verify coupon amounts
        expected_coupon = self.face_value * self.coupon_rate / self.frequency
        for i in range(len(student_cashflows) - 1):
            assert abs(student_cashflows.iloc[i] - expected_coupon) < tolerance, (
                f"Coupon at index {i} should be {expected_coupon:.2f}, "
                f"got {student_cashflows.iloc[i]:.2f}"
            )

        # Test 5: Verify final cashflow includes principal
        expected_final = self.face_value
        assert abs(student_cashflows.iloc[-1] - expected_final) < tolerance, (
            f"Final cashflow should be {expected_final:.2f}, "
            f"got {student_cashflows.iloc[-1]:.2f}"
        )

    def test_calc_clean_bond_price(self):
        """Test that clean bond price is calculated correctly."""

        # Calculate number of periods remaining
        # 5-year bond with semi-annual payments = 10 periods
        periods = 10

        # Calculate price using student function
        student_price = calc_clean_bond_price(
            face_value=self.face_value,
            coupon_rate=self.coupon_rate,
            ytm=self.ytm,
            periods=periods,
            frequency=self.frequency,
        )

        # Calculate price using QuantLib function
        ql_price = ql_calc_clean_bond_price(
            valuation_date=self.valuation_date,
            ytm=self.ytm,
            bond=self.fixed_bond,
        )

        # Test: Check that prices match within tolerance
        tolerance = 0.1  # 10 cents tolerance
        diff = abs(student_price - ql_price)

        assert (
            diff < tolerance
        ), f"Price mismatch: student={student_price:.4f}, ql={ql_price:.4f}, diff={diff:.4f}"

        # Additional sanity checks
        assert student_price > 0, "Bond price should be positive"

    def test_calc_clean_bond_price_at_par(self):
        """Test bond price when YTM equals coupon rate (should be par)."""

        # Calculate number of periods remaining
        # 5-year bond with semi-annual payments = 10 periods
        periods = 10
        ytm_at_par = self.coupon_rate  # YTM = coupon rate

        # Calculate price using student function
        student_price = calc_clean_bond_price(
            face_value=self.face_value,
            coupon_rate=self.coupon_rate,
            ytm=ytm_at_par,
            periods=periods,
            frequency=self.frequency,
        )

        # When YTM = coupon rate, price should equal face value
        assert (
            abs(student_price - self.face_value) < 0.01
        ), f"Bond should trade at par, got {student_price:.2f}"

    def test_calc_dirty_bond_price(self):
        """Test that dirty bond price is calculated correctly."""

        # Calculate number of periods remaining
        # 5-year bond with semi-annual payments = 10 periods
        periods = 10

        # For a bond issued on 2020-01-01, the first coupon is on 2020-07-01
        last_coupon_date = self.issue_date  # "2020-01-01"
        next_coupon_date = "2020-07-01"

        # Calculate clean price
        ql_clean_price = ql_calc_clean_bond_price(
            valuation_date=self.valuation_date,
            ytm=self.ytm,
            bond=self.fixed_bond,
        )

        # Calculate accrued interest with QuantLib function
        ql_accrued = ql_calc_accrued_interest(
            valuation_date=self.valuation_date,
            bond=self.fixed_bond,
        )

        # Calculate dirty price using student function
        student_price = calc_dirty_bond_price(
            clean_price=ql_clean_price,
            accrued_interest=ql_accrued,
        )

        # Calculate dirty price using QuantLib function
        ql_price = ql_calc_dirty_bond_price(
            valuation_date=self.valuation_date,
            ytm=self.ytm,
            bond=self.fixed_bond,
        )

        # Test: Check that prices match within tolerance
        tolerance = 0.1  # 10 cents tolerance
        diff = abs(student_price - ql_price)

        assert (
            diff < tolerance
        ), f"Price mismatch: student={student_price:.4f}, ql={ql_price:.4f}, diff={diff:.4f}"

        # Additional sanity checks
        assert student_price > 0, "Bond price should be positive"

    def test_calc_accrued_interest(self):
        """Test that accrued interest is calculated correctly."""

        # For a bond issued on 2020-01-01, the first coupon is on 2020-07-01
        last_coupon_date = self.issue_date  # "2020-01-01"
        next_coupon_date = "2020-07-01"

        # Calculate accrued interest using student function
        student_accrued = calc_accrued_interest(
            last_coupon_date=last_coupon_date,
            next_coupon_date=next_coupon_date,
            valuation_date=self.valuation_date,
            face_value=self.face_value,
            coupon_rate=self.coupon_rate,
            frequency=self.frequency,
        )

        # Calculate accrued interest using QuantLib function
        ql_accrued = ql_calc_accrued_interest(
            valuation_date=self.valuation_date, bond=self.fixed_bond
        )

        # Test: Check that accrued interest matches within tolerance
        tolerance = 0.05  # 5 cents tolerance
        diff = abs(student_accrued - ql_accrued)

        assert diff < tolerance, (
            f"Accrued interest mismatch: student={student_accrued:.4f}, "
            f"ql={ql_accrued:.4f}, diff={diff:.4f}"
        )

        # Additional sanity checks
        assert student_accrued >= 0, "Accrued interest should be non-negative"

    def test_calc_yield_to_maturity(self):
        """Test that yield to maturity is calculated correctly."""

        # First, calculate the clean price at a known YTM
        periods = 10
        known_ytm = self.ytm  # 0.045

        # Calc the clean price with the QuantLib function
        ql_clean_price = ql_calc_clean_bond_price(
            valuation_date=self.valuation_date,
            ytm=known_ytm,
            bond=self.fixed_bond,
        )

        print(ql_clean_price)

        # Now calculate YTM from that clean price (should recover the original YTM)
        student_ytm = calc_yield_to_maturity(
            clean_price=ql_clean_price,
            face_value=self.face_value,
            coupon_rate=self.coupon_rate,
            periods=periods,
            frequency=self.frequency,
        )

        # Get QuantLib YTM for comparison
        ql_ytm = ql_calc_yield_to_maturity(
            valuation_date=self.valuation_date,
            clean_price=ql_clean_price,
            bond=self.fixed_bond,
        )

        # Test: Check that YTMs match within tolerance
        tolerance = 0.0001  # 1 basis point
        diff = abs(student_ytm - ql_ytm)

        assert (
            diff < tolerance
        ), f"YTM mismatch: student={student_ytm:.6f}, ql={ql_ytm:.6f}, diff={diff:.6f}"

        # Should also recover the original known YTM
        assert (
            abs(student_ytm - known_ytm) < tolerance
        ), f"Should recover original YTM: student={student_ytm:.6f}, original={known_ytm:.6f}"

        # Additional sanity checks
        assert student_ytm > 0, "YTM should be positive"
        assert student_ytm < 1, "YTM should be less than 100%"

    def test_calc_macaulay_duration(self):
        """Test that Macaulay duration is calculated correctly."""

        periods = 10

        # Calculate Macaulay duration using student function
        student_duration = calc_macaulay_duration(
            face_value=self.face_value,
            coupon_rate=self.coupon_rate,
            ytm=self.ytm,
            periods=periods,
            frequency=self.frequency,
        )

        # Calculate Macaulay duration using QuantLib function
        ql_duration = ql_calc_macaulay_duration(
            valuation_date=self.valuation_date, ytm=self.ytm, bond=self.fixed_bond
        )

        # Test: Check that durations match within tolerance
        tolerance = 0.1  # 10 cents tolerance for duration in years
        diff = abs(student_duration - ql_duration)

        assert (
            diff < tolerance
        ), f"Duration mismatch: student={student_duration:.4f}, ql={ql_duration:.4f}, diff={diff:.4f}"

        # Additional sanity checks
        assert student_duration > 0, "Duration should be positive"

        # Duration should be less than time to maturity
        time_to_maturity = periods / self.frequency  # 10 periods / 2 = 5 years
        assert (
            student_duration < time_to_maturity
        ), f"Duration ({student_duration:.2f}) should be less than time to maturity ({time_to_maturity:.2f})"

    def test_calc_modified_duration(self):
        """Test that modified duration is calculated correctly."""

        periods = 10

        # Calculate modified duration using student function
        student_duration = calc_modified_duration(
            face_value=self.face_value,
            coupon_rate=self.coupon_rate,
            ytm=self.ytm,
            periods=periods,
            frequency=self.frequency,
        )

        # Calculate modified duration using QuantLib function
        ql_duration = ql_calc_modified_duration(
            valuation_date=self.valuation_date, ytm=self.ytm, bond=self.fixed_bond
        )

        # Test: Check that durations match within tolerance
        tolerance = 0.1  # 10 cents tolerance for duration in years
        diff = abs(student_duration - ql_duration)

        assert (
            diff < tolerance
        ), f"Duration mismatch: student={student_duration:.4f}, ql={ql_duration:.4f}, diff={diff:.4f}"

        # Additional sanity checks
        assert student_duration > 0, "Modified duration should be positive"


    def test_calc_dollar_duration(self):
        """Test that dollar duration (DV01) is calculated correctly."""

        periods = 10

        # Calculate dollar duration using student function
        student_dv01 = calc_dollar_duration(
            face_value=self.face_value,
            coupon_rate=self.coupon_rate,
            ytm=self.ytm,
            periods=periods,
            frequency=self.frequency,
        )

        # Calculate dollar duration using QuantLib function
        ql_dv01 = ql_calc_dollar_duration(
            valuation_date=self.valuation_date,
            ytm=self.ytm,
            bond=self.fixed_bond,
            face_value=self.face_value,
        )

        # Test: Check that dollar durations match within tolerance
        tolerance = 0.01  # 1 cent tolerance
        diff = abs(student_dv01 - ql_dv01)

        assert (
            diff < tolerance
        ), f"Dollar duration mismatch: student={student_dv01:.4f}, ql={ql_dv01:.4f}, diff={diff:.4f}"

        # Additional sanity checks
        assert student_dv01 > 0, "Dollar duration should be positive"
    
    def test_calc_convexity(self):
        """Test that convexity is calculated correctly."""

        periods = 10

        # Calculate convexity using student function
        student_convexity = calc_convexity(
            face_value=self.face_value,
            coupon_rate=self.coupon_rate,
            ytm=self.ytm,
            periods=periods,
            frequency=self.frequency,
        )

        # Calculate convexity using QuantLib function
        ql_convexity = ql_calc_convexity(
            valuation_date=self.valuation_date, 
            ytm=self.ytm, 
            bond=self.fixed_bond,
        )

        # Test: Check that convexities match within tolerance
        tolerance = 0.5  # Tolerance for convexity
        diff = abs(student_convexity - ql_convexity)

        assert (
            diff < tolerance
        ), f"Convexity mismatch: student={student_convexity:.4f}, ql={ql_convexity:.4f}, diff={diff:.4f}"

        # Additional sanity checks
        assert (
            student_convexity > 0
        ), "Convexity should be positive for option-free bonds"

    def test_calc_zero_bond_price(self):
        """Test that zero coupon bond price is calculated correctly."""

        # Calculate zero bond price using student function
        student_price = calc_zero_bond_price(
            face_value=self.face_value,
            ytm=self.ytm,
            years_to_maturity=5,  # 2025 - 2020
            frequency=self.frequency,
        )

        # Calculate zero bond price using QuantLib function
        ql_price = ql_calc_zero_coupon_bond_price(
            valuation_date=self.valuation_date, ytm=self.ytm, bond=self.zero_bond
        )

        # Test: Check that prices match within tolerance
        tolerance = 0.50  # 50 cents tolerance
        diff = abs(student_price - ql_price)

        assert (
            diff < tolerance
        ), f"Price mismatch: student={student_price:.4f}, ql={ql_price:.4f}, diff={diff:.4f}"

        # Additional sanity checks
        assert student_price > 0, "Zero bond price should be positive"
        assert (
            student_price < self.face_value
        ), f"Zero bond should trade at discount: price={student_price:.2f}, face={self.face_value:.2f}"

    def test_calc_zero_bond_yield(self):
        """Test that zero coupon bond yield is calculated correctly."""
        
        # First, calculate a price at a known yield
        known_yield = self.ytm  # 0.045
        
        # Get price from QuantLib
        ql_price = ql_calc_zero_coupon_bond_price(
            valuation_date=self.valuation_date,
            ytm=known_yield,
            bond=self.zero_bond
        )
        
        # Now calculate yield from that price using QuantLib function
        ql_yield = ql_calc_zero_bond_yield(
            valuation_date=self.valuation_date,
            price=ql_price,
            bond=self.zero_bond,
            frequency=self.frequency
        )
        
        # Calculate yield using student function
        student_yield = calc_zero_bond_yield(
            face_value=self.face_value,
            price=ql_price,
            years_to_maturity=5,  # 2025 - 2020
            frequency=self.frequency
        )
        
        # Test: Check that yields match within tolerance
        tolerance = 0.001  # 10 basis points tolerance
        diff = abs(student_yield - ql_yield)
        
        assert diff < tolerance, \
            f"Yield mismatch: student={student_yield:.4f}, ql={ql_yield:.4f}, diff={diff:.4f}"
        
        # Should recover the original known yield
        assert abs(student_yield - known_yield) < tolerance, \
            f"Should recover original yield: student={student_yield:.4f}, original={known_yield:.4f}"
        
        # Additional sanity checks
        assert student_yield > 0, "Yield should be positive"
        assert student_yield < 1, "Yield should be less than 100%"
        
        # Test round-trip: price -> yield -> price
        recovered_price = calc_zero_bond_price(
            face_value=self.face_value,
            ytm=student_yield,
            years_to_maturity=5,
            frequency=self.frequency
        )
        assert abs(recovered_price - ql_price) < 0.01, \
            "Round-trip conversion should recover original price"

    def test_calc_zero_bond_duration(self):
        """Test that zero coupon bond duration is calculated correctly."""
        
        # Calculate duration using QuantLib function
        ql_duration = ql_calc_zero_bond_duration(
            valuation_date=self.issue_date,
            bond=self.zero_bond
        )
        
        # Calculate duration using student function
        student_duration = calc_zero_bond_duration(
            issue_date=self.issue_date,
            maturity_date=self.maturity_date
        )
        
        # Test: Check that durations match
        tolerance = 0.1  # 10 cents tolerance
        diff = abs(student_duration - ql_duration)
        
        assert diff < tolerance, \
            f"Duration mismatch: student={student_duration:.4f}, ql={ql_duration:.4f}, diff={diff:.4f}"
        
        # Sanity checks
        assert student_duration > 0, "Duration should be positive"
        
        # For zero coupon bonds, duration should approximately equal time to maturity
        assert abs(student_duration - 5.0) < 0.1, \
            f"Zero bond duration should be close to 5 years, got {student_duration:.2f}"
        
        # Zero bond duration should be greater than coupon bond duration
        coupon_bond_duration = ql_calc_macaulay_duration(
            valuation_date=self.valuation_date,
            ytm=self.ytm,
            bond=self.fixed_bond  # Regular coupon bond from setup
        )
        
        assert student_duration > coupon_bond_duration, \
            f"Zero bond duration ({student_duration:.2f}) should be greater than " \
            f"coupon bond duration ({coupon_bond_duration:.2f})"
        
        # Test that duration equals time to maturity (key property of zero bonds)
        expected_duration = 5.0
        assert abs(student_duration - expected_duration) < tolerance, \
            "For zero coupon bonds, duration should equal time to maturity"

    def test_calc_zero_bond_convexity(self):
        """Test that zero coupon bond convexity is calculated correctly."""
        
        # Calculate convexity using QuantLib function
        ql_convexity = ql_calc_zero_bond_convexity(
            valuation_date=self.valuation_date,
            ytm=self.ytm,
            bond=self.zero_bond,
        )
        
        # Calculate convexity using student function
        student_convexity = calc_zero_bond_convexity(
            years_to_maturity=5.0,  # 2025 - 2020
            ytm=self.ytm,
            frequency=self.frequency
        )
        
        # Test: Check that convexities match
        tolerance = 0.5
        diff = abs(student_convexity - ql_convexity)
        
        assert diff < tolerance, \
            f"Convexity mismatch: student={student_convexity:.4f}, ql={ql_convexity:.4f}, diff={diff:.4f}"
        
        # Sanity checks
        assert student_convexity > 0, "Convexity should be positive"
        
        # Zero bond convexity should be greater than coupon bond convexity
        coupon_bond_convexity = ql_calc_convexity(
            valuation_date=self.valuation_date,
            ytm=self.ytm,
            bond=self.fixed_bond  # Regular coupon bond from setup
        )
        
        assert student_convexity > coupon_bond_convexity, \
            f"Zero bond convexity ({student_convexity:.2f}) should be greater than " \
            f"coupon bond convexity ({coupon_bond_convexity:.2f})"
        
        # Longer maturity should mean higher convexity
        longer_convexity = calc_zero_bond_convexity(
            years_to_maturity=10.0,
            ytm=self.ytm,
            frequency=self.frequency
        )
        
        assert longer_convexity > student_convexity, \
            "Longer maturity zero should have higher convexity"
        
        # For zeros, convexity ≈ duration² / (1+y)²
        # Rough approximation check
        duration = 5.0  # years to maturity
        approx_convexity = (duration ** 2) / ((1 + self.ytm / self.frequency) ** 2)
        
        # Should be in the same ballpark (within 50%)
        assert abs(student_convexity - approx_convexity) / approx_convexity < 0.5, \
            f"Convexity should be approximately duration² / (1+y)²"

    def test_calc_discount_factor(self):
        """Test that discount factor from zero bond price is calculated correctly."""
        
        # Calculate discount factor using QuantLib function
        ql_df = ql_calc_zero_bond_discount_factor(
            valuation_date=self.valuation_date,
            ytm=self.ytm,
            bond=self.zero_bond
        )
        
        # Calculate the zero bond price for student function
        zero_price = ql_calc_zero_coupon_bond_price(
            valuation_date=self.valuation_date,
            ytm=self.ytm,
            bond=self.zero_bond
        )
        
        # Calculate discount factor using student function
        student_df = calc_zero_bond_discount_factor(
            zero_price=zero_price,
            face_value=self.face_value
        )
        
        # Test: Check that discount factors match
        tolerance = 0.01
        diff = abs(student_df - ql_df)
        
        assert diff < tolerance, \
            f"Discount factor mismatch: student={student_df:.6f}, ql={ql_df:.6f}, diff={diff:.6f}"
        
        # Sanity checks
        assert 0 < student_df < 1, \
            f"Discount factor should be between 0 and 1, got {student_df:.4f}"

    def test_calc_current_yield(self):
        """Test that current yield is calculated correctly."""
        
        # Calc current price from QuantLib function
        ql_current_price = ql_calc_clean_bond_price(
            valuation_date=self.valuation_date,
            ytm=self.ytm,
            bond=self.fixed_bond,
        )
        
        # Calculate current yield using student function
        student_cy = calc_current_yield(
            face_value=self.face_value,
            coupon_rate=self.coupon_rate,
            current_price=ql_current_price
        )
        
        # Calculate current yield using QuantLib function
        ql_cy = ql_calc_current_yield(
            valuation_date=self.valuation_date,
            ytm=self.ytm,
            coupon_rate=self.coupon_rate,
            bond=self.fixed_bond,
        )
        
        # Test: Check that current yields match
        tolerance = 0.0001
        diff = abs(student_cy - ql_cy)
        
        assert diff < tolerance, \
            f"Current yield mismatch: student={student_cy:.4f}, ql={ql_cy:.4f}, diff={diff:.4f}"


