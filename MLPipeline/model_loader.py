import os
from sklearn.externals import joblib

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
