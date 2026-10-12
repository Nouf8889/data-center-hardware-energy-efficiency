FROM apache/airflow:2.10.5

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

USER airflow

RUN pip install --no-cache-dir \
    "dbt-core==1.10.15" \
    "dbt-bigquery==1.10.3"
