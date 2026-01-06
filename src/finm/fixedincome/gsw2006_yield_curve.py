"""
Implementation of Nelson-Siegel-Svensson yield curve model following Gurkaynak,
Sack, and Wright (2006).

Key components:
- Treasury security filtering based on GSW methodology
- Cash flow calculation for coupon-bearing bonds
- Nonlinear optimization for parameter estimation
- Spot rate and discount factor calculations

References:
Gürkaynak, Refet S., Brian Sack, and Jonathan H. Wright.
"The US Treasury yield curve: 1961 to the present."
 Journal of monetary Economics 54, no. 8 (2007): 2291-2304.
https://doi.org/10.1016/j.jmoneco.2007.06.029

Acknowledgements:
- The function to create the cashflows is from Mark Hendricks.
- Younghun Lee assisted with writing this code.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy.optimize import minimize

from finm.fixedincome.pricing import get_coupon_dates

# from ..data.CRSP import pull_CRSP_treasury
# from ..data.Federal_Reserve import pull_yield_curve_data

# from settings import config

# --------------------------
# Model Configuration
# --------------------------
# DATA_DIR = config("DATA_DIR")
# Nelson-Siegel-Svensson parameters
# "tau1", "tau2", "beta1", "beta2", "beta3", "beta4"
PARAM_NAMES = ("tau1", "tau2", "beta1", "beta2", "beta3", "beta4")
PARAMS0 = np.array([1.0, 10.0, 3.0, 3.0, 3.0, 3.0])

# Function required for GSW analysis
def filter_treasury_cashflows(
    CF, filter_maturity_dates=False, filter_benchmark_dates=False, filter_CF_strict=True
):
    mask_benchmark_dts = []

    # Filter by using only benchmark treasury dates
    for col in CF.columns:
        if filter_benchmark_dates:
            if col.month in [2, 5, 8, 11] and col.day == 15:
                mask_benchmark_dts.append(col)
        else:
            mask_benchmark_dts.append(col)

    if filter_maturity_dates:
        mask_maturity_dts = CF.columns[(CF >= 100).any()]
    else:
        mask_maturity_dts = CF.columns

    mask = [i for i in mask_benchmark_dts if i in mask_maturity_dts]

    CF_filtered = CF[mask]

    if filter_CF_strict:
        # drop issues that had CF on excluded dates
        mask_bnds = CF_filtered.sum(axis=1) == CF.sum(axis=1)
        CF_filtered = CF_filtered[mask_bnds]

    else:
        # drop issues that have no CF on included dates
        mask_bnds = CF_filtered.sum(axis=1) > 0
        CF_filtered = CF_filtered[mask_bnds]

    # update to drop dates with no CF
    CF_filtered = CF_filtered.loc[:, (CF_filtered > 0).any()]

    return CF_filtered


# Function required for GSW analysis
def calc_cashflows(quote_data, filter_maturity_dates=False):
    CF = pd.DataFrame(
        dtype=float,
        data=0,
        index=quote_data.index,
        columns=quote_data["tmatdt"].unique(),
    )

    for i in quote_data.index:
        coupon_dates = get_coupon_dates(
            quote_data.loc[i, "caldt"], quote_data.loc[i, "tmatdt"]
        )

        if coupon_dates is not None:
            CF.loc[i, coupon_dates] = quote_data.loc[i, "tcouprt"] / 2

        CF.loc[i, quote_data.loc[i, "tmatdt"]] += 100

    # Sort columns by maturity date
    CF = CF.fillna(0).sort_index(axis=1)
    # Drop columns (dates) that are all zeros
    CF.drop(columns=CF.columns[(CF == 0).all()], inplace=True)

    if filter_maturity_dates:
        CF = filter_treasury_cashflows(CF, filter_maturity_dates=True)

    return CF


# Function required for GSW analysis
def plot_spot_curve(params):
    """Plot the spot curve for the fitted NelsonSeigelSvensson instance"""
    t = np.linspace(1, 30, 100)
    spots = pd.Series(spot(t, params), index=t)
    ax = spots.plot(title="Spot Curve", xlabel="Maturity", ylabel="Spot Rate")

    plt.tight_layout()
    plt.show()

    return ax


# Function required for GSW analysis
def spot(maturities, params=PARAMS0):
    """Calculate Nelson-Siegel-Svensson spot rates for given maturities.

    These are the zero-coupon yields, from equation (22) in
    Gurkaynak, Sack, and Wright (2006)
    """
    tau1, tau2, beta1, beta2, beta3, beta4 = params

    t = np.asarray(maturities)
    tau1_exp = (1 - np.exp(-t / tau1)) / (t / tau1)
    tau2_exp = (1 - np.exp(-t / tau2)) / (t / tau2)

    return (
        beta1
        + beta2 * tau1_exp
        + beta3 * (tau1_exp - np.exp(-t / tau1))
        + beta4 * (tau2_exp - np.exp(-t / tau2))
    )


# Function required for GSW analysis
def discount(t, params=PARAMS0):
    """Calculate discount factors from spot rates.

    Args:
        t: Array of times to maturity in years

    Returns:
        array: Discount factors for each maturity
    """
    return np.exp(-spot(t, params=params) * t)


# Function required for GSW analysis
def predict_prices(quote_date, df_all, params=PARAMS0):
    """Calculate security prices from the parameters"""
    df = df_all[df_all["caldt"] == quote_date]
    cashflows = calc_cashflows(df)
    # Calculate time in years from quote date to each payment date
    payment_dates = cashflows.columns
    time_deltas = payment_dates - quote_date
    times = time_deltas.days / 365.25  # Convert to fractional years

    disc = discount(times, params=params)
    predicted_prices = cashflows @ disc
    predicted_prices.index = df["tcusip"]
    return predicted_prices


# Function required for GSW analysis
def fit(quote_date, df_all, params0=PARAMS0):
    """Fit NSS model to Treasury security data using nonlinear least squares.

    Optimization objective minimizes price errors weighted by duration:
        min Σ [(P_observed - P_model)^2 / D]

    Returns:
        tuple: (optimized_parameters, objective_value)

    ## Optimization Objective

    Implements the Gurkaynak-Sack-Wright (2006) objective function:

    ```math
    \min_{\beta,\tau} \sum_{i=1}^N \frac{(P_i^{obs} - P_i^{model})^2}{D_i}
    ```

    Where:
    - \(P_i^{obs}\) = Observed clean price (including accrued interest)
    - \(P_i^{model}\) = Model-implied price
    - \(D_i\) = Duration of security i

    ## Relationship to Yield Errors

    The price error objective is approximately equivalent to minimizing unweighted yield errors:

    ```math
    \frac{(P_i^{obs} - P_i^{model})^2}{D_i} \approx D_i \cdot (y_i^{obs} - y_i^{model})^2
    ```

    This approximation comes from the duration relationship:
    ```math
    P^{obs} - P^{model} \approx -D \cdot (y^{obs} - y^{model})
    ```

    Making the objective function:
    ```math
    \sum D_i \cdot (y_i^{obs} - y_i^{model})^2
    ```

    ## Why Price Errors Instead of Yield Errors?

    1. **Non-linear relationship**: The price/yield relationship is convex
       (convexity adjustment matters more for long-duration bonds)
    2. **Coupon effects**: Directly accounts for differential cash flow timing
    3. **Numerical stability**: Prices have linear sensitivity to parameters via
       discount factors, while yields require non-linear root-finding
    4. **Economic meaning**: Aligns with trader behavior that thinks in terms of
       price arbitrage

    Reference: Gurkaynak, Sack, and Wright (2006)
    """
    # Data preparation
    df = df_all[df_all["caldt"] == pd.to_datetime(quote_date)]
    cashflows = calc_cashflows(df)

    # Time calculations
    payment_dates = cashflows.columns
    times = (payment_dates - quote_date).days / 365.25

    # Optimization components
    observed_prices = df["price"].values
    weights = 1 / np.sqrt(df["tdduratn"].values)  # Square root of duration, since it
    # will be squared later

    def mean_squared_error(params):
        predicted_prices = cashflows @ discount(times, params)
        return np.mean(((observed_prices - predicted_prices) * weights) ** 2)

    # Bounds and constraints
    bounds = [
        (1e-06, None),
        (1e-06, None),
        (None, None),
        (None, None),
        (None, None),
        (None, None),
    ]
    result = minimize(
        mean_squared_error, params0, bounds=bounds, options={"maxiter": 1e5}
    )

    if not result.success:
        raise RuntimeError(f"Optimization failed: {result.message}")

    param_star = result.x

    return param_star, mean_squared_error(param_star)


# Function required for GSW analysis
def gurkaynak_sack_wright_filters(dff):
    """Apply Treasury security filters based on Gürkaynak, Sack, and Wright (2006).

    Implemented filters:
    1. Exclude securities with < 3 months to maturity
    2. Exclude on-the-run and first off-the-run issues after 1980
    3. Exclude T-bills (only keep notes and bonds)
    4. Exclude 20-year bonds after 1996 with decay
    5. Exclude callable bonds

    Still missing:
    - Ad hoc exclusions for specific issues

    ## Notes
    For (2), this is what the paper says:

    We exclude the two most recently issued securities with maturities of two,
    three, four, five, seven, ten, twenty, and thirty years for securities
    issued in 1980 or later. These are the "on-the-run" and "first off-the-run"
    issues that often trade at a premium to other Treasury securities, owing to
    their greater liquidity and their frequent specialness in the repo market.8
    Earlier in the sample, the concept of an on-the-run issue was not well
    defined, since the Treasury did not conduct regular auctions and the repo
    market was not well developed (as discussed by Garbade (2004)). Our cut-off
    point for excluding onthe- run and first off-the-run issues is somewhat
    arbitrary but is a conservative choice (in the sense of potentially erring
    on the side of being too early).

    For (4), this is what the paper says:

    We begin to exclude twenty-year bonds in 1996, because those securities
    often appeared cheap relative to ten-year notes with comparable duration.
    This cheapness could reflect their lower liquidity or the fact that their
    high coupon rates made them unattractive to hold for tax-related reasons.

    To avoid an abrupt change to the sample, we allow their weights to linearly
    decay from 1 to 0 over the year ending on January 2, 1996.
    """
    df = dff.copy()

    # Filter 1: Exclude < 3 months to maturity
    df = df[df["days_to_maturity"] > 92]

    # Filter 2: Exclude on-the-run and first off-the-run after 1980
    post_1980 = df["caldt"] >= pd.to_datetime("1980-01-01")
    df = df[~(post_1980 & (df["run"] <= 2))]

    # Filter 3: Only include notes (2) and bonds (1)
    df = df[df["itype"].isin([1, 2])]

    # Filter 4: Exclude 20-year bonds after 1996 with decay
    cutoff_date = pd.to_datetime("1996-01-02")
    decay_start = cutoff_date - pd.DateOffset(years=1)

    df["weight"] = 1.0
    # Apply linear decay only during 1995-01-02 to 1996-01-02
    mask_decay = (
        (df["original_maturity"] == 20)
        & (df["caldt"] >= decay_start)
        & (df["caldt"] <= cutoff_date)
    )
    # Calculate proper decay factor for the transition year
    decay_days = (cutoff_date - decay_start).days
    decay_factor = 1 - ((df["caldt"] - decay_start).dt.days / decay_days)
    df.loc[mask_decay, "weight"] *= decay_factor

    # Completely exclude 20-year bonds after cutoff date
    mask_exclude = (df["original_maturity"] == 20) & (df["caldt"] > cutoff_date)
    df.loc[mask_exclude, "weight"] = 0

    # Filter 5: Exclude callable bonds
    df = df[~df["callable"]]

    # Remove securities with zero/negative weights
    df = df[df["weight"] > 0]

    return df


# Function required for GSW analysis
def compare_fit(quote_date, df_all, params_star, actual_params, df):
    predicted_prices = predict_prices(quote_date, df_all, params=params_star)
    gsw_predicted_prices = predict_prices(quote_date, df_all, params=actual_params)

    actual_prices = df[["tcusip", "price"]].set_index("tcusip")["price"]

    # Compare with actual prices
    price_comparison = pd.DataFrame(
        {
            "Actual Price": actual_prices,
            "GSW Predicted Price": gsw_predicted_prices,
            "Model Predicted Price": predicted_prices,
            "Predicted - Actual %": (predicted_prices - actual_prices) / actual_prices,
            "Predicted - GSW %": (predicted_prices - gsw_predicted_prices)
            / gsw_predicted_prices,
        }
    )
    return price_comparison


# def _demo():
#     """
#     Demo of how the Nelson-Siegel-Svensson model works
#     """

