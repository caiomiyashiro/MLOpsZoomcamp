FROM python:3.9.7-slim

RUN pip install --upgrade pip
RUN apt-get update

# needed for psycopg2
RUN apt-get install -y gcc python3-dev libc-dev 

WORKDIR /app_root

COPY requirements.txt .
RUN pip install  -r requirements.txt

COPY simple_real_time_insert_postgres.py .
COPY utils/ ./utils

RUN ls

RUN ls utils

EXPOSE 8000

ENTRYPOINT ["python", "simple_real_time_insert_postgres.py"]
