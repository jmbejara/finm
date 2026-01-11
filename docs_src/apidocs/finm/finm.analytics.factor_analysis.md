# {py:mod}`finm.analytics.factor_analysis`

```{py:module} finm.analytics.factor_analysis
```

```{autodoc2-docstring} finm.analytics.factor_analysis
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`calculate_beta <finm.analytics.factor_analysis.calculate_beta>`
  - ```{autodoc2-docstring} finm.analytics.factor_analysis.calculate_beta
    :summary:
    ```
* - {py:obj}`calculate_factor_exposures <finm.analytics.factor_analysis.calculate_factor_exposures>`
  - ```{autodoc2-docstring} finm.analytics.factor_analysis.calculate_factor_exposures
    :summary:
    ```
* - {py:obj}`calculate_sharpe_ratio <finm.analytics.factor_analysis.calculate_sharpe_ratio>`
  - ```{autodoc2-docstring} finm.analytics.factor_analysis.calculate_sharpe_ratio
    :summary:
    ```
````

### API

````{py:function} calculate_beta(returns: pandas.Series, factor_returns: pandas.Series) -> float
:canonical: finm.analytics.factor_analysis.calculate_beta

```{autodoc2-docstring} finm.analytics.factor_analysis.calculate_beta
```
````

````{py:function} calculate_factor_exposures(returns: pandas.Series, factors: pandas.DataFrame, annualization_factor: float = 252.0) -> dict[str, float]
:canonical: finm.analytics.factor_analysis.calculate_factor_exposures

```{autodoc2-docstring} finm.analytics.factor_analysis.calculate_factor_exposures
```
````

````{py:function} calculate_sharpe_ratio(returns: pandas.Series, risk_free_rate: pandas.Series | float, annualization_factor: float = 252.0) -> float
:canonical: finm.analytics.factor_analysis.calculate_sharpe_ratio

```{autodoc2-docstring} finm.analytics.factor_analysis.calculate_sharpe_ratio
```
````
