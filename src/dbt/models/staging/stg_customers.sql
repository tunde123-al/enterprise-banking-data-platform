{{ config(materialized='view') }}

with source_data as (
    select
        cast(customer_id as varchar(32)) as customer_id,
        trim(first_name) as first_name,
        trim(last_name) as last_name,
        lower(trim(email)) as email,
        phone,
        upper(coalesce(kyc_tier, 'TIER_1')) as kyc_tier,
        upper(coalesce(status, 'ACTIVE')) as status,
        upper(country) as country,
        cast(created_date as date) as created_date
    from {{ source('lakehouse_silver', 'customers') }}
)

select * from source_data
