{{ config(
    materialized='incremental',
    unique_key='repayment_id'
) }}

select
    repayment_id,
    loan_id,
    payment_timestamp,
    amount,
    status as repayment_status
from {{ ref('stg_repayments') }}

{% if is_incremental() %}
    where payment_timestamp > (select coalesce(max(payment_timestamp), cast('1900-01-01' as timestamp)) from {{ this }})
{% endif %}