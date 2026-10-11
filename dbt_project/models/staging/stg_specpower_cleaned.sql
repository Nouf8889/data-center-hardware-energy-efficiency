{{ config(materialized='view') }}

with source_data as (

    select *
    from {{ source('raw_data', 'specpower_cleaned') }}

)

select *
from source_data
