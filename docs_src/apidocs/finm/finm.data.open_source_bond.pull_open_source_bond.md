# {py:mod}`finm.data.open_source_bond.pull_open_source_bond`

```{py:module} finm.data.open_source_bond.pull_open_source_bond
```

```{autodoc2-docstring} finm.data.open_source_bond.pull_open_source_bond
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`download_data <finm.data.open_source_bond.pull_open_source_bond.download_data>`
  - ```{autodoc2-docstring} finm.data.open_source_bond.pull_open_source_bond.download_data
    :summary:
    ```
* - {py:obj}`download_file <finm.data.open_source_bond.pull_open_source_bond.download_file>`
  - ```{autodoc2-docstring} finm.data.open_source_bond.pull_open_source_bond.download_file
    :summary:
    ```
* - {py:obj}`load_corporate_bond_returns <finm.data.open_source_bond.pull_open_source_bond.load_corporate_bond_returns>`
  - ```{autodoc2-docstring} finm.data.open_source_bond.pull_open_source_bond.load_corporate_bond_returns
    :summary:
    ```
* - {py:obj}`load_data_into_dataframe <finm.data.open_source_bond.pull_open_source_bond.load_data_into_dataframe>`
  - ```{autodoc2-docstring} finm.data.open_source_bond.pull_open_source_bond.load_data_into_dataframe
    :summary:
    ```
* - {py:obj}`load_treasury_returns <finm.data.open_source_bond.pull_open_source_bond.load_treasury_returns>`
  - ```{autodoc2-docstring} finm.data.open_source_bond.pull_open_source_bond.load_treasury_returns
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`DATA_INFO <finm.data.open_source_bond.pull_open_source_bond.DATA_INFO>`
  - ```{autodoc2-docstring} finm.data.open_source_bond.pull_open_source_bond.DATA_INFO
    :summary:
    ```
* - {py:obj}`MIN_N_ROWS_EXPECTED <finm.data.open_source_bond.pull_open_source_bond.MIN_N_ROWS_EXPECTED>`
  - ```{autodoc2-docstring} finm.data.open_source_bond.pull_open_source_bond.MIN_N_ROWS_EXPECTED
    :summary:
    ```
````

### API

````{py:data} DATA_INFO
:canonical: finm.data.open_source_bond.pull_open_source_bond.DATA_INFO
:value: >
   None

```{autodoc2-docstring} finm.data.open_source_bond.pull_open_source_bond.DATA_INFO
```

````

````{py:data} MIN_N_ROWS_EXPECTED
:canonical: finm.data.open_source_bond.pull_open_source_bond.MIN_N_ROWS_EXPECTED
:value: >
   500

```{autodoc2-docstring} finm.data.open_source_bond.pull_open_source_bond.MIN_N_ROWS_EXPECTED
```

````

````{py:function} download_data(url: str, csv: str, data_dir: pathlib.Path) -> pathlib.Path
:canonical: finm.data.open_source_bond.pull_open_source_bond.download_data

```{autodoc2-docstring} finm.data.open_source_bond.pull_open_source_bond.download_data
```
````

````{py:function} download_file(url: str, output_path: pathlib.Path) -> pathlib.Path
:canonical: finm.data.open_source_bond.pull_open_source_bond.download_file

```{autodoc2-docstring} finm.data.open_source_bond.pull_open_source_bond.download_file
```
````

````{py:function} load_corporate_bond_returns(data_dir: pathlib.Path) -> pandas.DataFrame
:canonical: finm.data.open_source_bond.pull_open_source_bond.load_corporate_bond_returns

```{autodoc2-docstring} finm.data.open_source_bond.pull_open_source_bond.load_corporate_bond_returns
```
````

````{py:function} load_data_into_dataframe(csv_path: pathlib.Path, check_n_rows: bool = True)
:canonical: finm.data.open_source_bond.pull_open_source_bond.load_data_into_dataframe

```{autodoc2-docstring} finm.data.open_source_bond.pull_open_source_bond.load_data_into_dataframe
```
````

````{py:function} load_treasury_returns(data_dir: pathlib.Path) -> pandas.DataFrame
:canonical: finm.data.open_source_bond.pull_open_source_bond.load_treasury_returns

```{autodoc2-docstring} finm.data.open_source_bond.pull_open_source_bond.load_treasury_returns
```
````
