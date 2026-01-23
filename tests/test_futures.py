"""
Tests for the futures module.
"""

import numpy as np
import pandas as pd

from datetime import datetime

from finm.futures import (
    calc_futures_implied_rate,
    calc_futures_price_from_rate,
    calc_futures_pnl,
)

# from tests.test_ql_futures_functions import (
    
# )

class TestEurodollarFutures:
    """Tests for Eurodollar futures functions."""
    
    def setup_method(self):
        """Set up parameters for Eurodollar futures tests."""
        # Common test parameters
        self.futures_price = 95.00  # Implies 5% rate
        self.implied_rate = 0.05  # 5%
        self.forward_rate = 0.0505  # 5.05% (slightly different due to convexity)
        self.contract_size = 1_000_000
        self.days_in_period = 90  # 3-month contract


    def test_calc_futures_implied_rate(self):
        """Test conversion from futures price to implied rate."""
        
        # Calculate implied rate using student function
        student_rate = calc_futures_implied_rate(
            futures_price=self.futures_price
        )
        
        # Expected rate: 100 - 95.00 = 5.00%
        expected_rate = (100 - self.futures_price) / 100
        
        # Test: Check that rates match
        tolerance = 0.0001  # 1 basis point
        diff = abs(student_rate - expected_rate)
        
        assert diff < tolerance, \
            f"Implied rate mismatch: student={student_rate:.4f}, expected={expected_rate:.4f}"
        
        # Sanity checks
        assert student_rate > 0, "Implied rate should be positive"
        assert student_rate < 1, "Implied rate should be less than 100%"
        
        # Test with different prices
        assert calc_futures_implied_rate(100.00) == 0.0, "Price of 100 should imply 0% rate"
        assert abs(calc_futures_implied_rate(97.50) - 0.025) < tolerance, "Price of 97.50 should imply 2.5%"

    def test_calc_futures_price_from_rate(self):
        """Test conversion from implied rate to futures price."""
        
        # Calculate futures price using student function
        student_price = calc_futures_price_from_rate(
            implied_rate=self.implied_rate
        )
        
        # Expected price: 100 - 5.00 = 95.00
        expected_price = 100 - (self.implied_rate * 100)
        
        # Test: Check that prices match
        tolerance = 0.01
        diff = abs(student_price - expected_price)
        
        assert diff < tolerance, \
            f"Futures price mismatch: student={student_price:.2f}, expected={expected_price:.2f}"
        
        # Sanity checks
        assert student_price > 0, "Futures price should be positive"
        assert student_price <= 100, "Futures price should be <= 100"
        
        # Test round-trip
        rate = calc_futures_implied_rate(student_price)
        assert abs(rate - self.implied_rate) < 0.0001, "Round-trip conversion should recover original rate"

    def test_calc_futures_pnl(self):
        """Test profit/loss calculation for Eurodollar futures."""
        
        # Long position: bought at 95.00, sold at 95.50
        initial_price = 95.00
        final_price = 95.50
        num_contracts = 10
        
        student_pnl = calc_futures_pnl(
            initial_price=initial_price,
            final_price=final_price,
            num_contracts=num_contracts,
            position_type="long"
        )
        
        # Each basis point = $25 per contract
        # Price change = 50 basis points = 0.50
        # PnL = 50 bp × $25 × 10 contracts = $12,500
        expected_pnl = (final_price - initial_price) * 100 * 25 * num_contracts
        
        tolerance = 0.01
        diff = abs(student_pnl - expected_pnl)
        
        assert diff < tolerance, \
            f"PnL mismatch: student=${student_pnl:.2f}, expected=${expected_pnl:.2f}"
        
        # Long position should profit when price rises
        assert student_pnl > 0, "Long position should profit when futures price rises"
        
        # Test short position (should be opposite)
        student_pnl_short = calc_futures_pnl(
            initial_price=initial_price,
            final_price=final_price,
            num_contracts=num_contracts,
            position_type="short"
        )
        
        assert abs(student_pnl_short + student_pnl) < tolerance, \
            "Short and long PnL should be opposite"