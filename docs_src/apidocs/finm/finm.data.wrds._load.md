---
orphan: true
---

# {py:mod}`finm.data.wrds._load`

```{py:module} finm.data.wrds._load
```

```{autodoc2-docstring} finm.data.wrds._load
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`load_corp_bond <finm.data.wrds._load.load_corp_bond>`
  - ```{autodoc2-docstring} finm.data.wrds._load.load_corp_bond
    :summary:
    ```
* - {py:obj}`load_treasury <finm.data.wrds._load.load_treasury>`
  - ```{autodoc2-docstring} finm.data.wrds._load.load_treasury
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`TreasuryVariantType <finm.data.wrds._load.TreasuryVariantType>`
  - ```{autodoc2-docstring} finm.data.wrds._load.TreasuryVariantType
    :summary:
    ```
````

### API

````{py:data} TreasuryVariantType
:canonical: finm.data.wrds._load.TreasuryVariantType
:value: >
   None

```{autodoc2-docstring} finm.data.wrds._load.TreasuryVariantType
```

````

````{py:function} load_corp_bond(data_dir: pathlib.Path | str) -> pandas.DataFrame
:canonical: finm.data.wrds._load.load_corp_bond

```{autodoc2-docstring} finm.data.wrds._load.load_corp_bond
```
````

````{py:function} load_treasury(data_dir: pathlib.Path | str, variant: finm.data.wrds._load.TreasuryVariantType = 'consolidated', with_runness: bool = True) -> pandas.DataFrame
:canonical: finm.data.wrds._load.load_treasury

```{autodoc2-docstring} finm.data.wrds._load.load_treasury
```
````
