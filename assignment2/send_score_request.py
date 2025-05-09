"""
This script sends GET and POST requests to a
FastAPI server to test various endpoints.
"""
import requests

HOST = "localhost"
PORT = 8081

# Request something which doesn't exist
response = requests.get(url=f"http://{HOST}:{PORT}/", timeout=10)
print(f"Result of doing a GET request from http://{HOST}:{PORT}/")
print(response)

print("-------------")

# Request the time (does not exist)
response = requests.get(url=f"http://{HOST}:{PORT}/get_time", timeout=10)
print(f"Result of doing a GET request from http://{HOST}:{PORT}/get_time")
print(response)
print("Response raw content:" + str(response))

print("-------------")

params = {
    "headlines": [
        "test2",
        "WOW THIS IS SO BAD EVIL TERRIBLE EVIL BAD \
            EVIL EVIL NIGHTMARE EVIL BAD AWFUL IT's TERRIBLE AND AWFUL UGH",
    ],
    "uc_grad": True,
}

# Request the churn probability (does not exist)
response = requests.post(url=f"http://{HOST}:{PORT}/get_churn_probability", json=params, timeout=10)
print(f"Result of doing a GET request from http://{HOST}:{PORT}/get_churn_probability")
print(response)
print("Response raw content:" + str(response))
print("Response text:", response.text)

print("-------------")

# Request the tonality of provided headlines
response = requests.post(url=f"http://{HOST}:{PORT}/score_headlines", json=params, timeout=10)
print(f"Result of doing a GET request from http://{HOST}:{PORT}/score_headlines")
print(response)
print("Response raw content:" + str(response))
print("Response text:", response.text)

print("-------------")


if __name__ == "__main__":
    pass
