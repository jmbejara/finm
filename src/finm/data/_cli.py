"""CLI for finm data module.

Usage:
    finm pull <dataset> [options]
    finm list
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Annotated, Optional

import typer

from finm.data._credentials import get_credentials, get_data_dir

app = typer.Typer(
    name="finm",
    help="finm data management CLI. Download and manage financial data from various sources.",
    no_args_is_help=True,
)


class Dataset(str, Enum):
    """Available datasets to pull."""

    fed_yield_curve = "fed_yield_curve"
    fama_french = "fama_french"
    he_kelly_manela = "he_kelly_manela"
    open_source_bond_treasury = "open_source_bond_treasury"
    open_source_bond_corporate = "open_source_bond_corporate"
    open_source_bond_corporate_daily = "open_source_bond_corporate_daily"
    open_source_bond_corporate_monthly = "open_source_bond_corporate_monthly"
    wrds_treasury = "wrds_treasury"
    wrds_corp_bond = "wrds_corp_bond"


class Format(str, Enum):
    """Output format options."""

    wide = "wide"
    long = "long"


@app.command("pull")
def pull(
    dataset: Annotated[Dataset, typer.Argument(help="Dataset to pull")],
    data_dir: Annotated[
        Optional[Path],
        typer.Option(
            "--data-dir",
            "-d",
            help="Directory for data storage. Overrides DATA_DIR env var.",
        ),
    ] = None,
    accept_license: Annotated[
        bool,
        typer.Option(
            "--accept-license",
            help="Acknowledge the data provider's license terms to proceed.",
        ),
    ] = False,
    wrds_username: Annotated[
        Optional[str],
        typer.Option(
            "--wrds-username",
            help="WRDS username (overrides env var). Required for WRDS datasets.",
        ),
    ] = None,
    start_date: Annotated[
        Optional[str],
        typer.Option("--start-date", help="Start date (YYYY-MM-DD)"),
    ] = None,
    end_date: Annotated[
        Optional[str],
        typer.Option("--end-date", help="End date (YYYY-MM-DD)"),
    ] = None,
    output_format: Annotated[
        Format,
        typer.Option("--format", "-f", help="Output format"),
    ] = Format.wide,
) -> None:
    """Pull a dataset from its source and save locally.

    Examples:

        finm pull fed_yield_curve

        finm pull wrds_treasury --wrds-username=myuser --start-date=2020-01-01

        finm pull he_kelly_manela --format=long
    """
    # Resolve data directory
    resolved_data_dir = get_data_dir(data_dir)
    resolved_data_dir.mkdir(parents=True, exist_ok=True)

    # Get credentials (will prompt interactively if needed for WRDS)
    requires_wrds = dataset.value.startswith("wrds_")
    credentials = get_credentials(
        wrds_username=wrds_username, interactive=requires_wrds
    )

    typer.echo(f"Pulling {dataset.value} to {resolved_data_dir}...")

    try:
        if dataset == Dataset.fed_yield_curve:
            from finm.data import federal_reserve

            federal_reserve.pull(
                data_dir=resolved_data_dir, accept_license=accept_license
            )

        elif dataset == Dataset.fama_french:
            from finm.data import fama_french

            fama_french.pull(data_dir=resolved_data_dir, accept_license=accept_license)

        elif dataset == Dataset.he_kelly_manela:
            from finm.data import he_kelly_manela

            he_kelly_manela.pull(
                data_dir=resolved_data_dir, accept_license=accept_license
            )

        elif dataset == Dataset.open_source_bond_treasury:
            from finm.data import open_source_bond

            open_source_bond.pull(
                data_dir=resolved_data_dir,
                variant="treasury",
                accept_license=accept_license,
            )

        elif dataset == Dataset.open_source_bond_corporate:
            from finm.data import open_source_bond

            open_source_bond.pull(
                data_dir=resolved_data_dir,
                variant="corporate_monthly",
                accept_license=accept_license,
            )

        elif dataset == Dataset.open_source_bond_corporate_daily:
            from finm.data import open_source_bond

            open_source_bond.pull(
                data_dir=resolved_data_dir,
                variant="corporate_daily",
                accept_license=accept_license,
            )

        elif dataset == Dataset.open_source_bond_corporate_monthly:
            from finm.data import open_source_bond

            open_source_bond.pull(
                data_dir=resolved_data_dir,
                variant="corporate_monthly",
                accept_license=accept_license,
            )

        elif dataset == Dataset.wrds_treasury:
            if not credentials.get("wrds_username"):
                raise typer.BadParameter(
                    "WRDS username required. Provide via --wrds-username or WRDS_USERNAME env var."
                )
            if not start_date or not end_date:
                raise typer.BadParameter(
                    "WRDS treasury requires --start-date and --end-date"
                )

            from finm.data import wrds

            wrds.pull(
                data_dir=resolved_data_dir,
                variant="treasury",
                wrds_username=credentials["wrds_username"],
                start_date=start_date,
                end_date=end_date,
            )

        elif dataset == Dataset.wrds_corp_bond:
            if not credentials.get("wrds_username"):
                raise typer.BadParameter(
                    "WRDS username required. Provide via --wrds-username or WRDS_USERNAME env var."
                )
            if not start_date or not end_date:
                raise typer.BadParameter(
                    "WRDS corp bond requires --start-date and --end-date"
                )

            from finm.data import wrds

            wrds.pull(
                data_dir=resolved_data_dir,
                variant="corp_bond",
                wrds_username=credentials["wrds_username"],
                start_date=start_date,
                end_date=end_date,
            )

        typer.echo(f"Successfully pulled {dataset.value} to {resolved_data_dir}")

    except Exception as e:
        typer.echo(f"Error pulling {dataset.value}: {e}", err=True)
        raise typer.Exit(code=1)


@app.command("list")
def list_datasets() -> None:
    """List all available datasets."""
    typer.echo("Available datasets:\n")

    datasets_info = [
        ("fed_yield_curve", "Federal Reserve GSW yield curve", "No"),
        ("fama_french", "Fama-French 3 factors (daily)", "No"),
        ("he_kelly_manela", "He-Kelly-Manela intermediary factors", "No"),
        (
            "open_source_bond_treasury",
            "Treasury bond returns (Open Bond Asset Pricing)",
            "No",
        ),
        (
            "open_source_bond_corporate",
            "Corporate bond returns (monthly, deprecated)",
            "No",
        ),
        (
            "open_source_bond_corporate_daily",
            "Corporate bond daily PRICES (TRACE Stage 1)",
            "No",
        ),
        (
            "open_source_bond_corporate_monthly",
            "Corporate bond monthly RETURNS + 108 factors",
            "No",
        ),
        ("wrds_treasury", "CRSP Treasury data", "Yes"),
        ("wrds_corp_bond", "WRDS corporate bond returns", "Yes"),
    ]

    # Print header
    typer.echo(f"{'Dataset':<30} {'Description':<45} {'WRDS?':<6}")
    typer.echo("-" * 81)

    for name, description, requires_wrds in datasets_info:
        typer.echo(f"{name:<30} {description:<45} {requires_wrds:<6}")


@app.command("info")
def info(
    dataset: Annotated[Dataset, typer.Argument(help="Dataset to get info about")],
) -> None:
    """Show detailed information about a dataset."""
    info_map = {
        Dataset.fed_yield_curve: {
            "name": "Federal Reserve Yield Curve",
            "source": "https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv",
            "description": "GSW (Gurkaynak, Sack, Wright) yield curve model data",
            "variants": ["standard (SVENY01-30)", "all (full dataset)"],
            "credentials": "None required",
        },
        Dataset.fama_french: {
            "name": "Fama-French 3 Factors",
            "source": "Ken French Data Library (via pandas-datareader)",
            "description": "Daily Fama-French 3 factors: Mkt-RF, SMB, HML, RF",
            "variants": ["daily", "monthly"],
            "credentials": "None required",
        },
        Dataset.he_kelly_manela: {
            "name": "He-Kelly-Manela Factors",
            "source": "https://asaf.manela.org/papers/hkm/intermediarycapitalrisk/",
            "description": "Intermediary capital risk factors from He, Kelly, and Manela (2017)",
            "variants": ["factors_monthly", "factors_daily", "all"],
            "credentials": "None required",
        },
        Dataset.open_source_bond_treasury: {
            "name": "Open Source Bond - Treasury Returns",
            "source": "https://openbondassetpricing.com/",
            "description": "Treasury bond returns from Open Bond Asset Pricing",
            "variants": ["treasury"],
            "credentials": "None required (--accept-license flag required)",
        },
        Dataset.open_source_bond_corporate: {
            "name": "Open Source Bond - Corporate Returns (Deprecated)",
            "source": "https://openbondassetpricing.com/",
            "description": "Use open_source_bond_corporate_monthly instead",
            "variants": ["corporate_monthly"],
            "credentials": "None required (--accept-license flag required)",
        },
        Dataset.open_source_bond_corporate_daily: {
            "name": "Open Source Bond - Corporate Daily Prices",
            "source": "https://openbondassetpricing.com/",
            "description": "Daily corporate bond PRICES from TRACE Stage 1 (~1.8GB)",
            "variants": ["corporate_daily"],
            "credentials": "None required (--accept-license flag required)",
        },
        Dataset.open_source_bond_corporate_monthly: {
            "name": "Open Source Bond - Corporate Monthly Returns",
            "source": "https://openbondassetpricing.com/",
            "description": "Monthly corporate bond RETURNS + 108 factor signals (~1.2GB)",
            "variants": ["corporate_monthly"],
            "credentials": "None required (--accept-license flag required)",
        },
        Dataset.wrds_treasury: {
            "name": "CRSP Treasury Data",
            "source": "WRDS CRSP US Treasury Database",
            "description": "Daily Treasury prices, yields, and characteristics",
            "variants": ["daily", "info", "consolidated"],
            "credentials": "WRDS_USERNAME required",
        },
        Dataset.wrds_corp_bond: {
            "name": "WRDS Corporate Bond Returns",
            "source": "WRDS wrdsapps.bondret",
            "description": "Monthly corporate bond returns with ratings",
            "variants": ["monthly"],
            "credentials": "WRDS_USERNAME required",
        },
    }

    dataset_info = info_map[dataset]

    typer.echo(f"\n{dataset_info['name']}")
    typer.echo("=" * len(dataset_info["name"]))
    typer.echo(f"\nSource: {dataset_info['source']}")
    typer.echo(f"Description: {dataset_info['description']}")
    typer.echo(f"Variants: {', '.join(dataset_info['variants'])}")
    typer.echo(f"Credentials: {dataset_info['credentials']}")


def main() -> None:
    """Entry point for CLI."""
    app()


if __name__ == "__main__":
    main()