#     actual_all = pull_yield_curve_data.load_fed_yield_curve_all(data_dir=DATA_DIR)
#     # Create copy of parameter DataFrame to avoid view vs copy issues
#     actual_params_all = actual_all.loc[
#         :, ["TAU1", "TAU2", "BETA0", "BETA1", "BETA2", "BETA3"]
#     ].copy()

#     # Convert percentage points to decimals for beta parameters
#     beta_columns = ["BETA0", "BETA1", "BETA2", "BETA3"]
#     actual_params_all[beta_columns] = actual_params_all[beta_columns] / 100

#     df_all = pull_CRSP_treasury.load_CRSP_treasury_consolidated(data_dir=DATA_DIR)
#     df_all = gurkaynak_sack_wright_filters(df_all)
#     df_all.info()

#     quote_dates = pd.date_range("2000-01-02", "2024-06-30", freq="BMS")
#     quote_date = quote_dates[-1]
#     # Subset df_all to quote_date
#     df = df_all[df_all["caldt"] == quote_date]
#     actual_params = actual_params_all[actual_params_all.index == quote_date].values[0]

#     # "tau1", "tau2", "beta1", "beta2", "beta3", "beta4"
#     # params0 = np.array([1.0, 10.0, 3.0, 3.0, 3.0, 3.0])
#     params0 = np.array([0.989721, 9.955324, 3.685087, 1.579927, 3.637107, 9.814584])
#     # params0 = np.array([1.0, 1.0, 0.001, 0.001, 0.001, 0.001])

#     params_star, error = fit(quote_date, df_all, params0)
#     print(params_star)
#     print(error)

#     plot_spot_curve(params_star)
#     plot_spot_curve(actual_params)

#     price_comparison = compare_fit(quote_date, df_all, params_star, actual_params, df)
#     return price_comparison, params_star


# if __name__ == "__main__":
#     pass
