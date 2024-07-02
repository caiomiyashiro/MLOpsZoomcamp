import json

import pandas as pd
import requests

from app import prepare_features


def test_prepare_features():
    ride = {"PULocationID": 10, "DOLocationID": 20, "trip_distance": 10}
    actual_features = prepare_features(ride)
    expected_features = pd.DataFrame({"location": ["10_20"], "trip_distance": [10]})

    pd.testing.assert_frame_equal(actual_features, expected_features)


def test_model_healthcheck():
    # pylint "twodots" disable=missing-timeout
    ride = {"PULocationID": 10, "DOLocationID": 20, "trip_distance": 10.0}

    response = requests.post(
        f"http://localhost:9696/predict",
        data=json.dumps(ride),
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 200


def test_model_sanity():
    ride = {"PULocationID": 10, "DOLocationID": 20, "trip_distance": 10.0}

    response = requests.post(
        f"http://localhost:9696/predict",
        data=json.dumps(ride),
        headers={"content-type": "application/json"},
    )
    output = response.json()["duration"]
    assert 0 < output < 120  # for example: 99% percentile
