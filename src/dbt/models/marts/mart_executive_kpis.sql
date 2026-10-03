{{ config(materialized='table') }}

-- Executive banking KPIs by geography, KYC tier and wealth segment.
with customer_marts as (
    select * from {{ ref('mart_customer_360') }}
),
account_summaries as (
    select * from {{ ref('int_customer_transactions_summary') }}
),
loans as (
    select * from {{ ref('stg_loans') }}
),
loan_rollup as (
    select
        customer_id,
        count(loan_id) as total_loans,
        sum(principal_amount) as total_loan_principal
    from loans
    group by customer_id
)

select
    c.country,
    c.kyc_tier,
    c.wealth_segment,
    count(distinct c.customer_id) as customer_count,
    sum(c.total_deposit_balance) as total_deposits,
    avg(c.total_deposit_balance) as average_deposits_per_customer,
    sum(coalesce(a.total_volume, 0)) as total_transaction_volume,
    sum(coalesce(a.total_transactions, 0)) as total_transaction_count,
    sum(coalesce(l.total_loans, 0)) as total_loans,
    sum(coalesce(l.total_loan_principal, 0)) as total_loan_principal,
    current_date as metric_calculation_date
from customer_marts c
left join account_summaries a on c.customer_id = a.customer_id
left join loan_rollup l on c.customer_id = l.customer_id
group by
    c.country,
    c.kyc_tier,
    c.wealth_segment
