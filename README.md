# Data Center Hardware & Energy Efficiency

An end-to-end data engineering project integrating SPECpower, Google Cluster Data, and AWS EC2 Pricing to analyze server performance, energy efficiency, workload utilization, and scenario-based infrastructure costs.

## Project Overview

This project explores how data can support better infrastructure decisions by analyzing server hardware configurations, energy efficiency, workload utilization, and cloud computing costs.

**Main Question:** How can we identify energy-efficient server configurations without compromising performance?

## Data Sources

| Data Source | Purpose |
|---|---|
| SPECpower | Analyze server performance and energy efficiency across hardware configurations |
| Google Cluster Data 2019 | Explore machine hardware capacity, workload usage, and power measurements |
| AWS EC2 Pricing | Compare cloud instance configurations and estimate infrastructure costs |

**Important:** Google Cluster Cell A power measurements and Cell G workload data are analyzed separately because they do not represent the same cluster cell.

## Project Structure

```text
data-center-energy/
├── data/                 # Raw extracts and processed CSV datasets
├── pipelines/
│   ├── aws/              # AWS pricing extraction, exploration, and verification
│   ├── google/           # Google Cluster data cleaning and workload joins
│   └── specpower/        # SPECpower exploration and configuration analysis
├── README.md
└── .gitignore
```

## Data Processing Workflow

1. **Extract:** Collect and export data from the selected sources.
2. **Clean:** Handle missing values, standardize columns, and prepare datasets.
3. **Validate:** Check data quality, duplicates, consistency, and pricing accuracy.
4. **Transform:** Prepare datasets for hardware, workload, and efficiency analysis.
5. **Store:** Load selected processed datasets into Google BigQuery.
6. **Analyze:** Explore infrastructure efficiency, utilization, and potential cost scenarios.

## Google BigQuery

**Google Cloud Project:** `data-center-hardware`

**Dataset:** `raw_data`

Processed datasets include:

- `aws_ec2_pricing_cleaned`
- `google_power_cella_pdu10_cleaned`
- `google_machine_hardware_cleaned`
- `google_hardware_workload_joined`

## Current Progress

- Completed initial SPECpower exploration and configuration analysis.
- Extracted, cleaned, and verified AWS EC2 pricing data.
- Processed Google Cluster power and machine hardware datasets.
- Created an exploratory hardware–workload dataset using sampled instance usage.
- Performed data quality checks and validation.
- Organized Python scripts by data source.

## Running the Pipelines

Run scripts from the project root directory to preserve relative paths to the `data/` folder.

Example:

```bash
python pipelines/google/google_hardware_cleaning.py
python pipelines/google/google_instance_usage_cleaning.py
python pipelines/google/google_hardware_workload_join.py
python pipelines/google/google_power_cleaning.py
python pipelines/aws/verify_aws_prices.py
```

**Note:** The Google instance usage dataset is based on a limited sample rather than the full dataset. Hardware–workload results should therefore be treated as exploratory. Some capacity values may not be time-aligned with the sampled usage observations.

## Project Status

**In Development** — Data preparation and validation are underway, with further analysis, orchestration, and visualization planned.
