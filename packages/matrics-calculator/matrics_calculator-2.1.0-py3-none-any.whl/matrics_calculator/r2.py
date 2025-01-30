# r-squared value calculation
def r2(predictor, response): 
    """
    Calculates r-squared using linear regression.

    Computes the r-squared value (coefficient of determination) using the provided predictor 
    list and response list.
    
    Parameters
    ----------
    predictor : list
        Predictor values to be used in calculating r-sqaured value.
    response : list
        Response values to be used in calculating r-sqaured value.

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
    
    if not isinstance(predictor, list) or not isinstance(predictor, list):
        print('Input must be lists')
        return None

    if len(predictor) == 0 or len(response) == 0:
        print('Input cannot be empty')
        return None
       
    if isinstance(predictor,list):
        predictor = np.array(predictor)
    if isinstance(response,list):
        response = np.array(response)
        
    model = LinearRegression()
    model.fit(predictor.reshape(-1,1),response)
    response_predicted =  model.predict(predictor.reshape(-1,1))
    response_mean = np.mean(response)
    RSS = sum(((response-response_predicted) ** 2))
    TSS = sum(((response-response_mean) ** 2))
    return round(1 - (RSS/TSS),3)