{{ config(materialized='view') }}

with source_data as (
    select
        cast(merchant_id as varchar(32)) as merchant_id,
        merchant_name,
        merchant_code,
        category_code,
        category_name,
        city,
        upper(country) as country
    from {{ source('lakehouse_silver', 'merchants') }}
)

select * from source_data