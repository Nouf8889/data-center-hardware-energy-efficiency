# Data Center Hardware & Energy Efficiency — System Architecture

This diagram represents the current implemented architecture.

```mermaid
flowchart TB
    subgraph Sources[Data Sources]
        SPEC[SPECpower Benchmarks]
        CLUSTER[Google Cluster 2019<br/>Cell G: Hardware and Workload]
        POWER[Google Power Data<br/>Cell A: PDU10]
        AWS[AWS EC2 Pricing]
    end

    PY[Python<br/>Data Preparation and Loading]

    subgraph BQ[Google BigQuery]
        RAW[(raw_data<br/>7 prepared tables)]
        STAGING[dbt Staging Models]
        MARTS[(analytics<br/>Analytical Marts)]
    end

    subgraph ORCH[Apache Airflow - Local Docker Environment]
        BUILD[dbt build]
        CHECKS[4 Python Validation Checks]
        BUILD --> CHECKS
    end

    subgraph DASH[Streamlit Dashboard]
        ANALYTICS[Server Efficiency<br/>Hardware and Workload<br/>Cloud Cost<br/>What-If Simulation]
        TRENDS[Power Trends]
    end

    SPEC --> PY
    CLUSTER --> PY
    POWER --> PY
    AWS --> PY

    PY --> RAW
    RAW --> STAGING
    STAGING --> MARTS

    BUILD -.-> STAGING
    CHECKS -.-> MARTS

    MARTS --> ANALYTICS
    RAW --> TRENDS

    classDef source fill:#EEF3FF,stroke:#A5B9E8,color:#26334D
    classDef process fill:#E7F3FF,stroke:#8CB8E8,color:#26334D
    classDef storage fill:#EEE9FF,stroke:#B4A4E3,color:#26334D
    classDef dashboard fill:#F3EEFF,stroke:#B4A4E3,color:#26334D

    class SPEC,CLUSTER,POWER,AWS source
    class PY,BUILD,CHECKS,STAGING process
    class RAW,MARTS storage
    class ANALYTICS,TRENDS dashboard



```

## Architecture Notes

- Python data preparation and loading run outside the current Airflow DAG.
- BigQuery stores seven prepared source tables in `raw_data`.
- dbt builds staging models and analytical marts.
- Airflow runs `dbt build`, followed by four validation checks.
- The current DAG is manually triggered, not scheduled.
- Four Streamlit pages query analytical marts.
- Power Trends queries cleaned Cell A power data directly from `raw_data`.
- Google Cell A power and Cell G workload datasets are separate and must not be treated as directly joined.
- Terraform and Cloud Run are not shown as deployed components until their implementation is confirmed.


