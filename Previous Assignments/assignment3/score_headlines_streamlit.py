"""
This is a python file which runs a streamlit application with
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

"""

import requests
import streamlit as st

st.markdown("# Scoring Headlines")

st.markdown("""
            # Current Status""")
response = requests.get(url="http://127.0.0.1:8081/status", timeout=10)
st.write(response.json()['status'])



st.markdown(""" ## Headline Tone Evaluator""")

st.markdown(""" Write your headline in the text boxes and click enter: """)


#st.write(st.session_state)
if 'headline_list' not in st.session_state:
    st.session_state.headline_list = ["test headline"]

delete_index = st.session_state.get("delete_index", None)
if delete_index is not None:
    if 0 <= delete_index < len(st.session_state.headline_list):
        st.session_state.headline_list.pop(delete_index)
    st.session_state.delete_index = None

for i, val in enumerate(st.session_state.headline_list):
    cols = st.columns([6, 1])
    new_val = cols[0].text_input(f"Item {i+1}", value=val, key=f"input_{i}")
    st.session_state.headline_list[i] = new_val

    if cols[1].button("X", key=f"delete_{i}"):
        st.session_state.delete_index = i
        st.rerun()

if st.button("+ Add more elements"):
    st.session_state.headline_list.append("test headline")
    st.rerun()


st.markdown("""Your headlines, and their sentiments, will be displayed below:""")

response = requests.post(url="http://127.0.0.1:8081/score_headlines",\
    json = {'headlines':st.session_state['headline_list']}, timeout=10)
headline_tonalities = response.json()['labels']


for item_index in reversed(range(len(st.session_state['headline_list']))):
    st.markdown("## Headline: "+st.session_state['headline_list'][item_index])
    st.markdown("### Tone: "+headline_tonalities[item_index])
    st.markdown("----------------------------------------------------------------")
