import pandas as pd
import warnings  

def future_value(principal, annual_rate, n_periods, contribution=0):
    """
    Calculates the future value of an investment with optional monthly contributions.

    Parameters
    ----------
    principal : float
        The initial investment (positive value) or loan (negative value).
    annual_rate : float
        Annual interest rate (as a percentage, e.g., 5 for 5%).
    n_periods : int
        Total number of periods (in months).
    contribution : float, optional
        Payment made per period (monthly contributions). Defaults to 0 if not provided.
        A negative contribution indicates withdrawals.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the following columns:
            - 'Future Value': The future value of the investment, including contributions.
            - 'Principal': The initial investment.
            - 'Contributions': Total amount contributed over the investment period.
            - 'Interest Earned': The total interest earned from the investment.

    Raises
    ------
    TypeError
        If any of `principal`, `annual_rate`, `n_periods`, or `contribution` is not a float or int.
    ValueError
        If `n_periods` is not positive.
        If `annual_rate` is negative.

    Warnings
    --------
    UserWarning
        If `annual_rate` is 0, the future value will be equal to the principal plus contributions.
        If `annual_rate` is unusually low (<1), indicating the user may have entered a percentage instead of a decimal.
        If `n_periods` is unusually low (<6), suggesting the user may have entered years instead of months.

    Examples
    --------
    >>> future_value(principal=1000, annual_rate=5, n_periods=120, contribution=100)
    """

    # Check input types are correct
        # Type checks
    if not isinstance(principal, (int, float)):
        raise TypeError("Principal must be a number (int or float).")
    if not isinstance(annual_rate, (int, float)):
        raise TypeError("Annual rate must be a number (int or float).")
    if not isinstance(n_periods, int):
        raise TypeError("Number of periods must be an integer.")
    if not isinstance(contribution, (int, float)):
        raise TypeError("Contribution must be a number (int or float).")
    
    # Check n_periods is positive, otherwise throw an error
    if n_periods <= 0:
        raise ValueError("Number of periods must be greater than zero.")
    
    # If annual rate provided is 0, issue a warning that future value will be equal to principal plus contributions
    if annual_rate == 0:
        warnings.warn("You entered an annual interest rate of 0. The future value will be equal to the principal plus contributions.", UserWarning)

    # If annual rate is between 0 and 1, issue a warning if the annual rate seems to catch if user accidentally entered percentage as a decimal
    if 0 < annual_rate <1:
        warnings.warn("Warning: The annual interest rate entered seems quite low. "
                       "Did you mean to enter it as a percentage (e.g., 5 for 5%)?", UserWarning)

    # If interest rate is negative, issue a warning. Negative interest rates are possible but very rare    
    if annual_rate < 0:
        warnings.warn("Warning: You entered a negative interest rate. This may lead to a decrease in your investment's value.", UserWarning)
        
     # Check if the user entered an unusually low value for n_periods (anything less than 6 months), and remind them it's in years
    if n_periods <= 5:
        warnings.warn("Warning: The number of periods entered seems quite low. "
                      "Note that n_periods should be entered in months (e.g., 12 months instead of 1 year)", UserWarning)

    # Calculate monthly interest rate from annual_rate and convert to decimal
    int_rate = annual_rate/12/100

    # Calculate value of contributions
    if int_rate == 0:  # If interest rate is zero, just multiply contribution by number of periods
        contribution_value = contribution * n_periods
    else:
        contribution_value = contribution * (((1 + int_rate) ** n_periods - 1) / int_rate)

    # Calculate future value
    future_value = (principal * (1 + int_rate) ** n_periods + contribution_value)

    # Calculate total contributions
    total_contributions = contribution * n_periods

    # Calculate total interest earned
    interest_earned = (future_value - (principal + total_contributions))

    # Round all the results to two decimal places only at the very end
    future_value = round(future_value, 2)
    total_contributions = round(total_contributions, 2)
    interest_earned = round(interest_earned, 2)

    #Create return dataframe
    data = {
        'Future Value': [future_value],
        'Principal': [principal],
        'Contributions': [total_contributions],
        'Interest Earned': [interest_earned]
    }

    # Return dataframe as function output
    return pd.DataFrame(data)