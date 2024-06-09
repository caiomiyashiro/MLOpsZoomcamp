import logging

import mlflow
import os

from flask import Flask, request, jsonify

# optional do download model from MLFLOW
# RUN_ID = 'dafcb234fvrwv24392ik'
# MLFLOW_TRACKING_URI = 'http:127.0.0.1:5000'
# ######
# logged_model = f'runs:/{RUN_ID}/model'
# model = mlflow.pyfunc.load_model(logged_model) # also better to download models and artifacts from storage instead of trackign server
# ######
# client = MlflowClient(tracking_uri = MLFLOW_TRACKING_URI)
# path = client.download_artifacts(run_id=RUN_ID, path='other_artifact.bin')
# with open(path, 'rb') as f:
#     other_artifact = pickle.load(f)

def get_model_from_mlflow():
    URL = os.getenv('MODEL_URL')
    logging.info(f"8888888888888 read MODEL URL")
    logging.info(f"8888888888888 {URL}")
    loaded_model = mlflow.pyfunc.load_model(URL)
    logging.info(f"!!!!!!!! Model loaded! ")
    logging.info(loaded_model)
    return loaded_model

app = Flask('duration-prediction')

def prepare_features(ride_input):
    location = str(ride_input['PULocationID']) + '_' + str(ride_input['DOLocationID'])
    trip_distance = ride_input['trip_distance']
    return [{'location': location, 'trip_distance': trip_distance}]

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride_input = request.get_json()
    model = get_model_from_mlflow()
    features = prepare_features(ride_input)
    pred = model.predict(features)[0]

    result = {
        'request_time': '23:23',
        'run_id':'12312331212312',
        'duration' : pred
    }
    return jsonify(result)

# for gunicorn in bash: gunicorn --bind 0.0.0.0:9696 app:app
# curl -X POST "http://0.0.0.0:9696/predict" -H "Content-Type: application/json" -d '{"DOLocationID":"20", "PULocationID":"10", "trip_distance":"10"}'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9696)