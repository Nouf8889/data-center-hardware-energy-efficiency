# Data Center Hardware & Energy Efficiency — System Architecture

This diagram shows the implemented data flow, local orchestration, and dashboard deployment. Numbered labels follow the main data path; Airflow and Terraform are shown as supporting components.

```mermaid
flowchart TB
    subgraph SOURCES["1 · Data Sources"]
        SPEC["SPECpower Benchmarks"]

        subgraph GOOGLE["Google Cluster Data 2019"]
            CLUSTER["Cell G<br/>Hardware and Workload"]
            POWER["Cell A · PDU10<br/>Power Utilization"]
        end

        AWS["AWS EC2 Pricing"]
    end

    PY["2 · Python<br/>Data Preparation and Loading"]

    subgraph BQ["Google BigQuery"]
        RAW[("3 · raw_data<br/>7 prepared tables")]
        STAGING["4 · dbt Staging Models"]
        MARTS[("5 · analytics<br/>4 Analytical Marts")]
        RAW --> STAGING --> MARTS
    end

    subgraph LOCAL["Local Docker Compose Environment"]
        AIRFLOW["Apache Airflow<br/>Manually Triggered DAG"]
        BUILD["dbt build"]
        CHECKS["4 Python Validation Checks"]
        AIRFLOW --> BUILD --> CHECKS
    end

    subgraph DEPLOY["Dashboard Deployment"]
        IMAGE["Docker Image"]
        REGISTRY["Artifact Registry"]
        CLOUDRUN["6 · Cloud Run<br/>Streamlit Dashboard"]
        IMAGE --> REGISTRY --> CLOUDRUN
    end

    subgraph PAGES["Dashboard Sections"]
        ANALYTICS["Server Efficiency<br/>Hardware and Workload<br/>Cloud Cost<br/>What-If Simulation"]
        TRENDS["Power Trends"]
    end

    TF["Terraform<br/>Infrastructure as Code"]

    SPEC --> PY
    CLUSTER --> PY
    POWER --> PY
    AWS --> PY
    PY --> RAW

    BUILD -. "runs dbt transformations and tests" .-> STAGING
    CHECKS -. "validates analytical data" .-> MARTS

    MARTS --> ANALYTICS
    RAW --> TRENDS
    CLOUDRUN --> ANALYTICS
    CLOUDRUN --> TRENDS
    TF -. "manages BigQuery datasets" .-> BQ

    classDef source fill:#EEF3FF,stroke:#A5B9E8,color:#26334D
    classDef process fill:#E7F3FF,stroke:#8CB8E8,color:#26334D
    classDef storage fill:#EEE9FF,stroke:#B4A4E3,color:#26334D
    classDef dashboard fill:#F3EEFF,stroke:#B4A4E3,color:#26334D
    classDef cloud fill:#E8F7F0,stroke:#70B98B,color:#244A35
    classDef infra fill:#FFF3DF,stroke:#D6A34B,color:#5A421C

    class SPEC,CLUSTER,POWER,AWS source
    class PY,STAGING,AIRFLOW,BUILD,CHECKS process
    class RAW,MARTS storage
    class ANALYTICS,TRENDS dashboard
    class IMAGE,REGISTRY,CLOUDRUN cloud
    class TF infra
```

## Legend

| Style | Meaning |
|---|---|
| Blue | Data sources, preparation, and orchestration |
| Purple | BigQuery datasets and analytical models |
| Green | Dashboard container and Google Cloud deployment |
| Amber | Terraform-managed infrastructure |
| Solid arrow | Data movement or deployment flow |
| Dashed arrow | Orchestration, validation, or infrastructure management |

## Architecture Notes

- Python data preparation and loading run outside the current Airflow DAG.
- Cell A PDU10 power data and Cell G hardware and workload data are both part of Google Cluster Data 2019, but come from different cells and are not directly joined.
- BigQuery stores seven prepared source tables in `raw_data` and four analytical marts in `analytics`.
- The manually triggered Airflow DAG runs `dbt build`, followed by four Python validation checks.
- Airflow runs locally through Docker Compose.
- The Streamlit dashboard is deployed on Google Cloud Run.
- The dashboard's analytical sections query the marts; Power Trends reads cleaned Cell A power data directly from `raw_data`.
- Terraform currently manages the BigQuery datasets. Cloud Run and Artifact Registry are not managed by Terraform.
