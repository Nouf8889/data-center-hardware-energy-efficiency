
from google.cloud import bigquery


PROJECT_ID = "data-center-hardware"
TABLE_ID = f"{PROJECT_ID}.analytics.mart_cloud_cost"

REQUIRED_COLUMNS = {
    "instance_type",
    "instance_family",
    "vcpu",
    "memory_gb",
    "physical_processor",
    "processor_architecture",
    "region",
    "operating_system",
    "tenancy",
    "pricing_type",
    "hourly_price_usd",
    "monthly_price_usd",
    "annual_price_usd",
    "hourly_cost_per_vcpu_usd",
    "hourly_cost_per_gb_memory_usd",
}


def run_validation():
    """Validate data quality for the Cloud Cost BigQuery table."""
    client = bigquery.Client(project=PROJECT_ID)
    errors = []

    # 1. Check that the table exists.
    try:
        table = client.get_table(TABLE_ID)
        print(f"PASS: Table exists: {TABLE_ID}")
    except Exception as exc:
        raise RuntimeError(
            f"FAIL: Cannot access BigQuery table {TABLE_ID}: {exc}"
        ) from exc

    # 2. Count rows directly from BigQuery.
    row_count_sql = (
        f"SELECT COUNT(*) AS total_rows FROM `{TABLE_ID}`"
    )
    row_count = next(
        iter(client.query(row_count_sql).result())
    ).total_rows

    if row_count == 0:
        errors.append("Table contains no rows.")
    else:
        print(f"PASS: Table contains {row_count} rows.")

    # 3. Validate required columns.
    actual_columns = {field.name for field in table.schema}
    missing_columns = REQUIRED_COLUMNS - actual_columns

    if missing_columns:
        errors.append(
            f"Missing required columns: {sorted(missing_columns)}"
        )
    else:
        print("PASS: All required columns exist.")

    if errors:
        raise ValueError(
            "Cloud Cost validation failed:\n- "
            + "\n- ".join(errors)
        )

    # 4. Validate data quality.
    sql = f"""
        SELECT
            COUNT(*) AS total_rows,

            COUNTIF(
                instance_type IS NULL
                OR TRIM(instance_type) = ''
            ) AS missing_instance_types,

            COUNTIF(
                instance_family IS NULL
                OR TRIM(instance_family) = ''
            ) AS missing_families,

            COUNTIF(vcpu IS NULL OR vcpu <= 0)
                AS invalid_vcpu,

            COUNTIF(
                memory_gb IS NULL
                OR memory_gb <= 0
            ) AS invalid_memory,

            COUNTIF(
                hourly_price_usd IS NULL
                OR hourly_price_usd <= 0
            ) AS invalid_hourly_prices,

            COUNTIF(
                monthly_price_usd IS NULL
                OR monthly_price_usd <= 0
            ) AS invalid_monthly_prices,

            COUNTIF(
                annual_price_usd IS NULL
                OR annual_price_usd <= 0
            ) AS invalid_annual_prices,

            COUNTIF(
                hourly_cost_per_vcpu_usd IS NULL
                OR hourly_cost_per_vcpu_usd <= 0
            ) AS invalid_vcpu_costs,

            COUNTIF(
                hourly_cost_per_gb_memory_usd IS NULL
                OR hourly_cost_per_gb_memory_usd <= 0
            ) AS invalid_memory_costs,

            COUNT(DISTINCT instance_type)
                AS unique_instance_types

        FROM `{TABLE_ID}`
    """

    result = next(iter(client.query(sql).result()))

    checks = {
        "missing instance types": result.missing_instance_types,
        "missing instance families": result.missing_families,
        "invalid vCPU values": result.invalid_vcpu,
        "invalid memory values": result.invalid_memory,
        "invalid hourly prices": result.invalid_hourly_prices,
        "invalid monthly prices": result.invalid_monthly_prices,
        "invalid annual prices": result.invalid_annual_prices,
        "invalid cost per vCPU": result.invalid_vcpu_costs,
        "invalid cost per GB memory": result.invalid_memory_costs,
    }

    for name, count in checks.items():
        if count:
            errors.append(
                f"{name}: {count} row(s) failed."
            )
        else:
            print(f"PASS: {name}")

    # 5. Check uniqueness of instance types.
    if result.total_rows != result.unique_instance_types:
        errors.append(
            "Duplicate instance types detected: "
            f"{result.total_rows} rows, "
            f"{result.unique_instance_types} unique types."
        )
    else:
        print("PASS: Instance types are unique.")

    # 6. Report final result.
    if errors:
        raise ValueError(
            "Cloud Cost validation failed:\n- "
            + "\n- ".join(errors)
        )

    print(
        "\nSUCCESS: All Cloud Cost validations passed "
        f"({result.total_rows} rows checked)."
    )
    return True


if __name__ == "__main__":
    run_validation()
