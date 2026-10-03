# System requirements specification (Phase 0 baseline)

## 1–7. Summary, problem, objectives, scope, exclusions, stakeholders, personas

See [business requirements](business-requirements.md). The system provides governed synthetic banking analytics; it does not process payments or make regulated decisions.

## 8–9. Business and functional requirements

BR-01 through BR-06 and FR-01 through FR-10 are defined in the linked requirements documents. Priority labels mean: **MVP** must be demonstrable in the portfolio, **Phase 2** follows the foundation, and **Production extension** is documented but not claimed as delivered.

## 10–16. Quality attributes

Performance, scalability, availability, reliability, recovery, maintainability, security, observability, data quality, and interoperability requirements are in [non-functional requirements](non-functional-requirements.md). MVP targets are measured baselines rather than invented enterprise SLAs.

## 17–22. Data, integration, security, compliance, governance, reporting

Data contracts and quality: [data requirements](data-requirements.md). Integration boundary: [integration requirements](integration-requirements.md). Security and GDPR-awareness: [security requirements](security-requirements.md). Governance/reporting/lineage requirements are in [data architecture](../architecture/5-data-architecture.md), [governance](../architecture/3-logical-architecture.md), and [lineage](../data/data-lineage.md).

## 23–28. Analytics, ML/AI, API, infrastructure, DevOps, testing

Analytics delivers five Gold products and Power BI models. Rule-based fraud/AML candidates and transparent risk features are MVP; model training, approval, monitoring, fairness evaluation, and model registry are Production extension. FastAPI is an optional synthetic event generator only. Azure infrastructure is declared and deployed after review. CI tests contracts, unit logic, dbt/data quality, and deployment plans; end-to-end acceptance tests reconcile dashboard values to Gold tables.

## 29. Acceptance criteria

1. A complete synthetic batch is traceable from source through report by batch/run ID.
2. Invalid rows are quarantined and counted, not discarded.
3. All five Gold products refresh and reconcile to their documented definitions.
4. Role restrictions and masking/RLS are demonstrated using test personas.
5. A failed job is restarted idempotently and a Delta recovery is evidenced.
6. No secrets or real data exist in the repository.

## 30–33. Risks, assumptions, constraints, future enhancements

Risks/mitigations and approval questions are in [business requirements](business-requirements.md). Future enhancements: Event Hubs streaming, Purview catalog automation, data sharing, model lifecycle/MLOps, regional DR, SIEM, and production compliance review.

## Technology responsibility matrix

| Technology | Explicit responsibility | MVP status |
| --- | --- | --- |
| Python / FastAPI | synthetic generator, integration helpers, optional event API | optional API |
| PostgreSQL | core banking simulation | source |
| Oracle | legacy ledger simulation | source/schema demonstration |
| SQL Server | lending/branch simulation | source/schema demonstration |
| Azure SQL Database | cloud digital application simulation | source |
| MongoDB | semi-structured customer interactions | source |
| Cassandra | high-volume event stream simulation | source |
| Apache Airflow | code/event/document workflow showcase | demonstration path |
| Azure Data Factory | scheduled relational extraction/landing | MVP |
| ADLS Gen2 | landing, Bronze/Silver/Gold, checkpoints | MVP |
| Azure Databricks / Spark / PySpark | scalable cleansing, enrichment, features, Delta pipelines | MVP |
| Delta Lake | ACID lakehouse tables, merges, time travel | MVP |
| Azure Synapse | SQL serving/warehouse marts | Phase 2 / serverless MVP option |
| dbt | serving transformations, tests, docs, lineage | Phase 2 |
| Power BI | semantic models, DAX, RLS, reports | Phase 2 |
| Azure Monitor / Log Analytics | service/run/quality observability | MVP |
| Entra ID / Key Vault | identity, authorization, secret protection | MVP |
