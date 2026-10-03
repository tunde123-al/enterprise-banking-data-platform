{{ config(
    materialized='incremental',
    unique_key='loan_id'
) }}

select
    loan_id,
    customer_id,
    account_id,
    branch_id,
    loan_type,
    principal_amount,
    interest_rate,
    current_balance,
    term_months,
    origination_date,
    maturity_date,
    status as loan_status,
    risk_rating
from {{ ref('stg_loans') }}

{% if is_incremental() %}
    where origination_date > (select coalesce(max(origination_date), cast('1900-01-01' as date)) from {{ this }})
{% endif %}