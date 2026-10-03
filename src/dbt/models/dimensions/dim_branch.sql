{{ config(materialized='table') }}

-- Branch dimension derived from the branch codes present on accounts.
with branches as (
    select distinct branch_code
    from {{ ref('stg_accounts') }}
    where branch_code is not null
)

select
    branch_code as branch_id,
    branch_code,
    concat('Branch ', branch_code) as branch_name
from branches