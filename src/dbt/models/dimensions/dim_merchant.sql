{{ config(materialized='table') }}

select
    merchant_id,
    merchant_name,
    merchant_code,
    category_code,
    category_name,
    city,
    country
from {{ ref('stg_merchants') }}