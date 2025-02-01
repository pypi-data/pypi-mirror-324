import math
import warnings

def n_periods(principal, annual_rate, future_value, contribution=0):
    """
    Calculates the number of periods (in months) needed to reach a specified future value,
    given an initial principal, an annual interest rate, and optional monthly contributions.

    Parameters
    ----------
    principal : float
        The initial amount, which can be a positive value for an investment or a negative value for a loan.
    annual_rate : float
        Annual interest rate (as a percentage, e.g., 5 for 5%).
    future_value : float
        The target future value of the investment or loan balance.
    contribution : float, optional
        Payment made per period (monthly contributions). Defaults to 0 if not provided.

    Returns
    -------
    n_periods : int
        The number of periods (in months) required to reach the future value.

    Raises
    ------
    TypeError
        If any of `principal`, `annual_rate`, `future_value`, or `contribution` is not a float or int.
    ValueError
        If both `principal` and `contribution` are 0.
        If `annual_rate` is negative.

    Warnings
    --------
    UserWarning
        If `annual_rate` is unusually low (<1), indicating the user may have entered a percentage instead of a decimal.
        If `annual_rate` is 0, the future value cannot be reached without a contribution.
        If `n_periods` is unusually low (<5), suggesting the user may have entered years instead of months.

    Examples
    --------
    >>> n_periods(principal=1000, annual_rate=5, future_value=2000, contribution=50)
    """
    # check types of the inputs
    if not isinstance(principal, (int, float)):  
        raise TypeError("Parameter 'principal' must be a number (int or float).")  
    if not isinstance(annual_rate, (int, float)):  
        raise TypeError("Parameter 'annual_rate' must be a number (int or float).")  
    if not isinstance(future_value, (int, float)):  
        raise TypeError("Parameter 'future_value' must be a number (int or float).")  
    if not isinstance(contribution, (int, float)): 
        raise TypeError("Parameter 'contribution' must be a number (int or float).")  
        
    if principal == future_value:
        return 0
        
    # convert annual rate to monthly rate
    monthly_rate = annual_rate / 100 / 12
    # warning: user might input a decimal instead of a percentage
    if 0 < annual_rate < 1:
        warnings.warn("The annual_rate is unusually low. Did you mean to enter a percentage instead of a decimal?", UserWarning)
    # warning: annual rate <= 0
    if annual_rate <= 0:
        warnings.warn("The annual_rate is zero or negative. This is unusual behavior.", UserWarning)


    # error raised when both principal and contribution are 0
    if principal == 0 and contribution == 0:
        raise ValueError("Either principal or contribution must be non-zero to reach a future value.")

    # if monthly rate is 0, just simple calculation 
    if monthly_rate == 0:
        if contribution == 0:
            raise ValueError("With a zero interest rate and no contribution, the future value cannot be reached.")
        n_periods = (future_value - principal) / contribution
    else:
    # compounding calculation
        n_periods = math.log((future_value * monthly_rate + contribution) / (principal * monthly_rate + contribution)) / math.log(1 + monthly_rate)

    # return a positive integar
    n_periods =  max(1, round(n_periods))

    # warning: if n_periods less than 5
    if 1 <= n_periods <= 5:
        warnings.warn("The number of periods is unusually low. Did you accidentally input years instead of months?", UserWarning)

    return n_periods

