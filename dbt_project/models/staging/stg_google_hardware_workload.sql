
with source_data as (

    select *
    from {{ source('raw_data', 'google_hardware_workload_joined') }}

)

select *
from source_data
