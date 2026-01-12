---
orphan: true
---

# {py:mod}`finm.data.wrds._transform`

```{py:module} finm.data.wrds._transform
```

```{autodoc2-docstring} finm.data.wrds._transform
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`corp_bond_to_long_format <finm.data.wrds._transform.corp_bond_to_long_format>`
  - ```{autodoc2-docstring} finm.data.wrds._transform.corp_bond_to_long_format
    :summary:
    ```
* - {py:obj}`treasury_to_long_format <finm.data.wrds._transform.treasury_to_long_format>`
  - ```{autodoc2-docstring} finm.data.wrds._transform.treasury_to_long_format
    :summary:
    ```
````

### API

````{py:function} corp_bond_to_long_format(df: pandas.DataFrame, value_column: str = 'ret_eom') -> pandas.DataFrame
:canonical: finm.data.wrds._transform.corp_bond_to_long_format

```{autodoc2-docstring} finm.data.wrds._transform.corp_bond_to_long_format
```
````

````{py:function} treasury_to_long_format(df: pandas.DataFrame, value_column: str = 'price') -> pandas.DataFrame
:canonical: finm.data.wrds._transform.treasury_to_long_format

```{autodoc2-docstring} finm.data.wrds._transform.treasury_to_long_format
```
````
