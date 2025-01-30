# Mean Absolute Percentage Error (MAPE) calculation
import numpy as np

def mean_absolute_percentage_error(y_true, y_pred):
    """
    Calculate the Mean Absolute Percentage Error (MAPE) metric for regression.

    This function computes the average percentage difference between the predicted values (`y_pred`)
    and the actual values (`y_true`). It measures the relative magnitude of errors in prediction, 
    expressed as a percentage. MAPE is widely used to evaluate regression models, especially when 
    relative error matters more than absolute error.

    Parameters:
    ----------
    y_true : array-like
        True values of the target variable.
    y_pred : array-like
        Predicted values from the model.

    Returns:
    -------
    float
        The Mean Absolute Percentage Error (as a percentage).

    Notes:
    ------
    MAPE is defined as:
        MAPE = (1 / n) * sum(|(y_true - y_pred) / y_true|) * 100
    where n is the number of observations.

    Examples:
    ---------
    >>> y_true = [100, 200, 300]
    >>> y_pred = [110, 190, 290]
    >>> mean_absolute_percentage_error(y_true, y_pred)
    3.3333
    """
    #convert inputs into numpy arrays
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    # Validate input lengths
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")

    # Check for zeros in y_true to prevent division by zero
    if np.any(y_true == 0):
        raise ValueError("y_true contains zero values, which would result in division by zero.")

    # Calculate MAPE
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    return mape
