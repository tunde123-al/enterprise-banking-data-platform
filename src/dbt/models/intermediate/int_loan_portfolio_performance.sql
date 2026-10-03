{{ config(materialized='view') }}

with loans as (
    select * from {{ ref('stg_loans') }}
)

select
    loan_type,
    count(loan_id) as total_loan_count,
    sum(principal_amount) as total_principal_issued,
    avg(interest_rate) as average_interest_rate,
    sum(case when status = 'active' then principal_amount else 0 end) as active_principal_balance,
    sum(case when status = 'defaulted' then 1 else 0 end) as defaulted_loans_count
from loans
group by loan_type
