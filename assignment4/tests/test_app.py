# pylint: disable=wrong-import-position
"""
This file contains the tests necessary to push code to main,
and eventually production, for this assignment.

"""


import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient  # pylint: disable=wrong-import-position
from score_headlines_api_personal import app  # pylint: disable=wrong-import-position, import-error

client = TestClient(app)


def test_status():
    """Test the /status GET endpoint"""
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_score_headlines_empty_list():
    """Test the /score_headlines POST endpoint with an empty headline list"""
    response = client.post("/score_headlines", json={"headlines": []})
    assert response.status_code == 200
    assert response.json()["labels"] == []

def test_score_headlines_simple_check():
    """Test the /score_headlines POST endpoint with an empty headline list"""
    response = client.post("/score_headlines", json={"headlines": ['wow this is so cool']})
    assert response.status_code == 200
    assert response.json()["labels"] == ['Neutral']
