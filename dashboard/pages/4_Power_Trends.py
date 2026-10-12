
import streamlit as st
import altair as alt
import pandas as pd
import math

from bigquery_utils import run_query

st.title("📈 Power Utilization Trends")
st.caption("Developed by: Nouf")

st.write(
    "Explore measured and production power utilization "
    "over time using Google Power data."
)


@st.cache_data(ttl=600)
def load_power_data():
    query = """
    SELECT
        hours_from_start,
        cell,
        pdu,
        measured_power_util,
        production_power_util,
        bad_measurement_data,
        bad_production_power_data
    FROM `data-center-hardware.raw_data.google_power_cella_pdu10_cleaned`
    ORDER BY hours_from_start
    """
    return run_query(query)


try:
    df = load_power_data()

    if df.empty:
        st.warning("No power data available.")
        st.stop()

    # Prepare numeric columns
    df["hours_from_start"] = pd.to_numeric(
        df["hours_from_start"], errors="coerce"
    )

    df = df.dropna(subset=["hours_from_start"])

    if df.empty:
        st.warning("No valid time values available.")
        st.stop()

    # -------------------------------
    # Filters
    # -------------------------------
    st.subheader("Filters")

    pdu_options = sorted(df["pdu"].dropna().unique().tolist())

    if not pdu_options:
        st.warning("No PDU values available.")
        st.stop()

    selected_pdu = st.selectbox("Select PDU", pdu_options)

    pdu_df = df[df["pdu"] == selected_pdu].copy()

    min_hour = float(pdu_df["hours_from_start"].min())
    max_hour = float(pdu_df["hours_from_start"].max())

    if min_hour < max_hour:
        # Use whole-hour boundaries to include all measurements,
        # including the last record with a fractional hour value.
        slider_min = math.floor(min_hour)
        slider_max = math.ceil(max_hour)

        selected_hours = st.slider(
            "Select Time Range (Hours from Start)",
            min_value=slider_min,
            max_value=slider_max,
            value=(slider_min, slider_max),
            step=1,
        )

        filtered_df = pdu_df[
            pdu_df["hours_from_start"].between(
                selected_hours[0],
                selected_hours[1]
            )
        ].copy()
    else:
        filtered_df = pdu_df.copy()
        st.info(f"Available time: {min_hour:.1f} hours")

    if filtered_df.empty:
        st.warning("No measurements in the selected time range.")
        st.stop()

    # -------------------------------
    # KPI Metrics
    # -------------------------------
    st.subheader("Power Utilization Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Avg. Measured Utilization",
            f"{filtered_df['measured_power_util'].mean():.1%}"
        )

    with col2:
        st.metric(
            "Avg. Production Utilization",
            f"{filtered_df['production_power_util'].mean():.1%}"
        )

    with col3:
        st.metric(
            "Total Measurements",
            f"{len(filtered_df):,}"
        )

    # -------------------------------
    # Power Trends Chart
    # -------------------------------
    st.subheader("Measured vs. Production Power Utilization")

    chart_df = filtered_df.melt(
        id_vars=["hours_from_start"],
        value_vars=[
            "measured_power_util",
            "production_power_util"
        ],
        var_name="Power Type",
        value_name="Power Utilization"
    )

    chart = (
        alt.Chart(chart_df)
        .mark_line()
        .encode(
            x=alt.X(
                "hours_from_start:Q",
                title="Hours from Start"
            ),
            y=alt.Y(
                "Power Utilization:Q",
                title="Power Utilization",
                scale=alt.Scale(domain=[0, 1])
            ),
            color=alt.Color(
                "Power Type:N",
                title="Power Type"
            ),
            tooltip=[
                alt.Tooltip(
                    "hours_from_start:Q",
                    title="Hour",
                    format=".1f"
                ),
                alt.Tooltip("Power Type:N"),
                alt.Tooltip(
                    "Power Utilization:Q",
                    format=".1%"
                )
            ]
        )
        .properties(height=400)
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

    st.caption(
        "The chart shows utilization ratios, not electricity "
        "consumption in kWh or measured energy savings."
    )

    # -------------------------------
    # Data Quality Overview
    # -------------------------------
    st.subheader("Data Quality Overview")

    measurement_flags = (
        filtered_df["bad_measurement_data"]
        .fillna(False)
        .eq(True)
        .sum()
    )

    production_flags = (
        filtered_df["bad_production_power_data"]
        .fillna(False)
        .eq(True)
        .sum()
    )

    q1, q2, q3 = st.columns(3)

    with q1:
        st.metric(
            "Flagged Measurements",
            f"{measurement_flags:,}"
        )

    with q2:
        st.metric(
            "Flagged Production Records",
            f"{production_flags:,}"
        )

    with q3:
        st.metric(
            "Records in Selected Range",
            f"{len(filtered_df):,}"
        )

    st.caption(
        "Quality flags are provided by the dataset. "
        "Flagged records are included in the chart and "
        "summary metrics; they are not automatically removed."
    )

except Exception as e:
    st.error(f"Unable to load power data: {e}")
