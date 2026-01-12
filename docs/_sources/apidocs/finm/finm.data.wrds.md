# {py:mod}`finm.data.wrds`

```{py:module} finm.data.wrds
```

```{autodoc2-docstring} finm.data.wrds
:allowtitles:
```

## Package Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`load <finm.data.wrds.load>`
  - ```{autodoc2-docstring} finm.data.wrds.load
    :summary:
    ```
* - {py:obj}`pull <finm.data.wrds.pull>`
  - ```{autodoc2-docstring} finm.data.wrds.pull
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`DatasetType <finm.data.wrds.DatasetType>`
  - ```{autodoc2-docstring} finm.data.wrds.DatasetType
    :summary:
    ```
* - {py:obj}`FormatType <finm.data.wrds.FormatType>`
  - ```{autodoc2-docstring} finm.data.wrds.FormatType
    :summary:
    ```
* - {py:obj}`TreasuryVariantType <finm.data.wrds.TreasuryVariantType>`
  - ```{autodoc2-docstring} finm.data.wrds.TreasuryVariantType
    :summary:
    ```
````

### API

````{py:data} DatasetType
:canonical: finm.data.wrds.DatasetType
:value: >
   None

```{autodoc2-docstring} finm.data.wrds.DatasetType
```

````

````{py:data} FormatType
:canonical: finm.data.wrds.FormatType
:value: >
   None

```{autodoc2-docstring} finm.data.wrds.FormatType
```

````

````{py:data} TreasuryVariantType
:canonical: finm.data.wrds.TreasuryVariantType
:value: >
   None

```{autodoc2-docstring} finm.data.wrds.TreasuryVariantType
```

````

````{py:function} load(data_dir: pathlib.Path | str, variant: finm.data.wrds.DatasetType, format: finm.data.wrds.FormatType = 'wide', treasury_variant: finm.data.wrds.TreasuryVariantType = 'consolidated', with_runness: bool = True, pull_if_not_found: bool = False, wrds_username: str | None = None, start_date: str | None = None, end_date: str | None = None, lazy: bool = False) -> typing.Union[polars.DataFrame, polars.LazyFrame]
:canonical: finm.data.wrds.load

```{autodoc2-docstring} finm.data.wrds.load
```
````

````{py:function} pull(data_dir: pathlib.Path | str, variant: finm.data.wrds.DatasetType, wrds_username: str, start_date: str | None = None, end_date: str | None = None, treasury_variant: finm.data.wrds.TreasuryVariantType = 'consolidated', with_runness: bool = True) -> pandas.DataFrame
:canonical: finm.data.wrds.pull

```{autodoc2-docstring} finm.data.wrds.pull
```
````
