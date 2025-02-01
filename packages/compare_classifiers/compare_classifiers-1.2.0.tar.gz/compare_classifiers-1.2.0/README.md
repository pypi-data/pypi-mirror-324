# compare_classifiers 
[![Documentation Status](https://readthedocs.org/projects/compare-classifiers-524/badge/?version=latest)](https://compare-classifiers-524.readthedocs.io/en/latest/?badge=latest)
[![Repo Status](https://img.shields.io/badge/repo%20status-Active-brightgreen)](https://github.com/UBC-MDS/compare_classifiers)  
[![Python Versions](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/downloads/)  
[![CI/CD](https://github.com/UBC-MDS/compare_classifiers/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/compare_classifiers/actions)  
[![codecov](https://codecov.io/gh/UBC-MDS/compare_classifiers/graph/badge.svg?token=Divjf41jU3)](https://codecov.io/gh/UBC-MDS/compare_classifiers)

Compare metrics such as f1 score and confusion matrices for your machine learning models and through voting or stacking them, then predict on test data with your choice of voting or stacking!

This package is helpful when you are deciding whether to use a single Classifier or combine multiple well-performing Classifiers through an ensemble using Voting or Stacking to yield a more stable and trustworthy classification result. Each of the four functions serves a unique purpose:

`confusion_matrices`: provides confusion matrices side-by-side for all Classifiers to compare their performances.

`compare_f1`: provides a Pandas data frame, each row listing model fit time, and training and test scores for each Classifier.

`ensemble_compare_f1`: provides a Pandas data frame containing model fit time, training and test scores for both Voting and Stacking ensembles, with each ensemble in its own row.

`ensemble_predict`: provides classification predictions via Voting or Stacking multiple Classifiers.

Before using `ensemble_predict` on test or unseen data, we recommend that you run each of the three other functions on training data to examine how Classifiers perform individually on their own, and the ensemble performances of Voting against Stacking to make a well-informed decision. Sometimes, an individual Classifier could generate a better controlled machine learning environment if its performance rivals that of an ensemble.

## Contributors

Ke Gao (kegao1995@gmail.com),
Bryan Lee (bryan.lee.9000@gmail.com),
Susannah Sun (x.sun@alumni.ubc.ca),
Wangkai Zhu (wzhu8410@gmail.com)

## Installation

```bash
$ pip install compare_classifiers
```

## Example Dataset

We have attached a downloaded version of the [UCI Wine Quality dataset](https://archive.ics.uci.edu/dataset/186/wine+quality), named 'example_dataset.csv'. The dataset contains physicochemical features as numerical values of wines and a `color` column containing text 'red' or 'white' for wine color, and a target variable, column `quality`, representing wine quality scores, with integer values from 3 to 9 (9 = highest quality; 3 = lowest quality).

## Usage

`compare_classifiers` can be used to show confusion matrices and f1 scores for individual estimators, as well as f1 score for voting or stacking the estimators. We made a [tutorial with detailed documentation](https://compare-classifiers-524.readthedocs.io/en/latest/example.html) and here is a brief overview of how to use the package:

### Step 1: Read in Data and Initial Processing

> _**Note:**_ We changed an original dataset column, `color` containing text indicating a wine being 'red' or 'white' into a binary column now named `is_red` with 1 indicating red wine, and 0 indicating white wine. This ensures all columns are numeric and facilitates the upcoming training process for our models.

```python
import pandas as pd
  
example_dataset = pd.read_csv('../example_dataset.csv')

# convert the `color` column to a binary variable: `is_red`: red = 1, white = 0, and drop the original `color` column
example_dataset['is_red'] = example_dataset['color'].apply(lambda x: 1 if x == 'red' else 0)
example_dataset = example_dataset.drop(['color'], axis=1)

# move the `color` column to the beginning
last_col = example_dataset.pop(example_dataset.columns[-1])
example_dataset.insert(0, last_col.name, last_col)
```

### Step 2: Train + Test Data Split

```python
from sklearn.model_selection import train_test_split

train_df, test_df = train_test_split(example_dataset, test_size=0.2)
X_train, X_test, y_train, y_test = (
    train_df.drop(columns='quality'), test_df.drop(columns='quality'),
    train_df['quality'], test_df['quality']
)
```

### Step 3: Compare Models and Ensembles

```python
from compare_classifiers.confusion_matrices import confusion_matrices
from compare_classifiers.compare_f1 import compare_f1
from compare_classifiers.ensemble_compare_f1 import ensemble_compare_f1

from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

logreg = LogisticRegression(multi_class='multinomial', solver='lbfgs', C=92)
gb = GradientBoostingClassifier(learning_rate=0.001, n_estimators=1000)
svm = SVC(kernel='rbf', decision_function_shape='ovr', max_iter=2000)
rf = RandomForestClassifier(n_estimators=10)
knn5 = KNeighborsClassifier(n_neighbors=5)

estimators = [
    ('logreg', logreg),
    ('gb', gb),
    ('svm', svm),
    ('rf', rf),
    ('knn5', knn5)
]

# show confusion matrices for estimators:
confusion_matrices(estimators, X_train, X_test, y_train, y_test)

# show cross validation fit time and f1 scores of each estimator:
compare_f1(estimators, X_train, y_train) 

# show cross validation fit time and f1 scores by voting and stacking the estimators:
ensemble_compare_f1(estimators, X_train, y_train) 
```

### (Optional) Step 4: Predict Using Ensemble

```python
from compare_classifiers.ensemble_predict import ensemble_predict

# predict class labels for unseen data through voting results of estimators:
ensemble_predict(estimators, X_train, y_train, 'voting', X_test) 
```

## Similar Packages

We are not aware of similar packages existing. Though there are available functions to present metrics for a single model and a single ensemble, we have not found functions that compare and display metrics and results for multiple models or ensembles all at once. Neither is there a function that predicts based on dynamic input of ensemble method.

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`compare_classifiers` was created by Ke Gao, Bryan Lee, Susannah Sun, and Wangkai Zhu. It is licensed under the terms of the MIT license.

## Credits

`compare_classifiers` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
