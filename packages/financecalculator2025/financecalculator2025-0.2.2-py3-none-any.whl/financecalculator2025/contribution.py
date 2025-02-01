import warnings

def calculate_contribution(principal, future_value, annual_rate, n_periods):
    """
    Calculates the contribution required per period to achieve a specified future value 
    or pay off a loan, considering the possibility of depositing or withdrawing funds.

    Parameters
    ----------
    principal : float
        The initial loan amount or investment (present value). For loans, this should be a 
        negative value (e.g., -1000 for a loan of 1000).
    future_value : float
        The target future value (amount remaining after n_periods). For loans, this is usually 0.
    annual_rate : float
        Annual interest rate (as a percentage, e.g., 5 for 5%).
    n_periods : int
        Total number of periods (e.g., months or years). Must be a positive integer.

    Returns
    -------
    float
        The payment amount per period required to reach the specified future value 
        or pay off the loan. A positive value represents an inflow (e.g., making deposits), 
        while a negative value represents an outflow (e.g., withdrawals or loan repayments).

    Raises
    ------
    ValueError
        If any input is invalid, such as non-numeric types or invalid ranges.

    Warnings
    --------
    UserWarning
        Warnings for potentially unusual inputs.

    Examples
    --------
    >>> calculate_contribution(principal=0, future_value=10000, annual_rate=5, n_periods=120)
    """
    # Input validation
    if not isinstance(principal, (int, float)):
        raise ValueError("Principal must be a number.")
    if not isinstance(future_value, (int, float)):
        raise ValueError("Future value must be a number.")
    if not isinstance(annual_rate, (int, float)) or annual_rate < -100:
        raise ValueError("Annual rate must be a number and greater than or equal to -100%.")
    if not isinstance(n_periods, int) or n_periods <= 0:
        raise ValueError("Number of periods must be a positive integer.")
    
    # Warnings for unusual inputs
    if 0 < annual_rate < 1:
        warnings.warn("Annual interest rate is unusually low. Did you mean to input a percentage (e.g., 5 for 5%)?", UserWarning)
    if n_periods <= 5:
        warnings.warn("Number of periods is unusually low. Did you intend to input months instead of years?", UserWarning)
    if annual_rate <= 0:
        warnings.warn("Annual interest rate is zero or negative, which is uncommon.", UserWarning)

    # Convert annual rate to decimal and adjust for monthly periods
    rate_per_period = (annual_rate / 100) / 12  # Assume monthly periods

    # Handle zero interest rate case
    if rate_per_period == 0:
        contribution = (future_value - principal) / n_periods
    else:
        # Calculate contribution using the financial formula
        contribution = (principal * rate_per_period * (1 + rate_per_period) ** n_periods +
                        future_value * rate_per_period) / ((1 + rate_per_period) ** n_periods - 1)
    
    # Adjust sign based on the relationship between principal and future value
    if principal > future_value:
        return -abs(contribution)  # Withdrawal or repayment (negative contribution)
    else:
        return abs(contribution)  # Deposit or investment (positive contribution)