from datetime import datetime
import pandas as pd
from pandas import Timestamp
from batch import prepare_data

def dt(hour, minute, second=0):
    """Create a datetime object for 2022-01-01 with the given hour, minute, and second."""
    return datetime(2022, 1, 1, hour, minute, second)

def test_prepare_data():
    """Test the prepare_data function."""
    data = [
    (None, None, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2), dt(1, 10)),
    (1, 2, dt(2, 2), dt(2, 3)),
    (None, 1, dt(1, 2, 0), dt(1, 2, 50)),
    (2, 3, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),     
]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    df = prepare_data(df, columns)

    import pickle
    with open('/Users/caiomiyashiro/repo/Personal/MLOpsZoomcamp/06-best-practices/homework-06/tests/model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)
    categorical = ['PULocationID', 'DOLocationID']
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)


    print('predicted sum duration:', y_pred.sum())



    expected_df = pd.DataFrame({'PULocationID': {0: '-1', 1: '1', 2: '1'}, 
                                'DOLocationID': {0: '-1', 1: '-1', 2: '2'}, 
                                'tpep_pickup_datetime': {0: '1640998920000000000', 
                                                         1: '1640998920000000000', 
                                                         2: '1641002520000000000'}, 
                                'tpep_dropoff_datetime': {0: '1640999400000000000',
                                                          1: '1640999400000000000',
                                                          2: '1641002580000000000'}, 
                                'duration': {0: 8.0, 1: 8.0, 2: 1.0}})

    assert df.equals(expected_df)