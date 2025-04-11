#Potential Installs
#pip install numpy pandas sentence_transformers joblib scikit-learn ipykernel

#Standard Libraries
import argparse
import os
import sys
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import datetime

#Third-Party
import joblib
from sentence_transformers import SentenceTransformer

#Local

def main():
    sentence_vector_transformer_model = SentenceTransformer("all-MiniLM-L6-v2")
    #print(sys.argv)
    if len(sys.argv) < 2:
        print("Error: Running this program requires providing two arguments, a headline text file name and a headline source.\n\
Two arguments are missing. Please write your command in the following format:\n\n\
py -3.10 score_headlines.py [INSERT TEXT DOCUMENT NAME].txt [INSERT HEADLINE SOURCE]")
        sys.exit(1)
    elif len(sys.argv) < 3:
        print("Error: Running this program requires providing two arguments, a headline text file name and a headline source.\n\
One of these arguments are missing. Please write your command in the following format:\n\n\
py -3.10 score_headlines.py [INSERT TEXT DOCUMENT NAME].txt [INSERT HEADLINE SOURCE]")
        sys.exit(1)
    
    headline_text_file = sys.argv[1]
    headline_source = sys.argv[2]
    
    print("Headline Text File:", headline_text_file)
    print("Headline Source:", headline_source)
    print("Test")
    
    headline_scoring_model = joblib.load('svm.joblib')
    prediction_check = headline_scoring_model.predict([sentence_vector_transformer_model.encode("Everything is terrible")])
    print("Prediction Check:", prediction_check)
    
    headline_from_file = None
    with open(headline_text_file, 'r') as file:
        headlines_from_file = file.readlines()
        
    headliens_from_file = headlines_from_file[:5]
    
    my_predictions_from_file = []
    model_vector_embeddings = sentence_vector_transformer_model.encode(headlines_from_file)
    for headline_received in model_vector_embeddings[:5]:
        scoring_model_prediction = headline_scoring_model.predict(headline_received.reshape(1,-1))
        print("CHECK PREDICTION:", scoring_model_prediction[0])
        my_predictions_from_file.append(scoring_model_prediction[0])
        
    
    existing_file_path_check = "headline_scores_"+headline_source+"_"+str(datetime.date.today().year)+"_"+str(datetime.date.today().month)+"_"+str(datetime.date.today().day)+".txt"
    if os.path.exists("./"+existing_file_path_check):
        with open("./"+existing_file_path_check, 'a+') as file:
            for prediction_index in range(len(my_predictions_from_file)):
                file.write(str(my_predictions_from_file[prediction_index])+","+str(headlines_from_file[prediction_index]))
    else:
        with open("./"+existing_file_path_check, 'w') as file:
            for prediction_index in range(len(my_predictions_from_file)):
                file.write(str(my_predictions_from_file[prediction_index])+","+str(headlines_from_file[prediction_index]))            
        

if __name__ == "__main__":
    main()