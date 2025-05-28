# pylint: disable=R0801
"""
The following code below takes a text file input of
provided headlines, converts them into their vector
representation, feeds them into a svc model,
gets a tone-based output, and writes these outputs
to a file.

This file should be run with the following command format:
"python score_headlines_personal.py [headline_file_name].txt headline_source"
For this program to run correctly, please either place the file in the
same directory as the score_headlines_personal.py file, or provide the
file path for the headlines text file you want to use.

To ensure computation results are similar across models,
please set an environment variable with the following command:
Linux (inside of .bashrc):
export TF_ENABLE_ONEDNN_OPTS=0
Note: Please source .bashrc afterward to confirm the instantiation
of this environment variable
Powershell:
$env:TF_ENABLE_ONEDNN_OPTS = "0"

Before running this file, please make sure you run the following command:
pip install -r requirements.txt
or
conda create -n a1_env python=3.10
conda activate myenv
pip install -r requirements.txt
"""

import datetime
import os
import sys
import joblib
from sentence_transformers import SentenceTransformer


# Potential Installs
# pip install numpy pandas sentence_transformers joblib scikit-learn ipykernel


def get_predictions_from_text(text_array, vector_encoding_model, headline_scoring_model):
    """
    Takes a text array of headlines, converts them into their vector representation, feeds
    them into a pre-trained model, and returns their predicted tones

    Args:
        text_array: a text array of strings provided by the user
        vector_encoding_model: the pre-trained model used create the
        vector representation of the headlines provided in the
        text array
        headline_sccoring_model: the pre-trained model used
        to create the predictions from the vector-represented
        headlines from the original text array
    Return:
        An array of all of the predicted tones for the headlines provided in the text array
    """
    my_predictions_from_file = []
    # Encode the text array to their vector representation using the provided model
    model_vector_embeddings = vector_encoding_model.encode(text_array)
    # Running and capturing the prediction for each headline
    for headline_received in model_vector_embeddings:
        scoring_model_prediction = headline_scoring_model.predict(headline_received.reshape(1, -1))
        # print("CHECK PREDICTION:", scoring_model_prediction[0])
        my_predictions_from_file.append(scoring_model_prediction[0])
    return my_predictions_from_file


def write_predictions_to_file(model_predictions, headline_source, file_headlines):
    """
    Takes a text array of headlines, converts them into
    their vector representation, feeds them into a
    pre-trained model, and returns their predicted tones

    Args:
        predictions: an array of string-represented predictions
        of tone from the previous model classification output
        file_headlines: an array containing the original
        string versions of the headlines
        headline_source: the source of the headlines
    """
    # Check if a output file already exists,
    # appending value to that file if true
    # and writing a new file if false
    existing_file_path_check = (
        "headline_scores_"
        + headline_source
        + "_"
        + str(datetime.date.today().year)
        + "_"
        + str(datetime.date.today().month)
        + "_"
        + str(datetime.date.today().day)
        + ".txt"
    )
    if os.path.exists("./" + existing_file_path_check):
        with open("./" + existing_file_path_check, "a+", encoding="utf-8") as file:
            for prediction_index, prediction_value in enumerate(model_predictions, start=0):
                file.write(str(prediction_value) + "," + str(file_headlines[prediction_index]))
    else:
        with open("./" + existing_file_path_check, "w", encoding="utf-8") as file:
            for prediction_index, prediction_value in enumerate(model_predictions, start=0):
                file.write(str(prediction_value) + "," + str(file_headlines[prediction_index]))


def main():
    """
    The main function of our program, ran whenever the file itself
    is ran.
    """
    # Loading the original SentenceTransformer Model
    sentence_vector_transformer_model = \
        SentenceTransformer("/opt/huggingface_models/all-MiniLM-L6-v2")
    # Printing system arguments to verify their values
    # print(sys.argv)
    # A quick length check to make sure that the program receives the correct number of arguments
    if len(sys.argv) < 2:
        print(
            "Error: Running this program requires providing two arguments, \
            a headline text file name and a headline source.\n\
Two arguments are missing. Please write your command in the following format:\n\n\
py -3.10 score_headlines.py [INSERT TEXT DOCUMENT NAME].txt [INSERT HEADLINE SOURCE]"
        )
        sys.exit(1)
    elif len(sys.argv) < 3:
        print(
            "Error: Running this program requires providing two arguments,\
            a headline text file name and a headline source.\n\
One of these arguments are missing. Please write your command in the following format:\n\n\
py -3.10 score_headlines.py [INSERT TEXT DOCUMENT NAME].txt [INSERT HEADLINE SOURCE]"
        )
        sys.exit(1)
    # Setting our variables for the file name and source using the provided system arguments
    headline_text_file = sys.argv[1]
    headline_source = sys.argv[2]
    # Test prints to verify the system arguments are received correctly
    # print("Headline Text File:", headline_text_file)
    # print("Headline Source:", headline_source)
    # print("Test")
    # Loading the model using joblib
    headline_scoring_model = joblib.load("svm.joblib")
    # Testing the models ability to predict with a simple case
    # prediction_check = headline_scoring_model.predict\
    # ([sentence_vector_transformer_model.encode("Everything is terrible")])
    # print("Prediction Check:", prediction_check)
    # Reading in the headlines from the provided headline text file
    with open(headline_text_file, "r", encoding="utf-8") as file:
        headlines_from_file = file.readlines()
    # Making tone predictions and writing those predictions to a file
    my_predictions_from_file = get_predictions_from_text(
        headlines_from_file, sentence_vector_transformer_model, headline_scoring_model
    )
    write_predictions_to_file(my_predictions_from_file, headline_source, headlines_from_file)


if __name__ == "__main__":
    main()
