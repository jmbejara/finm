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
# # Example - Analyzing Corporate Bond Data

# %% [markdown]
# ## Introduction
#
# In this example, we'll explore pulling corporate bond return data from WRDS,
# and running an analysis of returns based on the credit rating.

# %% [markdown]
# ## Imports
#
# We start with establishing the modules required for this example. Set the
# `WRDS_USERNAME` environment variable in your .env file.

# %%
import matplotlib.pyplot as plt
import os
import pandas as pd

from dotenv import load_dotenv
from finm import data
from pathlib import Path

load_dotenv()

DATA_DIR = Path(os.environ.get("DATA_DIR", "./_data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
WRDS_USERNAME = os.environ.get("WRDS_USERNAME", "")

# %% [markdown]
# ## Pull Corporate Bond Data
#
# Next, we will use the `pull_WRDS_corp_bond_monthly` function to pull the
# corporate bond data from WRDS. Refer to the docstring of the function for
# the parameters and fields that are included in the data from WRDS.

# %%
# Load corporate bond data with auto-pull from WRDS if not found locally
# Requires WRDS credentials
df = data.load_wrds_corp_bond(
    data_dir=DATA_DIR,
    pull_if_not_found=True,
    wrds_username=WRDS_USERNAME,
    start_date="2020-01-01",
    end_date="2020-12-31",
).to_pandas()
print(f"Corporate bond data loaded: {df.shape}")
print(df)

# %% [markdown]
# ## Filter Data By Credit Rating
#
# Next, we will investigate the data based on the `r_sp` column, which is the:
#
# - (r_sp) S&P Bond Issue Credit Rating
#
# Here we can identify the counts for each of the ratings:

# %%
# Function to isolate and plot the ratings counts for r_sp, r_mr, and r_fr
def isolate_plot_ratings_counts(rating_col: str):
    ratings_counts = df[rating_col].value_counts().sort_index()

    # Plot bar chart of ratings distribution
    plt.bar(ratings_counts.index, ratings_counts.values)
    plt.title(f"Distribution of Corporate Bond Ratings for {rating_col}")
    plt.xlabel("Ratings")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()
    return ratings_counts

# %%
# r_sp
isolate_plot_ratings_counts("r_sp")

# %%
# r_mr
isolate_plot_ratings_counts("r_mr")

# %%
# r_fr
isolate_plot_ratings_counts("r_fr")


# %% [markdown]
# Based on the above, best to use the r_mr ratings to have the most observations.
# Next, we will drop the NaN rows and look at returns by credit rating.

# %%
df_r_mr = df.dropna(subset=["r_mr", "n_mr"])
print(df_r_mr)

# %%
# Group by date and n_mr, then calculate value weighted returns
grouped = df_r_mr.groupby(["date", "n_mr"])
value_weighted_returns = grouped.apply(
    lambda x: (x["ret_eom"] * x["amount_outstanding"]).sum() / x["amount_outstanding"].sum()
)
value_weighted_returns = value_weighted_returns.reset_index()
value_weighted_returns.columns = ["date", "n_mr", "vw_ret"]
print(value_weighted_returns)

# %%
# Create pivot table of value weighted returns
pivot_table = value_weighted_returns.pivot(index="date", columns="n_mr", values="vw_ret")
print(pivot_table)

# %%
# Plot value weighted returns by credit rating
pivot_table.plot(figsize=(10, 6))
plt.title("Value Weighted Corporate Bond Returns by Credit Rating (r_mr)")
plt.xlabel("Date")
plt.ylabel("Value Weighted Return")
plt.legend(title="Credit Rating (n_mr)")
plt.grid()
plt.tight_layout()
plt.show()

# %%
# Calculate cumulative returns by credit rating
cumulative_returns = (1 + pivot_table).cumprod() - 1
print(cumulative_returns)

# %%
# Plot cumulative returns by credit rating
cumulative_returns.plot(figsize=(10, 6))
plt.title("Cumulative Corporate Bond Returns by Credit Rating (r_mr)")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend(title="Credit Rating (n_mr)")
plt.grid()
plt.tight_layout()
plt.show()

# %%
