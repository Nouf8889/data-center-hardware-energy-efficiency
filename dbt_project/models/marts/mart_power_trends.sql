{{ config(materialized='view') }}

WITH source_data AS (

    SELECT
        cell,
        pdu,
        hours_from_start,
        measured_power_util,
        production_power_util,
        bad_measurement_data,
        bad_production_power_data
    FROM {{ ref('stg_google_power_cella_pdu10') }}

),

hourly_trends AS (

    SELECT
        cell,
        pdu,
        CAST(FLOOR(hours_from_start) AS INT64) AS hour_bucket,

        COUNT(*) AS total_readings,

        COUNTIF(bad_measurement_data = TRUE)
            AS bad_measurement_count,

        COUNTIF(bad_production_power_data = TRUE)
            AS bad_production_count,

        AVG(
            IF(
                bad_measurement_data = FALSE,
                measured_power_util,
                NULL
            )
        ) AS avg_measured_power_util,

        AVG(
            IF(
                bad_production_power_data = FALSE,
                production_power_util,
                NULL
            )
        ) AS avg_production_power_util

    FROM source_data

    GROUP BY
        cell,
        pdu,
        hour_bucket

)

SELECT *
FROM hourly_trends
