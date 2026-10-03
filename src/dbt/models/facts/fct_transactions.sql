{{ config(
    materialized='incremental',
    unique_key='transaction_id'
) }}

select
    transaction_id,
    account_id,
    merchant_id,
    transaction_reference,
    amount,
    currency,
    transaction_type,
    transaction_category,
    transaction_timestamp,
    balance_after,
    status as transaction_status,
    fee
from {{ ref('stg_transactions') }}

{% if is_incremental() %}
    where transaction_timestamp > (select max(transaction_timestamp) from {{ this }})
{% endif %}
