
with source_data as (

    select *
    from {{ source('raw_data', 'google_machine_hardware_cleaned') }}

)

select *
from source_data
