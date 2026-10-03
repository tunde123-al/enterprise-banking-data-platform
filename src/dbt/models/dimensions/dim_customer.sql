{{ config(materialized='table') }}

select
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    kyc_tier,
    status as customer_status,
    country,
    created_date
from {{ ref('stg_customers') }}
