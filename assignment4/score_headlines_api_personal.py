# pylint: disable=R0801
"""
The following code is a REST API version of the previous
assignment in which I read in, transformed, and outputted
the tonality of newspaper headlines.

Before running, be sure to create your own environment with
the following commands:

conda create -n a2_env python=3.11

conda activate a2-env

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
from datetime import date


import joblib  # type: ignore
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
from pydantic import BaseModel


os.makedirs("./logs", exist_ok=True)


with open("score_headline_logging.json", "r", encoding="utf-8") as f:
    json_config = json.load(f)
    logging.config.dictConfig(json_config)


fname = os.path.basename(__file__)
log = logging.getLogger(fname)

log.info("Loading the sentence transformer model.")

model_path = "/opt/huggingface_models/all-MiniLM-L6-v2"

if os.path.exists(model_path):
    sentence_vector_transformer_model = SentenceTransformer(model_path)
else:
    # Fallback: download from Hugging Face, ONLY NECESSARY
    # IF THE MODEL DOES NOT EXIST ON THE SYSTEM RUNNING THIS PROGRAM
    sentence_vector_transformer_model = SentenceTransformer("all-MiniLM-L6-v2")
log.info("Loading the headline tone reading model.")
headline_scoring_model = joblib.load("svm.joblib")

app = FastAPI()


@app.get("/status")
def status():
    """
    Returns the status of the REST API web service via a python dictionary.

    Returns: A python dictionary containing status and OK.
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
    log.debug("Received the following headlines: %s.", client_props.headlines)
    my_headline_predictions = []
    model_vector_embeddings = sentence_vector_transformer_model.encode(
        client_props.headlines
    )
    # Running and capturing the prediction for each headline
    for headline_index, headline_received in enumerate(model_vector_embeddings):
        scoring_model_prediction = headline_scoring_model.predict(
            headline_received.reshape(1, -1)
        )
        log.debug(
            f"Headline {client_props.headlines[headline_index]} \
            at %d read as label: %s",
            headline_index,
            scoring_model_prediction,
        )
        my_headline_predictions.append(scoring_model_prediction[0])

    today_str = date.today().strftime("%Y_%m_%d")
    existing_file_path_check = f"headline_scores_{today_str}.txt"


    if os.path.exists(f"./results/{existing_file_path_check}"):
        with open(f"./results/{existing_file_path_check}", "a+", encoding="utf-8") as file:
            for prediction_index, prediction_value in enumerate(my_headline_predictions, start=0):
                file.write(str(prediction_value) + "," + str(client_props.headlines[prediction_index])+"\n")
    else:
        with open(f"./results/{existing_file_path_check}", "w", encoding="utf-8") as file:
            for prediction_index, prediction_value in enumerate(my_headline_predictions, start=0):
                file.write(str(prediction_value) + "," + str(client_props.headlines[prediction_index])+"\n")
    return {"labels": my_headline_predictions}
