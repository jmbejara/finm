---
orphan: true
---

# {py:mod}`finm.data._credentials`

```{py:module} finm.data._credentials
```

```{autodoc2-docstring} finm.data._credentials
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`get_credentials <finm.data._credentials.get_credentials>`
  - ```{autodoc2-docstring} finm.data._credentials.get_credentials
    :summary:
    ```
* - {py:obj}`get_data_dir <finm.data._credentials.get_data_dir>`
  - ```{autodoc2-docstring} finm.data._credentials.get_data_dir
    :summary:
    ```
* - {py:obj}`validate_credentials <finm.data._credentials.validate_credentials>`
  - ```{autodoc2-docstring} finm.data._credentials.validate_credentials
    :summary:
    ```
````

### API

````{py:function} get_credentials(wrds_username: typing.Optional[str] = None, env_file: typing.Optional[pathlib.Path] = None, interactive: bool = True) -> dict[str, typing.Optional[str]]
:canonical: finm.data._credentials.get_credentials

```{autodoc2-docstring} finm.data._credentials.get_credentials
```
````

````{py:function} get_data_dir(data_dir: typing.Optional[str | pathlib.Path] = None, env_file: typing.Optional[pathlib.Path] = None) -> pathlib.Path
:canonical: finm.data._credentials.get_data_dir

```{autodoc2-docstring} finm.data._credentials.get_data_dir
```
````

````{py:function} validate_credentials(required: list[str], credentials: dict[str, typing.Optional[str]]) -> None
:canonical: finm.data._credentials.validate_credentials

```{autodoc2-docstring} finm.data._credentials.validate_credentials
```
````
