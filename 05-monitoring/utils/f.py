import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine

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