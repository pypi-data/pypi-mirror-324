import sklearn
from sklearn.base import is_classifier

def check_valid_estimators(estimators, order):
    """Ensure estimators is a list of (name, estimator) tuples, consisting of individual models or pipelines to be processed through the voting or stacking classifying ensemble. Each tuple contains a string: name/label of estimator, and a model: the estimator, which implements
        the scikit-learn API (`fit`, `predict`, etc.), and raise errors according to conditions of failed check
    
    Parameters
    ----------
    estimators (Any): The input value to process

    order (Str): The order in which `estimators` was passed as input parameters in the calling function

    Raises:
    TypeError: If estimators is of an unsupported type
    ValueError: If estimators is a list that contains 0 or 1 element

    Returns:
    None

    Examples
    --------
    >>> check_valid_X([], 'first')
    """

    ESTIMATOR_ERROR = 'f{order} parameter has to be a list of (name, estimator) tuples where name is a string and estimator is a sklearn Classifier or pipeline'

    # Check if estimators is a list
    if not isinstance(estimators, list):
        raise TypeError(ESTIMATOR_ERROR)
    # Check if estimators is a list
    if len(estimators) == 0:
        raise ValueError(ESTIMATOR_ERROR)
    # Iterate through each element in the list
    for item in estimators:
        # Check if the item is a tuple with exactly two elements
        if not (isinstance(item, tuple) and len(item) == 2):
            raise TypeError(ESTIMATOR_ERROR)
        # Check if the first element is a string
        if not isinstance(item[0], str):
            raise TypeError(ESTIMATOR_ERROR)
        # Check if the second element is an instance of an sklearn classifier
        is_classifier_pipe = isinstance(item[1], sklearn.pipeline.Pipeline) and is_classifier(item[1].steps[-1][1])
        if not (is_classifier(item[1]) or is_classifier_pipe):
            raise TypeError(ESTIMATOR_ERROR)
    # Check there are more than one estimators
    if len(estimators) == 1:
        raise ValueError(f'{order} parameter must be a list of at least 2 tuples')