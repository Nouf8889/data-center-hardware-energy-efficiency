# dbt Project — Data Center Hardware Energy Efficiency

## Overview

This dbt project transforms data in Google BigQuery to support data center hardware energy-efficiency analytics.

The project uses the `dbt_project` profile and defines staging models and analytical marts.

## Prerequisites

- Python and dbt Core with the BigQuery adapter installed.
- Access to the Google Cloud project `data-center-hardware`.
- A valid dbt profile configured for BigQuery.
- Google Cloud authentication with the permissions required to access and query the relevant BigQuery datasets.

## Configuration

The dbt project expects a profile named `dbt_project`.

Create the local profile file at `~/.dbt/profiles.yml`. Configure its BigQuery output with the appropriate project, dataset, authentication method, execution location, and other required settings.

The profile should use OAuth authentication if you are following the local development setup.

**Security:** Keep `profiles.yml` and authentication credentials outside version control. Never commit access tokens, service-account keys, or other secrets.

## Running dbt

Run commands from the repository root:

Validate the project configuration and connection:

```bash
dbt debug --project-dir dbt_project --profiles-dir "$HOME/.dbt"
```

Build models and run configured data tests:

```bash
dbt build --project-dir dbt_project --profiles-dir "$HOME/.dbt"
```

Run data tests without rebuilding models:

```bash
dbt test --project-dir dbt_project --profiles-dir "$HOME/.dbt"
```

## Models and Data Quality

The project contains analytical marts for:

- Server efficiency
- Hardware workload
- Cloud cost
- Power trends

The build process runs the applicable dbt models and configured data-quality tests. Review the command output to confirm that the build and tests completed successfully.

## Airflow

The repository also includes a local Airflow environment that runs dbt and downstream validation checks. Refer to the root `README.md` for Docker Compose startup instructions and the required local Google Cloud authentication setup.

## Resources

- [dbt documentation](https://docs.getdbt.com/docs/introduction)
- [dbt BigQuery setup](https://docs.getdbt.com/docs/core/connect-data-platform/bigquery-setup)
