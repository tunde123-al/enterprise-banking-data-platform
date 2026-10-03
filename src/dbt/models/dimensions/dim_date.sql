{{ config(materialized='table') }}

-- Conformed date dimension (2020-01-01 .. 2026-12-31) built from a
-- portable digit cross-join so no seed table is required in Synapse.
with digits as (
    select 0 as digit union all select 1 union all select 2 union all select 3
    union all select 4 union all select 5 union all select 6 union all select 7
    union all select 8 union all select 9
),
numbers as (
    select row_number() over (order by (select 0)) - 1 as n
    from digits a
    cross join digits b
    cross join digits c
    cross join digits d
),
date_spine as (
    select dateadd(day, n, cast('2020-01-01' as date)) as full_date
    from numbers
    where n <= datediff(day, cast('2020-01-01' as date), cast('2026-12-31' as date))
)

select
    cast(convert(varchar(8), full_date, 112) as int) as date_key,
    full_date,
    datepart(weekday, full_date) as day_of_week,
    datename(weekday, full_date) as day_name,
    datepart(day, full_date) as day_of_month,
    datepart(month, full_date) as month_number,
    datename(month, full_date) as month_name,
    datepart(quarter, full_date) as calendar_quarter,
    datepart(year, full_date) as calendar_year,
    case when datepart(weekday, full_date) in (1, 7) then 1 else 0 end as is_weekend
from date_spine