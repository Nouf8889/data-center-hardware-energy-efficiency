
import streamlit as st
import pandas as pd
from bigquery_utils import run_query

TABLE = "`data-center-hardware.analytics.mart_server_efficiency`"

st.title("⚡ Server Energy Efficiency")
st.caption("Developed by: Ghadi")
st.markdown(
    "Explore server energy efficiency, power consumption, "
    "and hardware performance."
)

try:
    # 1. Summary KPIs
    summary = run_query(f"""
        SELECT
            COUNT(*) AS total_records,
            COUNT(DISTINCT hardware_vendor) AS vendors,
            COUNT(DISTINCT server_model) AS server_models,
            AVG(ssj_ops_per_watt) AS avg_efficiency,
            AVG(avg_watts_100) AS avg_full_load_watts,
            AVG(avg_watts_idle) AS avg_idle_watts
        FROM {TABLE}
    """)

    # 2. Average efficiency by vendor and server model
    models = run_query(f"""
        SELECT
            hardware_vendor,
            server_model,
            COUNT(*) AS records,
            AVG(ssj_ops_per_watt) AS avg_efficiency,
            AVG(avg_watts_100) AS avg_full_load_watts,
            AVG(avg_watts_idle) AS avg_idle_watts
        FROM {TABLE}
        WHERE hardware_vendor IS NOT NULL
          AND server_model IS NOT NULL
          AND ssj_ops_per_watt IS NOT NULL
        GROUP BY hardware_vendor, server_model
        ORDER BY avg_efficiency DESC
    """)

    # 3. Records for the power-efficiency comparison
    scatter = run_query(f"""
        SELECT
            hardware_vendor,
            server_model,
            avg_watts_100,
            ssj_ops_per_watt
        FROM {TABLE}
        WHERE avg_watts_100 IS NOT NULL
          AND ssj_ops_per_watt IS NOT NULL
    """)

    if summary.empty:
        st.warning("No server efficiency data was returned.")
        st.stop()

    metrics = summary.iloc[0]

    st.subheader("Key Performance Indicators")
    c1, c2, c3 = st.columns(3)
    c1.metric("Server Records", f"{int(metrics['total_records']):,}")
    c2.metric("Hardware Vendors", f"{int(metrics['vendors']):,}")
    c3.metric("Server Models", f"{int(metrics['server_models']):,}")

    c4, c5, c6 = st.columns(3)
    c4.metric(
        "Avg. Efficiency",
        f"{metrics['avg_efficiency']:,.1f}"
        if pd.notna(metrics["avg_efficiency"]) else "N/A",
        help="Average SSJ operations per watt, as provided by the dataset.",
    )
    c5.metric(
        "Avg. Full-Load Power",
        f"{metrics['avg_full_load_watts']:,.1f} W"
        if pd.notna(metrics["avg_full_load_watts"]) else "N/A",
    )
    c6.metric(
        "Avg. Idle Power",
        f"{metrics['avg_idle_watts']:,.1f} W"
        if pd.notna(metrics["avg_idle_watts"]) else "N/A",
    )

    st.divider()
    st.subheader("Explore Server Models")

    vendors = sorted(models["hardware_vendor"].dropna().unique().tolist())
    selected_vendors = st.multiselect(
        "Filter by hardware vendor",
        options=vendors,
        default=[],
        help="Leave empty to include all vendors.",
    )

    filtered = models.copy()
    if selected_vendors:
        filtered = filtered[
            filtered["hardware_vendor"].isin(selected_vendors)
        ]

    if filtered.empty:
        st.info("No models match the selected filters.")
    else:
        top_models = filtered.head(10).copy()
        top_models["model_label"] = (
            top_models["hardware_vendor"].astype(str)
            + " — "
            + top_models["server_model"].astype(str)
        )

        st.subheader("Top 10 Models by Average Energy Efficiency")
        st.caption(
            "Models are ranked by average SSJ operations per watt. "
            "Record counts show how many dataset records contribute "
            "to each model's average."
        )
        chart_data = top_models.set_index("model_label")[
            ["avg_efficiency"]
        ]
        st.bar_chart(chart_data, horizontal=True)

        st.subheader("Power Consumption vs. Energy Efficiency")
        if not scatter.empty:
            scatter_view = scatter.copy()
            if selected_vendors:
                scatter_view = scatter_view[
                    scatter_view["hardware_vendor"].isin(selected_vendors)
                ]

            st.scatter_chart(
                scatter_view,
                x="avg_watts_100",
                y="ssj_ops_per_watt",
                color="hardware_vendor",
                size=70,
            )
            st.caption(
                "Each point represents a dataset record. "
                "Higher efficiency means more SSJ operations per watt; "
                "power is measured in watts at full load."
            )

        st.subheader("Server Model Details")
        display = filtered.rename(columns={
            "hardware_vendor": "Hardware Vendor",
            "server_model": "Server Model",
            "records": "Record Count",
            "avg_efficiency": "Avg. Efficiency (SSJ/W)",
            "avg_full_load_watts": "Avg. Full-Load Power (W)",
            "avg_idle_watts": "Avg. Idle Power (W)",
        })

        st.dataframe(
            display,
            width="stretch",
            hide_index=True,
        )

except Exception as e:
    st.error("Unable to load server efficiency data from BigQuery.")
    st.exception(e)
