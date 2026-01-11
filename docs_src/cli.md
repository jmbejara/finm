# CLI Reference

The `finm` command-line interface provides commands for downloading and managing financial data.

## Installation

Install the CLI dependencies:

```bash
pip install finm[cli]
```

## Commands

### finm pull

Download a dataset from its source.

```bash
finm pull <dataset> [OPTIONS]
```

**Arguments:**
- `dataset`: Dataset to pull (required)

**Options:**
- `--data-dir, -d`: Directory for data storage (default: uses DATA_DIR env var or ./data_cache)
- `--wrds-username`: WRDS username (for WRDS datasets)
- `--start-date`: Start date (YYYY-MM-DD, for WRDS datasets)
- `--end-date`: End date (YYYY-MM-DD, for WRDS datasets)
- `--format, -f`: Output format: wide or long (default: wide)

**Examples:**

```bash
# Download Federal Reserve yield curve
finm pull fed_yield_curve

# Download with custom data directory
finm pull fed_yield_curve --data-dir ./my_data

# Download WRDS Treasury data (requires credentials)
finm pull wrds_treasury --wrds-username myuser --start-date 2020-01-01 --end-date 2023-12-31

# Download He-Kelly-Manela factors
finm pull he_kelly_manela
```

### finm list

List all available datasets.

```bash
finm list
```

**Output:**
```
Dataset                        Description                                   WRDS?
--------------------------------------------------------------------------------
fed_yield_curve                Federal Reserve GSW yield curve               No
fama_french                    Fama-French 3 factors (daily)                 No
he_kelly_manela                He-Kelly-Manela intermediary factors          No
open_source_bond_treasury      Treasury bond returns (Open Bond Asset...)    No
open_source_bond_corporate     Corporate bond returns (Open Bond Asset...)   No
wrds_treasury                  CRSP Treasury data                            Yes
wrds_corp_bond                 WRDS corporate bond returns                   Yes
```

### finm info

Show detailed information about a dataset.

```bash
finm info <dataset>
```

**Example:**

```bash
finm info fed_yield_curve
```

**Output:**
```
Federal Reserve Yield Curve
===========================

Source: https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv
Description: GSW (Gurkaynak, Sack, Wright) yield curve model data
Variants: standard (SVENY01-30), all (full dataset)
Credentials: None required
```

## Credential Configuration

For WRDS datasets, credentials can be provided via:

1. **CLI argument** (highest priority):
   ```bash
   finm pull wrds_treasury --wrds-username myuser
   ```

2. **Environment variable**:
   ```bash
   export WRDS_USERNAME=myuser
   finm pull wrds_treasury
   ```

3. **.env file**:
   ```
   # .env
   WRDS_USERNAME=myuser
   DATA_DIR=./data_cache
   ```

4. **Interactive prompt** (if terminal available):
   ```bash
   finm pull wrds_treasury
   # > WRDS username: _
   ```

## Environment Variables

- `DATA_DIR`: Default directory for data storage
- `WRDS_USERNAME`: WRDS username for authentication

## Example .env File

Create a `.env` file in your project root:

```
DATA_DIR=./data_cache
WRDS_USERNAME=your_wrds_username
```
