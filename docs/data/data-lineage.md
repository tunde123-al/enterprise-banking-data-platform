# Data lineage

Lineage is recorded at dataset and run level: source object → landing file/manifest → Bronze Delta → Silver Delta → Gold product → dbt/Synapse mart → Power BI semantic table/measure. Each run emits batch ID, source watermark, record counts, rejection count, quality result, code/version identifier, and timestamp.

Example: `postgres.transactions` → `bronze.transactions` → `silver.transaction` → `gold_fraud_transaction_score` → `mart.fact_fraud_event` → Power BI “Fraud Operations” report. Data stewards approve definitions; engineers own technical lineage; BI owners own measure/report lineage.
