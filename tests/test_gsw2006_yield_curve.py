import os
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv

import finm

# Load environment variables from .env file
load_dotenv()

# Get data directory from environment or use default
DATA_CACHE_DIR = Path(os.environ.get("DATA_DIR", "./_data"))


def test_fit_on_several_days():
    """
    Fit the Nelson-Siegel-Svensson model to the CRSP Treasury data for a specific date
    """

    ## Load Gurkaynak Sack Wright data from Federal Reserve's website
    # See here: https://www.federalreserve.gov/data/nominal-yield-curve.htm
    # and here: https://www.federalreserve.gov/data/yield-curve-tables/feds200628_1.html
    actual_all = finm.load_fed_yield_curve_all(data_dir=DATA_CACHE_DIR)
    # Create copy of parameter DataFrame to avoid view vs copy issues
    actual_params_all = actual_all.loc[
        :, ["TAU1", "TAU2", "BETA0", "BETA1", "BETA2", "BETA3"]
    ].copy()
    # Convert percentage points to decimals for beta parameters
    beta_columns = ["BETA0", "BETA1", "BETA2", "BETA3"]
    actual_params_all[beta_columns] = actual_params_all[beta_columns] / 100

    ## Load CRSP Treasury data from Wharton Research Data Services
    # We will fit a Nelson-Siegel-Svensson model to this data to see
    # if we can replicate the Gurkaynak Sack Wright results above.
    df_all = finm.load_CRSP_treasury_consolidated(data_dir=DATA_CACHE_DIR)
    df_all = finm.gurkaynak_sack_wright_filters(df_all)

    quote_dates = pd.date_range("2000-01-02", "2024-06-30", freq="BMS")
    # quote_date = quote_dates[-1]

    ## Test Day 1
    quote_date = pd.to_datetime("2024-06-03")
    # Subset df_all to quote_date
    df = df_all[df_all["caldt"] == quote_date]
    actual_params = actual_params_all[actual_params_all.index == quote_date].values[0]

    # "tau1", "tau2", "beta1", "beta2", "beta3", "beta4"
    # params0 = np.array([1.0, 10.0, 3.0, 3.0, 3.0, 3.0])
    params0 = np.array([0.989721, 9.955324, 3.685087, 1.579927, 3.637107, 9.814584])
    # params0 = np.array([1.0, 1.0, 0.001, 0.001, 0.001, 0.001])

    params_star, error = finm.fit(quote_date, df_all, params0)

    ## Visualize the fit
    # gsw2006_yield_curve.plot_spot_curve(params_star)
    # gsw2006_yield_curve.plot_spot_curve(actual_params)

    price_comparison = finm.compare_fit(
        quote_date, df_all, params_star, actual_params, df
    )

    ## Assert that column is close to 0 for all CUSIPs
    assert (price_comparison["Predicted - Actual %"].abs() < 0.05).all()
    assert (price_comparison["Predicted - GSW %"].abs() < 0.02).all()

    ## Test Day 2
    quote_date = pd.to_datetime("2000-06-05")
    # Subset df_all to quote_date
    df = df_all[df_all["caldt"] == quote_date]
    actual_params = actual_params_all[actual_params_all.index == quote_date].values[0]

    # "tau1", "tau2", "beta1", "beta2", "beta3", "beta4"
    # params0 = np.array([1.0, 10.0, 3.0, 3.0, 3.0, 3.0])
    params0 = np.array([0.989721, 9.955324, 3.685087, 1.579927, 3.637107, 9.814584])
    # params0 = np.array([1.0, 1.0, 0.001, 0.001, 0.001, 0.001])

    params_star, error = finm.fit(quote_date, df_all, params0)

    ## Visualize the fit
    # gsw2006_yield_curve.plot_spot_curve(params_star)
    # gsw2006_yield_curve.plot_spot_curve(actual_params)

    price_comparison = finm.compare_fit(
        quote_date, df_all, params_star, actual_params, df
    )

    ## Assert that column is close to 0 for all CUSIPs
    assert (price_comparison["Predicted - Actual %"].abs() < 0.05).all()
    assert (price_comparison["Predicted - GSW %"].abs() < 0.02).all()

    ## Test Day 3
    quote_date = pd.to_datetime("1990-06-05")
    # Subset df_all to quote_date
    df = df_all[df_all["caldt"] == quote_date]
    actual_params = actual_params_all[actual_params_all.index == quote_date].values[0]

    # "tau1", "tau2", "beta1", "beta2", "beta3", "beta4"
    # params0 = np.array([1.0, 10.0, 3.0, 3.0, 3.0, 3.0])
    params0 = np.array([0.989721, 9.955324, 3.685087, 1.579927, 3.637107, 9.814584])
    # params0 = np.array([1.0, 1.0, 0.001, 0.001, 0.001, 0.001])

    params_star, error = finm.fit(quote_date, df_all, params0)

    ## Visualize the fit
    # gsw2006_yield_curve.plot_spot_curve(params_star)
    # gsw2006_yield_curve.plot_spot_curve(actual_params)

    price_comparison = finm.compare_fit(
        quote_date, df_all, params_star, actual_params, df
    )

    ## Assert that column is close to 0 for all CUSIPs
    assert (price_comparison["Predicted - Actual %"].abs() < 0.05).all()
    assert (price_comparison["Predicted - GSW %"].abs() < 0.02).all()


def test_cashflow_construction():
    """
    Test that the cashflow construction is correct
    """

    sample_data = pd.DataFrame(
        {
            "tcusip": ["A", "B", "C", "D", "E"],
            "tmatdt": pd.to_datetime(
                ["2000-05-15", "2000-05-31", "2000-06-30", "2000-07-31", "2000-08-15"]
            ),
            "price": [101, 101, 100, 100, 103],
            "tcouprt": [6, 6, 0, 5, 6],
            "caldt": pd.to_datetime("2000-01-31"),
        }
    )

    cashflow = finm.calc_cashflows(sample_data)

    # Treasury securities have 2 coupon payments per year
    # and pay their final coupon and principal on the maturity date
    expected_cashflow = np.array(
        [
            [0.0, 103.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 103.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 100.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 102.5, 0.0],
            [3.0, 0.0, 0.0, 0.0, 0.0, 103.0],
        ]
    )
    expected_ttm = np.array([0.0411, 0.2877, 0.3315, 0.4137, 0.4986, 0.5397])

    # Assert almost equal
    assert np.allclose(expected_cashflow, cashflow.values)
    ttm = (cashflow.columns - sample_data.loc[0, "caldt"]).days / 365
    assert np.allclose(expected_ttm, ttm, atol=1e-2)
