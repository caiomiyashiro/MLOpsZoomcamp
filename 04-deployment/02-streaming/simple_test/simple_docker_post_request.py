import requests
import json
import logging

# Define the JSON data
data = {
    "PULocationID": "166",
    "DOLocationID": "143",
    "trip_distance": 30.0
}

# Convert the data to JSON format
json_data = json.dumps(data)

# Send the POST request with JSON data
url = "http://20.210.75.238:9696/predict"
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json_data, headers=headers)

# Check the response
if response.status_code == 200:
    logging.info("Request successful!")
    logging.info(response.json())
else:
    logging.info(f"Request failed with status code: {response.status_code}")