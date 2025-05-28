# pylint: disable=R0801
"""
The following code is a REST API version of the previous
assignment in which I read in, transformed, and outputted
the tonality of newspaper headlines.

Before running, be sure to create your own environment with
the following commands:

conda create -n a2_env python=3.11

conda activate a2_env

pip install -r requirements.txt

You can/should run this file with either of the following
commands:

fastapi dev score_headlines_api.py

or

uvicorn score_headlines_api:app --host 127.0.0.1 --port 8081


"""

from typing import List
import os
import logging
import logging.config
import json


import joblib
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
from pydantic import BaseModel


os.makedirs("./logs", exist_ok=True)

# Setting up logs
with open("score_headline_logging.json", "r", encoding="utf-8") as f:
    json_config = json.load(f)
    logging.config.dictConfig(json_config)


fname = os.path.basename(__file__)
log = logging.getLogger(fname)
# Loading the respective models
log.info("Loading the sentence transformer model.")
sentence_vector_transformer_model = SentenceTransformer("/opt/huggingface_models/all-MiniLM-L6-v2")
log.info("Loading the headline tone reading model.")
headline_scoring_model = joblib.load("svm.joblib")

app = FastAPI()
@app.get("/status")
def status():
    """
    Returns the status of the REST API web service via a python dictionary.

    Returns: A python dictionary containing status and OK if the web api is online.
    """
    log.debug("Status checking")
    d = {"status": "OK"}
    return d



class HeadlineData(BaseModel):
    """
    A class which contains the expected values necessary to
    check the tonality of headlines provided by the client.

    Parameters:
    headlines: a string list of headlines provided by the client

    """

    headlines: List[str]


@app.post("/score_headlines")
def score_headlines(client_props: HeadlineData):
    """
    A function which takes in a list of headlines provided by the client via
    json with a POST request transforms them with a specific sentence encoding,
    runs these encoded sentences through a model to check their tonality,
    then returns an array of tonality predictions.

    Arguments:
    client_props: Contains all of the arguments passed to the function via json
    in a POST request

    """
    log.info("Scoring Headlines function called.")
    log.debug(f"Received the following headlines: {client_props.headlines}.")
    my_headline_predictions = []
    model_vector_embeddings = sentence_vector_transformer_model.encode(client_props.headlines)

    # Running and capturing the prediction for each headline
    for headline_index, headline_received in enumerate(model_vector_embeddings):
        scoring_model_prediction = headline_scoring_model.predict(headline_received.reshape(1, -1))
        log.debug(
            f"Headline {client_props.headlines[headline_index]} \
            at {headline_index} read as label: {scoring_model_prediction}"
        )
        my_headline_predictions.append(scoring_model_prediction[0])
    return {"labels": my_headline_predictions}
