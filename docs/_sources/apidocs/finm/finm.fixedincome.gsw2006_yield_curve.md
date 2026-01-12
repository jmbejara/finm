# {py:mod}`finm.fixedincome.gsw2006_yield_curve`

```{py:module} finm.fixedincome.gsw2006_yield_curve
```

```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`calc_cashflows <finm.fixedincome.gsw2006_yield_curve.calc_cashflows>`
  - ```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.calc_cashflows
    :summary:
    ```
* - {py:obj}`compare_fit <finm.fixedincome.gsw2006_yield_curve.compare_fit>`
  - ```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.compare_fit
    :summary:
    ```
* - {py:obj}`discount <finm.fixedincome.gsw2006_yield_curve.discount>`
  - ```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.discount
    :summary:
    ```
* - {py:obj}`filter_treasury_cashflows <finm.fixedincome.gsw2006_yield_curve.filter_treasury_cashflows>`
  - ```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.filter_treasury_cashflows
    :summary:
    ```
* - {py:obj}`fit <finm.fixedincome.gsw2006_yield_curve.fit>`
  - ```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.fit
    :summary:
    ```
* - {py:obj}`gurkaynak_sack_wright_filters <finm.fixedincome.gsw2006_yield_curve.gurkaynak_sack_wright_filters>`
  - ```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.gurkaynak_sack_wright_filters
    :summary:
    ```
* - {py:obj}`plot_spot_curve <finm.fixedincome.gsw2006_yield_curve.plot_spot_curve>`
  - ```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.plot_spot_curve
    :summary:
    ```
* - {py:obj}`predict_prices <finm.fixedincome.gsw2006_yield_curve.predict_prices>`
  - ```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.predict_prices
    :summary:
    ```
* - {py:obj}`spot <finm.fixedincome.gsw2006_yield_curve.spot>`
  - ```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.spot
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`PARAMS0 <finm.fixedincome.gsw2006_yield_curve.PARAMS0>`
  - ```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.PARAMS0
    :summary:
    ```
* - {py:obj}`PARAM_NAMES <finm.fixedincome.gsw2006_yield_curve.PARAM_NAMES>`
  - ```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.PARAM_NAMES
    :summary:
    ```
````

### API

````{py:data} PARAMS0
:canonical: finm.fixedincome.gsw2006_yield_curve.PARAMS0
:value: >
   'array(...)'

```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.PARAMS0
```

````

````{py:data} PARAM_NAMES
:canonical: finm.fixedincome.gsw2006_yield_curve.PARAM_NAMES
:value: >
   ('tau1', 'tau2', 'beta1', 'beta2', 'beta3', 'beta4')

```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.PARAM_NAMES
```

````

````{py:function} calc_cashflows(quote_data, filter_maturity_dates=False)
:canonical: finm.fixedincome.gsw2006_yield_curve.calc_cashflows

```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.calc_cashflows
```
````

````{py:function} compare_fit(quote_date, df_all, params_star, actual_params, df)
:canonical: finm.fixedincome.gsw2006_yield_curve.compare_fit

```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.compare_fit
```
````

````{py:function} discount(t, params=PARAMS0)
:canonical: finm.fixedincome.gsw2006_yield_curve.discount

```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.discount
```
````

````{py:function} filter_treasury_cashflows(CF, filter_maturity_dates=False, filter_benchmark_dates=False, filter_CF_strict=True)
:canonical: finm.fixedincome.gsw2006_yield_curve.filter_treasury_cashflows

```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.filter_treasury_cashflows
```
````

````{py:function} fit(quote_date, df_all, params0=PARAMS0)
:canonical: finm.fixedincome.gsw2006_yield_curve.fit

```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.fit
```
````

````{py:function} gurkaynak_sack_wright_filters(dff)
:canonical: finm.fixedincome.gsw2006_yield_curve.gurkaynak_sack_wright_filters

```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.gurkaynak_sack_wright_filters
```
````

````{py:function} plot_spot_curve(params, alt_text=None)
:canonical: finm.fixedincome.gsw2006_yield_curve.plot_spot_curve

```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.plot_spot_curve
```
````

````{py:function} predict_prices(quote_date, df_all, params=PARAMS0)
:canonical: finm.fixedincome.gsw2006_yield_curve.predict_prices

```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.predict_prices
```
````

````{py:function} spot(maturities, params=PARAMS0)
:canonical: finm.fixedincome.gsw2006_yield_curve.spot

```{autodoc2-docstring} finm.fixedincome.gsw2006_yield_curve.spot
```
````
