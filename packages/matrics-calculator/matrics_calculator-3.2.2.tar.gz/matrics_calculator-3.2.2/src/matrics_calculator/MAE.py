# Mean Absolute Error (MAE) calculation
def mean_absolute_error(y_true, y_pred):
    """
    Calculate the Mean Absolute Error (MAE) metric for regression.

    This function computes the average absolute difference between the predicted values (`y_pred`) 
    and the actual values (`y_true`). It measures the magnitude of errors in prediction, providing 
    a straightforward evaluation of a model's accuracy.

    Parameters:
    ----------
    y_true : array-like
        True values of the target variable.
    y_pred : array-like
        Predicted values from the model.

    Returns:
    -------
    float
        The Mean Absolute Error.

    Notes:
    ------
    MAE is defined as:
        MAE = (1 / n) * sum(|y_true - y_pred|)
    where n is the number of observations.

    Examples:
    ---------
    >>> y_true = [100, 200, 300]
    >>> y_pred = [110, 190, 290]
    >>> mean_absolute_error(y_true, y_pred)
    10.0
    """
    if len(y_true) != len(y_pred):
        raise ValueError("The lengths of y_true and y_pred must be the same.")
    
    mae = sum(abs(true - pred) for true, pred in zip(y_true, y_pred)) / len(y_true)
    return mae
