from compare_classifiers.error_handling.check_valid_estimators import check_valid_estimators
from compare_classifiers.error_handling.check_valid_X import check_valid_X
from compare_classifiers.error_handling.check_valid_y import check_valid_y

from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

def confusion_matrices(estimators, X_train, X_test, y_train, y_test):
    """
    Display confusion matrices for multiple estimators on a dataset.

    Parameters:
    -----------
    estimators : list of tuples
        A list of (name, estimator) tuples, each containing a string: name/label of estimator, and a model: the estimator, which implements
        the scikit-learn API (`fit`, `predict`, etc.).

    X_train : Pandas data frame or Numpy array
        Data frame containing training data along with n features or ndarray with no feature names.
    
    X_test : Pandas data frame or Numpy array
        Data frame containing test data along with n features or ndarray with no feature names.
        
    y_train : Pandas series or Numpy array
        Target class labels for data in X_train.

    y_test : Pandas series or Numpy array
        Target class labels for data in X_test.
    
    Returns:
    --------    
    axes : numpy.ndarray or list of matplotlib.axes.Axes
        A 2D array (or list) of axes objects where the confusion matrices are plotted. Each element represents an individual subplot (axis) within the grid.

    Example:
    --------
    >>> estimators = [
    ...     ('rf', RandomForestClassifier(n_estimators=10, random_state=42)),
    ...     ('svm', make_pipeline(StandardScaler(), LinearSVC(random_state=42)))
    ... ]
    >>> confusion_matrices(estimators, X_train, X_test, y_train, y_test)
    """
    # Check if estimators is valid or raise errors
    check_valid_estimators(estimators, 'first')
    
    # Check if X_train is valid or raise errors
    check_valid_X(X_train, 'second')

    # Check if X_test is valid or raise errors
    check_valid_X(X_train, 'third')
    
    # Check if y_train is valid or raise errors
    check_valid_y(y_train, 'fourth')

    # Check if y_train is valid or raise errors
    check_valid_y(y_test, 'fifth')

    labels = [e[0] for e in estimators]
    classifiers = [e[1] for e in estimators]

    # Fit each estimator
    for cls in classifiers:
        cls.fit(X_train, y_train)

    # Plot confusion matrices in a single column
    fig, axes = plt.subplots(nrows=len(classifiers), ncols=1, figsize=(5*len(classifiers),5*len(classifiers)))
    for cls, ax in zip(classifiers, axes.flatten()):
        ConfusionMatrixDisplay(
            confusion_matrix=confusion_matrix(y_test, cls.predict(X_test), labels=cls.classes_), 
            display_labels=cls.classes_).plot(ax=ax)
        ax.title.set_text(labels[classifiers.index(cls)])
    plt.tight_layout()  
    plt.show()

    return axes