
{{ config(materialized='view') }}

with hardware_workload as (

    select *
    from {{ ref('stg_google_hardware_workload') }}

),

final as (

    select
        machine_id,
        platform_id,
        start_time,
        end_time,
        event_time,
        duration_minutes,
        avg_cpu_usage,
        avg_memory_usage,
        cpu_capacity,
        memory_capacity,
        cpu_to_capacity_ratio,
        memory_to_capacity_ratio
    from hardware_workload

)

select *
from final
