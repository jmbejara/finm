"""Tests for the analytics module."""

import numpy as np
import pandas as pd

from finm.analytics import (
    RegressionResult,
    calculate_beta,
    calculate_factor_exposures,
    calculate_sharpe_ratio,
    run_capm_regression,
    run_factor_regression,
    run_fama_french_regression,
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


class TestRunFactorRegression:
    """Tests for run_factor_regression and related functions."""

    def test_returns_regression_result(self):
        """Should return a RegressionResult dataclass."""
        dates = pd.date_range("2020-01-01", periods=100, freq="D")
        np.random.seed(42)
        returns = pd.Series(np.random.randn(100) * 0.01, index=dates)
        factor = pd.Series(np.random.randn(100) * 0.01, index=dates, name="factor")

        result = run_factor_regression(returns, factor)
        assert isinstance(result, RegressionResult)

    def test_beta_matches_calculate_beta(self):
        """CAPM beta should match simple beta calculation."""
        dates = pd.date_range("2020-01-01", periods=100, freq="D")
        np.random.seed(42)
        returns = pd.Series(np.random.randn(100) * 0.01, index=dates)
        factor = pd.Series(np.random.randn(100) * 0.01, index=dates)

        result = run_factor_regression(returns, factor)
        simple_beta = calculate_beta(returns, factor)

        # Should be very close (small differences due to OLS vs covariance)
        assert np.isclose(result.betas["factor"], simple_beta, rtol=0.01)

    def test_alpha_near_zero_for_perfect_fit(self):
        """Perfect linear relationship should have alpha near zero."""
        dates = pd.date_range("2020-01-01", periods=100, freq="D")
        np.random.seed(42)
        factor = pd.Series(np.random.randn(100) * 0.01, index=dates)
        # returns = 1.5 * factor exactly
        returns = factor * 1.5

        result = run_factor_regression(returns, factor)
        assert np.isclose(result.alpha, 0.0, atol=1e-10)
        assert np.isclose(result.betas["factor"], 1.5, rtol=1e-6)

    def test_r_squared_one_for_perfect_fit(self):
        """Perfect linear relationship should have R^2 = 1."""
        dates = pd.date_range("2020-01-01", periods=100, freq="D")
        np.random.seed(42)
        factor = pd.Series(np.random.randn(100) * 0.01, index=dates)
        returns = factor * 2.0 + 0.001  # Perfect linear relationship

        result = run_factor_regression(returns, factor)
        assert np.isclose(result.r_squared, 1.0, rtol=1e-6)

    def test_multi_factor_returns_all_betas(self):
        """Multi-factor regression should return all betas."""
        dates = pd.date_range("2020-01-01", periods=100, freq="D")
        np.random.seed(42)
        returns = pd.Series(np.random.randn(100) * 0.01, index=dates)
        factors = pd.DataFrame(
            {
                "Mkt-RF": np.random.randn(100) * 0.01,
                "SMB": np.random.randn(100) * 0.005,
                "HML": np.random.randn(100) * 0.005,
            },
            index=dates,
        )

        result = run_factor_regression(returns, factors)

        assert "Mkt-RF" in result.betas
        assert "SMB" in result.betas
        assert "HML" in result.betas
        assert len(result.betas) == 3

    def test_annualization_factor(self):
        """Annualized alpha should be scaled correctly."""
        dates = pd.date_range("2020-01-01", periods=100, freq="D")
        np.random.seed(42)
        returns = pd.Series(np.random.randn(100) * 0.01 + 0.001, index=dates)
        factor = pd.Series(np.random.randn(100) * 0.01, index=dates)

        result = run_factor_regression(returns, factor, annualization_factor=12)

        assert result.alpha_annualized is not None
        assert result.annualization_factor == 12
        assert np.isclose(result.alpha_annualized, result.alpha * 12, rtol=1e-6)

    def test_no_annualization(self):
        """Without annualization_factor, alpha_annualized should be None."""
        dates = pd.date_range("2020-01-01", periods=100, freq="D")
        np.random.seed(42)
        returns = pd.Series(np.random.randn(100) * 0.01, index=dates)
        factor = pd.Series(np.random.randn(100) * 0.01, index=dates)

        result = run_factor_regression(returns, factor)

        assert result.alpha_annualized is None
        assert result.annualization_factor is None

    def test_t_stats_and_pvalues(self):
        """Should return valid t-statistics and p-values."""
        dates = pd.date_range("2020-01-01", periods=100, freq="D")
        np.random.seed(42)
        returns = pd.Series(np.random.randn(100) * 0.01, index=dates)
        factor = pd.Series(np.random.randn(100) * 0.01, index=dates)

        result = run_factor_regression(returns, factor)

        # t-stats can be any real number
        assert isinstance(result.alpha_tstat, float)
        assert isinstance(result.beta_tstats["factor"], float)

        # p-values should be between 0 and 1
        assert 0 <= result.alpha_pvalue <= 1
        assert 0 <= result.beta_pvalues["factor"] <= 1

    def test_n_observations(self):
        """Should return correct number of observations."""
        dates = pd.date_range("2020-01-01", periods=100, freq="D")
        np.random.seed(42)
        returns = pd.Series(np.random.randn(100) * 0.01, index=dates)
        factor = pd.Series(np.random.randn(100) * 0.01, index=dates)

        result = run_factor_regression(returns, factor)
        assert result.n_observations == 100


class TestRunCAPMRegression:
    """Tests for run_capm_regression convenience function."""

    def test_returns_mkt_rf_beta(self):
        """Should return beta with key 'Mkt-RF'."""
        dates = pd.date_range("2020-01-01", periods=100, freq="D")
        np.random.seed(42)
        excess_ret = pd.Series(np.random.randn(100) * 0.01, index=dates)
        mkt_excess = pd.Series(np.random.randn(100) * 0.01, index=dates)

        result = run_capm_regression(excess_ret, mkt_excess)

        assert "Mkt-RF" in result.betas
        assert len(result.betas) == 1

    def test_matches_run_factor_regression(self):
        """Should give same results as run_factor_regression."""
        dates = pd.date_range("2020-01-01", periods=100, freq="D")
        np.random.seed(42)
        excess_ret = pd.Series(np.random.randn(100) * 0.01, index=dates)
        mkt_excess = pd.Series(np.random.randn(100) * 0.01, index=dates)

        result_capm = run_capm_regression(excess_ret, mkt_excess)
        result_manual = run_factor_regression(
            excess_ret, mkt_excess.to_frame(name="Mkt-RF")
        )

        assert np.isclose(result_capm.alpha, result_manual.alpha)
        assert np.isclose(
            result_capm.betas["Mkt-RF"], result_manual.betas["Mkt-RF"]
        )


class TestRunFamaFrenchRegression:
    """Tests for run_fama_french_regression convenience function."""

    def test_returns_all_three_betas(self):
        """Should return betas for Mkt-RF, SMB, HML."""
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

        result = run_fama_french_regression(returns, factors)

        assert "Mkt-RF" in result.betas
        assert "SMB" in result.betas
        assert "HML" in result.betas
        assert len(result.betas) == 3

    def test_computes_excess_returns(self):
        """Should subtract RF from returns internally."""
        dates = pd.date_range("2020-01-01", periods=100, freq="D")
        np.random.seed(42)

        # Create returns with known alpha and betas
        mkt_rf = np.random.randn(100) * 0.01
        smb = np.random.randn(100) * 0.005
        hml = np.random.randn(100) * 0.005
        rf = np.full(100, 0.001)
        # excess_returns = 1.0 * Mkt-RF + 0.5 * SMB + 0.3 * HML + alpha
        excess_returns = mkt_rf + 0.5 * smb + 0.3 * hml + 0.002
        raw_returns = excess_returns + rf

        returns = pd.Series(raw_returns, index=dates)
        factors = pd.DataFrame(
            {
                "Mkt-RF": mkt_rf,
                "SMB": smb,
                "HML": hml,
                "RF": rf,
            },
            index=dates,
        )

        result = run_fama_french_regression(returns, factors)

        # Market beta should be close to 1
        assert np.isclose(result.betas["Mkt-RF"], 1.0, rtol=0.05)
        # SMB beta should be close to 0.5
        assert np.isclose(result.betas["SMB"], 0.5, rtol=0.1)
        # HML beta should be close to 0.3
        assert np.isclose(result.betas["HML"], 0.3, rtol=0.15)
        # Alpha should be close to 0.002
        assert np.isclose(result.alpha, 0.002, atol=0.001)

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

        result = run_fama_french_regression(returns, factors)

        # Should use the intersection of dates
        assert result.n_observations < 100
        assert result.n_observations > 0
