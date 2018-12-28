
"""
    This module contains the functions that help in
       1. loading the raw data
       2. cleaning the raw data
       3. transforming it to a form usable by ML pipeline        
"""

import pandas as pd

data_path = '../Data/spam.csv'

import chardet
def get_encoding(data_path):
    with open(data_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

def load_data(data_path):
    encoding = get_encoding(data_path)
    df_raw = pd.read_csv(data_path, encoding=encoding)
    df = df_raw[['v1', 'v2']].rename(columns={'v1': 'label', 'v2': 'sms'})
    df.drop_duplicates(subset='sms', inplace=True)
    
    X = df['sms']
    y = df['label']
    print("X.shape is {} and y.shape is {}".format(X.shape, y.shape))

    return X, y

  
    
