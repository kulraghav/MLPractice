
"""
    A flask-API for spam filter

    Usage:
        $python application.py
         
        The application will run on localhost:5050/ and serves two API endpoints
            - Predict API: localhost:5050/predict
            - Retrain API: localhost:5050/retrain

        Predict API:
            >>> import requests
            >>> payload: {'text': "This is a sample message. Please predict if I am spam or ham."}
            >>> response =  requests.post(url='localhost:5050/predict', json=payload)
            >>> response.json()
            >>> {'prediction': 'ham', 'spam_score': 0.123}

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
def welcome_message():
    return "Welcome to the spam-filter web service!"

import os
def get_latest_model_path(model_dir):
    filenames = []
    for root, dirs, files in os.walk(model_dir):  
        for filename in files:
            filenames.append(filename)
            
    filenames.sort(key=lambda x: x.split('joblib')[-1], reverse=True)

    if not filenames:
        raise Exception("Model not found")
    
    return model_dir+filenames[0]
    

def load_model(path_to_model_dir="../Models/Spam/", path_to_model=""):
    if not path_to_model:
        path = get_latest_model_path(path_to_model_dir)
    else:
        path = path_to_model
    model = joblib.load(path)
    return model
    
model = load_model()    

@app.route("/predict", methods=['POST'], strict_slashes=False)
def predict():
    if request.method == 'POST':
        try:
            data = request.get_json()
            text = str(data['text'])
        
            prediction = model.predict([text])[0]
            spam_proba = model.predict_proba([text])[0][1] 
            
        except ValueError:
            return jsonify("Please enter a valid input: {'text': 'Your text goes here'}")

        return jsonify({'prediction': prediction, 'spam_proba': spam_proba})
    
if __name__ == '__main__':
    app.run(debug=True)
