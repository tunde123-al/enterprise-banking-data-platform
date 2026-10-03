{{ config(materialized='view') }}

with source_data as (
    select
        cast(transaction_id as varchar(64)) as transaction_id,
        cast(account_id as varchar(32)) as account_id,
        cast(merchant_id as varchar(32)) as merchant_id,
        transaction_reference,
        cast(amount as decimal(18,2)) as amount,
        currency,
        lower(transaction_type) as transaction_type,
        lower(transaction_category) as transaction_category,
        cast(transaction_date as timestamp) as transaction_timestamp,
        cast(balance_after as decimal(18,2)) as balance_after,
        lower(status) as status,
        cast(coalesce(fee, 0.0) as decimal(10,2)) as fee
    from {{ source('lakehouse_silver', 'transactions') }}
)

select * from source_data
