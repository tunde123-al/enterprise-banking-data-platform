{{ config(materialized='view') }}

with source_data as (
    select
        cast(account_id as varchar(32)) as account_id,
        cast(customer_id as varchar(32)) as customer_id,
        cast(branch_code as varchar(32)) as branch_code,
        account_number,
        lower(account_type) as account_type,
        currency,
        cast(balance as decimal(18,2)) as balance,
        cast(available_balance as decimal(18,2)) as available_balance,
        cast(opened_date as date) as opened_date,
        cast(closed_date as date) as closed_date,
        lower(status) as status
    from {{ source('lakehouse_silver', 'accounts') }}
)

select * from source_data
