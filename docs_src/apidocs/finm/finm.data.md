# {py:mod}`finm.data`

```{py:module} finm.data
```

```{autodoc2-docstring} finm.data
:allowtitles:
```

## Subpackages

```{toctree}
:titlesonly:
:maxdepth: 3

finm.data.fama_french
finm.data.federal_reserve
finm.data.he_kelly_manela
finm.data.open_source_bond
finm.data.wrds
```

## Package Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`calc_treasury_runness <finm.data.calc_treasury_runness>`
  - ```{autodoc2-docstring} finm.data.calc_treasury_runness
    :summary:
    ```
* - {py:obj}`load_corporate_bond_returns <finm.data.load_corporate_bond_returns>`
  - ```{autodoc2-docstring} finm.data.load_corporate_bond_returns
    :summary:
    ```
* - {py:obj}`load_fama_french_factors <finm.data.load_fama_french_factors>`
  - ```{autodoc2-docstring} finm.data.load_fama_french_factors
    :summary:
    ```
* - {py:obj}`load_fed_yield_curve <finm.data.load_fed_yield_curve>`
  - ```{autodoc2-docstring} finm.data.load_fed_yield_curve
    :summary:
    ```
* - {py:obj}`load_fed_yield_curve_all <finm.data.load_fed_yield_curve_all>`
  - ```{autodoc2-docstring} finm.data.load_fed_yield_curve_all
    :summary:
    ```
* - {py:obj}`load_he_kelly_manela_all <finm.data.load_he_kelly_manela_all>`
  - ```{autodoc2-docstring} finm.data.load_he_kelly_manela_all
    :summary:
    ```
* - {py:obj}`load_he_kelly_manela_factors_daily <finm.data.load_he_kelly_manela_factors_daily>`
  - ```{autodoc2-docstring} finm.data.load_he_kelly_manela_factors_daily
    :summary:
    ```
* - {py:obj}`load_he_kelly_manela_factors_monthly <finm.data.load_he_kelly_manela_factors_monthly>`
  - ```{autodoc2-docstring} finm.data.load_he_kelly_manela_factors_monthly
    :summary:
    ```
* - {py:obj}`load_treasury_returns <finm.data.load_treasury_returns>`
  - ```{autodoc2-docstring} finm.data.load_treasury_returns
    :summary:
    ```
* - {py:obj}`load_wrds_corp_bond <finm.data.load_wrds_corp_bond>`
  - ```{autodoc2-docstring} finm.data.load_wrds_corp_bond
    :summary:
    ```
* - {py:obj}`load_wrds_treasury <finm.data.load_wrds_treasury>`
  - ```{autodoc2-docstring} finm.data.load_wrds_treasury
    :summary:
    ```
* - {py:obj}`pull_fama_french_factors <finm.data.pull_fama_french_factors>`
  - ```{autodoc2-docstring} finm.data.pull_fama_french_factors
    :summary:
    ```
* - {py:obj}`pull_fed_yield_curve <finm.data.pull_fed_yield_curve>`
  - ```{autodoc2-docstring} finm.data.pull_fed_yield_curve
    :summary:
    ```
* - {py:obj}`pull_he_kelly_manela <finm.data.pull_he_kelly_manela>`
  - ```{autodoc2-docstring} finm.data.pull_he_kelly_manela
    :summary:
    ```
* - {py:obj}`pull_open_source_bond <finm.data.pull_open_source_bond>`
  - ```{autodoc2-docstring} finm.data.pull_open_source_bond
    :summary:
    ```
* - {py:obj}`pull_wrds_corp_bond <finm.data.pull_wrds_corp_bond>`
  - ```{autodoc2-docstring} finm.data.pull_wrds_corp_bond
    :summary:
    ```
