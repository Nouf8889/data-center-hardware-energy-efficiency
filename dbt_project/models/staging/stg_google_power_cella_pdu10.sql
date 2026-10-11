with source_data as (

    select *
    from {{ source('raw_data', 'google_power_cella_pdu10_cleaned') }}

)

select *
from source_data
