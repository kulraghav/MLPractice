
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
            >>> import requests
            >>> url = 'localhost:5050/retrain'
            >>> response = requests.get(url)
            >>> response.json()
            >>> {'model_path': 'model_joblib_2018_December_24', 'average_cv_score': 0.9345}            
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def welcome_message():
    return "Welcome to the spam-filter web service!"

from model_loader import load_model
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

from data_loader import load_data    
from trainer import train

@app.route("/retrain", methods=['GET'], strict_slashes=False)    
def retrain():
    if request.method == 'GET':
        try:
            X, y = load_data("../Data/spam.csv")
            print("loaded data")
            
            result = train(X, y, save=True)
            return jsonify(result)
        except:
            raise Exception("Training was unsuccessful!")

if __name__ == '__main__':
    app.run(debug=True)
