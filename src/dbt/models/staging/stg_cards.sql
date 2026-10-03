{{ config(materialized='view') }}

with source_data as (
    select
        cast(card_id as varchar(32)) as card_id,
        cast(customer_id as varchar(32)) as customer_id,
        masked_pan,
        upper(trim(card_type)) as card_type,
        upper(trim(status)) as card_status
    from {{ source('lakehouse_silver', 'cards') }}
)

select * from source_data