# CLI for Techtonique

This a **Command Line Interface** (CLI) for [Techtonique](https://www.techtonique.net)'s [API](https://www.techtonique.net/docs). Working on all operating systems (Windows, MacOS, Linux). You may find these resources useful: 
- [https://jeroenjanssens.com/dsatcl/chapter-5-scrubbing-data](https://jeroenjanssens.com/dsatcl/chapter-5-scrubbing-data)
- [https://jeroenjanssens.com/dsatcl/chapter-7-exploring-data](https://jeroenjanssens.com/dsatcl/chapter-7-exploring-data)

## 1 - Installation

In a virtual environment, run the following command:

```bash
pip install techtonique_cli
```

First, get a token from [techtonique.net/token](https://www.techtonique.net/token). If you want to avoid [providing a token](https://www.techtonique.net/token) each time you run the CLI, you can set the `TECHTONIQUE_API_TOKEN` environment variable (for 30 minutes). That is, either: 

- set the `TECHTONIQUE_API_TOKEN` environment variable by replacing the `TOKEN` value below with your token.
```bash
export TECHTONIQUE_API_TOKEN=TOKEN
```
- put the token in a `.env` file in the current directory, as `TECHTONIQUE_API_TOKEN=TOKEN`.


All the datasets used in the examples below are available in [Techtonique/datasets](https://github.com/Techtonique/datasets) repository.


## 2 - Examples

### 2 - 1 - General usage 

At the command line, type:

```bash
techtonique --help

techtonique forecasting --help

techtonique forecasting univariate --help

techtonique ml --help

techtonique ml classification --help

techtonique reserving --help

techtonique survival --help

#  Univariate forecasting
techtonique forecasting univariate /Users/t/Documents/datasets/time_series/univariate/a10.csv --base_model RidgeCV --h 3

# Multivariate forecasting
techtonique forecasting multivariate /Users/t/Documents/datasets/time_series/multivariate/ice_cream_vs_heater.csv --lags 25 --h 10

# Regression
techtonique ml regression /Users/t/Documents/datasets/tabular/regression/mtcars2.csv --base_model ElasticNet

# Survival Analysis
techtonique survival /Users/t/Documents/datasets/tabular/survival/kidney.csv --model coxph
```

### 2 - 2 - Interacting with output files

Then, either: 
- provide the token as a command line argument.
- set the `TECHTONIQUE_API_TOKEN` environment variable by replacing the `TOKEN` value below with your token.
```bash
export TECHTONIQUE_API_TOKEN=TOKEN
```
- put the token in a `.env` file in the current directory.

Here's how to **export results to a JSON file**:

```bash
techtonique forecasting univariate /Users/t/Documents/datasets/time_series/univariate/a10.csv --base_model RidgeCV --h 10 > forecast.json
```

Here's how to **export results to a CSV file with selected columns**:

```bash
techtonique forecasting univariate /Users/t/Documents/datasets/time_series/univariate/a10.csv --base_model RidgeCV --h 10 --select "lower, upper, mean" --to-csv forecast.csv
```

### 2 - 3 - Plotting

```bash
# Display plot interactively
techtonique forecasting univariate /Users/t/Documents/datasets/time_series/univariate/a10.csv --h 10 --plot

# Create forecast and save plot
techtonique forecasting univariate /Users/t/Documents/datasets/time_series/univariate/a10.csv --h 10 --plot-file forecast.png
```