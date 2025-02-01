from compare_classifiers.error_handling.check_valid_estimators import check_valid_estimators
from compare_classifiers.error_handling.check_valid_X import check_valid_X
from compare_classifiers.error_handling.check_valid_y import check_valid_y

from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import StackingClassifier

METHOD_ERROR = 'fourth parameter has to be a string of two possible values: "voting" and "stacking"'

def ensemble_predict(estimators, X_train, y_train, ensemble_method, test_data):
    """predict class for test data with provided estimators and whether predicting through Voting or Stacking

    Parameters
    ----------
    estimators : list of tuples
        A list of (name, estimator) tuples, consisting of individual estimators to be processed through the voting or stacking classifying ensemble. Each tuple contains a string: name/label of estimator, and a model: the estimator, which implements
        the scikit-learn API (`fit`, `predict`, etc.).
    X_train : Pandas data frame or Numpy array
        Data frame containing training data along with n features or ndarray with no feature names.
        
    y_train : Pandas series or Numpy array
        Target class labels for data in X_train.

    ensemble_method : str
        Whether prediction is made through voting or stacking. Possible values are: 'voting' or 'stacking'.
        
    test_data : Pandas data frame
        Data to make predictions on.

    Returns
    -------
    Numpy array
        Predicted class labels for test_data.

    Examples
    --------
    >>> estimators = [
    ...     ('rf', RandomForestClassifier(n_estimators=10, random_state=42)),
    ...     ('svm', make_pipeline(StandardScaler(), LinearSVC(random_state=42)))
    ... ]
    >>> ensemble_predict(estimators, X, y, unseen_data, 'voting')
    """

    # Check if estimators is valid or raise errors
    check_valid_estimators(estimators, 'first')
    
    # Check if X_train is valid or raise errors
    check_valid_X(X_train, 'second')
    
    # Check if y_train is valid or raise errors
    check_valid_y(y_train, 'third')
    
    # Check if ensemble_method is string
    if not isinstance(ensemble_method, str):
        raise TypeError(METHOD_ERROR)
    # Check if ensemble_method is either 'voting' or 'stacking'
    if (not ensemble_method == 'voting' and not ensemble_method == 'stacking'):
        raise ValueError(METHOD_ERROR)
    
    # Check if test_data is a Pandas data frame or raise errors
    check_valid_X(test_data, 'fifth')

    # Return predictions if voting    
    if ensemble_method == 'voting':
        ev = VotingClassifier(estimators)
        ev = ev.fit(X_train, y_train)
        return ev.predict(test_data)
    
    # Return predictions if stacking
    if ensemble_method == 'stacking':
        sc = StackingClassifier(estimators)
        sc = sc.fit(X_train, y_train)
        return sc.predict(test_data)
