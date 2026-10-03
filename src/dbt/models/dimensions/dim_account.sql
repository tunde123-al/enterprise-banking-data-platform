{{ config(materialized='table') }}

select
    account_id,
    customer_id,
    account_number,
    account_type,
    currency,
    opened_date,
    closed_date,
    status as account_status
from {{ ref('stg_accounts') }}
