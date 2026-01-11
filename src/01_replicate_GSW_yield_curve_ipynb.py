# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Replicating the Gurkaynak, Sack, and Wright (2006) Treasury Yield Curve
#
# ## Introduction
#
# In this section, we'll explore how to replicate the U.S. Treasury yield curve
# estimation methodology developed by Gurkaynak, Sack, and Wright (2006)
# (hereafter GSW). The GSW yield curve has become a standard benchmark in both
# academic research and industry practice. Their approach provides daily estimates
# of the U.S. Treasury yield curve from 1961 to the present, making it an
# invaluable resource for analyzing historical interest rate dynamics.
#
# ## The Nelson-Siegel-Svensson Model
#
# The GSW methodology employs the Nelson-Siegel-Svensson (NSS) model to fit the
# yield curve. The NSS model expresses instantaneous forward rates using a
# flexible functional form with six parameters:
#
# Example: NSS Forward Rate Function
# The instantaneous forward rate n years ahead is given by:
#
# $$
# f(n) = \beta_1 + \beta_2 e^{-n/\tau_1} + \beta_3\left(\frac{n}{\tau_1}\right)e^{-n/\tau_1} + \beta_4\left(\frac{n}{\tau_2}\right)e^{-n/\tau_2}
# $$
#
# This specification allows for rich curve shapes while maintaining smoothness
# and asymptotic behavior. The parameters have intuitive interpretations:
# - $\beta_1$: The asymptotic forward rate
# - $\beta_2$, $\beta_3$, $\beta_4$: Control the shape and humps of the curve
# - $\tau_1$, $\tau_2$: Determine the location of curve features
#
# $$
# y(t) = \beta_1 + \beta_2\left(\frac{1-e^{-t/\tau_1}}{t/\tau_1}\right) + \beta_3\left(\frac{1-e^{-t/\tau_1}}{t/\tau_1} - e^{-t/\tau_1}\right) + \beta_4\left(\frac{1-e^{-t/\tau_2}}{t/\tau_2} - e^{-t/\tau_2}\right)
# $$
#
# This equation shows the zero-coupon yield $y(t)$ for maturity $t$.

# %%
import os
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv

import finm

load_dotenv()

