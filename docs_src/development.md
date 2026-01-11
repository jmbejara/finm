# Development Guide

This guide covers setting up a development environment, running tests, and contributing to the finm package.

## Prerequisites

- Python 3.9 or higher
- [Hatch](https://hatch.pypa.io/) - Modern Python project manager

## Installing Hatch

```bash
# Using pip
pip install hatch

# Using pipx (recommended for CLI tools)
pipx install hatch

# On macOS with Homebrew
brew install hatch
```

## Setting Up Development Environment

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jmbejara/finm.git
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

## Running Tests

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

## Code Quality

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

## Building the Package

**Build distribution packages:**
```bash
hatch build
```

This creates both source distribution (`.tar.gz`) and wheel (`.whl`) files in the `dist/` directory.

**Clean build artifacts:**
```bash
hatch clean
```

## Project Structure

```
finm/
├── pyproject.toml          # Project configuration (hatch/hatchling)
├── README.md
├── LICENSE                  # MIT License
├── src/
│   └── finm/               # Main package
│       ├── __init__.py
│       ├── analytics/      # Factor analysis, beta, Sharpe ratio
│       ├── data/           # Data loading from multiple sources
│       └── fixedincome/    # Bond pricing, duration, yield curves
├── tests/                  # Test suite
└── docs_src/               # Documentation source (Sphinx)
```

## Contributing

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
