# finm - Financial Mathematics Python Package

A student-led Python package for financial mathematics and quantitative finance
education, created by students and educators at the University of Chicago
Financial Mathematics program.

```{warning}
This package is for **learning purposes only**. There are likely errors in the
implementations, and this software should **NOT** be used for any purposes
beyond education and research.
```

## Quick Start

```python
import finm

# Calculate present value
pv = finm.present_value(
    future_value=1000,
    rate=0.05,
    periods=2
)
print(f"Present Value: ${pv:.2f}")

# Calculate bond price
price = finm.bond_price(
    face_value=1000,
    coupon_rate=0.06,
    ytm=0.05,
    periods=10,
    frequency=2
)
print(f"Bond Price: ${price:.2f}")
```

## Installation

```bash
pip install finm
```

For development installation with all dependencies:

```bash
pip install finm[all]
```

## Features

### Fixed Income Analytics

- **Bond Pricing**: Calculate bond prices with various compounding methods
- **Yield Calculations**: Yield to maturity using Newton-Raphson method
- **Duration & Convexity**: Macaulay duration, modified duration, and convexity
- **Yield Curve Modeling**: Nelson-Siegel-Svensson model implementation
- **GSW Yield Curve**: Replicate the Gurkaynak, Sack, and Wright (2006) methodology

### Data Access

- **Federal Reserve**: Download yield curve parameters from the Fed
- **WRDS**: Pull CRSP Treasury and corporate bond data
- **He-Kelly-Manela**: Access credit risk factor data
- **Open Source Bond**: Load open source bond market returns

## Table of Contents

```{toctree}
:maxdepth: 2
:caption: API Reference

apidocs/index
```

## Indices

- {ref}`genindex`
- {ref}`modindex`
