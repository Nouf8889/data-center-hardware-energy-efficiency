import streamlit as st
from google.cloud import bigquery

PROJECT_ID = "data-center-hardware"


@st.cache_resource
def get_bigquery_client():
    """Create and reuse a BigQuery client using local Google Cloud credentials."""
    return bigquery.Client(project=PROJECT_ID)


@st.cache_data(ttl=600)
def run_query(sql: str):
    """Run a BigQuery SQL query and return a Pandas DataFrame."""
    client = get_bigquery_client()
    return client.query(sql).to_dataframe()
