
{{ config(materialized='view') }}

with source_data as (

    select *
    from {{ ref('stg_aws_ec2_pricing') }}

),

cloud_cost as (

    select
        instance_type,
        instance_family,
        vcpu,
        memory_gb,
        physical_processor,
        processor_architecture,
        region,
        operating_system,
        tenancy,
        pricing_type,

        hourly_price_usd,
        monthly_price_usd,
        annual_price_usd,

        safe_divide(hourly_price_usd, vcpu)
            as hourly_cost_per_vcpu_usd,

        safe_divide(hourly_price_usd, memory_gb)
            as hourly_cost_per_gb_memory_usd

    from source_data

)

select *
from cloud_cost
