---
orphan: true
---

# {py:mod}`finm.data.wrds._pull`

```{py:module} finm.data.wrds._pull
```

```{autodoc2-docstring} finm.data.wrds._pull
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`calc_runness <finm.data.wrds._pull.calc_runness>`
  - ```{autodoc2-docstring} finm.data.wrds._pull.calc_runness
    :summary:
    ```
* - {py:obj}`pull_corp_bond <finm.data.wrds._pull.pull_corp_bond>`
  - ```{autodoc2-docstring} finm.data.wrds._pull.pull_corp_bond
    :summary:
    ```
* - {py:obj}`pull_treasury <finm.data.wrds._pull.pull_treasury>`
  - ```{autodoc2-docstring} finm.data.wrds._pull.pull_treasury
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`TreasuryVariantType <finm.data.wrds._pull.TreasuryVariantType>`
  - ```{autodoc2-docstring} finm.data.wrds._pull.TreasuryVariantType
    :summary:
    ```
````

### API

````{py:data} TreasuryVariantType
:canonical: finm.data.wrds._pull.TreasuryVariantType
:value: >
   None

```{autodoc2-docstring} finm.data.wrds._pull.TreasuryVariantType
```

````

````{py:function} calc_runness(data: pandas.DataFrame) -> pandas.DataFrame
:canonical: finm.data.wrds._pull.calc_runness

```{autodoc2-docstring} finm.data.wrds._pull.calc_runness
```
````

````{py:function} pull_corp_bond(data_dir: pathlib.Path | str, wrds_username: str, start_date: str, end_date: str) -> pandas.DataFrame
:canonical: finm.data.wrds._pull.pull_corp_bond

```{autodoc2-docstring} finm.data.wrds._pull.pull_corp_bond
```
````

````{py:function} pull_treasury(data_dir: pathlib.Path | str, wrds_username: str, start_date: str, end_date: str, variant: finm.data.wrds._pull.TreasuryVariantType = 'consolidated', with_runness: bool = True) -> pandas.DataFrame
:canonical: finm.data.wrds._pull.pull_treasury

```{autodoc2-docstring} finm.data.wrds._pull.pull_treasury
```
````
