# {py:mod}`finm.analytics.factor_analysis`

```{py:module} finm.analytics.factor_analysis
```

```{autodoc2-docstring} finm.analytics.factor_analysis
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`RegressionResult <finm.analytics.factor_analysis.RegressionResult>`
  - ```{autodoc2-docstring} finm.analytics.factor_analysis.RegressionResult
    :summary:
    ```
````

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
* - {py:obj}`run_capm_regression <finm.analytics.factor_analysis.run_capm_regression>`
  - ```{autodoc2-docstring} finm.analytics.factor_analysis.run_capm_regression
    :summary:
    ```
* - {py:obj}`run_factor_regression <finm.analytics.factor_analysis.run_factor_regression>`
  - ```{autodoc2-docstring} finm.analytics.factor_analysis.run_factor_regression
    :summary:
    ```
* - {py:obj}`run_fama_french_regression <finm.analytics.factor_analysis.run_fama_french_regression>`
  - ```{autodoc2-docstring} finm.analytics.factor_analysis.run_fama_french_regression
    :summary:
    ```
````

### API

`````{py:class} RegressionResult
:canonical: finm.analytics.factor_analysis.RegressionResult

```{autodoc2-docstring} finm.analytics.factor_analysis.RegressionResult
```

````{py:attribute} adj_r_squared
:canonical: finm.analytics.factor_analysis.RegressionResult.adj_r_squared
:type: float
:value: >
   None

```{autodoc2-docstring} finm.analytics.factor_analysis.RegressionResult.adj_r_squared
```

````

````{py:attribute} alpha
:canonical: finm.analytics.factor_analysis.RegressionResult.alpha
:type: float
:value: >
   None

```{autodoc2-docstring} finm.analytics.factor_analysis.RegressionResult.alpha
```

````

````{py:attribute} alpha_annualized
:canonical: finm.analytics.factor_analysis.RegressionResult.alpha_annualized
:type: float | None
:value: >
   None

```{autodoc2-docstring} finm.analytics.factor_analysis.RegressionResult.alpha_annualized
```

````

````{py:attribute} alpha_pvalue
:canonical: finm.analytics.factor_analysis.RegressionResult.alpha_pvalue
:type: float
:value: >
   None

```{autodoc2-docstring} finm.analytics.factor_analysis.RegressionResult.alpha_pvalue
```

````

````{py:attribute} alpha_se
:canonical: finm.analytics.factor_analysis.RegressionResult.alpha_se
:type: float
:value: >
   None

```{autodoc2-docstring} finm.analytics.factor_analysis.RegressionResult.alpha_se
```

````

````{py:attribute} alpha_tstat
:canonical: finm.analytics.factor_analysis.RegressionResult.alpha_tstat
:type: float
:value: >
   None

```{autodoc2-docstring} finm.analytics.factor_analysis.RegressionResult.alpha_tstat
```

````

````{py:attribute} annualization_factor
:canonical: finm.analytics.factor_analysis.RegressionResult.annualization_factor
:type: float | None
:value: >
   None

```{autodoc2-docstring} finm.analytics.factor_analysis.RegressionResult.annualization_factor
```

````

````{py:attribute} beta_pvalues
:canonical: finm.analytics.factor_analysis.RegressionResult.beta_pvalues
:type: dict[str, float]
:value: >
   None

```{autodoc2-docstring} finm.analytics.factor_analysis.RegressionResult.beta_pvalues
```

````

````{py:attribute} beta_ses
:canonical: finm.analytics.factor_analysis.RegressionResult.beta_ses
:type: dict[str, float]
:value: >
   None

```{autodoc2-docstring} finm.analytics.factor_analysis.RegressionResult.beta_ses
```

````

````{py:attribute} beta_tstats
:canonical: finm.analytics.factor_analysis.RegressionResult.beta_tstats
:type: dict[str, float]
:value: >
   None

```{autodoc2-docstring} finm.analytics.factor_analysis.RegressionResult.beta_tstats
```

````

````{py:attribute} betas
:canonical: finm.analytics.factor_analysis.RegressionResult.betas
:type: dict[str, float]
:value: >
   None

```{autodoc2-docstring} finm.analytics.factor_analysis.RegressionResult.betas
```

````

````{py:attribute} n_observations
:canonical: finm.analytics.factor_analysis.RegressionResult.n_observations
:type: int
:value: >
   None

```{autodoc2-docstring} finm.analytics.factor_analysis.RegressionResult.n_observations
```

````

````{py:attribute} r_squared
:canonical: finm.analytics.factor_analysis.RegressionResult.r_squared
:type: float
:value: >
   None

```{autodoc2-docstring} finm.analytics.factor_analysis.RegressionResult.r_squared
```

````

````{py:attribute} residual_std
:canonical: finm.analytics.factor_analysis.RegressionResult.residual_std
:type: float
:value: >
   None

```{autodoc2-docstring} finm.analytics.factor_analysis.RegressionResult.residual_std
```

````

`````

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

````{py:function} run_capm_regression(excess_returns: pandas.Series, market_excess_returns: pandas.Series, annualization_factor: float | None = None) -> finm.analytics.factor_analysis.RegressionResult
:canonical: finm.analytics.factor_analysis.run_capm_regression

```{autodoc2-docstring} finm.analytics.factor_analysis.run_capm_regression
```
````

````{py:function} run_factor_regression(returns: pandas.Series, factors: pandas.DataFrame | pandas.Series, annualization_factor: float | None = None) -> finm.analytics.factor_analysis.RegressionResult
:canonical: finm.analytics.factor_analysis.run_factor_regression

```{autodoc2-docstring} finm.analytics.factor_analysis.run_factor_regression
```
````

````{py:function} run_fama_french_regression(returns: pandas.Series, factors: pandas.DataFrame, annualization_factor: float | None = None) -> finm.analytics.factor_analysis.RegressionResult
:canonical: finm.analytics.factor_analysis.run_fama_french_regression

```{autodoc2-docstring} finm.analytics.factor_analysis.run_fama_french_regression
```
````
