# assignment_1_pfm

### Note: Do not run any of the python notebooks current in this project or the file "score_headlines_personal.py" as they were previously used to either gather data, train the original headline scoring model, or contain an original local machine version of project code.

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