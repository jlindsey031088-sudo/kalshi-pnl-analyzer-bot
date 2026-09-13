#!/usr/bin/env python3
"""Main entry point for Kalshi P&L Analyzer Bot."""

import click
from pathlib import Path
from kalshi_analyzer import KalshiAnalyzer
from kalshi_analyzer.reporter import ReportGenerator


@click.group()
def cli():
    """Kalshi P&L Analyzer Bot - Analyze your trading performance."""
    pass


@cli.command()
@click.argument("csv_file", type=click.Path(exists=True))
@click.option(
    "--top",
    default=5,
    help="Number of top performers to display",
    type=int,
)
@click.option(
    "--bottom",
    default=5,
    help="Number of bottom performers to display",
    type=int,
)
@click.option(
    "--export",
    type=click.Path(),
    help="Export summary to JSON file",
)
def analyze(csv_file: str, top: int, bottom: int, export: str):
    """Analyze Kalshi CSV export file.
    
    CSV_FILE: Path to Kalshi CSV export
    """
    click.echo(f"Loading {csv_file}...")

    analyzer = KalshiAnalyzer(csv_file)
    metrics = analyzer.calculate_metrics()

    # Generate reports
    ReportGenerator.print_summary(metrics)
    ReportGenerator.print_top_performers(analyzer, n=top)
    ReportGenerator.print_bottom_performers(analyzer, n=bottom)

    # Export if requested
    if export:
        ReportGenerator.export_summary_json(metrics, export)
        click.echo(f"Summary exported to {export}")


if __name__ == "__main__":
    cli()
