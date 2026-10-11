
{{ config(materialized='table') }}

SELECT
    hardware_vendor,
    system_enclosure,
    server_model,
    cpu_model,
    cpu_description,
    cpu_mhz,
    cpu_chips,
    cpu_cores,
    cpu_threads,
    total_memory_gb,
    nodes,
    ssj_ops_100,
    avg_watts_100,
    avg_watts_idle,
    ssj_ops_per_watt,
    efficiency_100
FROM {{ ref('stg_specpower_energy') }}
