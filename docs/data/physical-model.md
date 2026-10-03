# Physical model

The serving schema is a star model: `fact_transaction`, `fact_loan_snapshot`, `fact_repayment`, `fact_fraud_event`, `fact_aml_alert`, `fact_customer_interaction`; dimensions `dim_customer`, `dim_account`, `dim_card`, `dim_merchant`, `dim_branch`, `dim_date`, and `dim_device`. Delta Bronze/Silver tables use natural/source keys plus technical audit columns; Gold/Synapse facts use surrogate dimension keys.

Required technical columns: `source_system VARCHAR`, `ingest_batch_id VARCHAR`, `ingested_at_utc TIMESTAMP`, `record_hash VARCHAR`, `quality_status VARCHAR`, `lineage_run_id VARCHAR`. Use DECIMAL for monetary amounts, UTC timestamps, string ISO currency/country codes, and never persist raw card PAN/CVV. Database-specific DDL remains a later implementation artifact and must conform to this model.
