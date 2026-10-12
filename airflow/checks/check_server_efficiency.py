
from google.cloud import bigquery


PROJECT_ID = "data-center-hardware"
DATASET_ID = "analytics"
TABLE_ID = "mart_server_efficiency"

TABLE = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

REQUIRED_COLUMNS = {
    "hardware_vendor",
    "server_model",
    "avg_watts_100",
    "ssj_ops_per_watt",
}


def run_validation():
    """Validate the server efficiency mart in BigQuery."""
    client = bigquery.Client(project=PROJECT_ID)

    # Check 1: The table exists and has the required columns.
    table = client.get_table(TABLE)
    actual_columns = {field.name for field in table.schema}
    missing_columns = REQUIRED_COLUMNS - actual_columns

    if missing_columns:
        raise RuntimeError(
            f"Validation failed: missing columns: "
            f"{', '.join(sorted(missing_columns))}"
        )

    # Check 2: The table contains at least one row.
    query = f"SELECT COUNT(*) AS row_count FROM `{TABLE}`"
    row_count = next(iter(client.query(query).result())).row_count

    if row_count == 0:
        raise RuntimeError(
            f"Validation failed: {TABLE} contains no rows."
        )

    # Check 3: Required values are present and numeric measures are valid.
    query = f"""
        SELECT
            COUNTIF(
                hardware_vendor IS NULL
                OR TRIM(hardware_vendor) = ''
            ) AS missing_vendor,
            COUNTIF(
                server_model IS NULL
                OR TRIM(server_model) = ''
            ) AS missing_model,
            COUNTIF(avg_watts_100 IS NULL) AS missing_power,
            COUNTIF(ssj_ops_per_watt IS NULL) AS missing_efficiency,
            COUNTIF(avg_watts_100 < 0) AS negative_power,
            COUNTIF(ssj_ops_per_watt < 0) AS negative_efficiency
        FROM `{TABLE}`
    """
    result = next(iter(client.query(query).result()))

    failures = {
        "missing hardware_vendor": result.missing_vendor,
        "missing server_model": result.missing_model,
        "missing avg_watts_100": result.missing_power,
        "missing ssj_ops_per_watt": result.missing_efficiency,
        "negative avg_watts_100": result.negative_power,
        "negative ssj_ops_per_watt": result.negative_efficiency,
    }

    failures = {
        name: count for name, count in failures.items() if count > 0
    }

    if failures:
        details = ", ".join(
            f"{name}: {count}" for name, count in failures.items()
        )
        raise RuntimeError(f"Validation failed: {details}")

    print(
        f"Validation passed for {TABLE}: "
        f"{row_count} rows checked."
    )
    return True


if __name__ == "__main__":
    run_validation()
