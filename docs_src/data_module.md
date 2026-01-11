# Data Module Guide

The `finm.data` module provides access to financial data from various sources with a
standardized interface.

## Standard Interface

Each data source submodule follows the same pattern:

```python
from finm.data import federal_reserve

# Download data from source
federal_reserve.pull(data_dir="./data")

# Load cached data (wide format)
df = federal_reserve.load(data_dir="./data")

# Load in long format for time series analysis
df_long = federal_reserve.load(data_dir="./data", format="long")

# Manual conversion to long format
df_long = federal_reserve.to_long_format(df)
```

### Long Format

The long format uses three standard columns:
- `unique_id`: Identifier for the time series (e.g., yield maturity, factor name, CUSIP)
- `ds`: Date
- `y`: Value

This format is useful for panel data analysis and time series forecasting.

## Available Data Sources

### Federal Reserve Yield Curve

GSW (Gurkaynak, Sack, Wright) yield curve model data.

```python
from finm.data import federal_reserve

# Download and save to ./data
federal_reserve.pull(data_dir="./data")

# Load standard yield columns (SVENY01-30)
df = federal_reserve.load(data_dir="./data", variant="standard")

# Load all columns
df_all = federal_reserve.load(data_dir="./data", variant="all")
```

### Fama-French Factors

Fama-French 3 factors from Ken French's Data Library.

```python
from finm.data import fama_french

# Load bundled data (no download needed)
df = fama_french.load()

# Filter by date
df = fama_french.load(start="2020-01-01", end="2023-12-31")

# Download latest data (requires pandas-datareader)
fama_french.pull(data_dir="./data", frequency="daily")
```

### He-Kelly-Manela Factors

Intermediary capital risk factors from He, Kelly, and Manela (2017).

```python
from finm.data import he_kelly_manela

# Download data
he_kelly_manela.pull(data_dir="./data")

# Load variants
df_monthly = he_kelly_manela.load(data_dir="./data", variant="factors_monthly")
df_daily = he_kelly_manela.load(data_dir="./data", variant="factors_daily")
df_all = he_kelly_manela.load(data_dir="./data", variant="all")
```

### Open Source Bond Returns

Treasury and corporate bond returns from Open Bond Asset Pricing.

```python
from finm.data import open_source_bond

# Download both datasets
open_source_bond.pull(data_dir="./data", variant="all")

# Or download individually
open_source_bond.pull(data_dir="./data", variant="treasury")
open_source_bond.pull(data_dir="./data", variant="corporate")

# Load data
treasury = open_source_bond.load(data_dir="./data", variant="treasury")
corporate = open_source_bond.load(data_dir="./data", variant="corporate")
```

### WRDS Data (Requires Credentials)

CRSP Treasury and corporate bond data from WRDS.

```python
from finm.data import wrds

# Pull Treasury data
wrds.pull(
    data_dir="./data",
    variant="treasury",
    wrds_username="your_username",
    start_date="2020-01-01",
    end_date="2023-12-31",
)

# Pull corporate bond data
wrds.pull(
    data_dir="./data",
    variant="corp_bond",
    wrds_username="your_username",
    start_date="2020-01-01",
    end_date="2023-12-31",
)

# Load from cache
df_treasury = wrds.load(data_dir="./data", variant="treasury")
df_corp = wrds.load(data_dir="./data", variant="corp_bond")
```

## Convenience Functions

The data module also provides descriptive function names at the module level:

```python
from finm import data

# Federal Reserve
data.pull_fed_yield_curve(data_dir="./data")
df = data.load_fed_yield_curve(data_dir="./data")

# Fama-French
df = data.load_fama_french_factors()

# He-Kelly-Manela
data.pull_he_kelly_manela(data_dir="./data")
df = data.load_he_kelly_manela_factors_monthly(data_dir="./data")

# Open Source Bond
data.pull_open_source_bond(data_dir="./data")
df = data.load_treasury_returns(data_dir="./data")
df = data.load_corporate_bond_returns(data_dir="./data")

# WRDS
data.pull_wrds_treasury(data_dir="./data", wrds_username="user", ...)
df = data.load_wrds_treasury(data_dir="./data")
```
