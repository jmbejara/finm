"""Tests for the analytics module."""

import numpy as np
import pandas as pd
import pytest

from finm.analytics import (
    calculate_beta,
    calculate_factor_exposures,
    calculate_sharpe_ratio,
)


class TestCalculateBeta:
    """Tests for calculate_beta function."""

    def test_beta_of_market_is_one(self):
        """Market beta with itself should be 1."""
        market_returns = pd.Series([0.01, -0.02, 0.015, -0.005, 0.03])
        beta = calculate_beta(market_returns, market_returns)
        assert np.isclose(beta, 1.0, rtol=1e-6)

    def test_beta_uncorrelated_is_near_zero(self):
        """Uncorrelated returns should have beta near zero."""
        np.random.seed(42)
        returns_a = pd.Series(np.random.randn(1000))
        returns_b = pd.Series(np.random.randn(1000))
        beta = calculate_beta(returns_a, returns_b)
        assert abs(beta) < 0.1  # Should be close to zero

    def test_beta_positive_correlation(self):
        """Positively correlated returns should have positive beta."""
        factor = pd.Series([0.01, 0.02, -0.01, 0.03, -0.02])
        returns = factor * 1.5 + 0.001  # returns = 1.5 * factor + noise
        beta = calculate_beta(returns, factor)
        assert beta > 1.0

    def test_beta_scaled_returns(self):
        """Beta of 2x factor should be approximately 2."""
        factor = pd.Series([0.01, 0.02, -0.01, 0.03, -0.02, 0.015, -0.025])
        returns = factor * 2.0
        beta = calculate_beta(returns, factor)
        assert np.isclose(beta, 2.0, rtol=1e-6)


class TestCalculateSharpeRatio:
    """Tests for calculate_sharpe_ratio function."""

    def test_sharpe_positive_excess_returns(self):
        """Positive excess returns should give positive Sharpe."""
        returns = pd.Series([0.01, 0.02, 0.015, 0.025, 0.01])
        rf = 0.0001
        sharpe = calculate_sharpe_ratio(returns, rf)
        assert sharpe > 0

    def test_sharpe_with_series_rf(self):
        """Should work with Series risk-free rate."""
        returns = pd.Series([0.01, 0.02, 0.015, 0.025, 0.01])
        rf = pd.Series([0.0001, 0.0001, 0.0001, 0.0001, 0.0001])
        sharpe = calculate_sharpe_ratio(returns, rf)
        assert sharpe > 0

    def test_sharpe_annualization(self):
        """Monthly annualization should differ from daily."""
        returns = pd.Series([0.01, 0.02, 0.015, 0.025, 0.01])
        rf = 0.0001
        sharpe_daily = calculate_sharpe_ratio(returns, rf, annualization_factor=252)
        sharpe_monthly = calculate_sharpe_ratio(returns, rf, annualization_factor=12)
        assert sharpe_daily > sharpe_monthly  # sqrt(252) > sqrt(12)

    def test_sharpe_no_annualization(self):
        """Sharpe with annualization_factor=1 should give raw ratio."""
        returns = pd.Series([0.01, 0.02, 0.015, 0.025, 0.01])
        rf = 0.0
        sharpe = calculate_sharpe_ratio(returns, rf, annualization_factor=1)
        # np.std uses ddof=0 by default, so we match that
        expected = returns.mean() / np.std(returns)
        assert np.isclose(sharpe, expected, rtol=1e-6)


class TestCalculateFactorExposures:
    """Tests for calculate_factor_exposures function."""

    def test_returns_all_keys(self):
        """Should return all expected statistics."""
        dates = pd.date_range("2020-01-01", periods=100, freq="D")
        np.random.seed(42)
        returns = pd.Series(np.random.randn(100) * 0.01, index=dates)
        factors = pd.DataFrame(
            {
                "Mkt-RF": np.random.randn(100) * 0.01,
                "SMB": np.random.randn(100) * 0.005,
                "HML": np.random.randn(100) * 0.005,
                "RF": np.full(100, 0.0001),
            },
            index=dates,
        )

        exposures = calculate_factor_exposures(returns, factors)

        assert "average_return" in exposures
        assert "volatility" in exposures
        assert "sharpe_ratio" in exposures
        assert "market_beta" in exposures
        assert "smb_beta" in exposures
        assert "hml_beta" in exposures

    def test_values_are_floats(self):
        """All returned values should be floats."""
        dates = pd.date_range("2020-01-01", periods=100, freq="D")
        np.random.seed(42)
        returns = pd.Series(np.random.randn(100) * 0.01, index=dates)
        factors = pd.DataFrame(
            {
                "Mkt-RF": np.random.randn(100) * 0.01,
                "SMB": np.random.randn(100) * 0.005,
                "HML": np.random.randn(100) * 0.005,
                "RF": np.full(100, 0.0001),
            },
            index=dates,
        )

        exposures = calculate_factor_exposures(returns, factors)

        for key, value in exposures.items():
            assert isinstance(value, float), f"{key} is not a float"

    def test_annualized_values(self):
        """Values should be annualized correctly."""
        dates = pd.date_range("2020-01-01", periods=100, freq="D")
        np.random.seed(42)
        # Use positive mean returns for clearer test
        returns = pd.Series(np.random.randn(100) * 0.01 + 0.001, index=dates)
        factors = pd.DataFrame(
            {
                "Mkt-RF": np.random.randn(100) * 0.01,
                "SMB": np.random.randn(100) * 0.005,
                "HML": np.random.randn(100) * 0.005,
                "RF": np.full(100, 0.0001),
            },
            index=dates,
        )

        exposures_daily = calculate_factor_exposures(
            returns, factors, annualization_factor=252
        )
        exposures_monthly = calculate_factor_exposures(
            returns, factors, annualization_factor=12
        )

        # Annualized volatility scales with sqrt of factor
        # So daily (252) should have higher annualized vol than monthly (12)
        assert exposures_daily["volatility"] > exposures_monthly["volatility"]

    def test_handles_misaligned_dates(self):
        """Should handle returns and factors with different dates."""
        dates_returns = pd.date_range("2020-01-01", periods=100, freq="D")
        dates_factors = pd.date_range("2020-01-15", periods=120, freq="D")

        np.random.seed(42)
        returns = pd.Series(np.random.randn(100) * 0.01, index=dates_returns)
        factors = pd.DataFrame(
            {
                "Mkt-RF": np.random.randn(120) * 0.01,
                "SMB": np.random.randn(120) * 0.005,
                "HML": np.random.randn(120) * 0.005,
                "RF": np.full(120, 0.0001),
            },
            index=dates_factors,
        )

        # Should not raise and should return valid results
        exposures = calculate_factor_exposures(returns, factors)
        assert all(
            key in exposures
            for key in [
                "average_return",
                "volatility",
                "sharpe_ratio",
                "market_beta",
                "smb_beta",
                "hml_beta",
            ]
        )
