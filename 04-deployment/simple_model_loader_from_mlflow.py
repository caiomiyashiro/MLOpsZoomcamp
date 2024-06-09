import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri('http://20.18.227.5:5000/')
mlflow.set_experiment("finally")

client = MlflowClient()
model_name = "ride-duration-prediction"
model_version = "1" 

model_uri = client.get_model_version_download_uri(model_name, model_version)
print(f"Model Download URI: {model_uri}")

loaded_model = mlflow.sklearn.load_model(model_uri)
print(loaded_model)

print(f"Prediction: {loaded_model.predict([['166_143', 10]])}")