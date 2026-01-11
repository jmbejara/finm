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

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`VariantType <finm.data.open_source_bond._transform.VariantType>`
  - ```{autodoc2-docstring} finm.data.open_source_bond._transform.VariantType
    :summary:
    ```
````

### API

````{py:data} VariantType
:canonical: finm.data.open_source_bond._transform.VariantType
:value: >
   None

```{autodoc2-docstring} finm.data.open_source_bond._transform.VariantType
```

````

````{py:function} portfolio_to_long_format(df: pandas.DataFrame) -> pandas.DataFrame
:canonical: finm.data.open_source_bond._transform.portfolio_to_long_format

```{autodoc2-docstring} finm.data.open_source_bond._transform.portfolio_to_long_format
```
````

````{py:function} to_long_format(df: pandas.DataFrame, id_column: str | None = None, date_column: str | None = None, value_column: str | None = None, variant: finm.data.open_source_bond._transform.VariantType | None = None) -> pandas.DataFrame
:canonical: finm.data.open_source_bond._transform.to_long_format

```{autodoc2-docstring} finm.data.open_source_bond._transform.to_long_format
```
````
