SELECT
    cell,
    pdu,
    hour_bucket,
    total_readings,
    bad_production_count,
    avg_production_power_util
FROM {{ ref('mart_power_trends') }}
WHERE
    (
        bad_production_count = total_readings
        AND avg_production_power_util IS NOT NULL
    )
    OR
    (
        bad_production_count < total_readings
        AND avg_production_power_util IS NULL
    )
