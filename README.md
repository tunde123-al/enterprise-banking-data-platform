# Enterprise Banking Data & Analytics Platform

A portfolio project by **Tunde Shiyanbade**: the design and code for a governed Azure
lakehouse serving **Fraud Risk, Credit Risk, AML Monitoring, Customer 360 and Executive
Banking Analytics**, built entirely on synthetic data.

> **What this is.** A local, runnable source-system layer (synthetic data generators,
> data-quality validation, database loaders, a FastAPI service) plus the code and
> definitions for the cloud layers (Airflow, Azure Data Factory, Databricks, Synapse, dbt,
> Power BI) and a full architecture and requirements document set.
>
> **What this is not.** Nothing here has been deployed to Azure, and it is not a claim of
> production banking compliance. See [Implementation status](#implementation-status) for
> exactly what has been run and what is code or design only.

## Implementation status

Terms used below:

- **Runs locally, tested** – executed on a developer machine and covered by the test suite.
- **Runs locally** – executed end to end on a developer machine; no automated test.
- **Code written, not executed** – the code or definition exists and is syntax-checked, but has not been run against its target platform from this repository.
- **Design** – documentation or diagrams only.

| Area | Status | Notes |
| --- | --- | --- |
| Synthetic data generation (11 datasets, deterministic seed) | Runs locally, tested | `src/data_generation/generate_all.py`; smoke-tested in `tests/` and CI |
| Data-quality validation | Runs locally | `validate_data.py` checks customers, accounts and transactions; the other eight datasets are not yet validated |
| FastAPI transaction service | Runs locally, tested | In-memory mock balances; simulates an operational API, no database behind it |
| PostgreSQL load | Runs locally | Docker container + `load_to_postgres.py`, verified with 1,000,000 transactions at scale 0.1 |
| MongoDB load | Runs locally | Docker container + `load_to_mongodb.py`, verified with 100,000 interactions |
| Oracle, SQL Server, Cassandra, Azure SQL loads | Code written, not executed | Init scripts and loaders exist; not verified end to end |
| Airflow DAGs | Code written, not executed | Three DAGs; Python syntax is checked, the DAGs have not been run |
| Azure Data Factory pipelines | Code written, not executed | JSON definitions, validated as JSON only |
| Databricks notebooks and jobs (Bronze → Silver → Gold, fraud, credit, AML, Customer 360) | Code written, not executed | PySpark/Delta code and job JSON; not run on a cluster |
| Synapse dedicated SQL pool (DDL, views, load pipeline) | Code written, not executed | Not deployed |
| dbt project (staging, intermediate, dimensions, facts, marts) | Code written, not executed | `ref`/`source` wiring is tested; `dbt build` has not been run against a warehouse |
| Power BI | Code written, not executed | DAX measures, RLS roles and two Python visual scripts; there is no `.pbix` file |
| Azure infrastructure | Code written, not executed | One ARM template (storage, Key Vault, Data Factory, Synapse); not deployed. Terraform is not implemented |
| Architecture, requirements, data models, ADRs, runbook, diagrams | Design | `docs/` and `DIAGRAM/` |
| CI | Workflow defined | GitHub Actions: compiles Python, parses JSON, runs the tests, generates and validates a small dataset |

## Documentation map

| Area | Where |
| --- | --- |
| Architecture (enterprise → deployment/recovery) | [`docs/architecture`](docs/architecture) |
| Requirements (SRS, business, functional, NFR, data, integration, security) | [`docs/requirements`](docs/requirements) |
| Data models (conceptual, logical, physical, dictionary, lineage) | [`docs/data`](docs/data) |
| Architecture Decision Records ADR-001…010 | [`docs/decisions`](docs/decisions) |
| Editable diagrams (Mermaid + draw.io XML for 15 views) | [`docs/diagrams`](docs/diagrams) |
| Presentation diagrams (rendered SVG + detailed Mermaid) | [`DIAGRAM`](DIAGRAM) |
| Operations (monitoring, backup/recovery, runbook) | [`docs/operations`](docs/operations) |
| Phase 1 source models (design DDL, source→Bronze mapping, DQ rules) | [`docs/phase1-data-models`](docs/phase1-data-models) |
| Infrastructure notes | [`infrastructure`](infrastructure) |

Every technology has one justified responsibility; see the
[technology responsibility matrix](docs/requirements/system-requirements-specification.md).

## Repository layout

```
src/
  data_generation/    Deterministic synthetic generators, loaders, DQ validation, database init scripts
  ingestion/          Airflow DAGs + Azure Data Factory pipeline definitions
  databricks/         PySpark/Delta notebooks + job definitions (Bronze→Silver→Gold, risk engines)
  dbt/                Serving-layer staging, dimensions, facts, marts, tests
  synapse/            Dedicated SQL pool DDL, views and warehouse-load pipeline
  power_bi/           DAX measures, RLS roles, Python visuals
  microservices/      FastAPI operational microservice (synthetic event API)
infrastructure/       ARM template (foundation resources)
docs/                 Architecture, requirements, data models, decisions, operations, diagrams
DIAGRAM/              Presentation-ready architecture diagrams
tests/                Unit + project-wiring tests
```

## Quickstart (local, synthetic)

Requires Python 3.10+ and, for the databases, Docker.

```bash
# 1) Install (core + test tooling; add the loader drivers for step 4)
pip install -e ".[dev,loaders]"

# 2) Generate and validate synthetic data
python -m src.data_generation.generate_all --scale 0.1 --output-dir data/generated
python -m src.data_generation.validate_data --data-dir data/generated

# 3) Run the API  ->  http://localhost:8000/docs
uvicorn src.microservices.fastapi_app.main:app --port 8000

# 4) Start source databases and load them
cp .env.example .env          # then set the three *_PASSWORD values
docker compose up -d postgres mongodb
set -a; source .env; set +a   # export the connection variables for the loaders
python -m src.data_generation.load_to_postgres --data-dir data/generated
python -m src.data_generation.load_to_mongodb

# 5) Tests
python -m pytest -q
```

`docker compose up -d` starts the whole stack (PostgreSQL, Oracle Free, SQL Server, MongoDB,
Cassandra, Airflow, the API). The full stack did not fit on an 8 GB development machine;
the subset above does. The Oracle, SQL Server and Cassandra loaders
(`load_to_oracle`, `load_to_sqlserver`, `load_to_cassandra`) exist but have not been
verified end to end.

The cloud layers need your own Azure subscription, Databricks workspace and Synapse pool;
the [runbook](docs/operations/runbook.md) describes the intended sequence.

## Guardrails

- Synthetic data only; never commit credentials, production extracts, API keys, or connection strings.
- `.env.example` documents variable names with placeholders only. Real values live in an
  untracked `.env` locally, and in Azure Key Vault / the Airflow secrets backend in a
  deployed environment.

## CI

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) compiles all Python, validates JSON
definitions, runs the unit + wiring test suite, and executes a small-scale generation +
data-quality run on Python 3.10 and 3.11.

## License

[MIT](LICENSE) © Tunde Shiyanbade
