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
# # Data Module Integration Tests
#
# This notebook provides integration tests for the `finm.data` module by:
# 1. Pulling each data source
# 2. Creating simple visualizations
# 3. Calculating factor exposures for asset return data
#
# **Data Sources:**
# - **Factor Data:** Fama-French 3 factors, Federal Reserve yield curve, He-Kelly-Manela factors
# - **Asset Returns:** Open Source Bond (treasury and corporate returns)

# %%
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv

import finm
from finm.data import fama_french, federal_reserve, he_kelly_manela, open_source_bond

load_dotenv()

DATA_DIR = Path(os.environ.get("DATA_DIR", "./_data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

print(f"Data directory: {DATA_DIR}")

# %% [markdown]
# ## 1. Fama-French Factors
#
# The Fama-French 3-factor model provides:
# - **Mkt-RF**: Market excess return
# - **SMB**: Small Minus Big (size factor)
# - **HML**: High Minus Low (value factor)
# - **RF**: Risk-free rate

# %%
# Load Fama-French data from bundled data (data_dir=None)
ff_factors = fama_french.load(
    data_dir=None,
).to_pandas()
ff_factors = ff_factors.set_index("Date")
print(f"Loaded Fama-French factors (converted to pandas DataFrame)")
print(f"\nFama-French factors shape: {ff_factors.shape}")
print(f"Columns: {ff_factors.columns}")
ff_factors.head()

# %%
# Plot Fama-French factors
fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

# Cumulative returns for each factor
for ax, factor in zip(axes, ["Mkt-RF", "SMB", "HML"]):
    cumulative = (1 + ff_factors[factor]).cumprod()
    ax.plot(cumulative.index, cumulative.values)
    ax.set_ylabel(factor)
    ax.set_title(f"{factor} Cumulative Return")
    ax.grid(True, alpha=0.3)

plt.xlabel("Date")
plt.tight_layout()
plt.show()

# %%
# Summary statistics
print("\nFama-French Factor Statistics (Daily):")
print(ff_factors[["Mkt-RF", "SMB", "HML", "RF"]].describe())

# %% [markdown]
# ## 2. Federal Reserve Yield Curve
#
# The GSW (Gurkaynak, Sack, Wright) yield curve provides:
# - Zero-coupon yields for maturities 1-30 years
# - Nelson-Siegel-Svensson model parameters
#
# **Note:** These are yields, not returns.

# %%
# Load Federal Reserve yield curve data with auto-pull
yields = federal_reserve.load(
    data_dir=DATA_DIR,
    variant="standard",
    pull_if_not_found=True,
    accept_license=True,
).to_pandas()
yields = yields.set_index("Date")

print(f"Yield curve shape: {yields.shape}")
print(f"Columns: {yields.columns}")
yields.head()

# %%
# Plot yield curve snapshot for the most recent date
latest_date = yields.index.max()
latest_yields = yields.loc[latest_date]

maturities = [int(col.replace("SVENY", "")) for col in latest_yields.index]

plt.figure(figsize=(10, 6))
plt.plot(maturities, latest_yields.values, "o-", linewidth=2, markersize=6)
plt.xlabel("Maturity (Years)")
plt.ylabel("Yield (%)")
plt.title(f"U.S. Treasury Yield Curve ({latest_date.strftime('%Y-%m-%d')})")
plt.grid(True, alpha=0.3)
plt.show()

# %%
# Plot time series of key maturities
key_maturities = ["SVENY02", "SVENY05", "SVENY10", "SVENY30"]
labels = ["2-Year", "5-Year", "10-Year", "30-Year"]

plt.figure(figsize=(12, 6))
for col, label in zip(key_maturities, labels):
    if col in yields.columns:
        plt.plot(yields.index, yields[col], label=label, alpha=0.8)

plt.xlabel("Date")
plt.ylabel("Yield (%)")
plt.title("U.S. Treasury Yields Over Time")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# %% [markdown]
# ## 3. He-Kelly-Manela Intermediary Factors
#
# The HKM factors capture:
# - **Intermediary capital ratio**: Capital of financial intermediaries
# - **Intermediary capital risk factor**: Innovation in capital ratio
#
# **Note:** These are factors, not asset returns.

# %%
# Load He-Kelly-Manela data with auto-pull
hkm_monthly = he_kelly_manela.load(
    data_dir=DATA_DIR,
    variant="factors_monthly",
    pull_if_not_found=True,
    accept_license=True,
).to_pandas()
hkm_monthly = hkm_monthly.set_index("yyyymm")

print(f"HKM monthly factors shape: {hkm_monthly.shape}")
print(f"Columns: {hkm_monthly.columns}")
hkm_monthly.head()

# %%
# Plot intermediary capital ratio
if "intermediary_capital_ratio" in hkm_monthly.columns:
    plt.figure(figsize=(12, 5))
    plt.plot(hkm_monthly.index, hkm_monthly["intermediary_capital_ratio"])
    plt.xlabel("Date")
    plt.ylabel("Capital Ratio")
    plt.title("Intermediary Capital Ratio Over Time")
    plt.grid(True, alpha=0.3)
    plt.show()
elif "capital_ratio" in hkm_monthly.columns:
    plt.figure(figsize=(12, 5))
    plt.plot(hkm_monthly.index, hkm_monthly["capital_ratio"])
    plt.xlabel("Date")
    plt.ylabel("Capital Ratio")
    plt.title("Intermediary Capital Ratio Over Time")
    plt.grid(True, alpha=0.3)
    plt.show()
else:
    print("Available columns:", list(hkm_monthly.columns))

# %% [markdown]
# ## 4. Open Source Bond Returns
#
# The Open Bond Asset Pricing project provides:
# - **Treasury bond returns**: Government bond returns
# - **Corporate bond monthly returns**: Monthly returns with 108 factor signals
# - **Corporate bond daily prices**: Daily prices from TRACE Stage 1
#
# These are **asset returns** that can be used for factor analysis.

# %%
# Load treasury returns with auto-pull if not found locally
treasury = open_source_bond.load(
    data_dir=DATA_DIR,
    variant="treasury",
    pull_if_not_found=True,
    accept_license=True,
).to_pandas()
print(f"Treasury returns shape: {treasury.shape}")
print(f"Treasury columns: {list(treasury.columns[:10])}...")

# %%
# Load corporate bond returns (monthly with factor signals) with auto-pull
corporate = open_source_bond.load(
    data_dir=DATA_DIR,
    variant="corporate_monthly",
    pull_if_not_found=True,
    accept_license=True,
).to_pandas()
print(f"Corporate returns shape: {corporate.shape}")
print(f"Corporate columns: {list(corporate.columns[:10])}...")
corporate.head()

# %%
# Plot treasury returns if available
if "bond_ret" in treasury.columns:
    # Aggregate treasury returns
    treasury_agg = treasury.groupby("date")["bond_ret"].mean()

    plt.figure(figsize=(12, 5))
    cumulative = (1 + treasury_agg).cumprod()
    plt.plot(cumulative.index, cumulative.values)
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.title("Average Treasury Bond Cumulative Returns")
    plt.grid(True, alpha=0.3)
    plt.show()
elif "ret" in treasury.columns:
    treasury_agg = treasury.groupby("date")["ret"].mean()

    plt.figure(figsize=(12, 5))
    cumulative = (1 + treasury_agg).cumprod()
    plt.plot(cumulative.index, cumulative.values)
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.title("Average Treasury Bond Cumulative Returns")
    plt.grid(True, alpha=0.3)
    plt.show()
else:
    print("Treasury columns:", list(treasury.columns))

# %%
# Plot corporate bond returns
# Note: Monthly corporate data uses ret_vw (volume-weighted total return)
ret_col = "ret_vw" if "ret_vw" in corporate.columns else "bond_ret"
if ret_col in corporate.columns:
    # Aggregate corporate returns by date (equal-weighted across bonds)
    corp_agg = corporate.groupby("date")[ret_col].mean()

    plt.figure(figsize=(12, 5))
    cumulative = (1 + corp_agg.dropna()).cumprod()
    plt.plot(cumulative.index, cumulative.values)
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.title("Average Corporate Bond Cumulative Returns (Volume-Weighted)")
    plt.grid(True, alpha=0.3)
    plt.show()
else:
    print("Corporate columns:", list(corporate.columns))

# %% [markdown]
# ## 5. Factor Analysis (Asset Returns Only)
#
# We calculate factor exposures for bond returns against the Fama-French factors.
# This analysis only applies to asset return data (Open Source Bond), not to
# yields (Federal Reserve) or factor data (HKM).

# %%
# Prepare Fama-French factors for merging
# Resample to monthly if needed for bond data
ff_monthly = ff_factors.resample("ME").last()
print(f"Monthly FF factors shape: {ff_monthly.shape}")

# %%
# Calculate factor exposures for corporate bonds
# Note: Monthly corporate data uses ret_vw (volume-weighted total return)
corp_ret_col = "ret_vw" if "ret_vw" in corporate.columns else "bond_ret"
if corp_ret_col in corporate.columns and "date" in corporate.columns:
    # Aggregate corporate returns by date (equal-weighted portfolio)
    corp_monthly = corporate.groupby("date")[corp_ret_col].mean()
    corp_monthly.index = pd.to_datetime(corp_monthly.index)

    # Resample to month-end to align with FF factors
    corp_monthly = corp_monthly.resample("ME").mean()

    # Calculate factor exposures
    exposures_corp = finm.calculate_factor_exposures(
        corp_monthly,
        ff_monthly,
        annualization_factor=12.0,  # Monthly data
    )

    print("\nCorporate Bond Factor Exposures:")
    print("-" * 40)
    for key, value in exposures_corp.items():
        print(f"  {key}: {value:.4f}")

# %%
# Calculate factor exposures for treasury bonds
if "bond_ret" in treasury.columns:
    # Aggregate treasury returns by date
    treas_monthly = treasury.groupby("date")["bond_ret"].mean()
    treas_monthly.index = pd.to_datetime(treas_monthly.index)
    treas_monthly = treas_monthly.resample("ME").mean()

    exposures_treas = finm.calculate_factor_exposures(
        treas_monthly, ff_monthly, annualization_factor=12.0
    )

    print("\nTreasury Bond Factor Exposures:")
    print("-" * 40)
    for key, value in exposures_treas.items():
        print(f"  {key}: {value:.4f}")
elif "ret" in treasury.columns:
    treas_monthly = treasury.groupby("date")["ret"].mean()
    treas_monthly.index = pd.to_datetime(treas_monthly.index)
    treas_monthly = treas_monthly.resample("ME").mean()

    exposures_treas = finm.calculate_factor_exposures(
        treas_monthly, ff_monthly, annualization_factor=12.0
    )

    print("\nTreasury Bond Factor Exposures:")
    print("-" * 40)
    for key, value in exposures_treas.items():
        print(f"  {key}: {value:.4f}")

# %%
# Summary comparison table
if "exposures_corp" in dir() and "exposures_treas" in dir():
    summary = pd.DataFrame(
        {
            "Corporate Bonds": exposures_corp,
            "Treasury Bonds": exposures_treas,
        }
    ).T

    print("\nFactor Exposure Comparison:")
    print("=" * 60)
    print(summary.to_string())

# %% [markdown]
# ## 6. WRDS Data (Optional)
#
# WRDS data requires authentication. This section is skipped if credentials
# are not available.

# %%
# Check for WRDS credentials
WRDS_USERNAME = os.environ.get("WRDS_USERNAME", "")

if WRDS_USERNAME:
    print(f"WRDS username found: {WRDS_USERNAME}")
    print("WRDS data pull is available but skipped in this notebook.")
    print("To pull WRDS data, use:")
    print("  from finm.data import wrds")
    print(
        "  wrds.pull(data_dir=DATA_DIR, variant='treasury', wrds_username=WRDS_USERNAME)"
    )
else:
    print("WRDS credentials not found.")
    print("To use WRDS data, set the WRDS_USERNAME environment variable:")
    print("  export WRDS_USERNAME=your_username")
    print("Or add to your .env file:")
    print("  WRDS_USERNAME=your_username")

# %% [markdown]
# ## Summary
#
# This notebook demonstrated:
#
# 1. **Fama-French Factors**: Loaded and visualized the 3-factor model data
# 2. **Federal Reserve Yield Curve**: Downloaded GSW yields and plotted the term structure
# 3. **He-Kelly-Manela Factors**: Pulled intermediary capital factor data
# 4. **Open Source Bond Returns**: Downloaded treasury and corporate bond returns
# 5. **Factor Analysis**: Calculated factor exposures for bond returns
#
# All data sources follow the standardized interface:
# - `pull(data_dir, accept_license=True)`: Download data from source
# - `load(data_dir, variant, pull_if_not_found, accept_license)`: Load cached data (returns polars DataFrame)
# - `to_long_format(df)`: Convert to long format
#
# **Note:** When using `pull_if_not_found=True`, you must also set `accept_license=True`
# to acknowledge the data provider's licensing terms. See each module's `LICENSE_INFO` for details.
