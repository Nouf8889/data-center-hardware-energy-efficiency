# Dashboard Testing Report

## 1. Overview

**Project:** Data Center Hardware & Energy Efficiency
**Component:** Streamlit Dashboard
**Testing Scope:** Dashboard functionality and final manual testing
**Status:** Manual testing completed; detailed verification documented below.

## 2. Environment

* **Application Framework:** Streamlit
* **Programming Language:** Python
* **Data Platform:** Google BigQuery
* **Local Environment:** VS Code Terminal
* **Python Environment:** Virtual environment (`.venv`)
* **Application Entry Point:** `dashboard/app.py`

## 3. Dependency Verification

The required dashboard libraries were successfully imported using the active Python environment.

Verified imports:

* Streamlit
* Pandas
* Plotly
* Google Cloud BigQuery client

**Result:** PASS

## 4. Application Startup

The dashboard was launched locally using:

```bash
streamlit run dashboard/app.py
```

Streamlit started successfully and provided a local application URL.

**Result:** PASS

## 5. Dashboard Page Testing

All five dashboard sections were opened and manually checked. The application appeared to work normally during the testing session.

| Dashboard Section   | Test Scope             | Result |
| ------------------- | ---------------------- | ------ |
| Server Efficiency   | Manual page inspection | PASS   |
| Hardware & Workload | Manual page inspection | PASS   |
| Cloud Cost          | Manual page inspection | PASS   |
| Power Trends        | Manual page inspection | PASS   |
| What-If Simulation  | Manual page inspection | PASS   |

**Note:** These results reflect manual inspection. Separate automated tests, exhaustive filter testing, and independent verification of every query and chart are not claimed by this report.

## 6. Data and Interpretation Considerations

The dashboard presents results from different datasets and analytical contexts.

* SPECpower benchmark results support server performance and energy-efficiency comparisons.
* Google Cluster workload records support hardware and resource-to-capacity analysis.
* AWS EC2 pricing data supports cloud cost comparisons.
* Google Cell A power data represents normalized power utilization, not physical energy consumption in kWh.
* Google Cell A power readings must not be presented as directly linked to Google Cell G workload records without a validated relationship.

These limitations should be preserved when interpreting dashboard results.

## 7. Outstanding Verification

The following checks should be completed or confirmed before final delivery:

* Verify that charts and filters respond correctly to different inputs.
* Verify that What-If Simulation results change appropriately when its inputs change.
* Check the handling and display of missing or invalid data.
* Confirm that BigQuery-backed pages load successfully and return expected results.
* Re-run the dashboard after the team's final merged changes.
* Capture screenshots for the final presentation.

## 8. Conclusion

The Streamlit dashboard launched successfully in the local development environment, the required libraries imported successfully, and all five dashboard sections were manually inspected and appeared to work normally.

A final verification pass is recommended after the team merges its changes to confirm the behavior of interactive controls, data queries, and visualizations before the project presentation.
