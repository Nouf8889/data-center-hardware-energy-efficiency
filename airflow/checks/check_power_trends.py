from google.cloud import bigquery


PROJECT_ID = "data-center-hardware"
DATASET_ID = "analytics"
TABLE_ID = "mart_power_trends"

TABLE = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

REQUIRED_COLUMNS = {
    "cell",
    "pdu",
    "hour_bucket",
    "total_readings",
    "bad_measurement_count",
    "bad_production_count",
    "avg_measured_power_util",
    "avg_production_power_util",
}


def run_validation():
    """Validate the Power Trends mart in BigQuery."""
    client = bigquery.Client(
        project=PROJECT_ID,
        location="EU",
    )

    print("\n=== Power Trends Data Quality Validation ===")

    # Check 1: Table/View exists.
    try:
        table = client.get_table(TABLE)
    except Exception as error:
        raise RuntimeError(
            f"FAIL: Cannot access {TABLE}: {error}"
        ) from error

    print(f"PASS: Table/View exists: {TABLE}")

    # Check 2: Required columns exist.
    actual_columns = {field.name for field in table.schema}
    missing_columns = REQUIRED_COLUMNS - actual_columns

    if missing_columns:
        raise RuntimeError(
            "FAIL: Missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    print("PASS: All 8 required columns exist.")

    # Check 3: Table contains data.
    query = f"""
        SELECT COUNT(*) AS row_count
        FROM `{TABLE}`
    """

    row_count = next(
        iter(client.query(query, location="EU").result())
    ).row_count

    if row_count == 0:
        raise RuntimeError(
            f"FAIL: {TABLE} contains no rows."
        )

    print(f"PASS: Table contains {row_count} rows.")

    # Check 4: Validate required values and ranges.
    query = f"""
        SELECT
            COUNTIF(
                cell IS NULL OR TRIM(cell) = ''
            ) AS missing_cell,

            COUNTIF(
                pdu IS NULL OR TRIM(pdu) = ''
            ) AS missing_pdu,

            COUNTIF(
                hour_bucket IS NULL
                OR hour_bucket < 0
            ) AS invalid_hour,

            COUNTIF(
                total_readings IS NULL
                OR total_readings <= 0
            ) AS invalid_readings,

            COUNTIF(
                bad_measurement_count IS NULL
                OR bad_measurement_count < 0
            ) AS invalid_measurement_count,

            COUNTIF(
                bad_production_count IS NULL
                OR bad_production_count < 0
            ) AS invalid_production_count,

            COUNTIF(
                (
                    avg_measured_power_util IS NULL
                    AND (
                        bad_measurement_count IS NULL
                        OR total_readings IS NULL
                        OR bad_measurement_count != total_readings
                    )
                )
                OR IS_NAN(avg_measured_power_util)
                OR IS_INF(avg_measured_power_util)
                OR avg_measured_power_util < 0
                OR avg_measured_power_util > 1
            ) AS invalid_measured_util,

            COUNTIF(
                (
                    avg_production_power_util IS NULL
                    AND (
                        bad_production_count IS NULL
                        OR total_readings IS NULL
                        OR bad_production_count != total_readings
                    )
                )
                OR IS_NAN(avg_production_power_util)
                OR IS_INF(avg_production_power_util)
                OR avg_production_power_util < 0
                OR avg_production_power_util > 1
            ) AS invalid_production_util,

            COUNTIF(
                bad_measurement_count > total_readings
            ) AS measurement_count_exceeds_total,

            COUNTIF(
                bad_production_count > total_readings
            ) AS production_count_exceeds_total,

            COUNTIF(
                avg_measured_power_util IS NULL
                AND total_readings > 0
                AND bad_measurement_count = total_readings
            ) AS expected_null_measured,

            COUNTIF(
                avg_production_power_util IS NULL
                AND total_readings > 0
                AND bad_production_count = total_readings
            ) AS expected_null_production

        FROM `{TABLE}`
    """

    result = next(
        iter(client.query(query, location="EU").result())
    )

    checks = {
        "Cell values are present": result.missing_cell,
        "PDU values are present": result.missing_pdu,
        "Hour buckets are valid": result.invalid_hour,
        "Total readings are positive": result.invalid_readings,
        "Measurement counts are valid":
            result.invalid_measurement_count,
        "Production counts are valid":
            result.invalid_production_count,
        "Measured utilization is valid":
            result.invalid_measured_util,
        "Production utilization is valid":
            result.invalid_production_util,
        "Measurement counts do not exceed total readings":
            result.measurement_count_exceeds_total,
        "Production counts do not exceed total readings":
            result.production_count_exceeds_total,
    }

    failures = {}

    for name, count in checks.items():
        if count > 0:
            print(f"FAIL: {name} ({count} rows)")
            failures[name] = count
        else:
            print(f"PASS: {name}")

    # Report expected NULL averages.
    if result.expected_null_measured > 0:
        print(
            "WARNING: "
            f"{result.expected_null_measured} hourly rows "
            "have NULL measured utilization because "
            "all readings were excluded by the mart filter."
        )

    if result.expected_null_production > 0:
        print(
            "WARNING: "
            f"{result.expected_null_production} hourly rows "
            "have NULL production utilization because "
            "all readings were excluded by the mart filter."
        )

    # Fail clearly if any validation check failed.
    if failures:
        details = ", ".join(
            f"{name}: {count}"
            for name, count in failures.items()
        )

        raise RuntimeError(
            f"Validation failed: {details}"
        )

    print(
        f"\nSUCCESS: All Power Trends validations passed "
        f"({row_count} rows checked)."
    )

    return True


if __name__ == "__main__":
    run_validation()
