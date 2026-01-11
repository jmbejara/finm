# Adding New Data Sources

This guide explains how to add a new data source to the `finm.data` module following
the standardized pattern.

## File Structure

Each data source should have the following structure:

```
src/finm/data/
└── your_source/
    ├── __init__.py      # Public API: pull(), load(), to_long_format()
    ├── _constants.py    # URLs, file names, metadata
    ├── _pull.py         # Download logic
    ├── _load.py         # Load from cache logic
    └── _transform.py    # Wide <-> Long format conversion
```

## Step 1: Create Constants

Create `_constants.py` with metadata about your data source:

```python
"""Constants for your data source."""

from typing import Final

DATASET_NAME: Final[str] = "your_source"
DISPLAY_NAME: Final[str] = "Your Data Source Name"

# Data source URL(s)
DATA_URL: Final[str] = "https://example.com/data.csv"

# Parquet file names
PARQUET_FILE: Final[str] = "your_data.parquet"

# Column names for long format (if applicable)
VALUE_COLUMNS: Final[list[str]] = ["col1", "col2", "col3"]
```

## Step 2: Implement Pull

Create `_pull.py` with download logic:

```python
"""Pull functions for your data source."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests

from finm.data.your_source._constants import DATA_URL, PARQUET_FILE


def pull_data(data_dir: Path | str) -> pd.DataFrame:
    """Download data from source and save to parquet.

    Parameters
    ----------
    data_dir : Path or str
        Directory to save the data.

    Returns
    -------
    pd.DataFrame
        Downloaded data.
    """
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    # Download data
    response = requests.get(DATA_URL)
    response.raise_for_status()

    # Parse and process
    df = pd.read_csv(BytesIO(response.content))

    # Save to parquet
    df.to_parquet(data_dir / PARQUET_FILE)

    return df
```

## Step 3: Implement Load

Create `_load.py` with cache loading logic:

```python
"""Load functions for your data source."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from finm.data.your_source._constants import PARQUET_FILE


def load_data(data_dir: Path | str) -> pd.DataFrame:
    """Load data from parquet cache.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet file.

    Returns
    -------
    pd.DataFrame
        Loaded data.
    """
    data_dir = Path(data_dir)
    return pd.read_parquet(data_dir / PARQUET_FILE)
```

## Step 4: Implement Transform

Create `_transform.py` with format conversion:

```python
"""Transform functions for your data source."""

from __future__ import annotations

import pandas as pd

from finm.data.your_source._constants import VALUE_COLUMNS


def to_long_format(df: pd.DataFrame) -> pd.DataFrame:
    """Convert from wide to long format.

    Parameters
    ----------
    df : pd.DataFrame
        Wide-format DataFrame.

    Returns
    -------
    pd.DataFrame
        Long-format DataFrame with columns [unique_id, ds, y].
    """
    # Reset index to make date a column
    df_reset = df.reset_index()
    date_col = df_reset.columns[0]

    # Melt from wide to long
    long_df = df_reset.melt(
        id_vars=[date_col],
        value_vars=VALUE_COLUMNS,
        var_name="unique_id",
        value_name="y",
    )

    # Rename date column to ds
    long_df = long_df.rename(columns={date_col: "ds"})

    # Reorder columns
    long_df = long_df[["unique_id", "ds", "y"]]

    # Drop NaN values
    long_df = long_df.dropna(subset=["y"])

    return long_df.reset_index(drop=True)
```

## Step 5: Create Public Interface

Create `__init__.py` with the standard interface:

```python
"""Your data source module.

Standard interface:
    - pull(data_dir): Download data from source
    - load(data_dir, format): Load cached data
    - to_long_format(df): Convert to long format
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pandas as pd

from finm.data.your_source._load import load_data
from finm.data.your_source._pull import pull_data
from finm.data.your_source._transform import to_long_format

FormatType = Literal["wide", "long"]


def pull(data_dir: Path | str) -> pd.DataFrame:
    """Download data from source.

    Parameters
    ----------
    data_dir : Path or str
        Directory to save downloaded data.

    Returns
    -------
    pd.DataFrame
        Downloaded data.
    """
    return pull_data(data_dir=data_dir)


def load(
    data_dir: Path | str,
    format: FormatType = "wide",
) -> pd.DataFrame:
    """Load data from cache.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing the parquet file.
    format : {"wide", "long"}, default "wide"
        Output format.

    Returns
    -------
    pd.DataFrame
        Loaded data.
    """
    df = load_data(data_dir=data_dir)

    if format == "long":
        df = to_long_format(df)

    return df


__all__ = ["pull", "load", "to_long_format"]
```

## Step 6: Register in Data Module

Add your source to `src/finm/data/__init__.py`:

```python
# Add import
from finm.data import your_source

# Add wrapper functions if desired
def pull_your_source(data_dir: Path | str) -> pd.DataFrame:
    """Download your data."""
    return your_source.pull(data_dir=data_dir)

def load_your_source(data_dir: Path | str, format: FormatType = "wide") -> pd.DataFrame:
    """Load your data."""
    return your_source.load(data_dir=data_dir, format=format)

# Add to __all__
__all__ = [
    # ...
    "your_source",
    "pull_your_source",
    "load_your_source",
]
```

## Step 7: Add CLI Support (Optional)

Update `src/finm/data/_cli.py` to include your dataset:

```python
class Dataset(str, Enum):
    # ...
    your_source = "your_source"

# In pull command
elif dataset == Dataset.your_source:
    from finm.data import your_source
    your_source.pull(data_dir=resolved_data_dir)
```

## Checklist

- [ ] Create `_constants.py` with URLs and file names
- [ ] Create `_pull.py` with download logic
- [ ] Create `_load.py` with cache loading
- [ ] Create `_transform.py` with long format conversion
- [ ] Create `__init__.py` with standard interface
- [ ] Register in `finm.data.__init__.py`
- [ ] Add CLI support if needed
- [ ] Add tests
- [ ] Update documentation
