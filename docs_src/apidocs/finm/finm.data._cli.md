---
orphan: true
---

# {py:mod}`finm.data._cli`

```{py:module} finm.data._cli
```

```{autodoc2-docstring} finm.data._cli
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Dataset <finm.data._cli.Dataset>`
  - ```{autodoc2-docstring} finm.data._cli.Dataset
    :summary:
    ```
* - {py:obj}`Format <finm.data._cli.Format>`
  - ```{autodoc2-docstring} finm.data._cli.Format
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`info <finm.data._cli.info>`
  - ```{autodoc2-docstring} finm.data._cli.info
    :summary:
    ```
* - {py:obj}`list_datasets <finm.data._cli.list_datasets>`
  - ```{autodoc2-docstring} finm.data._cli.list_datasets
    :summary:
    ```
* - {py:obj}`main <finm.data._cli.main>`
  - ```{autodoc2-docstring} finm.data._cli.main
    :summary:
    ```
* - {py:obj}`pull <finm.data._cli.pull>`
  - ```{autodoc2-docstring} finm.data._cli.pull
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`app <finm.data._cli.app>`
  - ```{autodoc2-docstring} finm.data._cli.app
    :summary:
    ```
````

### API

`````{py:class} Dataset()
:canonical: finm.data._cli.Dataset

Bases: {py:obj}`str`, {py:obj}`enum.Enum`

```{autodoc2-docstring} finm.data._cli.Dataset
```

```{rubric} Initialization
```

```{autodoc2-docstring} finm.data._cli.Dataset.__init__
```

````{py:attribute} fama_french
:canonical: finm.data._cli.Dataset.fama_french
:value: >
   'fama_french'

```{autodoc2-docstring} finm.data._cli.Dataset.fama_french
```

````

````{py:attribute} fed_yield_curve
:canonical: finm.data._cli.Dataset.fed_yield_curve
:value: >
   'fed_yield_curve'

```{autodoc2-docstring} finm.data._cli.Dataset.fed_yield_curve
```

````

````{py:attribute} he_kelly_manela
:canonical: finm.data._cli.Dataset.he_kelly_manela
:value: >
   'he_kelly_manela'

```{autodoc2-docstring} finm.data._cli.Dataset.he_kelly_manela
```

````

````{py:attribute} open_source_bond_corporate
:canonical: finm.data._cli.Dataset.open_source_bond_corporate
:value: >
   'open_source_bond_corporate'

```{autodoc2-docstring} finm.data._cli.Dataset.open_source_bond_corporate
```

````

````{py:attribute} open_source_bond_treasury
:canonical: finm.data._cli.Dataset.open_source_bond_treasury
:value: >
   'open_source_bond_treasury'

```{autodoc2-docstring} finm.data._cli.Dataset.open_source_bond_treasury
```

````

````{py:attribute} wrds_corp_bond
:canonical: finm.data._cli.Dataset.wrds_corp_bond
:value: >
   'wrds_corp_bond'

```{autodoc2-docstring} finm.data._cli.Dataset.wrds_corp_bond
```

````

````{py:attribute} wrds_treasury
:canonical: finm.data._cli.Dataset.wrds_treasury
:value: >
   'wrds_treasury'

```{autodoc2-docstring} finm.data._cli.Dataset.wrds_treasury
```

````

`````

`````{py:class} Format()
:canonical: finm.data._cli.Format

Bases: {py:obj}`str`, {py:obj}`enum.Enum`

```{autodoc2-docstring} finm.data._cli.Format
```

```{rubric} Initialization
```

```{autodoc2-docstring} finm.data._cli.Format.__init__
```

````{py:attribute} long
:canonical: finm.data._cli.Format.long
:value: >
   'long'

```{autodoc2-docstring} finm.data._cli.Format.long
```

````

````{py:attribute} wide
:canonical: finm.data._cli.Format.wide
:value: >
   'wide'

```{autodoc2-docstring} finm.data._cli.Format.wide
```

````

`````

````{py:data} app
:canonical: finm.data._cli.app
:value: >
   'Typer(...)'

```{autodoc2-docstring} finm.data._cli.app
```

````

````{py:function} info(dataset: typing.Annotated[finm.data._cli.Dataset, typer.Argument(help='Dataset to get info about')]) -> None
:canonical: finm.data._cli.info

```{autodoc2-docstring} finm.data._cli.info
```
````

````{py:function} list_datasets() -> None
:canonical: finm.data._cli.list_datasets

```{autodoc2-docstring} finm.data._cli.list_datasets
```
````

````{py:function} main() -> None
:canonical: finm.data._cli.main

```{autodoc2-docstring} finm.data._cli.main
```
````

````{py:function} pull(dataset: typing.Annotated[finm.data._cli.Dataset, typer.Argument(help='Dataset to pull')], data_dir: typing.Annotated[typing.Optional[pathlib.Path], typer.Option('--data-dir', '-d', help='Directory for data storage. Overrides DATA_DIR env var.')] = None, wrds_username: typing.Annotated[typing.Optional[str], typer.Option('--wrds-username', help='WRDS username (overrides env var). Required for WRDS datasets.')] = None, start_date: typing.Annotated[typing.Optional[str], typer.Option('--start-date', help='Start date (YYYY-MM-DD)')] = None, end_date: typing.Annotated[typing.Optional[str], typer.Option('--end-date', help='End date (YYYY-MM-DD)')] = None, output_format: typing.Annotated[finm.data._cli.Format, typer.Option('--format', '-f', help='Output format')] = Format.wide) -> None
:canonical: finm.data._cli.pull

```{autodoc2-docstring} finm.data._cli.pull
```
````
