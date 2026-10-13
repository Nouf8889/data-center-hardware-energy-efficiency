# Data Center Hardware & Energy Efficiency
## Capstone Presentation — 5 Minutes

**Team:** 5 presenters
**Format:** 5 slides, approximately 1 minute per presenter

---

## Slide 1 — Problem & Business Value
**Duration:** 50–60 seconds
**Presenter:** To be assigned

### On-slide Content

**The Challenge**
- Data center infrastructure decisions must balance performance, energy efficiency, and cost.
- Comparing hardware, workload, pricing, and power data is difficult when insights are scattered.

**Our Solution**
- A data engineering pipeline that prepares and analyzes multiple infrastructure datasets.
- An interactive dashboard for exploring server efficiency, resource allocation, cloud pricing, and power utilization.

**Business Value**
- Support performance-aware server selection.
- Highlight resource allocation patterns worth investigating.
- Compare cloud pricing by CPU and memory requirements.
- Monitor normalized power utilization trends.

### Speaker Notes

"Our project addresses a common infrastructure challenge: how to choose
hardware and cloud resources while balancing performance, energy efficiency,
and cost. We built a data platform that transforms multiple datasets into
analytical models and an interactive dashboard. It helps decision-makers
compare server configurations, investigate resource allocation, explore
cloud pricing, and monitor power utilization trends."

---

## Slide 2 — System Architecture
**Duration:** 60 seconds
**Presenter:** To be assigned

### On-slide Content

**Data Sources**
- SPECpower server benchmarks
- Google Cluster 2019 hardware and workload data (Cell G)
- Google power utilization data (Cell A)
- AWS EC2 pricing data

**Data Pipeline**
1. Python prepares and loads datasets into BigQuery `raw_data`.
2. dbt builds staging models and analytical marts in BigQuery.
3. Apache Airflow runs `dbt build`, followed by four validation checks.
4. Streamlit queries BigQuery to display interactive analytics.

**Architecture Notes**
- Python ingestion is not orchestrated by the current Airflow DAG.
- Four analytical dashboard pages query analytics marts.
- Power Trends queries the cleaned power table in `raw_data` directly.
- Docker Compose supports the local Airflow environment.

### Speaker Notes

"Our pipeline starts with four data sources: SPECpower benchmarks,
Google Cluster hardware and workload data, Google power utilization,
and AWS EC2 pricing. Python prepares these datasets and loads them
into BigQuery. Then dbt transforms the raw tables into staging models
and analytical marts. Apache Airflow orchestrates the dbt build and
four downstream validation checks. Finally, Streamlit queries BigQuery
to provide interactive dashboards. The Power Trends page currently
reads cleaned raw data directly, while the other analytical pages
use the marts."

---

## Slide 3 — Analytics & Interactive Demo
**Duration:** 60 seconds
**Presenter:** To be assigned

### On-slide Content

**Key Analytical Findings**
- Server selection depends on performance requirements and energy efficiency.
- 94.4% of sampled workload records have CPU-to-capacity ratios below 5%.
- AWS EC2 pricing shows different cost advantages for CPU and memory.

**Interactive What-If Simulation**
- Set minimum server performance (ssj_ops at 100% load).
- Set maximum full-load power consumption (watts).
- Filter eligible benchmark records.
- Recommend the highest-efficiency eligible record using `efficiency_100`.

**Business Value**
- Turn infrastructure data into practical decision support.
- Compare options under user-defined constraints.

### Speaker Notes

"Our analytics reveal several useful patterns. Server selection changes
depending on performance requirements, while sampled workload records
highlight opportunities to investigate resource allocation. Cloud pricing
also shows that the best option depends on whether CPU or memory cost
matters more.

For our interactive demonstration, the What-If Simulation lets users
set minimum performance and maximum power limits. It filters eligible
SPECpower benchmark records and recommends the most efficient option
at full load. This supports informed server selection rather than
choosing hardware based on performance alone."

### Demo Plan

1. Open the What-If Simulation page.
2. Show the minimum performance and maximum power sliders.
3. Adjust one constraint.
4. Explain how the eligible configurations and recommendation respond.

