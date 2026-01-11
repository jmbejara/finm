# {py:mod}`finm.data.wrds_data.pull_CRSP_treasury`

```{py:module} finm.data.wrds_data.pull_CRSP_treasury
```

```{autodoc2-docstring} finm.data.wrds_data.pull_CRSP_treasury
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`calc_runness <finm.data.wrds_data.pull_CRSP_treasury.calc_runness>`
  - ```{autodoc2-docstring} finm.data.wrds_data.pull_CRSP_treasury.calc_runness
    :summary:
    ```
* - {py:obj}`load_CRSP_treasury_consolidated <finm.data.wrds_data.pull_CRSP_treasury.load_CRSP_treasury_consolidated>`
  - ```{autodoc2-docstring} finm.data.wrds_data.pull_CRSP_treasury.load_CRSP_treasury_consolidated
    :summary:
    ```
* - {py:obj}`load_CRSP_treasury_daily <finm.data.wrds_data.pull_CRSP_treasury.load_CRSP_treasury_daily>`
  - ```{autodoc2-docstring} finm.data.wrds_data.pull_CRSP_treasury.load_CRSP_treasury_daily
    :summary:
    ```
* - {py:obj}`load_CRSP_treasury_info <finm.data.wrds_data.pull_CRSP_treasury.load_CRSP_treasury_info>`
  - ```{autodoc2-docstring} finm.data.wrds_data.pull_CRSP_treasury.load_CRSP_treasury_info
    :summary:
    ```
* - {py:obj}`pull_CRSP_treasury_consolidated <finm.data.wrds_data.pull_CRSP_treasury.pull_CRSP_treasury_consolidated>`
  - ```{autodoc2-docstring} finm.data.wrds_data.pull_CRSP_treasury.pull_CRSP_treasury_consolidated
    :summary:
    ```
* - {py:obj}`pull_CRSP_treasury_daily <finm.data.wrds_data.pull_CRSP_treasury.pull_CRSP_treasury_daily>`
  - ```{autodoc2-docstring} finm.data.wrds_data.pull_CRSP_treasury.pull_CRSP_treasury_daily
    :summary:
    ```
* - {py:obj}`pull_CRSP_treasury_info <finm.data.wrds_data.pull_CRSP_treasury.pull_CRSP_treasury_info>`
  - ```{autodoc2-docstring} finm.data.wrds_data.pull_CRSP_treasury.pull_CRSP_treasury_info
    :summary:
    ```
````

### API

````{py:function} calc_runness(data: pandas.DataFrame) -> pandas.DataFrame
:canonical: finm.data.wrds_data.pull_CRSP_treasury.calc_runness

```{autodoc2-docstring} finm.data.wrds_data.pull_CRSP_treasury.calc_runness
```
````

````{py:function} load_CRSP_treasury_consolidated(data_dir: pathlib.Path | str, with_runness: bool = True) -> pandas.DataFrame
:canonical: finm.data.wrds_data.pull_CRSP_treasury.load_CRSP_treasury_consolidated

```{autodoc2-docstring} finm.data.wrds_data.pull_CRSP_treasury.load_CRSP_treasury_consolidated
```
````

````{py:function} load_CRSP_treasury_daily(data_dir: pathlib.Path | str) -> pandas.DataFrame
:canonical: finm.data.wrds_data.pull_CRSP_treasury.load_CRSP_treasury_daily

```{autodoc2-docstring} finm.data.wrds_data.pull_CRSP_treasury.load_CRSP_treasury_daily
```
````

````{py:function} load_CRSP_treasury_info(data_dir: pathlib.Path | str) -> pandas.DataFrame
:canonical: finm.data.wrds_data.pull_CRSP_treasury.load_CRSP_treasury_info

```{autodoc2-docstring} finm.data.wrds_data.pull_CRSP_treasury.load_CRSP_treasury_info
```
````

````{py:function} pull_CRSP_treasury_consolidated(start_date: str, end_date: str, wrds_username: str) -> pandas.DataFrame
:canonical: finm.data.wrds_data.pull_CRSP_treasury.pull_CRSP_treasury_consolidated

```{autodoc2-docstring} finm.data.wrds_data.pull_CRSP_treasury.pull_CRSP_treasury_consolidated
```
````

````{py:function} pull_CRSP_treasury_daily(start_date: str, end_date: str, wrds_username: str) -> pandas.DataFrame
:canonical: finm.data.wrds_data.pull_CRSP_treasury.pull_CRSP_treasury_daily

```{autodoc2-docstring} finm.data.wrds_data.pull_CRSP_treasury.pull_CRSP_treasury_daily
```
````

````{py:function} pull_CRSP_treasury_info(wrds_username: str) -> pandas.DataFrame
:canonical: finm.data.wrds_data.pull_CRSP_treasury.pull_CRSP_treasury_info

```{autodoc2-docstring} finm.data.wrds_data.pull_CRSP_treasury.pull_CRSP_treasury_info
```
````
