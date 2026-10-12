
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Data Center Hardware & Energy Efficiency",
    page_icon="⚡",
    layout="wide",
)

# Main title
st.title("⚡ Data Center Hardware & Energy Efficiency")
st.caption("Developed and Integrated by: Amal Alamri")

# Project introduction
st.markdown(
    """
    ### Welcome to the Data Center Energy Intelligence Dashboard

    Explore data-driven insights into server energy efficiency,
    hardware utilization, cloud costs, and power utilization trends.

    This dashboard transforms data from multiple sources into
    interactive visualizations to support better hardware
    selection and energy efficiency decisions.
    """
)

st.divider()

# Dashboard sections
st.subheader("📊 Dashboard Sections")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        #### ⚡ Server Efficiency
        Analyze server performance and energy efficiency
        using SPECpower benchmark data.

        #### 🖥️ Hardware & Workload
        Explore hardware characteristics and workload
        patterns from Google Cluster data.
        """
    )

with col2:
    st.markdown(
        """
        #### ☁️ Cloud Cost
        Compare AWS EC2 instance specifications
        and pricing.

        #### 📈 Power Trends
        Explore power utilization patterns and
        identify periods of relatively high demand.
        """
    )

st.divider()

# What-If Simulation
st.subheader("🔮 What-If Simulation")

st.markdown(
    """
    Explore different server selection scenarios by adjusting
    performance requirements and full-load power limits.

    Compare eligible servers and identify energy-efficient
    hardware options based on SPECpower benchmark results.
    """
)

st.info(
    "👈 Use the sidebar to navigate between dashboard pages "
    "and explore the What-If Simulation."
)

# Footer
st.divider()

st.caption(
    "Data Sources: SPECpower | AWS EC2 Pricing | Google Cluster"
)

st.caption(
    "Data Engineering Project | SDA × Le Wagon"
)
