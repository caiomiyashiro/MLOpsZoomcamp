import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle
import mlflow

df1 = pd.read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-01.parquet')
df2 = pd.read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-02.parquet')

df = pd.concat([df1, df2])

df['location'] = df['PULocationID'].astype(str) + '_' + df['DOLocationID'].astype(str)
df['duration_mins'] = (df['lpep_dropoff_datetime'] - df['lpep_pickup_datetime']).dt.seconds/60

X = df[['location', 'trip_distance']]
y = df['duration_mins']

TRAINING_MODE = "MLFLOW"

if TRAINING_MODE == "SIMPLE":
    rf = RandomForestRegressor(max_depth=7, random_state=0).fit(X, y)
    with open('rf_model.pickle', 'wb') as f:
        pickle.dump(rf, f)
elif TRAINING_MODE == "MLFLOW":
    mlflow.set_tracking_uri('http://20.18.227.5:5000/')
    mlflow.set_experiment("finally")
    mlflow.sklearn.autolog()

    with mlflow.start_run():
        rf = RandomForestRegressor(max_depth=7, random_state=0).fit(X, y)
        # mlflow.sklearn.log_model(rf, artifact_path="models")

