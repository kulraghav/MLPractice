
"""
    A flask-API for spam filter

    Usage:

        $python application.py
         
        The application will run on localhost:5050/ and serves
            - Predict API at localhost:5050/predict/
            - Retrain API at localhost:5050/retrain/

        Predict API:
            - accepts POST request at /predict/ e.g. requests.post(url, json=payload)
            - expects a payload: {'text': "This is a sample message. Please predict if I am spam or ham."}
            - returns a response: {'prediction': 'ham', 'spam_score': 0.123}

        Retrain API:
            - accepts GET request at /retrain
            - retrains the model and saves it in a file
                - filename is appended with current date, e.g.,  model_joblib_2018_December_24
            - returns a response: {'status': 1, 'filename': 'model_joblib_2018_December_24', 'score': 0.9345}            
"""

from flask import Flask, request, jsonify
from sklearn.externals import joblib
import pandas as pd

app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to the spam-filter web service!"

"""
    This function will be used when we combine different features
    A sample input: X = pd.DataFrame({'sms': [text], 'len': [len(text)]})
    A sample usage: prediction = model.predict(get_features(X_text))[0]
"""
from scipy import sparse
def get_features(X):
    X_text_features = vectorizer.transform(list(X['sms']))
    X_len_features = sparse.csr_matrix(X['len']).T
    X_features = sparse.hstack([X_text_features, X_len_features])
    return X_

model = joblib.load("../Models/pipeline.joblib")

@app.route("/predict/", methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print(data)
            text = str(data['text'])
        
            prediction = model.predict([text])[0]
            spam_proba = model.predict_proba([text])[0][1] 
            
        except ValueError:
            return jsonify("Please enter a valid input.")

        return jsonify({'prediction': prediction, 'spam_proba': spam_proba})
    
if __name__ == '__main__':
    app.run(debug=True)
