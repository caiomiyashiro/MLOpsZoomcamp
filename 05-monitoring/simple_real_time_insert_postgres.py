import pandas as pd
import numpy as np
import prometheus_client as pc
from datetime import datetime
from sqlalchemy import create_engine
import psycopg2
import pytz
from utils.f import convert_date_to_recent_data, recreate_empty_table
from utils.system_metrics import get_system_metrics
import time

# time.sleep(10) # wait for the database to be ready
print("started!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
time.sleep(10) # wait for the database to be ready
df = pd.read_parquet("https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2024-01.parquet")

time_ = convert_date_to_recent_data(df)
cols = ['trip_distance', 'payment_type']
df2 = df[cols].copy() # do a smaller copy of the dataframe
df2['time'] = time_

# Create a PostgreSQL engine
conn = psycopg2.connect(
    host="db",
    database="postgres",
    user="postgres",
    password="example"
)

recreate_empty_table(conn)
engine = create_engine(f'postgresql://postgres:example@db:5432/postgres')
df2_ix = 0

while df2_ix < df2.shape[0]:                            # while all rows haven't been processed
    # 
    data_amount = int(np.random.normal(100, 200))       # sort a specific number of rows
    sub_df = df2.iloc[df2_ix:df2_ix+data_amount].copy() # get the subset of the data
    tz = pytz.timezone('Japan')
    sub_df['time'] = datetime.now(tz)        # simulate that data came from specific day
    df2_ix = df2_ix + data_amount                       # update the index
    sub_df.to_sql('trips', engine, if_exists='append', index=False)
    print(f'{sub_df.shape[0]} inserted into the database')
    # sort a integer between 1 and 5 with uniform distribution
    wait_time = np.random.randint(1, 5)

    _ = get_system_metrics()

    time.sleep(wait_time)

