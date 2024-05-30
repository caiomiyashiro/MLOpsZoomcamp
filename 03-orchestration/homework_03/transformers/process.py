from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction import DictVectorizer

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    data['duration'] = data.tpep_dropoff_datetime - data.tpep_pickup_datetime
    data.duration = data.duration.dt.total_seconds() / 60

    data = data[(data.duration >= 1) & (data.duration <= 60)]

    # categorical = ['PULocationID', 'DOLocationID']
    # data[categorical] = data[categorical].astype(str)

    X = data[['PULocationID', 'DOLocationID', 'trip_distance']]
    y = data['duration']
    
    dv = DictVectorizer()
    data_dicts = X.to_dict(orient='records')
    X = dv.fit_transform(data_dicts)

    lr = LinearRegression()
    lr.fit(X, y)
    print(lr.coef_)
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