* - {py:obj}`pull_wrds_treasury <finm.data.pull_wrds_treasury>`
  - ```{autodoc2-docstring} finm.data.pull_wrds_treasury
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`FormatType <finm.data.FormatType>`
  - ```{autodoc2-docstring} finm.data.FormatType
    :summary:
    ```
````

### API

````{py:data} FormatType
:canonical: finm.data.FormatType
:value: >
   None

```{autodoc2-docstring} finm.data.FormatType
```

````

````{py:function} calc_treasury_runness(data: pandas.DataFrame) -> pandas.DataFrame
:canonical: finm.data.calc_treasury_runness

```{autodoc2-docstring} finm.data.calc_treasury_runness
```
````

````{py:function} load_corporate_bond_returns(data_dir: pathlib.Path | str, format: finm.data.FormatType = 'wide') -> pandas.DataFrame
:canonical: finm.data.load_corporate_bond_returns

```{autodoc2-docstring} finm.data.load_corporate_bond_returns
```
````

````{py:function} load_fama_french_factors(data_dir: pathlib.Path | str | None = None, start: str | datetime.datetime | None = None, end: str | datetime.datetime | None = None, format: finm.data.FormatType = 'wide') -> pandas.DataFrame
:canonical: finm.data.load_fama_french_factors

```{autodoc2-docstring} finm.data.load_fama_french_factors
```
````

````{py:function} load_fed_yield_curve(data_dir: pathlib.Path | str, format: finm.data.FormatType = 'wide') -> pandas.DataFrame
:canonical: finm.data.load_fed_yield_curve

```{autodoc2-docstring} finm.data.load_fed_yield_curve
```
````

````{py:function} load_fed_yield_curve_all(data_dir: pathlib.Path | str, format: finm.data.FormatType = 'wide') -> pandas.DataFrame
:canonical: finm.data.load_fed_yield_curve_all

```{autodoc2-docstring} finm.data.load_fed_yield_curve_all
```
````

````{py:function} load_he_kelly_manela_all(data_dir: pathlib.Path | str, format: finm.data.FormatType = 'wide') -> pandas.DataFrame
:canonical: finm.data.load_he_kelly_manela_all

```{autodoc2-docstring} finm.data.load_he_kelly_manela_all
```
````

````{py:function} load_he_kelly_manela_factors_daily(data_dir: pathlib.Path | str, format: finm.data.FormatType = 'wide') -> pandas.DataFrame
:canonical: finm.data.load_he_kelly_manela_factors_daily

```{autodoc2-docstring} finm.data.load_he_kelly_manela_factors_daily
```
````

````{py:function} load_he_kelly_manela_factors_monthly(data_dir: pathlib.Path | str, format: finm.data.FormatType = 'wide') -> pandas.DataFrame
:canonical: finm.data.load_he_kelly_manela_factors_monthly

```{autodoc2-docstring} finm.data.load_he_kelly_manela_factors_monthly
```
````

````{py:function} load_treasury_returns(data_dir: pathlib.Path | str, format: finm.data.FormatType = 'wide') -> pandas.DataFrame
:canonical: finm.data.load_treasury_returns

```{autodoc2-docstring} finm.data.load_treasury_returns
```
````

````{py:function} load_wrds_corp_bond(data_dir: pathlib.Path | str, format: finm.data.FormatType = 'wide') -> pandas.DataFrame
:canonical: finm.data.load_wrds_corp_bond

```{autodoc2-docstring} finm.data.load_wrds_corp_bond
```
````

````{py:function} load_wrds_treasury(data_dir: pathlib.Path | str, variant: typing.Literal[daily, info, consolidated] = 'consolidated', with_runness: bool = True, format: finm.data.FormatType = 'wide') -> pandas.DataFrame
:canonical: finm.data.load_wrds_treasury

```{autodoc2-docstring} finm.data.load_wrds_treasury
```
````

````{py:function} pull_fama_french_factors(data_dir: pathlib.Path | str, start: str | datetime.datetime | None = None, end: str | datetime.datetime | None = None, frequency: typing.Literal[daily, monthly] = 'daily') -> pandas.DataFrame
:canonical: finm.data.pull_fama_french_factors

```{autodoc2-docstring} finm.data.pull_fama_french_factors
```
````

````{py:function} pull_fed_yield_curve(data_dir: pathlib.Path | str) -> tuple[pandas.DataFrame, pandas.DataFrame]
:canonical: finm.data.pull_fed_yield_curve

```{autodoc2-docstring} finm.data.pull_fed_yield_curve
```
````

````{py:function} pull_he_kelly_manela(data_dir: pathlib.Path | str) -> None
:canonical: finm.data.pull_he_kelly_manela

```{autodoc2-docstring} finm.data.pull_he_kelly_manela
```
````

````{py:function} pull_open_source_bond(data_dir: pathlib.Path | str, variant: typing.Literal[treasury, corporate, all] = 'all') -> None
:canonical: finm.data.pull_open_source_bond

```{autodoc2-docstring} finm.data.pull_open_source_bond
```
````

````{py:function} pull_wrds_corp_bond(data_dir: pathlib.Path | str, wrds_username: str, start_date: str, end_date: str) -> pandas.DataFrame
:canonical: finm.data.pull_wrds_corp_bond

```{autodoc2-docstring} finm.data.pull_wrds_corp_bond
```
````

````{py:function} pull_wrds_treasury(data_dir: pathlib.Path | str, wrds_username: str, start_date: str, end_date: str, variant: typing.Literal[daily, info, consolidated] = 'consolidated', with_runness: bool = True) -> pandas.DataFrame
:canonical: finm.data.pull_wrds_treasury

```{autodoc2-docstring} finm.data.pull_wrds_treasury
```
````
