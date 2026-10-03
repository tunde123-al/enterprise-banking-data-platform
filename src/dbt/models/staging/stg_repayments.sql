{{ config(materialized='view') }}

with source_data as (
    select
        cast(repayment_id as varchar(32)) as repayment_id,
        cast(loan_id as varchar(32)) as loan_id,
        cast(payment_ts as timestamp) as payment_timestamp,
        cast(amount as decimal(18,2)) as amount,
        upper(trim(status)) as status
    from {{ source('lakehouse_silver', 'repayments') }}
)

select * from source_data