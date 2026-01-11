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
# # Cleaning Summary: Corporate Bond Returns

# %%
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv

import finm
from finm.data import open_source_bond

load_dotenv()

DATA_DIR = Path(os.environ.get("DATA_DIR", "./_data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

print(f"Data directory: {DATA_DIR}")

# %% [markdown]
# ## Data Cleaning - He, Kelly, and Manella (HKM) follow Nozawa (2017)
#
# The data cleaning procedure used by **He, Kelly, and Manella** is based on
# the meticulous framework established in **Nozawa (2017)**. This process
# ensures consistency, comparability, and robustness in corporate bond
# return analysis.

# %% [markdown]
# ## Data Cleaning Summary - Nozawa (2017)
#
# Nozawa (2017) constructs a high-quality corporate bond dataset by applying
# the following key cleaning steps:
#
# ### Bond Selection Criteria
#
# * **Exclude bonds** with:
#   * **Floating rate coupons**
#   * **Non-callable option features** (e.g., puts, convertibles). However,
#     callable bonds are retained due to their prevalence in historical data.
# * **Price filters**:
#   * Remove observations where the **corporate bond price exceeds** the price
#     of its matched Treasury.
#   * Drop observations where price < **$0.01 per $1 face value**.
# * **Return reversals**:
#   * Eliminate both return observations if the **product of adjacent returns
#     is < -0.04**, suggesting a data entry error or extreme correction.
#
# ### Data Sources Used
#
# * Combined data from:
#   * **Lehman Brothers Fixed Income Database**
#   * **Mergent FISD/NAIC Database**
#   * **TRACE**
#   * **DataStream**
# * Defaults are verified and completed using **Moody's Default Risk Service**.
# * **CRSP** and **Compustat** are used to supplement with equity and
#   accounting data.
#
# ### Synthetic Treasury Construction
#
# * For each corporate bond, a **synthetic Treasury bond** with an identical
#   cash flow structure is constructed.
# * Treasury prices are based on **Federal Reserve constant-maturity yield data**.
# * This enables clean computation of **excess returns** and **credit spreads**,
#   expressed in **price terms** rather than yield spreads, to maintain
#   linearity and reduce approximation error.
#
# ### Additional Adjustments
#
# * Callable bonds are retained and accounted for using **fixed effects** in
#   regression models (callability has minor pricing impact, ~9 bps).
# * The study uses **monthly returns**, avoiding the need for reinvestment
#   assumptions.

# %% [markdown]
# This rigorous cleaning pipeline underpins Nozawa's variance decomposition
# framework, enabling a reliable split of credit spreads into **expected
# credit loss** and **risk premium** components.

# %%
# Pull the He-Kelly-Manela data
finm.pull_he_kelly_manela(data_dir=DATA_DIR, accept_license=True)

# %%
hkm = finm.load_he_kelly_manela_all(data_dir=DATA_DIR)
copr_bonds_hkm = hkm.iloc[:, 44:54].copy()
copr_bonds_hkm["yyyymm"] = hkm["yyyymm"]
copr_bonds_hkm.head()

# %%
copr_bonds_hkm.tail()

# %%
copr_bonds_hkm.describe()

# %%
copr_bonds_hkm.isnull().sum()

# %% [markdown]
# ## Open Source Bond Asset Pricing Data
#
# The Open Source Bond Asset Pricing project provides:
# - **Monthly corporate bond returns** with 108 factor signals
# - Data based on TRACE (Trade Reporting and Compliance Engine)
# - Market microstructure-adjusted prices and returns
#
# Website: [openbondassetpricing.com](https://openbondassetpricing.com/)
# GitHub: [trace-data-pipeline](https://github.com/Alexander-M-Dickerson/trace-data-pipeline)

# %% [markdown]
# ## Data Cleaning and Construction - Following Nozawa (2017)
#
# The dataset adheres to the rigorous data cleaning methodology
# established by Nozawa (2017), ensuring high-quality and reliable corporate
# bond return data. The key cleaning steps are mentioned above.

# %% [markdown]
# ## Understanding the TRACE Dataset
#
# The TRACE dataset is meticulously curated to provide accurate and
# comprehensive corporate bond data. Key aspects include:
#
# * **Market Microstructure Adjustments**:
#   * Implementation of corrections for market microstructure noise (MMN) to
#     enhance the reliability of bond price and return data.
#
# * **Data Filters**:
#   * Application of stringent filters to ensure data quality, such as:
#     * Inclusion of only U.S.-domiciled firms.
#     * Exclusion of private placements, convertible bonds, and bonds with
#       non-standard interest payment structures.
#     * Removal of bonds with insufficient outstanding amounts or missing
#       critical information.
#
# By leveraging the TRACE dataset from openbondassetpricing.com, the
# dataset ensures a robust foundation for analyzing corporate bond returns,
# adhering to established methodologies and incorporating comprehensive data
# cleaning procedures.

# %%
# Pull corporate bond monthly returns from Open Source Bond Asset Pricing
open_source_bond.pull(
    data_dir=DATA_DIR,
    variant="corporate_monthly",
    accept_license=True,
)
print("Corporate bond data downloaded successfully.")

# %%
corp_bonds_returns = finm.calc_corp_bond_returns(data_dir=DATA_DIR)

# %%
corp_bonds_returns.describe()

# %% [markdown]
# ## How Returns Are Computed
#
# For each decile, the **monthly return** is computed as a **value-weighted
# average of bond-level returns**:
#
# $$
# r_{portfolio, t} = \sum_{i \in \text{portfolio}} w_{i,t} \cdot \text{bond\_ret}_{i,t}
# $$
#
# where:
#
# * `bond_ret` is the **monthly return** of an individual bond.
# * $w_{i,t} = \frac{\text{bond value}_{i,t}}{\sum_{j \in \text{portfolio}} \text{bond value}_{j,t}}$
#   is the **weight** of bond $i$ in the portfolio at time $t$.
# * `bond value` is calculated as the product of the **MMN-adjusted clean price**
#   and **amount outstanding**.
#
# This weighting ensures that larger bonds have a proportionally larger impact
# on the portfolio return.

# %% [markdown]
# ## Comparing FTSFR with He Kelly Manela

# %%
# Convert yyyymm to datetime (last day of each month)
copr_bonds_hkm["date"] = pd.to_datetime(
    copr_bonds_hkm["yyyymm"].astype(int).astype(str), format="%Y%m"
) + pd.offsets.MonthEnd(0)
copr_bonds_hkm.set_index("date", inplace=True)

# Now both DataFrames have datetime index with last day of month
print("HKM Corporate Bonds shape:", copr_bonds_hkm.shape)
print("Corporate Bond Returns shape:", corp_bonds_returns.shape)

# Display the date ranges to verify alignment
print(
    "\nHKM Corporate Bonds date range:",
    copr_bonds_hkm.index.min(),
    "to",
    copr_bonds_hkm.index.max(),
)
print(
    "Corporate Bond Returns date range:",
    corp_bonds_returns.index.min(),
    "to",
    corp_bonds_returns.index.max(),
)

# Merge the dataframes
merged_df = pd.merge(
    corp_bonds_returns, copr_bonds_hkm, left_index=True, right_index=True, how="inner"
)

# Create subplots for each pair of columns
fig, axes = plt.subplots(5, 2, figsize=(15, 20))
axes = axes.flatten()

for i in range(10):
    col1 = i + 1  # Column from corp_bonds_returns
    col2 = f"US_bonds_{i + 11}"  # Column from copr_bonds_hkm

    ax = axes[i]
    ax.plot(merged_df.index, merged_df[col1], label=f"Decile {i + 1}", color="blue")
    ax.plot(merged_df.index, merged_df[col2], label=f"HKM {i + 11}", color="red")
    ax.set_title(f"Comparison: Decile {i + 1} vs HKM {i + 11}")
    ax.legend()
    ax.grid(True)

    # Rotate x-axis labels for better readability
    plt.setp(ax.get_xticklabels(), rotation=45)

plt.tight_layout()
plt.show()

# Print correlation between corresponding columns
print("\nCorrelations between corresponding columns:")
for i in range(10):
    col1 = i + 1
    col2 = f"US_bonds_{i + 11}"
    corr = merged_df[col1].corr(merged_df[col2])
    print(f"Decile {i + 1} vs HKM {i + 11}: {corr:.4f}")

# %% [markdown]
# ## Comparison of Corporate Bond Portfolio Returns: FTSFR Deciles vs. HKM Portfolios
#
# The figure above compares the time-series returns of corporate bond portfolios:
#
# * **Deciles 1-10** (in blue): Portfolios constructed by **FTSFR**, where bonds
#   are sorted into deciles based on a chosen signal.
# * **HKM Portfolios 11-20** (in red): Portfolios from **He, Kelly, and Manella
#   (HKM)** that correspond to the same strategy but are indexed from 11 to 20.
#
# The HKM portfolios are indexed from **11 to 20**, with portfolio 11
# corresponding to the lowest decile (Decile 1) and portfolio 20 corresponding
# to the highest (Decile 10). Therefore, the matching scheme is:
#
# * **Decile 1 -> HKM 11**
# * **Decile 2 -> HKM 12**
# * ...
# * **Decile 5 -> HKM 15**
# * ...
# * **Decile 10 -> HKM 20**

# %% [markdown]
# ## Observations
#
# * The plotted returns between **FTSFR deciles (blue)** and **HKM portfolios
#   (red)** are **visibly similar**, indicating that both datasets reflect
#   consistent underlying return dynamics.
# * Particularly during volatile periods like the **2008 financial crisis**,
#   both series exhibit synchronized spikes or drops, reflecting shared
#   exposure to credit market risk.
# * Deviations are expected due to:
#   * Variation in data sources and MMN adjustments.
#   * Differences in exact sorting filters.
#
# These comparisons validate that the FTSFR replication accurately captures
# the structure and behavior of the HKM portfolio.
