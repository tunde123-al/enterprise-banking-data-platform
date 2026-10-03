{{ config(materialized='table') }}

-- Card dimension. Only the masked PAN and last four digits are exposed to BI;
-- full PANs never leave the card systems, per the security architecture.
select
    card_id,
    customer_id,
    card_type,
    card_status,
    right(masked_pan, 4) as masked_pan_last4
from {{ ref('stg_cards') }}