import pickle
from flask import Flask, request, jsonify 
import pandas as pd

with open('rf_model.pickle', 'rb') as f:
    model = pickle.load(f)

app = Flask('duration-prediction')

def prepare_features(ride_input): 
    location = str(ride_input['PULocationID']) + '_' + str(ride_input['DOLocationID'])
    trip_distance = ride_input['trip_distance']
    return pd.DataFrame({'location': [location], 'trip_distance': [trip_distance]})

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride_input = request.get_json()

    features = prepare_features(ride_input)
    pred = model.predict(features)

    result = {
        'duration' : pred[0]
    }
    return jsonify(result)

# for gunicorn in bash: gunicorn --bind 0.0.0.0:9696 app:app
# curl -X POST "http://0.0.0.0:9696/predict" -H "Content-Type: application/json" -d '{"DOLocationID":"20", "PULocationID":"10", "trip_distance":"10"}'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9696)