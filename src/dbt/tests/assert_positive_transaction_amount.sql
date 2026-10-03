-- Test: Transaction amounts must always be strictly greater than zero
select
    transaction_id,
    amount
from {{ ref('stg_transactions') }}
where amount <= 0
