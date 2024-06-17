import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine
from evidently.ui.workspace import Workspace
import psycopg2
from utils.f import convert_date_to_recent_data, recreate_empty_table, insert_sample_data
from utils.evidently import create_report, create_project, get_df_evidently_metrics

# batch
def process_raw_data(df:pd.DataFrame) -> pd.DataFrame:
    df.rename(columns={"PULocationID": "pulocationid", "DOLocationID":"dolocationid"}, inplace=True)
    num_features = ["passenger_count", "trip_distance", "fare_amount", "total_amount"]
    cat_features = ["pulocationid", "dolocationid"]
    df[cat_features] = df[cat_features].astype('str')

    tz = 'Japan'
    time = df['lpep_pickup_datetime'].dt.tz_localize(tz, nonexistent='shift_forward', ambiguous='infer')
    df = df[num_features + cat_features]
    df['time'] = time
    return df

YEAR = 2023

SAMPLE_REFERENCE_DATA = pd.read_parquet("https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-01.parquet").sample(frac=0.2, random_state=42)
SAMPLE_REFERENCE_DATA = process_raw_data(SAMPLE_REFERENCE_DATA)

EVIDENTLY_WORKSPACE = "model_monitoring_workspace"
EVIDENTLY__PROJECT_NAME = "ride_prediction_project"
ws = Workspace.create(EVIDENTLY_WORKSPACE) # If already exists, it just returns the workspace
project = create_project(ws)

# Create a PostgreSQL engine
conn = psycopg2.connect(
    host="db",
    database="postgres",
    user="postgres",
    password="example"
)

recreate_empty_table(conn, version=2)
recreate_empty_table(conn, version=3)
engine = create_engine(f'postgresql://postgres:example@db:5432/postgres')

for month in range(2, 4):
    print(f'Downloading data for {YEAR}-{month:02d}')
    df = pd.read_parquet(f"https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-{month:02d}.parquet")
    df = df.sample(frac=0.2, random_state=42)
    df = process_raw_data(df)

    # time = convert_date_to_recent_data(df)
    # cols = ['trip_distance', 'payment_type']
    # df2 = df[cols].copy() # do a smaller copy of the dataframe
    # df2['time'] = time

    insert_sample_data(df, engine, table_name='trips_batch')

    # Evidently monitoring
    report = create_report(ref_data=SAMPLE_REFERENCE_DATA, cur_data=df)
    df_evidently_metrics = get_df_evidently_metrics(report.as_dict())
    insert_sample_data(df_evidently_metrics, engine, table_name='evidently_metrics')



