import azure.functions as func
import datetime
import json
import logging
import requests

app = func.FunctionApp()

# @app.route(route="http_trigger", auth_level=func.AuthLevel.ANONYMOUS)
# def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         test = {'name':f'{name}++', 'Gender':'M'}
#         return func.HttpResponse(json.dumps(test), mimetype="application/json")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )
##### Test the above endpoint    
# POST /echo/post/json HTTP/1.1
# Host: reqbin.com
# Accept: application/json
# Content-Type: application/json
# Content-Length: 81

# {
#   "Id": 78912,
#   "Customer": "Jason Sweet",
#   "Quantity": 1,
#   "Price": 18.00
# }

import mlflow
import os

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="myeventhub",
                               connection="myEventHubConnectionAppSetting") 
def eventhub_trigger(azeventhub: func.EventHubEvent):
    # mlflow.set_tracking_uri('http://20.18.227.5:5000/')
    # mlflow.set_experiment("finally")

    # client = MlflowClient()
    # model_name = "ride-duration-prediction"
    # model_version = "1" 
    # URI = client.get_model_version_download_uri(model_name, model_version)
    # print(URI)
    logging.info('Going to read json data from streaming')
    received_data = json.loads(azeventhub.get_body().decode('utf-8'))
    logging.info(f'Data: {received_data}')

    logging.info('Going to get API_ENDPOINT')
    api_end_point = os.getenv('API_ENDPOINT')
    url = f"http://{api_end_point}:9696/predict"
    headers = {'Content-Type': 'application/json'}
    logging.info('Going to call API')
    response = requests.post(url, data=json.dumps(received_data), headers=headers)
    logging.info(f'Finished request!')
    if response.status_code == 200:
        logging.info("Request successful!")
        logging.info(response.json())
    else:
        logging.error(f"Request failed with status code: {response.status_code}")
        logging.error(f"Error content: {response.text}")
    
    # logging.info(f"Python EventHub trigger processed an event:")

