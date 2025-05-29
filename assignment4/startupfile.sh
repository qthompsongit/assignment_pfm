#!/bin/bash

uvicorn score_headlines_api_personal:app --host 0.0.0.0 --port 8081 &

streamlit run score_headlines_streamlit_personal.py --server.port 9081
