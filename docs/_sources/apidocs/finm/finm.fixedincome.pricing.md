# {py:mod}`finm.fixedincome.pricing`

```{py:module} finm.fixedincome.pricing
```

```{autodoc2-docstring} finm.fixedincome.pricing
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`bond_price <finm.fixedincome.pricing.bond_price>`
  - ```{autodoc2-docstring} finm.fixedincome.pricing.bond_price
    :summary:
    ```
* - {py:obj}`bond_price_ql <finm.fixedincome.pricing.bond_price_ql>`
  - ```{autodoc2-docstring} finm.fixedincome.pricing.bond_price_ql
    :summary:
    ```
* - {py:obj}`get_coupon_dates <finm.fixedincome.pricing.get_coupon_dates>`
  - ```{autodoc2-docstring} finm.fixedincome.pricing.get_coupon_dates
    :summary:
    ```
* - {py:obj}`get_coupon_dates_ql <finm.fixedincome.pricing.get_coupon_dates_ql>`
  - ```{autodoc2-docstring} finm.fixedincome.pricing.get_coupon_dates_ql
    :summary:
    ```
````

### API

````{py:function} bond_price(face_value: float, coupon_rate: float, ytm: float, periods: int, frequency: int = 2) -> float
:canonical: finm.fixedincome.pricing.bond_price

```{autodoc2-docstring} finm.fixedincome.pricing.bond_price
```
````

````{py:function} bond_price_ql(face_value: float, coupon_rate: float, ytm: float, periods: int, frequency: int = 2) -> float
:canonical: finm.fixedincome.pricing.bond_price_ql

```{autodoc2-docstring} finm.fixedincome.pricing.bond_price_ql
```
````

````{py:function} get_coupon_dates(quote_date, maturity_date)
:canonical: finm.fixedincome.pricing.get_coupon_dates

```{autodoc2-docstring} finm.fixedincome.pricing.get_coupon_dates
```
````

````{py:function} get_coupon_dates_ql(quote_date, maturity_date, calendar=ql.UnitedStates(m=ql.UnitedStates.GovernmentBond), business_convention=ql.Following, end_of_month=False)
:canonical: finm.fixedincome.pricing.get_coupon_dates_ql

```{autodoc2-docstring} finm.fixedincome.pricing.get_coupon_dates_ql
```
````
