import pandas as pd, numpy as np

def check_valid_X(X, order):
    """Ensure X is a non-empty Pandas data frame or Numpy array, and raise errors according to conditions of failed check
    
    Parameters
    ----------
    X (Any): The input value to process

    order (Str): The order in which `estimators` was passed as input parameters in the calling function

    Raises:
    TypeError: If X is of an unsupported type
    ValueError: If X is an empty Pandas data frame or Numpy array

    Returns:
    None

    Examples
    --------
    >>> check_valid_X([], 'first')
    """
    # Check if X_train is Pandas data frame or Numpy array
    if not (isinstance(X, pd.DataFrame) or isinstance(X, np.ndarray)):
        raise TypeError(f'{order} parameter has to be a Pandas data frame or Numpy array containing training data')   
    # Check if X_train contains data
    empty_df = isinstance(X, pd.DataFrame) and X.empty
    empty_ndarr = isinstance(X, np.ndarray) and X.size == 0
    if (empty_df or empty_ndarr):
        raise ValueError(f'{order} parameter seems to be an empty Pandas data frame or Numpy array. Please ensure data is present.') 