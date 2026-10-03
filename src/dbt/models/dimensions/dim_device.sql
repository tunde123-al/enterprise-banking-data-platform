{{ config(materialized='table') }}

select
    device_id,
    customer_id,
    platform,
    risk_score,
    trusted
from {{ ref('stg_devices') }}