import requests
import json

# Define the API endpoint URL
url = "http://localhost:7071/api/http_trigger"

# Define the JSON data to be sent
data = {
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com"
}

# Send the POST request with JSON data
response = requests.post(url, json=data)

# Check the response status code
if response.status_code == 200:
    print("Data sent successfully!")
    # Process the response data if needed
    response_data = json.loads(response.content)['name']
    print(f'{response_data} !!!!')
else:
    print(f"Error: {response.status_code} - {response.text}")