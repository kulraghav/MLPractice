
"""
    This module trains the model and saves it with date-appended name
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from datetime import date


def train(X, y, save=True):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    print("Shape of X is {}".format(X.shape))
    print("Shape of X_train is {} and shape of y_train is {}".format(X_train.shape, y_train.shape))
    print("Shape of X_test is {} and shape of y_test is {}".format(X_test.shape, y_test.shape))

    pipeline = Pipeline([('vectorizer', TfidfVectorizer()),
                         ('classifier', LogisticRegression())])


    cv_scores = cross_val_score(pipeline, X=X_train, y=y_train, cv=5)
    print("The cross validation scores are: {}".format(cv_scores))

    """
        If cross-validation scores are satisfactory then train the model on entire data and save the model.
    """
    pipeline.fit(X, y)

    model_path = "model_path_not_specified"
    if save == True:
        version = date.today().strftime("%Y_%B_%d")
        model_path = '../Models/Spam/model.joblib_{}'.format(version)
        joblib.dump(pipeline, model_path)

    result = {'model_path': model_path, "average_cv_score": cv_scores.mean()}

    return result