**Important Limitations**
- The 94.4% figure refers to sampled records, not unique machines.
- Low resource-to-capacity ratios do not prove overprovisioning.
- AWS comparisons cover the selected region and On-Demand pricing.
- The simulation does not calculate electricity bills or cost savings.
- Overall SPECpower efficiency and full-load efficiency are different metrics.

---

## Slide 4 — Testing & Reliability
**Duration:** 60 seconds
**Presenter:** To be assigned

### On-slide Content

**Verified Pipeline Results**
- dbt build: 27 PASS, 0 WARN, 0 ERROR.
- Airflow DAG: 5 of 5 tasks succeeded on October 12, 2026.
- Four downstream Python validation checks completed successfully.

**Data Quality & Reliability**
- dbt tests validate analytical model data.
- Python checks verify the four analytical marts.
- Airflow provides a repeatable workflow for building and validating models.
- The local Airflow environment runs using Docker Compose.

**Execution Scope**
- The DAG is manually triggered (`schedule_interval=None`).
- Python data preparation and ingestion run outside the DAG.
- The current Airflow setup uses SequentialExecutor.

### Speaker Notes

"To make our analytics more reliable, we implemented multiple validation
layers. Our verified dbt build completed with 27 passes and no warnings
or errors. We also successfully ran the Airflow DAG, with all five tasks
completing: one dbt build task followed by four Python validation checks.

Airflow gives us a repeatable process for transforming and validating
the analytical data. At this stage, the workflow is manually triggered
and runs locally through Docker Compose. Automated scheduling and
end-to-end ingestion orchestration are possible future improvements."

---

## Slide 5 — Limitations & Future Work
**Duration:** 50–60 seconds
**Presenter:** To be assigned

### On-slide Content

**Current Limitations**
- Google Cell A power and Cell G workload datasets cannot be directly linked.
- Power utilization values are normalized ratios, not kWh.
- Benchmark performance may differ from real-world workloads.
- AWS pricing analysis covers a limited region and pricing model.
- Python ingestion is outside the current Airflow DAG.

**Future Improvements**
- Orchestrate Python ingestion and data preparation with Airflow.
- Add scheduled runs, monitoring, and failure notifications.
- Expand cloud pricing coverage and workload-aware recommendations.
- Investigate actual energy and cost savings using compatible measurements.
- Explore Terraform infrastructure provisioning and Cloud Run deployment.

**Deployment Status**
- Terraform and Cloud Run are team-owned work in progress.
- Confirm implementation status before the final presentation.

### Speaker Notes

"Our project provides a foundation for data-driven infrastructure
decisions, but it also has important limitations. For example,
Google power and workload datasets come from different cells,
so we cannot directly attribute power readings to individual
machines. Also, normalized power utilization does not represent
electricity consumption in kilowatt-hours.

Our next steps include orchestrating the ingestion process,
scheduling Airflow runs, expanding cloud cost comparisons,
and improving monitoring. The team is also exploring Terraform
and Cloud Run deployment, which we will report according to
their verified implementation status.

Overall, our project demonstrates how data engineering can
turn infrastructure datasets into useful decision-support tools."

---

## Final Presentation Checklist

- [ ] Confirm the five presenters and slide assignments.
- [ ] Rehearse the full presentation within five minutes.
- [ ] Verify the dashboard and What-If demo before presenting.
- [ ] Capture screenshots of successful dbt and Airflow runs.
- [ ] Confirm Terraform and Cloud Run status with the team.
- [ ] Review bootcamp guide requirements when available.
- [ ] Avoid claiming measured energy savings or a direct Cell A–Cell G join.

## Proposed Speaker Assignments

| Slide | Presenter | Target Duration |
|---|---|---|
| 1 — Problem & Business Value | Nouf | 50 seconds |
| 2 — System Architecture | Amal | 60 seconds |
| 3 — Analytics & Interactive Demo | Atheer | 60 seconds |
| 4 — Testing & Reliability | Ghadi | 60 seconds |
| 5 — Limitations & Future Work | Abrar | 50 seconds |

**Total target:** 4 minutes 40 seconds.
**Transition buffer:** 20 seconds.
**Status:** Proposed; awaiting team confirmation.
