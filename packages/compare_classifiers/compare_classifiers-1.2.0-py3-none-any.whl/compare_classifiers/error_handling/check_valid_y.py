import pandas as pd, numpy as np

def check_valid_y(y, order):
    """Ensure y is a non-empty Pandas series or Numpy array, and raise errors according to conditions of failed check
    
    Parameters
    ----------
    y (Any): The input value to process

    order (Str): The order in which `estimators` was passed as input parameters in the calling function

    Raises:
    TypeError: If y is of an unsupported type
    ValueError: If y is an empty Pandas series or Numpy array

    Returns:
    None

    Examples
    --------
    >>> check_valid_y(np.empty(0), 'second')
    """
    # Check if y_train is Pandas series
    if not (isinstance(y, pd.Series) or isinstance(y, np.ndarray)):
        print('type error being raised')
        raise TypeError(f'{order} parameter has to be a Pandas series or Numpy array containing target class values for training data')
    # Check if y_train contains data
    empty_series = isinstance(y, pd.Series) and y.empty
    empty_ndarr = isinstance(y, np.ndarray) and y.size == 0
    if (empty_series or empty_ndarr):
        print('value error being raised')
        raise ValueError(f'{order} parameter seems to be an empty Pandas series. Please ensure your series contains data.') 