import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine
import psycopg2
from utils.f import convert_date_to_recent_data, recreate_empty_table, insert_sample_data

# batch

def convert_date_to_recent_data(df:pd.DataFrame, date_column:str='lpep_pickup_datetime') -> pd.Series:
    """ This function simulates a real-world scenario where the date column is always represented as recent data.
    """
    lpep_pickup_datetime_f = pd.to_datetime(df[date_column].dt.strftime('%Y-%m-%d'))
    today = pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))
    time_diff = today - lpep_pickup_datetime_f
    return lpep_pickup_datetime_f + np.min(time_diff)

def recreate_empty_table(conn, table_name:str='trips') -> None:
    cursor = conn.cursor()

    # Create a table with the desired columns
    create_table_query = f"""

        DROP TABLE IF EXISTS {table_name};

        CREATE TABLE {table_name} (
            time TIMESTAMPTZ,
            trip_distance FLOAT,
            payment_type VARCHAR(10)
        )
        """
    cursor.execute(create_table_query)
    conn.commit()

def insert_sample_data(df:pd.DataFrame, engine, table_name:str='trips') -> None:
    # Insert data from the DataFrame into the table
    engine = create_engine(f'postgresql://postgres:example@localhost:5432/postgres')
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f'FINISHED')


####################################
####################################
####################################

# df = pd.read_parquet("https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2024-01.parquet")

# time = convert_date_to_recent_data(df)
# cols = ['trip_distance', 'payment_type']
# df2 = df[cols].copy() # do a smaller copy of the dataframe
# df2['time'] = time

# Create a PostgreSQL engine
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="example"
)
    
recreate_empty_table(conn)
# engine = create_engine(f'postgresql://postgres:example@localhost:5432/postgres')
# insert_sample_data(df2, engine)
