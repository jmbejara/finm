# {py:mod}`finm.data.fama_french`

```{py:module} finm.data.fama_french
```

```{autodoc2-docstring} finm.data.fama_french
:allowtitles:
```

## Package Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`load <finm.data.fama_french.load>`
  - ```{autodoc2-docstring} finm.data.fama_french.load
    :summary:
    ```
* - {py:obj}`pull <finm.data.fama_french.pull>`
  - ```{autodoc2-docstring} finm.data.fama_french.pull
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`FormatType <finm.data.fama_french.FormatType>`
  - ```{autodoc2-docstring} finm.data.fama_french.FormatType
    :summary:
    ```
* - {py:obj}`FrequencyType <finm.data.fama_french.FrequencyType>`
  - ```{autodoc2-docstring} finm.data.fama_french.FrequencyType
    :summary:
    ```
````

### API

````{py:data} FormatType
:canonical: finm.data.fama_french.FormatType
:value: >
   None

```{autodoc2-docstring} finm.data.fama_french.FormatType
```

````

````{py:data} FrequencyType
:canonical: finm.data.fama_french.FrequencyType
:value: >
   None

```{autodoc2-docstring} finm.data.fama_french.FrequencyType
```

````

````{py:function} load(data_dir: pathlib.Path | str | None = None, start: str | datetime.datetime | None = None, end: str | datetime.datetime | None = None, format: finm.data.fama_french.FormatType = 'wide', frequency: finm.data.fama_french.FrequencyType = 'daily', pull_if_not_found: bool = False, accept_license: bool = False, lazy: bool = False) -> typing.Union[polars.DataFrame, polars.LazyFrame]
:canonical: finm.data.fama_french.load

```{autodoc2-docstring} finm.data.fama_french.load
```
````

````{py:function} pull(data_dir: pathlib.Path | str, start: str | datetime.datetime | None = None, end: str | datetime.datetime | None = None, frequency: finm.data.fama_french.FrequencyType = 'daily', accept_license: bool = False) -> pandas.DataFrame
:canonical: finm.data.fama_french.pull

```{autodoc2-docstring} finm.data.fama_french.pull
```
````
