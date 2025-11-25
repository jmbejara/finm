# finm

**Financial Mathematics Python Package**

A student-led Python package for financial mathematics and quantitative finance education, created by students and educators at the **University of Chicago Financial Mathematics** program.

---

> ⚠️ **IMPORTANT DISCLAIMER**
>
> This package is for **learning purposes only**. There are likely errors in the implementations, and this software should **NOT** be used for any purposes beyond education and research. The authors make no guarantees about the correctness, accuracy, or reliability of any calculations.
>
> **Do not use this package for:**
> - Production trading systems
> - Real financial decision-making
> - Any commercial applications
>
> If you need reliable financial calculations, please use professionally audited and maintained libraries.

---

## About

**finm** is a collaborative, open-source project designed to help students learn financial mathematics concepts through practical Python implementations. The package covers various topics in quantitative finance including:

- Fixed Income (bond pricing, duration, convexity, yield calculations)
- *More modules coming soon...*

This project is maintained by students and educators at the University of Chicago Financial Mathematics program as a learning resource for the quantitative finance community.

## Installation

### From PyPI (when published)

```bash
pip install finm
```

### From Source

```bash
git clone https://github.com/uchicago-finmath/finm.git
cd finm
pip install .
```

## Quick Start

```python
import finm

# Calculate bond price
price = finm.bond_price(
    face_value=1000,
    coupon_rate=0.06,    # 6% annual coupon
    ytm=0.05,            # 5% yield to maturity
    periods=10,          # 10 semi-annual periods (5 years)
    frequency=2          # Semi-annual payments
)
print(f"Bond Price: ${price:.2f}")

# Calculate present value
pv = finm.present_value(
    future_value=1000,
    rate=0.05,
    periods=2
)
print(f"Present Value: ${pv:.2f}")

# Calculate duration and convexity
dur = finm.duration(1000, 0.06, 0.05, 10, frequency=2)
mod_dur = finm.modified_duration(1000, 0.06, 0.05, 10, frequency=2)
conv = finm.convexity(1000, 0.06, 0.05, 10, frequency=2)

print(f"Macaulay Duration: {dur:.4f} years")
print(f"Modified Duration: {mod_dur:.4f}")
print(f"Convexity: {conv:.4f}")
```

## Available Functions

### Fixed Income Module (`finm.fixedincome`)

| Function | Description |
|----------|-------------|
| `present_value()` | Calculate present value of a future cash flow |
| `future_value()` | Calculate future value of a present cash flow |
| `bond_price()` | Calculate the price of a coupon bond |
| `yield_to_maturity()` | Calculate YTM using Newton-Raphson method |
| `duration()` | Calculate Macaulay duration |
| `modified_duration()` | Calculate modified duration |
| `convexity()` | Calculate bond convexity |

---

## For Developers

This section provides instructions for setting up the development environment, running tests, and building the package locally.

### Prerequisites

- Python 3.9 or higher
- [Hatch](https://hatch.pypa.io/) - Modern Python project manager

### Installing Hatch

```bash
# Using pip
pip install hatch

# Using pipx (recommended for CLI tools)
pipx install hatch

# On macOS with Homebrew
brew install hatch
```

### Setting Up Development Environment

1. **Clone the repository:**

   ```bash
   git clone https://github.com/uchicago-finmath/finm.git
   cd finm
   ```

2. **Install in development mode:**

   Using pip with editable install:
   ```bash
   pip install -e ".[dev]"
   ```

   Or using Hatch (creates an isolated environment):
   ```bash
   hatch shell
   ```

### Running Tests

**Using pytest directly:**
```bash
pytest tests/
```

**Using pytest with coverage:**
```bash
pytest --cov=finm --cov-report=term-missing tests/
```

**Using Hatch scripts:**
```bash
# Run tests
hatch run test

# Run tests with coverage
hatch run test-cov
```

### Code Quality

**Format code with Black:**
```bash
hatch run lint:fmt
```

**Check code with Ruff:**
```bash
hatch run lint:check
```

**Type checking with mypy:**
```bash
hatch run lint:typing
```

**Run all linting checks:**
```bash
hatch run lint:all
```

### Building the Package

**Build distribution packages:**
```bash
hatch build
```

This creates both source distribution (`.tar.gz`) and wheel (`.whl`) files in the `dist/` directory.

**Clean build artifacts:**
```bash
hatch clean
```

### Project Structure

```
finm/
├── pyproject.toml          # Project configuration (hatch/hatchling)
├── README.md               # This file
├── LICENSE                 # MIT License
├── src/
│   └── finm/               # Main package
│       ├── __init__.py     # Package initialization
│       └── fixedincome/    # Fixed income submodule
│           ├── __init__.py
│           └── bonds.py    # Bond calculations
└── tests/
    ├── __init__.py
    └── test_fixedincome.py # Tests for fixed income module
```

### Contributing

We welcome contributions from students and educators! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/new-function`)
3. **Write** your code with docstrings and type hints
4. **Add** tests for your new functionality
5. **Run** the test suite to ensure everything passes
6. **Submit** a pull request

Please ensure your code:
- Follows PEP 8 style guidelines (use `black` for formatting)
- Includes comprehensive docstrings with examples
- Has corresponding unit tests
- Passes all existing tests

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project is created and maintained by students and educators at the **University of Chicago Financial Mathematics** program. We thank all contributors who have helped make this educational resource possible.

---

*Remember: This is an educational project. Always verify calculations independently before using them for any real-world applications.*

