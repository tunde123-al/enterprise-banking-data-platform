{{ config(materialized='table') }}

-- AML monitoring mart: rule-based suspicious activity candidates for the
-- compliance dashboard. Mirrors the PySpark engine in the Databricks job.
with txns as (
    select * from {{ ref('stg_transactions') }}
),
structuring as (
    select
        transaction_id,
        account_id,
        amount,
        transaction_timestamp,
        'STRUCTURING_SUB_10K' as aml_rule,
        0.85 as risk_score
    from txns
    where amount >= 8500 and amount < 10000
),
high_value as (
    select
        transaction_id,
        account_id,
        amount,
        transaction_timestamp,
        'HIGH_VALUE_CTR' as aml_rule,
        0.70 as risk_score
    from txns
    where amount >= 25000
),
rapid_movement as (
    select
        transaction_id,
        account_id,
        amount,
        transaction_timestamp,
        'RAPID_CASH_MOVEMENT' as aml_rule,
        0.75 as risk_score
    from (
        select
            transaction_id,
            account_id,
            amount,
            transaction_timestamp,
            sum(case when transaction_type = 'withdrawal' and amount >= 3000 then 1 else 0 end)
                over (partition by account_id, cast(transaction_timestamp as date)) as daily_heavy_withdrawals
        from txns
    ) scored
    where daily_heavy_withdrawals >= 3
),
all_alerts as (
    select * from structuring
    union all
    select * from high_value
    union all
    select * from rapid_movement
)

select distinct
    concat('AML-', transaction_id) as aml_alert_id,
    transaction_id,
    account_id,
    amount,
    transaction_timestamp,
    aml_rule,
    risk_score,
    case when risk_score >= 0.80 then 1 else 0 end as sar_recommended,
    cast(transaction_timestamp as date) as flagged_date
from all_alerts