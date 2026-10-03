# Data pipeline runbook

## 1. Before you start
- Confirm the repository is on the expected Git revision and the environment file is loaded:
  `set -a; source .env; set +a` (Windows PowerShell: environment comes from the IDE / `docker compose`).
- Confirm local source databases are healthy: `docker compose ps` (repository root).

## 2. Local end-to-end demonstration (synthetic)
```bash
# 1) Start source systems (PostgreSQL, Oracle Free, SQL Server, MongoDB, Cassandra)
docker compose up -d

# 2) Generate deterministic synthetic data (scale 0.1 = ~10%, 1.0 = full volumes)
python -m src.data_generation.generate_all --scale 0.1 --output-dir data/generated

# 3) Validate referential integrity and domain rules
python -m src.data_generation.validate_data --data-dir data/generated

# 4) Load each source system (loaders read connection vars from the environment)
python -m src.data_generation.load_to_postgres --data-dir data/generated
python -m src.data_generation.load_to_oracle
python -m src.data_generation.load_to_sqlserver
python -m src.data_generation.load_to_mongodb
python -m src.data_generation.load_to_cassandra

# 5) Airflow orchestration (web UI on http://localhost:8080, admin/admin)
docker compose up -d airflow
#    Enable and trigger: master_banking_orchestration_dag,
#    mongodb_interactions_ingestion_dag, cassandra_events_ingestion_dag

# 6) Databricks lakehouse (in Databricks, run the ETL and analytics jobs defined in
#    src/databricks/jobs) or locally with Spark/Delta:
python src/databricks/notebooks/1_bronze_to_silver.py data/generated data/lakehouse/silver
python src/databricks/notebooks/2_silver_to_gold.py data/lakehouse/silver data/lakehouse/gold

# 7) dbt serving marts (requires SYNAPSE_* environment variables)
cd src/dbt && dbt build --target synapse
```

## 3. Failure classification and recovery

| Class | Examples | Action |
| --- | --- | --- |
| Transient infrastructure | connection refused, timeout, 5xx, cluster unavailable | Retry with backoff (3 attempts), then re-run the batch from the recorded watermark |
| Source availability | database down during a run | Fix source, retry idempotently (ingestion is watermark-incremental) |
| Schema/contract | unexpected column, type change, missing required column | Quarantine batch; notify data owner; update contract + code under review |
| Data quality gate | DQ rule failure, reconciliation mismatch | Quarantine; do not bypass the gate; correct generator/transformation and rerun |
| Transformation defect | wrong metric after code change | Fix under review, rerun idempotent batch; for corrected Delta gold tables rebuild affected products (`DeltaTable` overwrite/version rollback) |

Process:
1. Check the monitoring view for the failed run ID, stage, error, record counts, and source watermark.
2. Classify the failure (table above).
3. Retry only transient failures. For quality/schema failures, quarantine and notify the data owner.
4. Correct configuration/code under review, then rerun the idempotent batch from the recorded watermark.
5. Reconcile source/target counts, quality result, Gold outputs, and Power BI refresh timestamp; record resolution.

## 4. FastAPI microservice
```bash
# Local run
uvicorn src.microservices.fastapi_app.main:app --reload --port 8000
# Health check
curl http://localhost:8000/health
# Synthetic transaction event (mock balances only)
curl -X POST http://localhost:8000/transactions/ \
  -H "Content-Type: application/json" \
  -d '{"account_id":"ACC00000001","amount":250.0,"transaction_type":"withdrawal","channel":"online"}'
```

## 5. Power BI
1. Refresh imports after a successful dbt build.
2. Validate the five marts (`mart_executive_kpis`, `mart_fraud_monitoring`, `mart_aml_monitoring`, `mart_credit_risk`, `mart_customer_360`) and their views.
3. Verify RLS personas (`branch_manager@example.test`, `aml_officer@example.test`, `retail_exec@example.test`).

## 6. Security incident notes
Escalate suspected credential exposure immediately: revoke/rotate through the platform owner and remove the secret from all logs/history using the organisation's incident process.
