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
# # Factor Regression Analysis with finm
#
# This notebook demonstrates how to use the `finm` package to perform
# factor regression analysis, including CAPM and Fama-French 3-factor models.
#
# ## Learning Objectives
#
# 1. Understand Jensen's alpha and factor betas
# 2. Run CAPM regression and interpret results
# 3. Run Fama-French 3-factor regression
# 4. Interpret statistical significance of alpha and betas
#
# ## Key Functions
#
# - `finm.run_factor_regression()` - Core OLS regression with full statistics
# - `finm.run_capm_regression()` - Convenience wrapper for CAPM
# - `finm.run_fama_french_regression()` - Convenience wrapper for FF3

# %%
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dotenv import load_dotenv

import finm
from finm.data import fama_french

load_dotenv()

DATA_DIR = Path(os.environ.get("DATA_DIR", "./_data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

print(f"Data directory: {DATA_DIR}")

# %% [markdown]
# ## 1. Load Fama-French Factors
#
# The Fama-French 3-factor model includes:
# - **Mkt-RF**: Market excess return (market return minus risk-free rate)
# - **SMB**: Small Minus Big (size factor)
# - **HML**: High Minus Low (value factor)
# - **RF**: Risk-free rate

# %%
# Load Fama-French data from bundled data
ff_factors = fama_french.load(data_dir=None).to_pandas()
ff_factors = ff_factors.set_index("Date")
print(f"Fama-French factors shape: {ff_factors.shape}")
print(f"Date range: {ff_factors.index.min()} to {ff_factors.index.max()}")
ff_factors.head()

# %% [markdown]
# ## 2. Create Synthetic Portfolio Returns
#
# For demonstration, we'll create synthetic portfolio returns with known
# characteristics. In practice, you would use actual portfolio or asset returns.

# %%
# Create synthetic portfolio returns with known factor exposures
np.random.seed(42)

# Use a subset of dates
dates = ff_factors.index[-120:]  # Last 10 years of monthly data
factors = ff_factors.loc[dates]

# Simulate a portfolio with:
# - Market beta = 1.2
# - SMB beta = 0.5 (tilted toward small caps)
# - HML beta = 0.3 (tilted toward value)
# - Alpha = 0.002 per month (about 2.4% annually)

market_beta = 1.2
smb_beta = 0.5
hml_beta = 0.3
monthly_alpha = 0.002

# Generate portfolio excess returns
noise = np.random.randn(len(dates)) * 0.01
portfolio_excess = (
    monthly_alpha
    + market_beta * factors["Mkt-RF"]
    + smb_beta * factors["SMB"]
    + hml_beta * factors["HML"]
    + noise
)

# Raw returns = excess returns + risk-free rate
portfolio_returns = portfolio_excess + factors["RF"]

print("Synthetic portfolio created with known exposures:")
print(f"  Target Market Beta: {market_beta}")
print(f"  Target SMB Beta: {smb_beta}")
print(f"  Target HML Beta: {hml_beta}")
print(f"  Target Monthly Alpha: {monthly_alpha}")

# %% [markdown]
# ## 3. CAPM Regression
#
# The Capital Asset Pricing Model (CAPM) regresses portfolio excess returns
# on market excess returns:
#
# $$R_p - R_f = \alpha + \beta (R_m - R_f) + \epsilon$$
#
# Where:
# - $R_p$ is portfolio return
# - $R_f$ is risk-free rate
# - $R_m$ is market return
# - $\alpha$ is Jensen's alpha (abnormal return)
# - $\beta$ is market beta (systematic risk)

# %%
# Run CAPM regression
capm_result = finm.run_capm_regression(
    excess_returns=portfolio_excess,
    market_excess_returns=factors["Mkt-RF"],
    annualization_factor=12,  # Monthly data, annualize alpha
)

print("CAPM Regression Results")
print("=" * 50)
print(f"Alpha (monthly):     {capm_result.alpha:>10.4f}")
print(f"Alpha (annualized):  {capm_result.alpha_annualized:>10.2%}")
print(f"Alpha t-stat:        {capm_result.alpha_tstat:>10.2f}")
print(f"Alpha p-value:       {capm_result.alpha_pvalue:>10.4f}")
print(f"")
print(f"Market Beta:         {capm_result.betas['Mkt-RF']:>10.2f}")
print(f"Beta t-stat:         {capm_result.beta_tstats['Mkt-RF']:>10.2f}")
print(f"Beta p-value:        {capm_result.beta_pvalues['Mkt-RF']:>10.4f}")
print(f"")
print(f"R-squared:           {capm_result.r_squared:>10.2%}")
print(f"Observations:        {capm_result.n_observations:>10d}")

# %% [markdown]
# ### Interpretation of CAPM Results
#
# - **Alpha**: The intercept represents Jensen's alpha - the average return
#   not explained by market exposure. A positive alpha suggests outperformance.
#
# - **Beta**: Measures sensitivity to market movements. Beta > 1 means the
#   portfolio is more volatile than the market.
#
# - **t-statistic**: Tests if the coefficient is significantly different from
#   zero. Generally, |t| > 2 is considered statistically significant.
#
# - **p-value**: Probability of observing this result if the true coefficient
#   is zero. p < 0.05 is often used as a significance threshold.
#
# - **R-squared**: Proportion of variance explained by the model.

# %% [markdown]
# ## 4. Fama-French 3-Factor Regression
#
# The Fama-French 3-factor model extends CAPM by adding size and value factors:
#
# $$R_p - R_f = \alpha + \beta_{MKT}(R_m - R_f) + \beta_{SMB} \cdot SMB + \beta_{HML} \cdot HML + \epsilon$$
#
# This model captures additional sources of systematic risk:
# - **SMB (Small Minus Big)**: Return of small-cap stocks minus large-cap stocks
# - **HML (High Minus Low)**: Return of value stocks minus growth stocks

# %%
# Run Fama-French 3-factor regression
ff_result = finm.run_fama_french_regression(
    returns=portfolio_returns,
    factors=factors,
    annualization_factor=12,
)

print("Fama-French 3-Factor Regression Results")
print("=" * 50)
print(f"Alpha (monthly):     {ff_result.alpha:>10.4f}")
print(f"Alpha (annualized):  {ff_result.alpha_annualized:>10.2%}")
print(f"Alpha t-stat:        {ff_result.alpha_tstat:>10.2f}")
print(f"Alpha p-value:       {ff_result.alpha_pvalue:>10.4f}")
print(f"")
print("Factor Betas:")
for factor in ["Mkt-RF", "SMB", "HML"]:
    print(
        f"  {factor:8s}:        {ff_result.betas[factor]:>10.2f}  "
        f"(t={ff_result.beta_tstats[factor]:>6.2f}, p={ff_result.beta_pvalues[factor]:.4f})"
    )
print(f"")
print(f"R-squared:           {ff_result.r_squared:>10.2%}")
print(f"Adj R-squared:       {ff_result.adj_r_squared:>10.2%}")
print(f"Observations:        {ff_result.n_observations:>10d}")

# %% [markdown]
# ### Comparing CAPM and FF3 Results
#
# Notice how the results change when we account for size and value exposures:
# - The market beta changes when we control for other factors
# - The R-squared increases (more variance explained)
# - Alpha may change as the model explains more of the returns

# %%
# Create comparison table
comparison_data = {
    "Statistic": ["Alpha (monthly)", "Alpha (annual)", "Alpha t-stat", "Market Beta", "R-squared"],
    "CAPM": [
        f"{capm_result.alpha:.4f}",
        f"{capm_result.alpha_annualized:.2%}",
        f"{capm_result.alpha_tstat:.2f}",
        f"{capm_result.betas['Mkt-RF']:.2f}",
        f"{capm_result.r_squared:.2%}",
    ],
    "FF3": [
        f"{ff_result.alpha:.4f}",
        f"{ff_result.alpha_annualized:.2%}",
        f"{ff_result.alpha_tstat:.2f}",
        f"{ff_result.betas['Mkt-RF']:.2f}",
        f"{ff_result.r_squared:.2%}",
    ],
}
comparison_df = pd.DataFrame(comparison_data)
print("Model Comparison")
print("=" * 50)
print(comparison_df.to_string(index=False))

# %% [markdown]
# ## 5. Using the Generic run_factor_regression()
#
# The `run_factor_regression()` function is the core function that handles
# both single-factor and multi-factor regressions. It provides full flexibility
# for custom factor models.

# %%
# Example: Run a custom 2-factor model (Market + SMB only)
custom_factors = factors[["Mkt-RF", "SMB"]]

custom_result = finm.run_factor_regression(
    returns=portfolio_excess,
    factors=custom_factors,
    annualization_factor=12,
)

print("Custom 2-Factor Model (Market + SMB)")
print("=" * 50)
print(f"Alpha (annualized):  {custom_result.alpha_annualized:>10.2%}")
for factor_name, beta in custom_result.betas.items():
    print(f"{factor_name} Beta:         {beta:>10.2f}")
print(f"R-squared:           {custom_result.r_squared:>10.2%}")

# %% [markdown]
# ## 6. Accessing the RegressionResult Dataclass
#
# The `RegressionResult` dataclass provides a structured way to access
# all regression statistics. Here's a complete view of available attributes:

# %%
# Display all available attributes
print("RegressionResult Attributes")
print("=" * 50)
print(f"alpha:             {ff_result.alpha}")
print(f"alpha_tstat:       {ff_result.alpha_tstat}")
print(f"alpha_pvalue:      {ff_result.alpha_pvalue}")
print(f"alpha_se:          {ff_result.alpha_se}")
print(f"betas:             {ff_result.betas}")
print(f"beta_tstats:       {ff_result.beta_tstats}")
print(f"beta_pvalues:      {ff_result.beta_pvalues}")
print(f"beta_ses:          {ff_result.beta_ses}")
print(f"r_squared:         {ff_result.r_squared}")
print(f"adj_r_squared:     {ff_result.adj_r_squared}")
print(f"n_observations:    {ff_result.n_observations}")
print(f"residual_std:      {ff_result.residual_std}")
print(f"alpha_annualized:  {ff_result.alpha_annualized}")
print(f"annualization_factor: {ff_result.annualization_factor}")

# %% [markdown]
# ## Summary
#
# This notebook demonstrated:
#
# 1. **`run_capm_regression()`**: Single-factor model for market beta and alpha
# 2. **`run_fama_french_regression()`**: Three-factor model with size and value
# 3. **`run_factor_regression()`**: Generic function for custom factor models
# 4. **`RegressionResult`**: Dataclass containing all regression statistics
#
# ### Key Takeaways
#
# - Alpha represents the abnormal return not explained by factor exposures
# - Betas measure sensitivity to each factor
# - T-statistics and p-values indicate statistical significance
# - R-squared shows how much variance is explained by the model
# - Adding more factors typically increases R-squared but may reduce alpha
