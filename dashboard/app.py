import streamlit as st

st.set_page_config(
    page_title="Data Center Energy Intelligence",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ Data Center Hardware & Energy Efficiency")
st.caption("Developed and Integrated by: Amal Alamri")

st.markdown(
    """
    Explore data-driven insights into server energy efficiency,
    hardware utilization, cloud costs, and power utilization trends.
    """
)

st.subheader("Dashboard Sections")

st.info(
    "Use the sidebar to explore Server Efficiency, "
    "Hardware & Workload, Cloud Cost, and Power Trends."
)

st.markdown("---")

st.caption(
    "Data Sources: SPECpower | AWS EC2 Pricing | Google Cluster"
)

from bigquery_utils import run_query

st.subheader("BigQuery Connection Test")

try:
    df = run_query("""
        SELECT COUNT(*) AS total_records
        FROM `data-center-hardware.analytics.mart_power_trends`
    """)

    st.success("Connected to BigQuery successfully!")
    st.metric("Power Trend Records", int(df.iloc[0]["total_records"]))

except Exception as e:
    st.error(f"BigQuery connection failed: {e}")
