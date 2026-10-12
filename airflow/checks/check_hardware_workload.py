import os

from google.cloud import bigquery


PROJECT_ID = os.getenv("GCP_PROJECT_ID", "data-center-hardware")
DATASET_ID = "analytics"
TABLE_ID = "mart_hardware_workload"

REQUIRED_COLUMNS = {
    "machine_id",
    "start_time",
    "end_time",
    "avg_cpu_usage",
    "avg_memory_usage",
    "cpu_capacity",
    "memory_capacity",
    "cpu_to_capacity_ratio",
    "memory_to_capacity_ratio",
}


def run_validation():
    """Validate the schema and data quality of the hardware workload table."""
    client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    # Check table access and required columns.
    table = client.get_table(table_ref)
    actual_columns = {field.name for field in table.schema}
    missing_columns = REQUIRED_COLUMNS - actual_columns

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    # Check that the table contains valid data.
    query = f"""
        SELECT
            COUNT(*) AS total_rows,
            COUNTIF(machine_id IS NULL) AS null_machine_ids,
            COUNTIF(start_time IS NULL) AS null_start_times,
            COUNTIF(end_time IS NULL) AS null_end_times,
            COUNTIF(
                cpu_capacity IS NULL OR cpu_capacity <= 0
            ) AS invalid_cpu_capacity,
            COUNTIF(
                memory_capacity IS NULL OR memory_capacity <= 0
            ) AS invalid_memory_capacity,
            COUNTIF(
                cpu_to_capacity_ratio IS NULL
                OR memory_to_capacity_ratio IS NULL
            ) AS null_usage_ratios
        FROM `{table_ref}`
    """

    result = next(iter(client.query(query).result()))

    failures = []

    if result.total_rows == 0:
        failures.append("Table contains no rows")

    if result.null_machine_ids:
        failures.append(f"Null machine IDs: {result.null_machine_ids}")

    if result.null_start_times:
        failures.append(f"Null start times: {result.null_start_times}")

    if result.null_end_times:
        failures.append(f"Null end times: {result.null_end_times}")

    if result.invalid_cpu_capacity:
        failures.append(
            f"Invalid CPU capacity: {result.invalid_cpu_capacity}"
        )

    if result.invalid_memory_capacity:
        failures.append(
            f"Invalid memory capacity: {result.invalid_memory_capacity}"
        )

    if result.null_usage_ratios:
        failures.append(
            f"Null usage ratios: {result.null_usage_ratios}"
        )

    if failures:
        raise ValueError(
            "Hardware workload validation failed:\n- "
            + "\n- ".join(failures)
        )

    print(
        f"PASS: {table_ref} contains {result.total_rows} rows; "
        "all validation checks passed."
    )
    return True


if __name__ == "__main__":
    run_validation()
