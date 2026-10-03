{{ config(materialized='table') }}

with loans as (
    select * from {{ ref('stg_loans') }}
),

customers as (
    select * from {{ ref('mart_customer_360') }}
)

select
    l.loan_id,
    l.customer_id,
    concat(c.first_name, ' ', c.last_name) as customer_name,
    c.wealth_segment,
    l.loan_type,
    l.principal_amount,
    l.interest_rate,
    l.term_months,
    l.status as loan_status,
    l.risk_rating,
    c.total_deposit_balance,
    round(
        l.principal_amount / (case when c.total_deposit_balance > 0 then c.total_deposit_balance else 1.0 end),
        2
    ) as debt_to_deposit_ratio,
    case
        when l.status = 'defaulted' then 'DEFAULT'
        when (l.principal_amount / (case when c.total_deposit_balance > 0 then c.total_deposit_balance else 1.0 end)) > 5.0 then 'HIGH_RISK_CCC'
        when (l.principal_amount / (case when c.total_deposit_balance > 0 then c.total_deposit_balance else 1.0 end)) > 2.0 then 'MODERATE_RISK_BBB'
        else 'LOW_RISK_AAA'
    end as risk_rating_band
from loans l
left join customers c on l.customer_id = c.customer_id
