with source_data as (

select *
from {{ source('raw_data', 'aws_ec2_pricing_cleaned') }}

)

select *
from source_data
