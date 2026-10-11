
with source_data as (

    select *
    from {{ source('raw_data', 'specpower_energy') }}

)

select *
from source_data
