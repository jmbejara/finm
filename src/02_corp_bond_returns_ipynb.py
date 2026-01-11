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
import os
from pathlib import Path

import matplotlib.pyplot as plt
from dotenv import load_dotenv

import finm

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
df = finm.load_wrds_corp_bond(
    data_dir=DATA_DIR,
    pull_if_not_found=True,
    wrds_username=WRDS_USERNAME,
    start_date="2020-01-01",
    end_date="2020-12-31",
).to_pandas()
print(f"Corporate bond data loaded: {df.shape}")
df

# %% [markdown]
# ## Filter Data By Credit Rating
#
# Next, we will investigate the data based on the `r_sp` column, which is the:
#
# - (r_sp) S&P Bond Issue Credit Rating
#
# Here we can identify the counts for each of the ratings:

# %%
# Isolate the ratings counts for r_sp
r_sp_ratings_counts = df["r_sp"].value_counts().sort_index()
r_sp_ratings_counts

# %% [markdown]
# And then plot the distribution:

# %%
# Plot bar chart of ratings distribution
plt.bar(r_sp_ratings_counts.index, r_sp_ratings_counts.values)
plt.title("Distribution of Corporate Bond Ratings (r_sp)")
plt.xlabel("Ratings")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.tight_layout()
plt.show()

# %% [markdown]
# Interestingly, we can see that many of the rows 177,706 out of 290,831
# do not have a rating.
