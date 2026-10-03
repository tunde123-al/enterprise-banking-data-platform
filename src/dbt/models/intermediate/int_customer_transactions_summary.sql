{{ config(materialized='view') }}

with accounts as (
    select * from {{ ref('stg_accounts') }}
),

transactions as (
    select * from {{ ref('stg_transactions') }}
),

account_aggregations as (
    select
        t.account_id,
        count(t.transaction_id) as total_transactions,
        sum(case when t.transaction_type = 'deposit' then t.amount else 0 end) as total_deposits,
        sum(case when t.transaction_type != 'deposit' then t.amount else 0 end) as total_withdrawals,
        sum(t.amount) as total_volume,
        avg(t.amount) as avg_transaction_amount,
        max(t.transaction_timestamp) as last_transaction_at
    from transactions t
    group by t.account_id
),

joined as (
    select
        a.account_id,
        a.customer_id,
        a.account_type,
        a.balance,
        coalesce(agg.total_transactions, 0) as total_transactions,
        coalesce(agg.total_deposits, 0) as total_deposits,
        coalesce(agg.total_withdrawals, 0) as total_withdrawals,
        coalesce(agg.total_volume, 0) as total_volume,
        coalesce(agg.avg_transaction_amount, 0) as avg_transaction_amount,
        agg.last_transaction_at
    from accounts a
    left join account_aggregations agg on a.account_id = agg.account_id
)

select * from joined
