# {py:mod}`finm.data.federal_reserve`

```{py:module} finm.data.federal_reserve
```

```{autodoc2-docstring} finm.data.federal_reserve
:allowtitles:
```

## Package Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`load <finm.data.federal_reserve.load>`
  - ```{autodoc2-docstring} finm.data.federal_reserve.load
    :summary:
    ```
* - {py:obj}`pull <finm.data.federal_reserve.pull>`
  - ```{autodoc2-docstring} finm.data.federal_reserve.pull
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`FormatType <finm.data.federal_reserve.FormatType>`
  - ```{autodoc2-docstring} finm.data.federal_reserve.FormatType
    :summary:
    ```
* - {py:obj}`VariantType <finm.data.federal_reserve.VariantType>`
  - ```{autodoc2-docstring} finm.data.federal_reserve.VariantType
    :summary:
    ```
````

### API

````{py:data} FormatType
:canonical: finm.data.federal_reserve.FormatType
:value: >
   None

```{autodoc2-docstring} finm.data.federal_reserve.FormatType
```

````

````{py:data} VariantType
:canonical: finm.data.federal_reserve.VariantType
:value: >
   None

```{autodoc2-docstring} finm.data.federal_reserve.VariantType
```

````

````{py:function} load(data_dir: pathlib.Path | str, variant: finm.data.federal_reserve.VariantType = 'standard', format: finm.data.federal_reserve.FormatType = 'wide', pull_if_not_found: bool = False, accept_license: bool = False, lazy: bool = False) -> typing.Union[polars.DataFrame, polars.LazyFrame]
:canonical: finm.data.federal_reserve.load

```{autodoc2-docstring} finm.data.federal_reserve.load
```
````

````{py:function} pull(data_dir: pathlib.Path | str, accept_license: bool = False) -> tuple[pandas.DataFrame, pandas.DataFrame]
:canonical: finm.data.federal_reserve.pull

```{autodoc2-docstring} finm.data.federal_reserve.pull
```
````
