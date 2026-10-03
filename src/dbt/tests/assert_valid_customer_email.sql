-- Test: Customers must have non-empty valid email formatting
select
    customer_id,
    email
from {{ ref('stg_customers') }}
where email is null or email not like '%@%.%'
