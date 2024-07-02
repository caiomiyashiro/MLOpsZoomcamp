#!/usr/bin/env python
# coding: utf-8

import sys
import pickle
import pandas as pd


def prepare_data(df_, categorical_cols):
    """"
    Preprocess the data
    """
    df_['duration'] = df_.tpep_dropoff_datetime - df_.tpep_pickup_datetime
    df_['duration'] = df_.duration.dt.total_seconds() / 60

    df_ = df_[(df_.duration >= 1) & (df_.duration <= 60)].copy()

    df_[categorical_cols] = df_[categorical_cols].fillna(-1).astype('int').astype('str')
    return df_

def read_data(filename):
    """
    Read data from a parquet file and preprocess it
    """
    df_ = pd.read_parquet(filename)
    return df_


if __name__ == "__main__":
    year = int(sys.argv[1])
    month = int(sys.argv[2])

    input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f'output/yellow_tripdata_{year:04d}-{month:02d}.parquet'


    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)


    categorical = ['PULocationID', 'DOLocationID']

    df = read_data(input_file)
    df = prepare_data(df, categorical)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)


    print('predicted mean duration:', y_pred.mean())


    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred


    df_result.to_parquet(output_file, engine='pyarrow', index=False)
