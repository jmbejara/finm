---
orphan: true
---

# {py:mod}`finm.data.open_source_bond._transform`

```{py:module} finm.data.open_source_bond._transform
```

```{autodoc2-docstring} finm.data.open_source_bond._transform
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`portfolio_to_long_format <finm.data.open_source_bond._transform.portfolio_to_long_format>`
  - ```{autodoc2-docstring} finm.data.open_source_bond._transform.portfolio_to_long_format
    :summary:
    ```
* - {py:obj}`to_long_format <finm.data.open_source_bond._transform.to_long_format>`
  - ```{autodoc2-docstring} finm.data.open_source_bond._transform.to_long_format
    :summary:
    ```
````

### API

````{py:function} portfolio_to_long_format(df: pandas.DataFrame) -> pandas.DataFrame
:canonical: finm.data.open_source_bond._transform.portfolio_to_long_format

```{autodoc2-docstring} finm.data.open_source_bond._transform.portfolio_to_long_format
```
````

````{py:function} to_long_format(df: pandas.DataFrame, id_column: str = 'cusip', date_column: str = 'date', value_column: str = 'bond_ret') -> pandas.DataFrame
:canonical: finm.data.open_source_bond._transform.to_long_format

```{autodoc2-docstring} finm.data.open_source_bond._transform.to_long_format
```
````
