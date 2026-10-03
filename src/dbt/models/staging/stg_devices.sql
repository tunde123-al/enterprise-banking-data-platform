{{ config(materialized='view') }}

with source_data as (
    select
        cast(device_id as varchar(32)) as device_id,
        cast(customer_id as varchar(32)) as customer_id,
        upper(trim(platform)) as platform,
        cast(risk_score as decimal(6,4)) as risk_score,
        trusted
    from {{ source('lakehouse_silver', 'devices') }}
)

select * from source_data