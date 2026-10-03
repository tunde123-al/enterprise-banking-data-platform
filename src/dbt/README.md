# dbt analytics project

Analytical transformations, tests, documentation and lineage for the Enterprise Banking
Data & Analytics Platform. dbt owns the *serving-layer* transformations on top of the
Databricks Delta Lake Gold/Silver surfaces and against Azure Synapse dedicated SQL.

## What this project contains

```
models/staging/      Staging views over Silver source tables (light casting/normalisation)
models/intermediate/ Account and loan rollups used by multiple marts
models/dimensions/   Conformed dimensions (customer, account, card, merchant, branch, device, date)
models/facts/        Transaction / loan / repayment facts (incremental)
models/marts/        Fraud, Credit risk, AML, Customer 360 and Executive KPI products
models/staging/schema.yml  Sources (lakehouse_silver) and column-level tests
tests/               Singular assertions (positive amounts, valid emails)
profiles.yml         Env-var driven profiles (Synapse primary, Databricks secondary)
```

## Running

```bash
# Install the adapter
pip install -e ".[dev]"          # includes dbt-synapse

# Export connection settings (see .env.example) then:
cd src/dbt
dbt deps
dbt build --target synapse       # or --target databricks
dbt test                         # run only the test suite
dbt docs generate                # produce HTML docs + lineage graph
```

Secrets are never stored in this repository: every field in `profiles.yml` is populated
from environment variables or a dbt secrets backend (Airflow Variables / Vault).

## Responsibility boundaries

- dbt performs **serving-layer ELT**: lightweight staging, dims, facts, marts, tests, docs.
- Databricks/PySpark performs **heavy lakehouse transforms**: Bronze → Silver → Gold.
- See `docs/decisions/ADR-010-airflow-adf.md` and `docs/architecture/2-solution-architecture.md`
  for the ETL/ELT responsibility split and Oracle, Databricks and Silver/Gold flow.