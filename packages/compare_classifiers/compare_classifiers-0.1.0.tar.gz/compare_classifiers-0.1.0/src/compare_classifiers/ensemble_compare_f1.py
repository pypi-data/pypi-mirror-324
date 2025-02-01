from compare_classifiers.error_handling.check_valid_estimators import check_valid_estimators
from compare_classifiers.error_handling.check_valid_X import check_valid_X
from compare_classifiers.error_handling.check_valid_y import check_valid_y

from sklearn.ensemble import VotingClassifier, StackingClassifier
from sklearn.model_selection import cross_validate
import pandas as pd
from sklearn.linear_model import LogisticRegression

def ensemble_compare_f1(estimators, X_train, y_train):
    """Show cross validation results, including fit time and f1 scores by stacking and voting the estimators.

    Parameters
    ----------
    estimators : list of tuples
        A list of (name, estimator) tuples, consisting of individual estimators to be processed through the voting or stacking classifying ensemble. Each tuple contains a string: name/label of estimator, and a model: the estimator, which implements
        the scikit-learn API (`fit`, `predict`, etc.).
    
    X_train : Pandas data frame
        Data frame containing training data along with n features or ndarray with no feature names.
        
    y_train : Pandas series or Numpy array
        Target class labels for data in X_train.

    Returns
    -------
    Pandas data frame
        A data frame showing cross validation results on training data, with 3 columns: fit_time, test_score, train_score and 2 rows: voting, stacking.
    
    Examples
    --------
    >>> estimators = [
    ...     ('rf', RandomForestClassifier(n_estimators=10, random_state=42)),
    ...     ('svm', make_pipeline(StandardScaler(), LinearSVC(random_state=42)))
    ... ]
    >>> ensemble_compare_f1(estimators, X, y)
    """

    # Check if estimators is valid or raise errors
    check_valid_estimators(estimators, 'first')
    
    # Check if X_train is valid or raise errors
    check_valid_X(X_train, 'second')
    
    # Check if y_train is valid or raise errors
    check_valid_y(y_train, 'third')

    results = []

    for method in ['voting', 'stacking']:
        if method == 'voting':
            ensemble = VotingClassifier(estimators=estimators, voting='hard')
        if method == 'stacking':
            ensemble = StackingClassifier(estimators=estimators, final_estimator=LogisticRegression())

        cv_results = cross_validate(ensemble, X_train, y_train, cv=5, scoring='f1_macro', return_train_score=True)
        
        results_df = pd.DataFrame({
            'method': method,
            'fit_time': cv_results['fit_time'].mean(),
            'test_f1_score': cv_results['test_score'].mean(),
            'train_f1_score': cv_results['train_score'].mean()
        }, index=[0])

        results.append(results_df)

    return pd.concat(results, ignore_index=True)
