
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

DBT_DIR = "/opt/airflow/dbt_project"
PROFILES_DIR = "/home/airflow/.dbt"
CHECKS_DIR = "/opt/airflow/checks"

DBT_ENV = {
    "DBT_LOG_PATH": "/tmp/dbt_logs",
    "DBT_TARGET_PATH": "/tmp/dbt_target",
    "GOOGLE_CLOUD_PROJECT": "data-center-hardware",
}

with DAG(
    dag_id="data_center_hardware_energy_efficiency",
    description="Build dbt models and validate data center analytics marts",
    start_date=datetime(2026, 10, 1),
    schedule_interval=None,
    catchup=False,
    tags=["data-engineering", "bigquery", "dbt"],
) as dag:

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            f"dbt build --project-dir {DBT_DIR} "
            f"--profiles-dir {PROFILES_DIR}"
        ),
        env=DBT_ENV,
        append_env=True,
    )

    check_server_efficiency = BashOperator(
        task_id="check_server_efficiency",
        bash_command=f"python {CHECKS_DIR}/check_server_efficiency.py",
    )

    check_hardware_workload = BashOperator(
        task_id="check_hardware_workload",
        bash_command=f"python {CHECKS_DIR}/check_hardware_workload.py",
    )

    check_cloud_cost = BashOperator(
        task_id="check_cloud_cost",
        bash_command=f"python {CHECKS_DIR}/check_cloud_cost.py",
    )

    check_power_trends = BashOperator(
        task_id="check_power_trends",
        bash_command=f"python {CHECKS_DIR}/check_power_trends.py",
    )

    dbt_build >> [
        check_server_efficiency,
        check_hardware_workload,
        check_cloud_cost,
        check_power_trends,
    ]
