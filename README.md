[![PyPI - Version](https://img.shields.io/pypi/v/finm?logo=pypi)](https://pypi.org/project/finm)
[![PyPI - Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue?logo=python)](https://pypi.org/project/finm)
[![GitHub Stars](https://img.shields.io/github/stars/jmbejara/finm?style=flat&logo=github)](https://github.com/jmbejara/finm)
[![Documentation](https://img.shields.io/badge/docs-jeremybejarano.com%2Ffinm-blue)](https://jeremybejarano.com/finm/)

<p align="center">
  <img src="https://raw.githubusercontent.com/jmbejara/finm/main/docs_src/_static/logo.png" alt="finm logo" width="400">
</p>

# finm

A Python package for financial mathematics and quantitative finance education, created by students and educators at the University of Chicago Financial Mathematics program.

> [!CAUTION]
> This package is for **learning purposes only**. There are likely errors in the implementations, and this software should not be used for production trading systems, real financial decision-making, or commercial applications. Always verify calculations independently.

## Installation

```bash
pip install finm
```

For all optional dependencies (CLI, data access):

```bash
pip install finm[all]
```

## Data Access

Load financial data from multiple sources with a consistent interface. See the [Data Module documentation](https://jeremybejarano.com/finm/data_module.html) for details.

> [!IMPORTANT]
> **License Acknowledgment Required:** All data pull functions require `accept_license=True` to confirm you understand that the data is subject to the original provider's licensing terms. See [Data Licensing](#data-licensing) below.

```python
import finm

# Fama-French factors (bundled data, no download needed)
factors = finm.load_fama_french_factors()
factors = finm.load_fama_french_factors(start="2020-01-01", end="2023-12-31")

# Pull fresh data from Ken French's Data Library
finm.pull_fama_french_factors(data_dir="./data", accept_license=True)

# Federal Reserve yield curve (GSW model)
finm.pull_fed_yield_curve(data_dir="./data", accept_license=True)
yields = finm.load_fed_yield_curve(data_dir="./data")

# He-Kelly-Manela intermediary capital factors
finm.pull_he_kelly_manela(data_dir="./data", accept_license=True)
hkm = finm.load_he_kelly_manela_factors_monthly(data_dir="./data")

# Open Source Bond Asset Pricing data
finm.pull_open_source_bond(data_dir="./data", accept_license=True)
treasury = finm.load_treasury_returns(data_dir="./data")
corporate = finm.load_corporate_bond_returns(data_dir="./data")

# WRDS data (requires authentication)
finm.pull_wrds_treasury(
    data_dir="./data",
    wrds_username="your_username",
    start_date="2020-01-01",
    end_date="2023-12-31"
)
```

## Analytics

Calculate risk metrics and factor exposures.

```python
import finm

# Load factors
factors = finm.load_fama_french_factors()

# Fama-French 3-factor exposures
exposures = finm.calculate_factor_exposures(stock_returns, factors)
print(f"Market Beta: {exposures['market_beta']:.3f}")
print(f"SMB Beta:    {exposures['smb_beta']:.3f}")
print(f"HML Beta:    {exposures['hml_beta']:.3f}")
print(f"Sharpe:      {exposures['sharpe_ratio']:.3f}")

# Individual metrics
beta = finm.calculate_beta(stock_returns, market_returns)
sharpe = finm.calculate_sharpe_ratio(returns, risk_free_rate=0.02)
```

## Fixed Income

Bond pricing, duration, and yield curve modeling.

```python
import finm

# Bond pricing
price = finm.bond_price(
    face_value=1000,
    coupon_rate=0.05,
    ytm=0.04,
    periods=10,
    frequency=2  # semiannual
)

# Duration and convexity
dur = finm.duration(1000, 0.05, 0.04, 10, frequency=2)
mod_dur = finm.modified_duration(1000, 0.05, 0.04, 10, frequency=2)
conv = finm.convexity(1000, 0.05, 0.04, 10, frequency=2)

# Yield to maturity
ytm = finm.yield_to_maturity(
    price=1050,
    face_value=1000,
    coupon_rate=0.05,
    periods=10,
    frequency=2
)

# Time value of money
pv = finm.present_value(future_value=1000, rate=0.05, periods=3)
fv = finm.future_value(present_value=1000, rate=0.05, periods=3)
```

The package also includes an implementation of the Gurkaynak-Sack-Wright (2006) yield curve model. See the [API documentation](https://jeremybejarano.com/finm/apidocs/index.html) for `spot`, `discount`, `fit`, and related functions.

## Command Line Interface

Manage data downloads from the terminal. See the [CLI documentation](https://jeremybejarano.com/finm/cli.html) for details.

```bash
# List available datasets
finm list

# Get info about a dataset
finm info fama_french

# Pull data (--accept-license flag required)
finm pull fama_french --data-dir=./data --accept-license
finm pull fed_yield_curve --data-dir=./data --accept-license

# Pull WRDS data (requires credentials)
finm pull wrds_treasury --wrds-username=myuser --start-date=2020-01-01 --end-date=2023-12-31 --accept-license
```

## Documentation

Full documentation is available at [jeremybejarano.com/finm](https://jeremybejarano.com/finm/).

## Data Licensing

> [!WARNING]
> **Third-Party Data Disclaimer:** The `finm.data` module provides convenient access to financial datasets from various third-party sources. **The finm package maintainers are not responsible for the accuracy, completeness, or licensing of this data.** Usage is subject to the original data provider's terms and conditions.

### Citation Requirements

When using data from these sources in academic work, please cite appropriately:

| Data Source | Citation |
|-------------|----------|
| **Fama-French** | Fama, E.F. and French, K.R. (1993). Common Risk Factors in the Returns on Stocks and Bonds. *Journal of Financial Economics* 33(1): 3-56. |
| **Federal Reserve** | Board of Governors of the Federal Reserve System. GSW Yield Curve Data. https://www.federalreserve.gov/ |
| **He-Kelly-Manela** | He, Z., Kelly, B., and Manela, A. (2017). Intermediary Asset Pricing: New Evidence from Many Asset Classes. *Journal of Financial Economics* 126(1): 1-35. |
| **Open Source Bond** | Dickerson, A., Robotti, C., and Rossetti, G. (2026). The Corporate Bond Factor Replication Crisis. Working Paper. |
| **WRDS** | Wharton Research Data Services. https://wrds-www.wharton.upenn.edu/ |

### License Types

| Data Source | License | Terms URL |
|-------------|---------|-----------|
| Fama-French | Copyright Fama & French | [Ken French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) |
| Federal Reserve | Public Domain | [Federal Reserve Disclaimer](https://www.federalreserve.gov/disclaimer.htm) |
| He-Kelly-Manela | Academic Use | [HKM Website](https://asaf.manela.org/papers/hkm/intermediarycapitalrisk/) |
| Open Source Bond | MIT License | [GitHub Repository](https://github.com/Alexander-M-Dickerson/trace-data-pipeline) |
| WRDS | Subscription-based | [WRDS Terms](https://wrds-www.wharton.upenn.edu/) |

### Fair Use

The data access functionality in this package is provided for:
- Educational purposes
- Academic research
- Personal, non-commercial analysis

For commercial use, please consult the original data provider's licensing terms.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

Created and maintained by students and educators at the University of Chicago Financial Mathematics program.
