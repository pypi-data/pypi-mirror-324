# **FinanceCalculator2025**

------------------------------------------------------------------------
[![Documentation Status](https://readthedocs.org/projects/financecalculator/badge/?version=latest)](https://financecalculator.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/UBC-MDS/FinanceCalculator2025/graph/badge.svg?token=n9iRr2joRS)](https://codecov.io/gh/UBC-MDS/FinanceCalculator2025)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![ci-cd](https://github.com/UBC-MDS/financecalculator2025/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/financecalculator2025/actions/workflows/ci-cd.yml)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)]

<img src="https://github.com/UBC-MDS/FinanceCalculator2025/blob/main/img/finance-calculator-200px.png?raw=true">

## Project Summary

**`FinanceCalculator2025`** is a Python package for calculating financial metrics specifically designed for loans or investment scenarios.\
This package serves as a convenient tool for managing personal finances, offering functionalities such as Contributions (`calculate_contribution`), Future Value (`future_value`), Present Value (`present_value`), and Number of Periods (`n_periods`) Calculations.

------------------------------------------------------------------------

## Contributors

-   Chaoyu Ou [Shell-human](https://github.com/Shell-human)
-   Meagan L. Gardner [meagangardner](https://github.com/meagangardner)
-   Ziming Fang [ethanfang08](https://github.com/ethanfang08)
-   Zoe Ren [sgdkd](https://github.com/sgdkd)

------------------------------------------------------------------------

## Installation

``` bash
$ pip install financecalculator2025
```
------------------------------------------------------------------------

## Documentation
Our online documentation can be found [here](https://financecalculator.readthedocs.io/en/latest/?badge=latest)

------------------------------------------------------------------------

## Package Content

This package offers four key functions:

### **Functions:**

1.  **`calculate_contribution`:** Calculates the periodic payment (contribution) required to pay off a loan or reach a specified future value over a given number of periods.
2.  **`future_value`:** Calculates the future value of an investment or loan, factoring in optional periodic contributions.
3.  **`present_value`:** Calculates the present value of an investment or loan, considering optional monthly contributions.
4.  **`n_periods`:** Calculates the number of periods (in months) required to reach a specified future value, given an initial principal, an annual interest rate, and optional monthly contributions.

------------------------------------------------------------------------

### **Common Parameters:**

-   **`principal`** *(float)*:\
    The initial investment or loan amount (also known as Present Value in financial terms).

-   **`future_value`** *(float)*:\
    The desired amount at the end of the calculation period (e.g., remaining loan balance or target savings).

-   **`annual_rate`** *(float)*:\
    Annual interest rate expressed as a percentage (e.g., 5 for 5%).

-   **`n_periods`** *(int)*:\
    Total number of periods (typically in months) over which the calculation will be performed.

-   **`contribution`** *(float, optional)*:\
    The amount paid or contributed per period (e.g., monthly contributions). Defaults to 0 if not provided.

------------------------------------------------------------------------

## Python Ecosystem

The `FinanceCalculator2025` package situates itself within the Python ecosystem as a learning-oriented initiative aimed at developing practical skills in financial computation and programming. While the Python ecosystem already includes robust packages and applications like [Loan Calculator](https://github.com/yanomateus/loan-calculator) and [Financial Calculator App](https://github.com/dilumdesilva/Financial-Calculator-App), this project differentiates itself by offering an accessible, user-friendly tools that simplifies core financial concepts.   
  
With intuitive function names like `calculate_contribution`, `future_value`, `present_value`, and `n_periods`, this package allows users — especially beginners and students — to quickly grasp the essentials without needing to understand complex financial formulas. This package also serves as a hands-on exercise for those eager to deepen their understanding of both finance and Python programming, making it a valuable resource for anyone looking to deepen their understanding of financial concepts and Python development.

------------------------------------------------------------------------

## Developer Note
1. Clone this repository and navigate to the project root directory.

2. Create a new virtual environment in terminal and activate it:
```
conda create --name financecalculator2025 python=3.11.0
conda activate financecalculator2025
```

3. To install the needed packages via poetry, run the following command. If poetry hasn't been set up yet, please following [this link](https://python-poetry.org/docs/) for installtion.
```
poetry install
```
4. To test the package and check coverage, run the following command
```
pytest tests/
pytest tests/ --cov=financecalculator2025
```
5. The set up is done! You can now use the `FinanceCalculator2025` package! Please click on the function documentation at the top of this README on how to use the package.


## Usage

The `FinanceCalculator2025` package allows users to perform essential financial calculations conveniently. Below is a quick start example of how to use this package:

```
import pandas as pd

import financecalculator2025
from financecalculator2025.present_value import present_value
from financecalculator2025.future_value import future_value
from financecalculator2025.contribution import calculate_contribution
from financecalculator2025.n_periods import n_periods
```

**Calculate periodic payments for a loan:**
```
payment = calculate_contribution(principal=20000, future_value=0, annual_rate=5, n_periods=24)
```

**Calculate future value of an investment:**
```
fv = future_value(principal=5000, annual_rate=7, n_periods=36, contribution=200)
```
<img src="https://github.com/UBC-MDS/FinanceCalculator2025/blob/main/img/fv_df_output.png?raw=true">

**Calculate present value for a target amount**
```
pv = present_value(principal=5000, annual_rate=4, n_periods=120, contribution=50)
```
<img src="https://github.com/UBC-MDS/FinanceCalculator2025/blob/main/img/pv_df_output.png?raw=true">

**Calculate the number of months to reach a goal**
```
months = n_periods(principal=10000, annual_rate=6, future_value=50000, contribution=300)
```

------------------------------------------------------------------------

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

------------------------------------------------------------------------

## License

`FinanceCalculator2025` was created by Meagan Gardner, Zoe Ren, Ziming Fang, and Chaoyu Ou. It is licensed under the terms of the MIT license.

------------------------------------------------------------------------

## Credits

`FinanceCalculator2025` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
