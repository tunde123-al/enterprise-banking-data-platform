{{ config(materialized='table') }}

with customers as (
    select * from {{ ref('stg_customers') }}
),

account_summaries as (
    select * from {{ ref('int_customer_transactions_summary') }}
),

customer_rollup as (
    select
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email,
        c.kyc_tier,
        c.status,
        c.country,
        c.created_date,
        count(distinct a.account_id) as total_accounts,
        coalesce(sum(a.balance), 0) as total_deposit_balance,
        coalesce(sum(a.total_volume), 0) as lifetime_transaction_volume,
        coalesce(sum(a.total_transactions), 0) as lifetime_transaction_count,
        max(a.last_transaction_at) as last_seen_at
    from customers c
    left join account_summaries a on c.customer_id = a.customer_id
    group by
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email,
        c.kyc_tier,
        c.status,
        c.country,
        c.created_date
)

select
    *,
    case
        when total_deposit_balance >= 100000 then 'TIER_1_PRIVATE_WEALTH'
        when total_deposit_balance >= 25000 then 'TIER_2_AFFLUENT'
        when total_deposit_balance >= 5000 then 'TIER_3_MASS_AFFLUENT'
        else 'TIER_4_RETAIL'
    end as wealth_segment
from customer_rollup
