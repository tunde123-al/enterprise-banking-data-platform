{{ config(materialized='table') }}

with txns as (
    select * from {{ ref('stg_transactions') }}
),

accounts as (
    select * from {{ ref('stg_accounts') }}
),

flagged_txns as (
    select
        t.transaction_id,
        t.account_id,
        a.customer_id,
        t.amount,
        t.transaction_type,
        t.transaction_timestamp,
        case
            when t.amount >= 10000 then 0.90
            when t.amount >= 5000 then 0.65
            when t.transaction_type = 'withdrawal' and t.amount >= 3000 then 0.50
            else 0.10
        end as fraud_score
    from txns t
    join accounts a on t.account_id = a.account_id
)

select
    transaction_id,
    account_id,
    customer_id,
    amount,
    transaction_type,
    transaction_timestamp,
    fraud_score,
    case
        when fraud_score >= 0.70 then 'HIGH_ALERT'
        when fraud_score >= 0.40 then 'MEDIUM_ALERT'
        else 'LOW_RISK'
    end as risk_band
from flagged_txns
where fraud_score >= 0.40
