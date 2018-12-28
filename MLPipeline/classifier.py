
"""
    This module contains the functions related to ML classifier
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

from dataloader import load_data

def train(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    print("Shape of X is {} and shape of y is {}".format(X.shape, y.shape))
    print("Shape of X_train is {} and shape of y_train is {}".format(X_train.shape, y_train.shape))
    print("Shape of X_test is {} and shape of y_test is {}".format(X_test.shape, y_test.shape))

    model = Pipeline([('vectorizer', TfidfVectorizer()),
                         ('classifier', LogisticRegression())])
    print("The cross validation scores are: {}".format(cross_val_score(model, X=X_train, y=y_train, cv=5)))

    """
        When we want to put in production, 
        shall we train it on X, y and then return ?
    """
    model.fit(X_train, y_train)
    return model

