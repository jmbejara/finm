"""Tests for the Fama-French data module."""

import pandas as pd
import polars as pl
import pytest

from finm.data import fama_french


class TestLoadFamaFrenchFactors:
    """Tests for fama_french.load() function."""

    def test_returns_polars_dataframe(self):
        """Should return a polars DataFrame."""
        df = fama_french.load()
        assert isinstance(df, pl.DataFrame)

    def test_has_required_columns(self):
        """Should have all required columns."""
        df = fama_french.load()
        required_cols = ["Mkt-RF", "SMB", "HML", "RF"]
        for col in required_cols:
            assert col in df.columns

    def test_date_filtering_start(self):
        """Should filter by start date."""
        df = fama_french.load(start="2020-01-01")
        date_col = "Date" if "Date" in df.columns else df.columns[0]
        min_date = df[date_col].min()
        assert min_date >= pd.Timestamp("2020-01-01")

    def test_date_filtering_end(self):
        """Should filter by end date."""
        df = fama_french.load(end="2024-12-31")
        date_col = "Date" if "Date" in df.columns else df.columns[0]
        max_date = df[date_col].max()
        # Convert polars datetime to python datetime for comparison
        if hasattr(max_date, "to_pydatetime"):
            max_date = max_date.to_pydatetime()
        assert max_date <= pd.Timestamp("2024-12-31")

    def test_date_filtering_range(self):
        """Should filter by date range."""
        df = fama_french.load(start="2022-01-01", end="2023-12-31")
        date_col = "Date" if "Date" in df.columns else df.columns[0]
        min_date = df[date_col].min()
        max_date = df[date_col].max()
        # Convert polars datetime to python datetime for comparison
        if hasattr(min_date, "to_pydatetime"):
            min_date = min_date.to_pydatetime()
        if hasattr(max_date, "to_pydatetime"):
            max_date = max_date.to_pydatetime()
        assert min_date >= pd.Timestamp("2022-01-01")
        assert max_date <= pd.Timestamp("2023-12-31")

    def test_values_are_decimals(self):
        """Values should be in decimal form (not percentages)."""
        df = fama_french.load()
        # Typical daily returns should be < 0.5 (50%) even on extreme days
        assert df["Mkt-RF"].abs().max() < 0.5
        # RF should be very small daily (< 1%)
        assert df["RF"].abs().max() < 0.01

    def test_has_date_column(self):
        """Should have a Date column."""
        df = fama_french.load()
        assert "Date" in df.columns

    def test_has_substantial_data(self):
        """Bundled data should have substantial data coverage."""
        df = fama_french.load()
        # Bundled data has ~1200+ daily observations (about 5 years of recent data)
        assert len(df) > 1000

    def test_data_starts_from_2021(self):
        """Bundled data should start from 2021."""
        df = fama_french.load()
        date_col = "Date" if "Date" in df.columns else df.columns[0]
        min_date = df[date_col].min()
        # Convert polars datetime to python datetime
        if hasattr(min_date, "to_pydatetime"):
            min_date = min_date.to_pydatetime()
        assert min_date.year == 2021

    def test_long_format(self):
        """Should return long format when requested."""
        df = fama_french.load(format="long")
        assert "unique_id" in df.columns
        assert "ds" in df.columns
        assert "y" in df.columns

    def test_lazy_returns_lazyframe(self):
        """Should return LazyFrame when lazy=True."""
        lf = fama_french.load(lazy=True)
        assert isinstance(lf, pl.LazyFrame)


class TestLongFormat:
    """Tests for to_long_format transformation."""

    def test_to_long_format(self):
        """Should convert wide to long format."""
        # Load as pandas for to_long_format (which expects pandas)
        df_wide = fama_french.load().to_pandas()
        df_wide = df_wide.set_index("Date")
        df_long = fama_french.to_long_format(df_wide)

        assert "unique_id" in df_long.columns
        assert "ds" in df_long.columns
        assert "y" in df_long.columns

        # Should have one row per factor per date
        n_factors = len(df_wide.columns)
        n_dates = len(df_wide)
        # Allow for some NaN values being dropped
        assert len(df_long) <= n_factors * n_dates


class TestPullFamaFrenchFactors:
    """Tests for fama_french.pull() function (requires network)."""

    @pytest.mark.skip(reason="Requires network access and pandas_datareader")
    def test_pull_daily_factors(self):
        """Should download daily factors."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            df = fama_french.pull(
                data_dir=tmpdir,
                start="2023-01-01",
                end="2023-01-31",
                frequency="daily",
            )
            assert isinstance(df, pd.DataFrame)
            assert len(df) > 0

    @pytest.mark.skip(reason="Requires network access and pandas_datareader")
    def test_pull_monthly_factors(self):
        """Should download monthly factors."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            df = fama_french.pull(
                data_dir=tmpdir,
                start="2023-01-01",
                end="2023-12-31",
                frequency="monthly",
            )
            assert isinstance(df, pd.DataFrame)
            assert len(df) > 0
