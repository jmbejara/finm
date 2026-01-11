---
orphan: true
---

# {py:mod}`finm.data.fama_french._pull`

```{py:module} finm.data.fama_french._pull
```

```{autodoc2-docstring} finm.data.fama_french._pull
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`pull_data <finm.data.fama_french._pull.pull_data>`
  - ```{autodoc2-docstring} finm.data.fama_french._pull.pull_data
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`FrequencyType <finm.data.fama_french._pull.FrequencyType>`
  - ```{autodoc2-docstring} finm.data.fama_french._pull.FrequencyType
    :summary:
    ```
````

### API

````{py:data} FrequencyType
:canonical: finm.data.fama_french._pull.FrequencyType
:value: >
   None

```{autodoc2-docstring} finm.data.fama_french._pull.FrequencyType
```

````

````{py:function} pull_data(data_dir: pathlib.Path | str, start: str | datetime.datetime | None = None, end: str | datetime.datetime | None = None, frequency: finm.data.fama_french._pull.FrequencyType = 'daily', accept_license: bool = False) -> pandas.DataFrame
:canonical: finm.data.fama_french._pull.pull_data

```{autodoc2-docstring} finm.data.fama_french._pull.pull_data
```
````
