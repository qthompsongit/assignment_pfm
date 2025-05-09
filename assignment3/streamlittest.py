"""
This is test code to check out streamlit and
its capabilities.
"""
import streamlit as st
st.write("Hello World")
st.write("This is a test")
st.write("BIG LETTERS!")

st.markdown("# THIS IS WRITTEN IN MARKDOWN")

namecheck = st.text_input("What is your name")
if len(namecheck.strip()) == 0:
    st.warning("Who are you?")
else :
    st.write(f"{namecheck}, pleased to meet you!")
