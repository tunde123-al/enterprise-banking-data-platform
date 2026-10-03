# Enterprise Banking Data & Analytics Platform

> **Status: implementation-ready portfolio project.** Private, synthetic-data-only repository.
> The full Phase 0 architecture & requirements baseline, source-system layer, orchestration,
> lakehouse, warehouse, analytics-engineering, BI and operational assets are implemented.
> This is **not** an assertion of production banking compliance.

A governed Azure lakehouse design for **Fraud Risk, Credit Risk, AML Monitoring,
Customer 360, and Executive Banking Analytics**. Every technology has one justified
responsibility (see the [technology responsibility matrix](docs/requirements/system-requirements-specification.md)).

## Documentation map

| Area | Where |
| --- | --- |
| Architecture (enterprise → deployment/recovery) | [`docs/architecture`](docs/architecture) |
| Requirements (SRS, business, functional, NFR, data, integration, security) | [`docs/requirements`](docs/requirements) |
| Data models (conceptual, logical, physical, dictionary, lineage) | [`docs/data`](docs/data) |
| Architecture Decision Records ADR-001…010 | [`docs/decisions`](docs/decisions) |
| Diagrams (Mermaid + draw.io XML for 15 views) | [`docs/diagrams`](docs/diagrams) |
| Operations (monitoring, backup/recovery, runbook) | [`docs/operations`](docs/operations) |
| Phase 1 source models (DDL, source→Bronze mapping, DQ rules) | [`docs/phase1-data-models`](docs/phase1-data-models) |

## Repository layout

```
src/
  data_generation/    Deterministic synthetic generators, loaders, DQ validation, init DDL
  ingestion/          Airflow DAGs + Azure Data Factory pipeline definitions
  databricks/         PySpark/Delta notebooks + job definitions (Bronze→Silver→Gold, risk engines)
  dbt/                Serving-layer marts, dims, facts, tests, docs
  synapse/            Dedicated SQL pool DDL, views and warehouse-load pipeline
  power_bi/           DAX measures, RLS roles, Python visuals
  microservices/      FastAPI operational microservice (synthetic event API)
infrastructure/       ARM templates (foundation deployment)
tests/                Unit + wiring tests
```

## Quickstart (local, synthetic)

```bash
# 1) Source systems + Airflow + FastAPI
docker compose up -d

# 2) Generate and validate synthetic data
python -m src.data_generation.generate_all --scale 0.1 --output-dir data/generated
python -m src.data_generation.validate_data --data-dir data/generated

# 3) Load the source systems (see .env.example for connection variables)
python -m src.data_generation.load_to_postgres --data-dir data/generated
python -m src.data_generation.load_to_oracle
python -m src.data_generation.load_to_sqlserver
python -m src.data_generation.load_to_mongodb
python -m src.data_generation.load_to_cassandra

# 4) Run the pipeline end-to-end
#    Airflow UI: http://localhost:8080 (admin/admin) - master_banking_orchestration_dag
#    Databricks: deploy src/databricks/jobs/*.json (ETL + analytics)
#    dbt:        cd src/dbt && dbt build --target synapse
```

See the [runbook](docs/operations/runbook.md) for the full walk-through.

## Guardrails

- Synthetic data only; never commit credentials, production extracts, API keys, or connection strings.
- The repository is intended to remain a **private** GitHub repository.
- `.env.example` contains names and dev-only Docker placeholders; real secrets belong in
  Azure Key Vault / the Airflow secrets backend in a deployed environment.

## CI

`.github/workflows/ci.yml` compiles all Python, validates JSON definitions, runs the unit +
wiring test suite, and executes a small-scale end-to-end generation + DQ run.

## Delivery roadmap (status)

| Phase | Status |
| --- | --- |
| 0 Architecture and requirements | ✅ Complete (architecture, SRS, 15 diagrams, ADRs) |
| 1 Source systems and data model | ✅ Complete (DDL for all 6 sources, source→Bronze mapping) |
| 2 Data generation | ✅ Complete (11 datasets, deterministic, validated) |
| 3 PostgreSQL/Oracle/SQL Server/MongoDB/Cassandra | ✅ Loaders, init schemas, Docker stack |
| 4 Airflow + ADF | ✅ DAGs and ADF pipeline definitions |
| 5 Azure Storage / ADLS | ✅ ARM foundation templates + environment config |
| 6 Databricks + PySpark + Delta Lake | ✅ Notebooks and job definitions for all entities |
| 7 Synapse / Azure Warehouse | ✅ SQL pool DDL, views, warehouse-load pipeline |
| 8 dbt | ✅ Profiles, staging/intermediate/dims/facts/marts, tests |
| 9 Power BI | ✅ DAX measures, RLS roles, Python visuals, semantic model |
| 10 Fraud / Credit / AML / Customer 360 | ✅ Gold engines + marts per use case |
| 11 Security / governance / monitoring | ✅ Documented architecture + operations |
| 12 Testing and hardening | ✅ Unit, wiring, DQ validation, CI workflow |
| 13 Portfolio documentation | ✅ README, runbook, diagram catalogue, phase-1 docs |
