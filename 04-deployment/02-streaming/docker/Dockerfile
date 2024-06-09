FROM mcr.microsoft.com/azure-functions/python:3.0-python3.9

RUN pip install update pip
RUN apt-get update && apt-get install -y && rm -rf /var/lib/apt/lists/*

COPY ["requirements.txt", "./"]
RUN pip install  -r requirements.txt

COPY ["docker_predict.py", "./"]

ENV MODEL_URL=$MODEL_URL
ENV AZURE_STORAGE_CONNECTION_STRING=$AZURE_STORAGE_CONNECTION_STRING

EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "docker_predict:app"]

