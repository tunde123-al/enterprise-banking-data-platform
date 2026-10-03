{{ config(materialized='view') }}

with source_data as (
    select
        cast(loan_id as varchar(32)) as loan_id,
        cast(customer_id as varchar(32)) as customer_id,
        cast(account_id as varchar(32)) as account_id,
        cast(branch_id as varchar(32)) as branch_id,
        lower(loan_type) as loan_type,
        cast(principal_amount as decimal(18,2)) as principal_amount,
        cast(interest_rate as decimal(5,4)) as interest_rate,
        cast(current_balance as decimal(18,2)) as current_balance,
        cast(term_months as int) as term_months,
        cast(origination_date as date) as origination_date,
        cast(maturity_date as date) as maturity_date,
        lower(status) as status,
        upper(risk_rating) as risk_rating
    from {{ source('lakehouse_silver', 'loans') }}
)

select * from source_data
