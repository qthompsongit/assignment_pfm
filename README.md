# assignment_1_pfm

### Note: Do not run any of the python notebooks current in this project or the file "score_headlines_personal.py" as they were previously used to either gather data, train the original headline scoring model, or contain an original local machine version of project code.


# assignment1
This project takes a text file input of
provided headlines, converts them into their vector
representation, feeds them into a svc model,
gets a tone-based output, and writes these outputs
to a file.

To run this project, run the following command:
"python score_headlines.py [headline_file_name].txt headline_source"
For this program to run correctly, please either place the file in the
same directory as the score_headlines.py file, or provide the
file path for the headlines text file you want to use.

To ensure computation results are similar across models,
please set an environment variable with the following command:

Linux (inside of .bashrc):

export TF_ENABLE_ONEDNN_OPTS=0

Note: Please source .bashrc afterward to confirm the instantiation
of this environment variable

Powershell:
$env:TF_ENABLE_ONEDNN_OPTS = "0"

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

NOTE: Please make sure that the programs and files in this directory have read, write, and execute privileges. You can ensure this by running the following command while inside this assignment's directory:

chmod 777 .

# assignment_2

*NOTE, please correctly set up your environment before running or install the packages in this directory with

pip install -r requirement.txt

To run this project, please use one of the following commands in the assignment2 directory:

You can/should run this file with either of the following commands:

fastapi dev score_headlines_api.py

or

uvicorn score_headlines_api:app --host 127.0.0.1 --port 8081

You can also run this assignment headless using "nohup" at the start of these commands.

Be sure to kill -9 [pid] once you are done running the web service.

The "send_score_request.py" is a python file used to test current and old (get_time, get_churn_probability) functionality of the webservice. This is not required for testing purposes, but it can be another vector to ensure everything runs as expected.


# assignment3

This project allows a user to run a streamlit application with
the ability to communicate with a web service that
labels the tonality of headlines provided to it.

To run this file correctly, please use the following commmand:

streamlit run score_headlines_streamlit.py --server.port 9081

Make sure that the score_headlines_api service is running first by
using one of the following commands:

You can/should run this file with either of the following
commands:

fastapi dev score_headlines_api.py

or

uvicorn score_headlines_api:app --host 127.0.0.1 --port 8081
