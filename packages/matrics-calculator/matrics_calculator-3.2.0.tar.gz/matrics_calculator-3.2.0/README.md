[![Documentation Status](https://readthedocs.org/projects/matrics-calculator/badge/?version=latest)](https://matrics-calculator.readthedocs.io/en/latest/?badge=latest)
# matrics_calculator

A package providing functions to calculate key regression metrics: R-squared, Mean Absolute Error (MAE), Mean Squared Error (MSE), and Mean Absolute Percentage Error (MAPE).

## Python Ecosystem

matrics_calculator provides a lightweight and easy-to-use alternative for calculating key regression metrics, complementing existing libraries like scikit-learn. While scikit-learn offers a full suite of machine learning tools, matrics_calculator focuses solely on evaluation metrics, making it a useful option for quick analysis, custom workflows, or educational purposes. Its simplicity makes it accessible for users who need essential regression metrics without the overhead of a larger machine learning framework.

## Features

This package consists of four functions:
- `r_squared`:
    - This function calculates the R-squared of the model, which measures how well the model explains the variation in the data. 
- `mean_absolute_error`: 
    - This function finds the average difference between predicted and actual values.
- `mean_squared_error`:
    - This function calculates the average of the squared differences between predictions and actual values. 
- `mean_absolute_percentage_error`:
    - This function shows prediction error as a percentage, making it easy to understand.

##  matrics_calculator in the Python Ecosystem

`matrics_calculator` works alongside Python libraries like `scikit-learn` by providing simple implementations of regression metrics. Unlike `scikit-learn`’s full toolkit for modeling and evaluation, this package focuses only on metrics, making it easy to use for quick analysis or custom workflows.

## Installation

```bash
$ pip install matrics_calculator
```

## Usage

Here’s how to use the functions in this package:
1. Import the Package
```bash
from matrics_calculator.r2 import r2_score
from matrics_calculator.MAE import mean_absolute_error
from matrics_calculator.MSE import mean_squared_error
from matrics_calculator.MAPE import mean_absolute_percentage_error
```

2. Prepare Your Data Ensure you have two arrays:

    `y_true`: The actual target values

    `y_pred`: The predicted values from your regression model

    Example:
```bash
y_true = [100, 200, 300]
y_pred = [110, 190, 290]
```
3. Calculate Metrics Use the functions to evaluate your model:
```bash
# Calculate MAPE
mape = mean_absolute_percentage_error(y_true, y_pred)
print(f"MAPE: {mape:.2f}%")

# Calculate MAE
mae = mean_absolute_error(y_true, y_pred)
print(f"MAE: {mae:.2f}")

# Calculate MSE
mse = mean_squared_error(y_true, y_pred)
print(f"MSE: {mse:.2f}")

# Calculate R-squared
r2 = r2_score(y_true, y_pred)
print(f"R-squared: {r2:.2f}")
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`matrics_calculator` was created by Celine Habashy, Jay Mangat, Yajing Liu, Zhiwei Zhang. It is licensed under the terms of the MIT license.

## Credits

`matrics_calculator` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

## Constributors

- Celine Habashy
- Jay Mangat
- Yajing Liu
- Zhiwei Zhang