DATA_DIR = Path(os.environ.get("DATA_DIR", "./_data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
WRDS_USERNAME = os.environ.get("WRDS_USERNAME", "")

# %%
# Nelson-Siegel-Svensson parameters
# "tau1", "tau2", "beta1", "beta2", "beta3", "beta4"
params = np.array([1.0, 10.0, 3.0, 3.0, 3.0, 3.0])

finm.plot_spot_curve(params)

# %%
# Nelson-Siegel-Svensson parameters
# "tau1", "tau2", "beta1", "beta2", "beta3", "beta4"
params = np.array([1.0, 10.0, 3.0, 3.0, 3.0, 30.0])

finm.plot_spot_curve(params)

# %% [markdown]
# ## Theoretical Foundations
#
# The Nelson-Siegel-Svensson model is commonly used in practice to fit the yield
# curve. It has statistically appealing properties, but it is not arbitrage-free.
# Here's a detailed breakdown of why:
#
# ### 1. **Static Curve-Fitting Approach**
#    - The NSS model is primarily a **parametric curve-fitting tool** that
#      focuses on matching observed yields at a single point in time.
#    - It does not model the **dynamic evolution of interest rates** or enforce
#      consistency between short-term rate expectations and long-term yields
#      over time, a key requirement for no-arbitrage models.
#
# ### 2. **Absence of No-Arbitrage Restrictions**
#    - No-arbitrage models impose constraints to prevent risk-free profits.
#      For example, affine term structure models derive bond prices from:
#
#      $$
#      P(t,T) = \mathbb{E}^\mathbb{Q}\left[e^{-\int_t^T r_s ds}\right],
#      $$
#
#      where $\mathbb{Q}$ is the risk-neutral measure. The NSS model lacks
#      such theoretical foundations.
#    - The NSS parameters (e.g., level, slope, curvature) are **statistically
#      estimated** rather than derived from economic principles or
#      arbitrage-free dynamics.
#
# ### 3. **Factor Dynamics and Risk Premiums**
#    - In arbitrage-free models, factor dynamics (e.g., mean reversion) and
#      risk premiums are explicitly defined to ensure consistency across
#      maturities. The NSS model treats factors as **latent variables**
#      without specifying their stochastic behavior or market price of risk.
#    - This omission allows potential inconsistencies between short-rate
#      expectations and long-term yields, creating theoretical arbitrage
#      opportunities.
#
# ### 4. **Contrast with Arbitrage-Free Extensions**
#    - The **arbitrage-free Nelson-Siegel (AFNS)** model, developed by
#      Christensen et al. (2007), addresses these limitations by:
#      - Embedding Nelson-Siegel factors into a dynamic arbitrage-free
#        framework.
#      - Explicitly defining factor dynamics under both physical ($\mathbb{P}$)
#        and risk-neutral ($\mathbb{Q}$) measures.
#      - Ensuring internal consistency between yields of different maturities.
#
# ### 5. **Empirical vs. Theoretical Focus**
#    - The NSS model prioritizes **empirical flexibility** (e.g., fitting
#      yield curve shapes like humps) over theoretical rigor. While it
#      performs well in practice, this trade-off inherently sacrifices
#      no-arbitrage guarantees.
#
# In summary, the NSS model's lack of dynamic factor specifications, absence
# of explicit no-arbitrage constraints, and focus on cross-sectional fitting
# rather than intertemporal consistency render it theoretically incompatible
# with arbitrage-free principles. Its successors, such as the AFNS model,
# bridge this gap by integrating no-arbitrage restrictions while retaining
# empirical tractability.

# %% [markdown]
# ## Data Filtering
#
# One important step of the GSW methodology is careful filtering of Treasury
# securities.
#
# The following filters are implemented:
#
# 1. Exclude securities with < 3 months to maturity
# 2. Exclude on-the-run and first off-the-run issues after 1980
# 3. Exclude T-bills (only keep notes and bonds)
# 4. Exclude 20-year bonds after 1996 with decay
# 5. Exclude callable bonds
#
# The GSW paper also includes ad hoc exclusions for specific issues, which
# are not implemented here.
#
# Why are these filters important?
#
# For (2), this is what the paper says:
#
# > We exclude the two most recently issued securities with maturities of two,
# > three, four, five, seven, ten, twenty, and thirty years for securities
# > issued in 1980 or later. These are the "on-the-run" and "first off-the-run"
# > issues that often trade at a premium to other Treasury securities, owing to
# > their greater liquidity and their frequent specialness in the repo market.
# > Earlier in the sample, the concept of an on-the-run issue was not well
# > defined, since the Treasury did not conduct regular auctions and the repo
# > market was not well developed (as discussed by Garbade (2004)). Our cut-off
# > point for excluding on-the-run and first off-the-run issues is somewhat
# > arbitrary but is a conservative choice (in the sense of potentially erring
# > on the side of being too early).
#
# For (4), this is what the paper says:
#
# > We begin to exclude twenty-year bonds in 1996, because those securities
# > often appeared cheap relative to ten-year notes with comparable duration.
# > This cheapness could reflect their lower liquidity or the fact that their
# > high coupon rates made them unattractive to hold for tax-related reasons.
# >
# > To avoid an abrupt change to the sample, we allow their weights to linearly
# > decay from 1 to 0 over the year ending on January 2, 1996.

# %% [markdown]
# Let's examine how this affects the data.

# %%
# Load Gurkaynak Sack Wright data from Federal Reserve's website
# See here: https://www.federalreserve.gov/data/nominal-yield-curve.htm
# and here: https://www.federalreserve.gov/data/yield-curve-tables/feds200628_1.html

df_all, df = finm.pull_fed_yield_curve()

path = Path(DATA_DIR) / "fed_yield_curve_all.parquet"
df_all.to_parquet(path)

path = Path(DATA_DIR) / "fed_yield_curve.parquet"
df.to_parquet(path)

# %%
actual_all = finm.load_fed_yield_curve_all(data_dir=DATA_DIR)

# Create copy of parameter DataFrame to avoid view vs copy issues
actual_params_all = actual_all.loc[
    :, ["TAU1", "TAU2", "BETA0", "BETA1", "BETA2", "BETA3"]
].copy()

# Convert percentage points to decimals for beta parameters
beta_columns = ["BETA0", "BETA1", "BETA2", "BETA3"]
actual_params_all[beta_columns] = actual_params_all[beta_columns] / 100

# %%
# Load CRSP Treasury data from Wharton Research Data Services
# We will fit a Nelson-Siegel-Svensson model to this data to see
# if we can replicate the Gurkaynak Sack Wright results above.
df = finm.pull_CRSP_treasury_consolidated(
    start_date="1970-01-01",
    end_date=datetime.today().strftime("%Y-%m-%d"),
    wrds_username=WRDS_USERNAME,
)

path = Path(DATA_DIR) / "CRSP_TFZ_consolidated.parquet"
df.to_parquet(path)

df = finm.calc_runness(df)

path = Path(DATA_DIR) / "CRSP_TFZ_with_runness.parquet"
df.to_parquet(path)

df_all = finm.load_CRSP_treasury_consolidated(data_dir=DATA_DIR)

# %%
df_all.tail()

# %%
df_all.describe()

# %%
df_all = finm.gurkaynak_sack_wright_filters(df_all)
df_all.describe()

# %% [markdown]
# ## Implementation Steps
#
# ### 1. Data Preparation
# First, we load and clean the CRSP Treasury data

# %%
df_all = finm.load_CRSP_treasury_consolidated(data_dir=DATA_DIR)

# %% [markdown]
# ### 2. Cashflow Construction
# For each Treasury security, we need to calculate its future cashflows.
# Consider the following simplified example:

# %%
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

# %%
cashflow

# %% [markdown]
# ### 3. Model Fitting
# The NSS model is fit by minimizing price errors weighted by duration:
#
# $$
# \min_{\beta,\tau} \sum_{i=1}^N \frac{(P_i^{obs} - P_i^{model})^2}{D_i}
# $$
#
# where:
# - $P_i^{obs}$ = Observed clean price (including accrued interest)
# - $P_i^{model}$ = Model-implied price
# - $D_i$ = Duration of security i
#
# Now, why are the squared errors weighted by the duration?
#
# Recall that bond duration is a measurement of how much a bond's price will
# change in response to interest rate changes. Thus, the price error objective
# is approximately equivalent to minimizing unweighted yield errors:
#
# $$
# \frac{(P_i^{obs} - P_i^{model})^2}{D_i} \approx D_i \cdot (y_i^{obs} - y_i^{model})^2
# $$
#
# This approximation comes from the duration relationship:
# $$
# P^{obs} - P^{model} \approx -D \cdot (y^{obs} - y^{model})
# $$
#
# Making the objective function:
# $$
# \sum D_i \cdot (y_i^{obs} - y_i^{model})^2
# $$
#
# So, why Price Errors Instead of Yield Errors?
#
# 1. **Non-linear relationship**: The price/yield relationship is convex
#     (convexity adjustment matters more for long-duration bonds)
# 2. **Coupon effects**: Directly accounts for differential cash flow timing
# 3. **Numerical stability**: Prices have linear sensitivity to parameters via
#     discount factors, while yields require non-linear root-finding
# 4. **Economic meaning**: Aligns with trader behavior that thinks in terms of
#     price arbitrage
#
# Reference: Gurkaynak, Sack, and Wright (2006)

# %% [markdown]
# ## Testing and Validation
#
# To validate our implementation, we compare our fitted yields against the
# official GSW yields published by the Federal Reserve:

# %%
# Load Gurkaynak Sack Wright data from Federal Reserve's website
actual_all = finm.load_fed_yield_curve_all(data_dir=DATA_DIR)
# Create copy of parameter DataFrame to avoid view vs copy issues
actual_params_all = actual_all.loc[
    :, ["TAU1", "TAU2", "BETA0", "BETA1", "BETA2", "BETA3"]
].copy()
# Convert percentage points to decimals for beta parameters
beta_columns = ["BETA0", "BETA1", "BETA2", "BETA3"]
actual_params_all[beta_columns] = actual_params_all[beta_columns] / 100


# Load CRSP Treasury data from Wharton Research Data Services
df_all = finm.load_CRSP_treasury_consolidated(data_dir=DATA_DIR)
df_all = finm.gurkaynak_sack_wright_filters(df_all)

quote_dates = pd.date_range("2000-01-02", "2024-06-30", freq="BMS")

# %% [markdown]
# ### Test Day 1

# %%
# Test Day 1
quote_date = pd.to_datetime("2024-06-03")
# Subset df_all to quote_date
df = df_all[df_all["caldt"] == quote_date]
actual_params = actual_params_all[actual_params_all.index == quote_date].values[0]

# "tau1", "tau2", "beta1", "beta2", "beta3", "beta4"
params0 = np.array([0.989721, 9.955324, 3.685087, 1.579927, 3.637107, 9.814584])

params_star, error = finm.fit(quote_date, df_all, params0)

# %%
# Visualize the fit
finm.plot_spot_curve(params_star)

# %%
finm.plot_spot_curve(actual_params)

# %%
price_comparison = finm.compare_fit(quote_date, df_all, params_star, actual_params, df)
price_comparison

# %%
# Assert that column is close to 0 for all CUSIPs
assert (price_comparison["Predicted - Actual %"].abs() < 0.05).all()
assert (price_comparison["Predicted - GSW %"].abs() < 0.02).all()

# %% [markdown]
# ### Test Day 2

# %%
# Test Day 2
quote_date = pd.to_datetime("2000-06-05")
# Subset df_all to quote_date
df = df_all[df_all["caldt"] == quote_date]
actual_params = actual_params_all[actual_params_all.index == quote_date].values[0]

params0 = np.array([0.989721, 9.955324, 3.685087, 1.579927, 3.637107, 9.814584])

params_star, error = finm.fit(quote_date, df_all, params0)

price_comparison = finm.compare_fit(quote_date, df_all, params_star, actual_params, df)

# Assert that column is close to 0 for all CUSIPs
assert (price_comparison["Predicted - Actual %"].abs() < 0.05).all()
assert (price_comparison["Predicted - GSW %"].abs() < 0.02).all()

# %% [markdown]
# ### Test Day 3

# %%
# Test Day 3
quote_date = pd.to_datetime("1990-06-05")
# Subset df_all to quote_date
df = df_all[df_all["caldt"] == quote_date]
actual_params = actual_params_all[actual_params_all.index == quote_date].values[0]

params0 = np.array([0.989721, 9.955324, 3.685087, 1.579927, 3.637107, 9.814584])

params_star, error = finm.fit(quote_date, df_all, params0)

price_comparison = finm.compare_fit(quote_date, df_all, params_star, actual_params, df)

# Assert that column is close to 0 for all CUSIPs
assert (price_comparison["Predicted - Actual %"].abs() < 0.05).all()
assert (price_comparison["Predicted - GSW %"].abs() < 0.02).all()

# %% [markdown]
# ## Conclusion
#
# The GSW yield curve methodology provides a robust framework for estimating
# the U.S. Treasury yield curve. By carefully implementing their filtering
# criteria and optimization approach, we can replicate their results with
# high accuracy. This implementation allows us to extend their analysis to
# current data and provides a foundation for various fixed-income applications.
#
# Example: Model Performance
# Our implementation typically achieves price errors below 0.02% compared to
# the official GSW yields, demonstrating the reliability of the replication.
