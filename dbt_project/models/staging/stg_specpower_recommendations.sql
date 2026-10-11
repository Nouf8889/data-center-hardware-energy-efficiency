
with source_data as (

    select *
    from {{ source('raw_data', 'specpower_recommendations') }}

)

select *
from source_data
