import click
import requests
import os
from pathlib import Path
import sys
import csv
import json
import matplotlib.pyplot as plt
import numpy as np


@click.command()
def cli():
    """Main entry point for the CLI."""
    click.echo("Welcome to Techtonique CLI!")

# # Help
# techtonique --help
# techtonique forecasting --help
# techtonique forecasting univariate --help
# techtonique ml --help
# techtonique ml classification --help
# techtonique reserving --help
# techtonique survival --help
# # Univariate forecasting
# techtonique forecasting univariate /Users/t/Documents/datasets/time_series/univariate/a10.csv --base_model RidgeCV --h 3
# # Multivariate forecasting
# techtonique forecasting multivariate /Users/t/Documents/datasets/time_series/multivariate/ice_cream_vs_heater.csv --lags 25 --h 10
# # Regression
# techtonique ml regression /Users/t/Documents/datasets/tabular/regression/mtcars2.csv --base_model ElasticNet
# # Survival Analysis
# techtonique survival /Users/t/Documents/datasets/tabular/survival/kidney.csv --model coxph
class TechtoniqueCLI:
    def __init__(self, token=None):
        self.base_url = "https://www.techtonique.net"
        self.token = token or os.getenv("TECHTONIQUE_API_TOKEN")
        if not self.token:
            # Only prompt if token not found in environment
            print("Enter your API token: ", file=sys.stderr, flush=True, end='')
            self.token = input()
            if not self.token:
                raise ValueError(
                    "API token must be provided or set in TECHTONIQUE_API_TOKEN environment variable"
                )

    def _make_request(self, endpoint, file_path, params):
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            # Extract to_csv parameter before making request
            to_csv_file = params.pop('to_csv', None)  # Remove from params and store
            
            with open(file_path, "rb") as f:
                # Explicitly set the content type as 'text/csv'
                files = {"file": (file_path.name, f, "text/csv")}
                # Ensure params are strings
                str_params = {k: str(v) for k, v in params.items()}
                
                response = requests.post(
                    f"{self.base_url}/{endpoint}",
                    headers=headers,
                    files=files,
                    params=str_params,  # Use string parameters
                )
                
            response.raise_for_status()
            result = response.json()
            
            # Handle select parameter if present
            if 'select' in params and params['select']:
                keys = [k.strip() for k in params['select'].split(',')]
                result = {k: result[k] for k in keys if k in result}
                # Parse string representations of lists into actual lists
                for k, v in result.items():
                    if isinstance(v, str) and v.startswith('[') and v.endswith(']'):
                        result[k] = json.loads(v)
            
            # Handle CSV conversion if to_csv_file is present
            if to_csv_file:
                if all(isinstance(v, list) for v in result.values()):
                    with open(to_csv_file, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        # Write header
                        writer.writerow(result.keys())
                        # Write data rows
                        writer.writerows(zip(*result.values()))
                    return f"Results written to {to_csv_file}"
                else:
                    click.echo(f"Warning: Data format not suitable for CSV conversion", err=True)
            
            return result
        except requests.exceptions.RequestException as e:
            click.echo(f"Error making request: {e}", err=True)
            return None


def init_cli(ctx):
    """Initialize CLI if not in help mode"""
    if ctx.obj is None:
        ctx.ensure_object(dict)

    if "--help" not in ctx.args and "-h" not in ctx.args:
        token = ctx.obj.get("token")
        if "cli" not in ctx.obj:
            try:
                ctx.obj["cli"] = TechtoniqueCLI(token)
            except ValueError as e:
                click.echo(str(e), err=True)
                ctx.exit(1)


@click.group()
@click.option("--token", envvar="TECHTONIQUE_API_TOKEN", help="API token", required=False)
@click.pass_context
def cli(ctx, token):
    """Techtonique API CLI tool"""
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


@cli.group()
@click.pass_context
def forecasting(ctx):
    """Forecasting commands"""
    pass


@forecasting.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--base_model", default="RidgeCV", help="Base model to use")
@click.option("--n-hidden-features", default=5, help="Number of hidden features")
@click.option("--lags", default=25, help="Number of lags")
@click.option("--type-pi", default="kde", help="Type of prediction interval")
@click.option("--replications", default=4, help="Number of replications")
@click.option("--h", default=3, help="Forecast horizon")
@click.option("--select", help="Comma-separated list of keys to select from output")
@click.option("--to-csv", help="Output results to CSV file")
@click.option("--plot", help="Save forecast plot to file (e.g., 'forecast.png') or display if no filename given", is_flag=True)
@click.option("--plot-file", help="Save forecast plot to specified file")
@click.pass_context
def univariate(ctx, file, base_model, n_hidden_features, lags, type_pi, replications, h, select, to_csv, plot, plot_file):
    """Univariate forecasting

    Parameters:
        file: str
            Path to the CSV file
        base_model: str
            Base model to use
        n_hidden_features: int
            Number of hidden features
        lags: int
            Number of lags
        type_pi: str
            Type of prediction interval
        replications: int
            Number of replications
        h: int
            Forecast horizon
        select: str
            Comma-separated list of keys to select from output
        to_csv: str
            Output results to CSV file
        plot: bool
            Save forecast plot to file (e.g., 'forecast.png') or display if no filename given
        plot_file: str
            Save forecast plot to specified file

    Returns:
        dict: Result of the forecasting

    Example:

        ```python

        techtonique forecasting univariate /Users/t/Documents/datasets/time_series/univariate/a10.csv --base_model RidgeCV --h 3
        
        ```
    """
    init_cli(ctx)
    params = {
        "base_model": base_model,
        "n_hidden_features": n_hidden_features,
        "lags": lags,
        "type_pi": type_pi,
        "replications": replications,
        "h": h,
        "select": select or "mean,lower,upper" if (plot or plot_file) else select,
        "to_csv": to_csv
    }
    result = ctx.obj["cli"]._make_request("forecasting", Path(file), params)
        
    # Handle plotting if requested
    if (plot or plot_file) and isinstance(result, dict):
        required_keys = {'mean', 'lower', 'upper'}
        if all(k in result for k in required_keys):
            try:
                plt.figure(figsize=(10, 6))
                x = range(len(result['mean']))
                
                # Parse string lists if necessary
                mean = json.loads(result['mean']) if isinstance(result['mean'], str) else result['mean']
                lower = json.loads(result['lower']) if isinstance(result['lower'], str) else result['lower']
                upper = json.loads(result['upper']) if isinstance(result['upper'], str) else result['upper']
                
                # Debug information
                click.echo(f"Debug - Data lengths: mean={len(mean)}, lower={len(lower)}, upper={len(upper)}", err=True)
                
                # Plot mean forecast
                plt.plot(x, mean, 'b-', label='Forecast')
                
                # Plot confidence interval
                plt.fill_between(x, lower, upper, color='b', alpha=0.1, label='Confidence Interval')
                
                plt.title('Forecast with Confidence Intervals')
                plt.xlabel('Time Steps')
                plt.ylabel('Value')
                plt.legend()
                plt.grid(True)
                
                if plot_file:
                    # Save plot to file
                    plt.savefig(plot_file)
                    plt.close()
                    click.echo(f"Plot saved to {plot_file}")
                elif plot:
                    # Display plot
                    plt.show(block=True)
                
            except Exception as e:
                click.echo(f"Error creating plot: {str(e)}", err=True)
        else:
            click.echo(f"Debug - Missing required keys. Available keys: {result.keys()}", err=True)
    
    click.echo(result)


@forecasting.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--base_model", default="RidgeCV", help="Base model to use")
@click.option("--n-hidden-features", default=5, help="Number of hidden features")
@click.option("--lags", default=25, help="Number of lags")
@click.option("--h", default=3, help="Forecast horizon")
@click.option("--select", help="Comma-separated list of keys to select from output")
@click.option("--to-csv", help="Output results to CSV file")
@click.pass_context
def multivariate(ctx, file, base_model, n_hidden_features, lags, h, select, to_csv):
    """Multivariate forecasting

    Parameters:
        file: str
            Path to the CSV file
        base_model: str
            Base model to use
        n_hidden_features: int
            Number of hidden features
        lags: int
            Number of lags
        h: int
            Forecast horizon
        select: str
            Comma-separated list of keys to select from output
        to_csv: str
            Output results to CSV file

    Returns:
        dict: Result of the forecasting

    Example:

        ```python

        techtonique forecasting multivariate /Users/t/Documents/datasets/time_series/multivariate/ice_cream_vs_heater.csv --lags 25 --h 10

        ```
    """
    init_cli(ctx)
    params = {
        "base_model": base_model,
        "n_hidden_features": n_hidden_features,
        "lags": lags,
        "h": h,
        "select": select,
        "to_csv": to_csv
    }
    result = ctx.obj["cli"]._make_request("forecasting", Path(file), params)
    click.echo(result)


@cli.group()
def ml():
    """Machine Learning commands"""
    pass


@ml.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--base_model", default="RandomForestRegressor", help="Base model to use")
@click.option("--n-hidden-features", default=5, help="Number of hidden features")
@click.option("--select", help="Comma-separated list of keys to select from output")
@click.option("--to-csv", help="Output results to CSV file")
@click.pass_context
def classification(ctx, file, base_model, n_hidden_features, select, to_csv):
    """Classification tasks

    Parameters:
        file: str
            Path to the CSV file
        base_model: str
            Base model to use
        n_hidden_features: int
            Number of hidden features
        select: str
            Comma-separated list of keys to select from output
        to_csv: str
            Output results to CSV file

    Returns:
        dict: Result of the classification

    Example:

        ```python

        techtonique ml classification /Users/t/Documents/datasets/tabular/classification/iris_dataset2.csv --base_model RandomForestRegressor

        ```
    """
    init_cli(ctx)
    params = {"base_model": base_model, "n_hidden_features": n_hidden_features, "select": select, "to_csv": to_csv}
    result = ctx.obj["cli"]._make_request("mlclassification", Path(file), params)
    click.echo(result)


@ml.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--base_model", default="ElasticNet", help="Base model to use")
@click.option("--n-hidden-features", default=5, help="Number of hidden features")
@click.option("--select", help="Comma-separated list of keys to select from output")
@click.option("--to-csv", help="Output results to CSV file")
@click.pass_context
def regression(ctx, file, base_model, n_hidden_features, select, to_csv):
    """Regression tasks

    Parameters:
        file: str
            Path to the CSV file
        base_model: str
            Base model to use
        n_hidden_features: int
            Number of hidden features
        select: str
            Comma-separated list of keys to select from output
        to_csv: str
            Output results to CSV file

    Returns:
        dict: Result of the regression

    Example:

        ```python

        techtonique ml regression /Users/t/Documents/datasets/tabular/regression/mtcars2.csv --base_model ElasticNet

        ```
    """
    init_cli(ctx)
    params = {"base_model": base_model, "n_hidden_features": n_hidden_features, "select": select, "to_csv": to_csv}
    result = ctx.obj["cli"]._make_request("mlregression", Path(file), params)
    click.echo(result)


@cli.group()
def reserving():
    """Reserving commands"""
    pass


@reserving.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--select", help="Comma-separated list of keys to select from output")
@click.option("--to-csv", help="Output results to CSV file")
@click.pass_context
def chainladder(ctx, file, select, to_csv):
    """Chain Ladder method

    Parameters:
        file: str
            Path to the CSV file
        select: str
            Comma-separated list of keys to select from output
        to_csv: str
            Output results to CSV file

    Returns:
        dict: Result of the chain ladder

    Example:

        ```python

        techtonique reserving chainladder /Users/t/Documents/datasets/tabular/triangle/abc.csv

        ```
    """
    init_cli(ctx)
    params = {"method": "chainladder", "select": select, "to_csv": to_csv}
    result = ctx.obj["cli"]._make_request("reserving", Path(file), params)
    click.echo(result)


@reserving.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--select", help="Comma-separated list of keys to select from output")
@click.option("--to-csv", help="Output results to CSV file")
@click.pass_context
def mack(ctx, file, select, to_csv):
    """Mack Chain Ladder method

    Parameters:
        file: str
            Path to the CSV file
        select: str
            Comma-separated list of keys to select from output
        to_csv: str
            Output results to CSV file

    Returns:
        dict: Result of the mack chain ladder

    Example:

        ```python

        techtonique reserving mack /Users/t/Documents/datasets/tabular/triangle/abc.csv

        ```
    """
    init_cli(ctx)
    params = {"method": "mack", "select": select, "to_csv": to_csv}
    result = ctx.obj["cli"]._make_request("reserving", Path(file), params)
    click.echo(result)


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--model", default="coxph", help="Survival model to use")
@click.option("--select", help="Comma-separated list of keys to select from output")
@click.option("--to-csv", help="Output results to CSV file")
@click.pass_context
def survival(ctx, file, model, select, to_csv):
    """Survival Analysis

    Parameters:
        file: str
            Path to the CSV file
        model: str
            Survival model to use
        select: str
            Comma-separated list of keys to select from output
        to_csv: str
            Output results to CSV file

    Returns:
        dict: Result of the survival analysis

    Example:

        ```python

            techtonique survival /Users/t/Documents/datasets/tabular/survival/kidney.csv --model coxph

        ```
    """
    init_cli(ctx)
    params = {"model": model, "select": select, "to_csv": to_csv}
    result = ctx.obj["cli"]._make_request("survivalregression", Path(file), params)
    click.echo(result)


if __name__ == "__main__":
    cli()
