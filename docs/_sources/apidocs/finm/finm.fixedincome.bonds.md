# {py:mod}`finm.fixedincome.bonds`

```{py:module} finm.fixedincome.bonds
```

```{autodoc2-docstring} finm.fixedincome.bonds
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`convexity <finm.fixedincome.bonds.convexity>`
  - ```{autodoc2-docstring} finm.fixedincome.bonds.convexity
    :summary:
    ```
* - {py:obj}`duration <finm.fixedincome.bonds.duration>`
  - ```{autodoc2-docstring} finm.fixedincome.bonds.duration
    :summary:
    ```
* - {py:obj}`future_value <finm.fixedincome.bonds.future_value>`
  - ```{autodoc2-docstring} finm.fixedincome.bonds.future_value
    :summary:
    ```
* - {py:obj}`get_coupon_dates <finm.fixedincome.bonds.get_coupon_dates>`
  - ```{autodoc2-docstring} finm.fixedincome.bonds.get_coupon_dates
    :summary:
    ```
* - {py:obj}`modified_duration <finm.fixedincome.bonds.modified_duration>`
  - ```{autodoc2-docstring} finm.fixedincome.bonds.modified_duration
    :summary:
    ```
* - {py:obj}`present_value <finm.fixedincome.bonds.present_value>`
  - ```{autodoc2-docstring} finm.fixedincome.bonds.present_value
    :summary:
    ```
* - {py:obj}`yield_to_maturity <finm.fixedincome.bonds.yield_to_maturity>`
  - ```{autodoc2-docstring} finm.fixedincome.bonds.yield_to_maturity
    :summary:
    ```
````

### API

````{py:function} convexity(face_value: float, coupon_rate: float, ytm: float, periods: int, frequency: int = 2) -> float
:canonical: finm.fixedincome.bonds.convexity

```{autodoc2-docstring} finm.fixedincome.bonds.convexity
```
````

````{py:function} duration(face_value: float, coupon_rate: float, ytm: float, periods: int, frequency: int = 2) -> float
:canonical: finm.fixedincome.bonds.duration

```{autodoc2-docstring} finm.fixedincome.bonds.duration
```
````

````{py:function} future_value(present_value: float, rate: float, periods: float, compounding: str = 'discrete') -> float
:canonical: finm.fixedincome.bonds.future_value

```{autodoc2-docstring} finm.fixedincome.bonds.future_value
```
````

````{py:function} get_coupon_dates(quote_date, maturity_date)
:canonical: finm.fixedincome.bonds.get_coupon_dates

```{autodoc2-docstring} finm.fixedincome.bonds.get_coupon_dates
```
````

````{py:function} modified_duration(face_value: float, coupon_rate: float, ytm: float, periods: int, frequency: int = 2) -> float
:canonical: finm.fixedincome.bonds.modified_duration

```{autodoc2-docstring} finm.fixedincome.bonds.modified_duration
```
````

````{py:function} present_value(future_value: float, rate: float, periods: float, compounding: str = 'discrete') -> float
:canonical: finm.fixedincome.bonds.present_value

```{autodoc2-docstring} finm.fixedincome.bonds.present_value
```
````

````{py:function} yield_to_maturity(price: float, face_value: float, coupon_rate: float, periods: int, frequency: int = 2, tolerance: float = 1e-08, max_iterations: int = 100) -> float
:canonical: finm.fixedincome.bonds.yield_to_maturity

```{autodoc2-docstring} finm.fixedincome.bonds.yield_to_maturity
```
````
