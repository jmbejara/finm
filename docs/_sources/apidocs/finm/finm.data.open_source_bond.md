# {py:mod}`finm.data.open_source_bond`

```{py:module} finm.data.open_source_bond
```

```{autodoc2-docstring} finm.data.open_source_bond
:allowtitles:
```

## Package Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`load <finm.data.open_source_bond.load>`
  - ```{autodoc2-docstring} finm.data.open_source_bond.load
    :summary:
    ```
* - {py:obj}`pull <finm.data.open_source_bond.pull>`
  - ```{autodoc2-docstring} finm.data.open_source_bond.pull
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`FormatType <finm.data.open_source_bond.FormatType>`
  - ```{autodoc2-docstring} finm.data.open_source_bond.FormatType
    :summary:
    ```
* - {py:obj}`PullVariantType <finm.data.open_source_bond.PullVariantType>`
  - ```{autodoc2-docstring} finm.data.open_source_bond.PullVariantType
    :summary:
    ```
* - {py:obj}`VariantType <finm.data.open_source_bond.VariantType>`
  - ```{autodoc2-docstring} finm.data.open_source_bond.VariantType
    :summary:
    ```
````

### API

````{py:data} FormatType
:canonical: finm.data.open_source_bond.FormatType
:value: >
   None

```{autodoc2-docstring} finm.data.open_source_bond.FormatType
```

````

````{py:data} PullVariantType
:canonical: finm.data.open_source_bond.PullVariantType
:value: >
   None

```{autodoc2-docstring} finm.data.open_source_bond.PullVariantType
```

````

````{py:data} VariantType
:canonical: finm.data.open_source_bond.VariantType
:value: >
   None

```{autodoc2-docstring} finm.data.open_source_bond.VariantType
```

````

````{py:function} load(data_dir: pathlib.Path | str, variant: finm.data.open_source_bond.VariantType = 'treasury', format: finm.data.open_source_bond.FormatType = 'wide', pull_if_not_found: bool = False, accept_license: bool = False, lazy: bool = False) -> typing.Union[polars.DataFrame, polars.LazyFrame]
:canonical: finm.data.open_source_bond.load

```{autodoc2-docstring} finm.data.open_source_bond.load
```
````

````{py:function} pull(data_dir: pathlib.Path | str, variant: finm.data.open_source_bond.PullVariantType = 'all', accept_license: bool = False, download_readme: bool = True) -> None
:canonical: finm.data.open_source_bond.pull

```{autodoc2-docstring} finm.data.open_source_bond.pull
```
````
