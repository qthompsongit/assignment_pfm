import datetime
import os
import sys
import joblib
from sentence_transformers import SentenceTransformer
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

error_messages = ["Error: Running this program requires providing two arguments, \
            a headline text file name and a headline source.\n\
Two arguments are missing. Please write your command in the following format:\n\n\
py -3.10 score_headlines.py [INSERT TEXT DOCUMENT NAME].txt [INSERT HEADLINE SOURCE]",
"Error: Running this program requires providing two arguments,\
            a headline text file name and a headline source.\n\
One of these arguments are missing. Please write your command in the following format:\n\n\
py -3.10 score_headlines.py [INSERT TEXT DOCUMENT NAME].txt [INSERT HEADLINE SOURCE]"]

sentence_vector_transformer_model = SentenceTransformer("all-MiniLM-L6-v2")
headline_scoring_model = joblib.load('svm.joblib')

app = FastAPI()

@app.get('/status')
def status():
    d = {'status': 'OK'}
    return d

@app.get('/get_time')
def get_time():
    d = {'current_time':datetime.now().strftime("%H:%M")}
    return d

class HeadlineData(BaseModel):
    headlines: List[str]
    uc_grad: bool

@app.post('/score_headlines')
def score_headlines(client_props: HeadlineData):
    my_headline_predictions = []
    model_vector_embeddings = sentence_vector_transformer_model.encode(client_props.headlines)
    #Running and capturing the prediction for each headline
    for headline_received in model_vector_embeddings:
        scoring_model_prediction = headline_scoring_model.\
            predict(headline_received.reshape(1,-1))
        my_headline_predictions.append(scoring_model_prediction[0])
    return {'labels':my_headline_predictions}

@app.post('/get_churn_probability')
def get_churn_probability(client_props: HeadlineData):

    #if 'UC_GRAD' not in client_properties:
    #    pass throw error

    # Our churn model is fake, we don't actually use an ML model :(
    if client_props.uc_grad == "true":
        return {'churn_prob':0.34}
    else:
        return {'churn_prob':0.87}


# fastapi dev serve_json.py
