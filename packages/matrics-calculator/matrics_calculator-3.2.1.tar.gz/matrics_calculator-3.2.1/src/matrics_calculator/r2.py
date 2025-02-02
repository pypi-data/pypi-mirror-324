# r-squared value calculation
def r2(y_pred, y_true): 
    """
    Calculates r-squared using linear regression.

    Computes the r-squared value (coefficient of determination) using the provided y_pred 
    list and y_true list.
    
    Parameters
    ----------
    y_pred : list
        y_pred values to be used in calculating r-sqaured value.
    y_true : list
        y_true values to be used in calculating r-sqaured value.

    Returns
    -------
    float
        r-sqaured value which is <= 1. 1 is the best score and a score below 0 is worse than 
        using the mean of the target as predictions.

    Examples
    --------
    data = {
    'math_test': [80, 85, 90, 95],
    'science_test': [78, 82, 88, 92],
    'final_grade': [84, 87, 91, 94],
    'absences': [3, 0, 1, 30]
    }
    >>> r2(data['math_test'],data['final_grade'])
    0.997
    >>> r2(data['math_test'],data['absences'])
    0.541
    """
    from sklearn.linear_model import LinearRegression
    import numpy as np
    
    if not isinstance(y_pred, list) or not isinstance(y_pred, list):
        print('Input must be lists')
        return None

    if len(y_pred) == 0 or len(y_true) == 0:
        print('Input cannot be empty')
        return None
       
    if isinstance(y_pred,list):
        y_pred = np.array(y_pred)
    if isinstance(y_true,list):
        y_true = np.array(y_true)
        
    model = LinearRegression()
    model.fit(y_pred.reshape(-1,1),y_true)
    y_true_predicted =  model.predict(y_pred.reshape(-1,1))
    y_true_mean = np.mean(y_true)
    RSS = sum(((y_true-y_true_predicted) ** 2))
    TSS = sum(((y_true-y_true_mean) ** 2))
    return round(1 - (RSS/TSS),3)