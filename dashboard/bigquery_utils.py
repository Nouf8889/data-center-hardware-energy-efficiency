import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT_ID = "data-center-hardware"


@st.cache_resource
def get_bigquery_client():
    """Create and reuse a BigQuery client."""
    if "gcp_service_account" in st.secrets:
        credentials = service_account.Credentials.from_service_account_info(
            dict(st.secrets["gcp_service_account"])
        )
        return bigquery.Client(
            project=PROJECT_ID,
            credentials=credentials,
        )

    return bigquery.Client(project=PROJECT_ID)


@st.cache_data(ttl=600)
def run_query(sql: str):
    """Run a BigQuery SQL query and return a Pandas DataFrame."""
    client = get_bigquery_client()
    return client.query(sql).to_dataframe()
